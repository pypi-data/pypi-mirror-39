#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2018 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.backend.python module of the BEAT platform.   #
#                                                                             #
# Commercial License Usage                                                    #
# Licensees holding valid commercial BEAT licenses may use this file in       #
# accordance with the terms contained in a written agreement between you      #
# and Idiap. For further information contact tto@idiap.ch                     #
#                                                                             #
# Alternatively, this file may be used under the terms of the GNU Affero      #
# Public License version 3 as published by the Free Software and appearing    #
# in the file LICENSE.AGPL included in the packaging of this file.            #
# The BEAT platform is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY  #
# or FITNESS FOR A PARTICULAR PURPOSE.                                        #
#                                                                             #
# You should have received a copy of the GNU Affero Public License along      #
# with the BEAT platform. If not, see http://www.gnu.org/licenses/.           #
#                                                                             #
###############################################################################


"""
========
executor
========

A class that can setup and execute loop algorithm blocks on the backend
"""

import logging
import os
import json
import zmq

from ..algorithm import Algorithm
from ..baseformat import baseformat
from ..dataformat import DataFormat
from ..helpers import create_inputs_from_configuration
from ..helpers import create_outputs_from_configuration
from ..helpers import AccessMode
from ..exceptions import RemoteException

from .helpers import make_data_format


logger = logging.getLogger(__name__)


class LoopChannel(object):
    """ The LoopChannel class is a direct communication link between a loop
    using algorithm and the loop itself
    """

    def __init__(self, socket):
        """ Constructor

        Parameters:
            socket (:py:class:`zmq.Socket`): Socket for zmq communication
        """

        self.socket = socket

    def setup(self, algorithm, prefix):
        """ Setup the channel internals

        Parameters:
            algorithm (:py:class:`algorithm.Algorithm`) : algorithm for which
            the communication channel is setup.

            prefix (str) : Folder were the prefix is located.
        """

        request_format_name = algorithm.loop_map["request"]
        self.request_data_format = DataFormat(prefix, request_format_name)

        answer_format_name = algorithm.loop_map["answer"]
        self.answer_data_format = DataFormat(prefix, answer_format_name)

    def validate(self, hypothesis):
        """ This method will request validation for the hypothesis passed in
        parameter.

        Parameters:
            hypothesis (dict) : Computed hypothesis that must be validated by
            the loop algorithm.
        """
        data = make_data_format(hypothesis, self.request_data_format)

        self.socket.send_string("val", zmq.SNDMORE)
        self.socket.send(data.pack())

        answer = self.socket.recv()

        if answer == b"err":
            kind = self.socket.recv()
            message = self.socket.recv()
            raise RemoteException(kind, message)

        packed = self.socket.recv()

        data_format = self.answer_data_format.type()
        data = data_format.unpack(packed)

        return (answer == b"True", data)


class LoopExecutor(object):
    """Executors runs the code given an execution block information

    Parameters:

      socket (zmq.Socket): A pre-connected socket to send and receive messages
        from.

      directory (str): The path to a directory containing all the information
        required to run the user experiment.

      dataformat_cache (:py:class:`dict`, Optional): A dictionary mapping
        dataformat names to loaded dataformats. This parameter is optional and,
        if passed, may greatly speed-up database loading times as dataformats
        that are already loaded may be re-used. If you use this parameter, you
        must guarantee that the cache is refreshed as appropriate in case the
        underlying dataformats change.

      database_cache (:py:class:`dict`, Optional): A dictionary mapping
        database names to loaded databases. This parameter is optional and, if
        passed, may greatly speed-up database loading times as databases that
        are already loaded may be re-used. If you use this parameter, you must
        guarantee that the cache is refreshed as appropriate in case the
        underlying databases change.

      library_cache (:py:class:`dict`, Optional): A dictionary mapping library
        names to loaded libraries. This parameter is optional and, if passed,
        may greatly speed-up library loading times as libraries that are
        already loaded may be re-used. If you use this parameter, you must
        guarantee that the cache is refreshed as appropriate in case the
        underlying libraries change.  """

    def __init__(
        self,
        message_handler,
        directory,
        dataformat_cache=None,
        database_cache=None,
        library_cache=None,
        cache_root="/cache",
        db_socket=None,
    ):

        self._runner = None
        self.algorithm = None
        self.output_list = None

        self.db_socket = db_socket

        self.configuration = os.path.join(directory, "configuration.json")

        with open(self.configuration, "r") as f:
            conf_data = f.read()
            self.data = json.loads(conf_data)["loop"]

        self.prefix = os.path.join(directory, "prefix")

        # Temporary caches, if the user has not set them, for performance
        database_cache = database_cache if database_cache is not None else {}
        dataformat_cache = dataformat_cache if dataformat_cache is not None else {}
        library_cache = library_cache if library_cache is not None else {}

        # Load the algorithm
        self.algorithm = Algorithm(
            self.prefix, self.data["algorithm"], dataformat_cache, library_cache
        )

        if not self.algorithm.valid:
            logger.warning(
                "Failed to load algorithm:\n%s" % "\n".join(self.algorithm.errors)
            )

        if db_socket:
            db_access_mode = AccessMode.REMOTE
            databases = None
        else:
            db_access_mode = AccessMode.LOCAL
            databases = database_cache

        self.input_list, self.data_loaders = create_inputs_from_configuration(
            self.data,
            self.algorithm,
            self.prefix,
            cache_root,
            cache_access=AccessMode.LOCAL,
            db_access=db_access_mode,
            socket=self.db_socket,
            databases=databases,
        )

        self.message_handler = message_handler
        self.message_handler.setup(self.algorithm, self.prefix)
        self.message_handler.set_executor(self)

    @property
    def runner(self):
        """Returns the algorithm runner

        This property allows for lazy loading of the runner
        """

        if self._runner is None:
            self._runner = self.algorithm.runner()
        return self._runner

    def setup(self):
        """Sets up the algorithm to start processing"""

        retval = self.runner.setup(self.data["parameters"])
        logger.debug("User loop is setup: {}".format(retval))
        return retval

    def prepare(self):
        """Prepare the algorithm"""

        retval = self.runner.prepare(self.data_loaders)
        logger.debug("User loop is prepared: {}".format(retval))
        return retval

    def process(self):
        """Executes the user algorithm code using the current interpreter.
        """

        self.message_handler.start()

    def validate(self, hypothesis):
        """Executes the loop validation code"""

        is_valid, answer = self.runner.validate(hypothesis)
        logger.debug("User loop has validated: {}\n{}".format(is_valid, answer))
        return is_valid, answer

    @property
    def address(self):
        """ Address of the message handler"""

        return self.message_handler.address

    @property
    def valid(self):
        """A boolean that indicates if this executor is valid or not"""
        return not bool(self.errors)

    def wait(self):
        """Wait for the message handle to finish"""

        self.message_handler.join()
        self.message_handler = None

#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/           #
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
==================
Database execution
==================

Execution utilities
"""

import os

import logging

import simplejson

from ..database import Database


logger = logging.getLogger(__name__)


class DBExecutor(object):
    """Executor specialised in database views


    Parameters:

      prefix (str): Establishes the prefix of your installation.

      data (dict, str): The piece of data representing the block to be
        executed.
        It must validate against the schema defined for execution blocks. If a
        string is passed, it is supposed to be a fully qualified absolute path
        to a JSON file containing the block execution information.

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


    Attributes:

      errors (list): A list containing errors found while loading this
        execution block.

      data (dict): The original data for this executor, as loaded by our JSON
        decoder.

      databases (dict): A dictionary in which keys are strings with database
        names and values are :py:class:`.database.Database`, representing the
        databases required for running this block. The dictionary may be empty
        in case all inputs are taken from the file cache.

      views (dict): A dictionary in which the keys are tuples pointing to the
        ``(<database-name>, <protocol>, <set>)`` and the value is a setup view
        for that particular combination of details. The dictionary may be empty
        in case all inputs are taken from the file cache.

      input_list (inputs.InputList): A list of inputs that will be served to
        the algorithm.

      data_sources (list): A list with all data-sources created by our
        execution loader.

    """

    def __init__(
        self,
        message_handler,
        prefix,
        cache_root,
        data,
        dataformat_cache=None,
        database_cache=None,
    ):

        # Initialisation
        self.prefix = prefix
        self.databases = {}
        self.views = {}
        self.errors = []
        self.data = None
        self.message_handler = None
        self.data_sources = {}
        self.message_handler = message_handler

        # Temporary caches, if the user has not set them, for performance
        database_cache = database_cache if database_cache is not None else {}
        self.dataformat_cache = dataformat_cache if dataformat_cache is not None else {}

        # Load the data
        if not isinstance(data, dict):  # User has passed a file name
            if not os.path.exists(data):
                self.errors.append("File not found: %s" % data)
                return

            with open(data) as f:
                self.data = simplejson.load(f)
        else:
            self.data = data

        # this runs basic validation, including JSON loading if required
        # self.data, self.errors = schema.validate('execution', data)
        # if self.errors: return #don't proceed with the rest of validation

        # Load the databases
        for name, details in self.data["inputs"].items():
            if "database" not in details:
                continue

            # Load the database
            if details["database"] not in self.databases:

                if details["database"] in database_cache:  # reuse
                    db = database_cache[details["database"]]
                else:  # load it
                    db = Database(
                        self.prefix, details["database"], self.dataformat_cache
                    )
                    database_cache[db.name] = db

                self.databases[details["database"]] = db

                if not db.valid:
                    self.errors += db.errors
            else:
                db = self.databases[details["database"]]

            if not db.valid:
                continue

            # Create and load the required views
            key = (details["database"], details["protocol"], details["set"])
            if key not in self.views:
                view = db.view(details["protocol"], details["set"])

                if details["channel"] == self.data["channel"]:  # synchronized
                    start_index, end_index = self.data.get("range", (None, None))
                else:
                    start_index, end_index = (None, None)

                view.setup(
                    os.path.join(cache_root, details["path"]),
                    start_index=start_index,
                    end_index=end_index,
                )

                self.views[key] = view

        # Create the data sources
        for name, details in self.data["inputs"].items():
            if "database" not in details:
                continue

            view_key = (details["database"], details["protocol"], details["set"])
            view = self.views[view_key]

            self.data_sources[name] = view.data_sources[details["output"]]

        self.message_handler.set_data_sources(self.data_sources)

    def process(self):
        """ Starts the message handler"""

        self.message_handler.start()

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

    def __str__(self):
        return simplejson.dumps(self.data, indent=4)

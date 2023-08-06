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


# Tests for experiment execution

import os
import logging
import unittest
import zmq
import tempfile
import shutil
import simplejson
import numpy as np

from copy import deepcopy

from ..execution import AlgorithmExecutor
from ..execution import LoopExecutor
from ..execution import MessageHandler
from ..execution import LoopMessageHandler
from ..exceptions import RemoteException

from ..algorithm import Algorithm
from ..dataformat import DataFormat
from ..data import CachedDataSink
from ..data import CachedDataSource

from ..helpers import convert_experiment_configuration_to_container
from ..helpers import AccessMode

from . import prefix


logger = logging.getLogger(__name__)


#----------------------------------------------------------


CONFIGURATION = {
    'algorithm': '',
    'channel': 'main',
    'parameters': {
    },
    'inputs': {
        'in': {
            'path': 'INPUT',
            'channel': 'main',
        }
    },
    'outputs': {
        'out': {
            'path': 'OUTPUT',
            'channel': 'main'
        }
    },
    'loop': {
        'algorithm': '',
        'channel': 'main',
        'parameters': {
            'threshold': 1
        },
        'inputs': {
            'in': {
                'path': 'INPUT',
                'channel': 'main'
            }
        }
    }
}



#----------------------------------------------------------


class TestExecution(unittest.TestCase):

    def setUp(self):
        self.cache_root = tempfile.mkdtemp(prefix=__name__)
        self.working_dir = tempfile.mkdtemp(prefix=__name__)

        self.message_handler = None
        self.loop_message_handler = None
        self.executor_socket = None
        self.loop_executor = None
        self.loop_socket = None
        self.zmq_context = None


    def tearDown(self):
        shutil.rmtree(self.cache_root)
        shutil.rmtree(self.working_dir)

        if self.loop_executor:
            self.loop_executor.wait()

        for handler in [self.message_handler, self.loop_message_handler]:
            if handler is not None:
                handler.kill()
                handler.join()
                handler.destroy()
                handler = None


        for socket in [self.executor_socket, self.loop_socket]:
            if socket is not None:
                socket.setsockopt(zmq.LINGER, 0)
                socket.close()
                socket = None

        self.zmq_context.destroy()
        self.zmq_context = None


    def writeData(self, input_name, indices, start_value):
        filename = os.path.join(self.cache_root, CONFIGURATION['inputs'][input_name]['path'] + '.data')

        dataformat = DataFormat(prefix, 'user/single_integer/1')
        self.assertTrue(dataformat.valid)

        data_sink = CachedDataSink()
        self.assertTrue(data_sink.setup(filename, dataformat, indices[0][0], indices[-1][1]))

        for i in indices:
            data = dataformat.type()
            data.value = np.int32(start_value + i[0])
            data_sink.write(data, i[0], i[1])

        (nb_bytes, duration) = data_sink.statistics()
        self.assertTrue(nb_bytes > 0)
        self.assertTrue(duration > 0)

        data_sink.close()
        del data_sink


    def process(self, algorithm_name, loop_algorithm_name):
        self.writeData('in', [(0, 0), (1, 1), (2, 2), (3, 3)], 1000)

        # -------------------------------------------------------------------------
        config = deepcopy(CONFIGURATION)
        config['algorithm'] = algorithm_name
        config['loop']['algorithm'] = loop_algorithm_name

        config = convert_experiment_configuration_to_container(config)

        with open(os.path.join(self.working_dir, 'configuration.json'), 'wb') as f:
            data = simplejson.dumps(config, indent=4).encode('utf-8')
            f.write(data)

        working_prefix = os.path.join(self.working_dir, 'prefix')
        if not os.path.exists(working_prefix):
            os.makedirs(working_prefix)

        algorithm = Algorithm(prefix, algorithm_name)
        assert(algorithm.valid)
        algorithm.export(working_prefix)

        # -------------------------------------------------------------------------

        loop_algorithm = Algorithm(prefix, loop_algorithm_name)
        assert(loop_algorithm.valid)
        loop_algorithm.export(working_prefix)

        # -------------------------------------------------------------------------

        self.message_handler = MessageHandler('127.0.0.1')
        self.message_handler.start()
        self.loop_message_handler = LoopMessageHandler('127.0.0.1')

        self.zmq_context = zmq.Context()
        self.executor_socket = self.zmq_context.socket(zmq.PAIR)
        self.executor_socket.connect(self.message_handler.address)
        self.loop_socket = self.zmq_context.socket(zmq.PAIR)
        self.loop_socket.connect(self.loop_message_handler.address)

        self.loop_executor = LoopExecutor(self.loop_message_handler, self.working_dir, cache_root=self.cache_root)
        self.assertTrue(self.loop_executor.setup())
        self.assertTrue(self.loop_executor.prepare())
        self.loop_executor.process()

        executor = AlgorithmExecutor(self.executor_socket, self.working_dir, cache_root=self.cache_root, loop_socket=self.loop_socket)

        self.assertTrue(executor.setup())
        self.assertTrue(executor.prepare())

        self.assertTrue(executor.process())

        cached_file = CachedDataSource()
        self.assertTrue(cached_file.setup(os.path.join(self.cache_root, CONFIGURATION['outputs']['out']['path'] + '.data'), prefix))

        for i in range(len(cached_file)):
            data, start, end = cached_file[i]
            self.assertEqual(data.value, 1000 + i)
            self.assertEqual(start, i)
            self.assertEqual(end, i)



    def test_autonomous_loop(self):
        self.process('autonomous/loop_user/1',
                     'autonomous/loop/1')

    def test_autonomous_loop_invalid_output(self):
        with self.assertRaises(RemoteException):
            self.process('autonomous/loop_user/1',
                         'autonomous/invalid_loop_output/1')
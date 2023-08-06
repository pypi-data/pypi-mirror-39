#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2017 Idiap Research Institute, http://www.idiap.ch/           #
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
logger = logging.getLogger(__name__)

import unittest
import zmq
import tempfile
import shutil

from ..execution import DBExecutor
from ..execution import MessageHandler
from ..database import Database
from ..data_loaders import DataLoader
from ..data import RemoteDataSource
from ..hash import hashDataset
from ..hash import toPath

from . import prefix


#----------------------------------------------------------


DB_VIEW_HASH = hashDataset('integers_db/1', 'double', 'double')
DB_INDEX_PATH = toPath(DB_VIEW_HASH, suffix='.db')

CONFIGURATION = {
    'queue': 'queue',
    'algorithm': 'user/sum/1',
    'nb_slots': 1,
    'channel': 'integers',
    'parameters': {
    },
    'environment': {
        'name': 'Python 2.7',
        'version': '1.2.0'
    },
    'inputs': {
        'a': {
            'database': 'integers_db/1',
            'protocol': 'double',
            'set': 'double',
            'output': 'a',
            'endpoint': 'a',
            'channel': 'integers',
            'path': DB_INDEX_PATH,
            'hash': DB_VIEW_HASH,
        },
        'b': {
            'database': 'integers_db/1',
            'protocol': 'double',
            'set': 'double',
            'output': 'b',
            'endpoint': 'b',
            'channel': 'integers',
            'path': DB_INDEX_PATH,
            'hash': DB_VIEW_HASH,
        }
    },
    'outputs': {
        'sum': {
            'endpoint': 'sum',
            'channel': 'integers',
            'path': '20/61/b6/2df3c3bedd5366f4a625c5d87ffbf5a26007c46c456e9abf21b46c6681',
            'hash': '2061b62df3c3bedd5366f4a625c5d87ffbf5a26007c46c456e9abf21b46c6681',
        }
    }
}


#----------------------------------------------------------


class TestExecution(unittest.TestCase):

    def setUp(self):
        self.cache_root = tempfile.mkdtemp(prefix=__name__)

        database = Database(prefix, 'integers_db/1')
        view = database.view('double', 'double')

        view.index(os.path.join(self.cache_root, DB_INDEX_PATH))

        self.db_executor = None
        self.client_context = None
        self.client_socket = None


    def tearDown(self):
        if self.client_socket is not None:
            self.client_socket.send_string('don')

        if self.db_executor is not None:
            self.db_executor.wait()

        if self.client_socket is not None:
            self.client_socket.setsockopt(zmq.LINGER, 0)
            self.client_socket.close()
            self.client_context.destroy()

        shutil.rmtree(self.cache_root)


    def test_success(self):
        message_handler = MessageHandler('127.0.0.1')

        self.db_executor = DBExecutor(message_handler, prefix, self.cache_root, CONFIGURATION)

        self.assertTrue(self.db_executor.valid)

        self.db_executor.process()

        self.client_context = zmq.Context()
        self.client_socket = self.client_context.socket(zmq.PAIR)
        self.client_socket.connect(self.db_executor.address)

        data_loader = DataLoader(CONFIGURATION['channel'])

        database = Database(prefix, 'integers_db/1')

        for input_name, input_conf in CONFIGURATION['inputs'].items():
            dataformat_name = database.set(input_conf['protocol'], input_conf['set'])['outputs'][input_conf['output']]

            data_source = RemoteDataSource()
            data_source.setup(self.client_socket, input_name, dataformat_name, prefix)
            data_loader.add(input_name, data_source)


        self.assertEqual(data_loader.count('a'), 9)
        self.assertEqual(data_loader.count('b'), 9)

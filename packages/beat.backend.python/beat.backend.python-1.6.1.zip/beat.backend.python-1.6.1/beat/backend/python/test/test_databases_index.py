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

import unittest
import multiprocessing
import tempfile
import shutil

from ..scripts import index
from ..hash import hashDataset
from ..hash import toPath

from . import prefix


#----------------------------------------------------------


class IndexationProcess(multiprocessing.Process):

    def __init__(self, queue, arguments):
        super(IndexationProcess, self).__init__()

        self.queue = queue
        self.arguments = arguments


    def run(self):
        self.queue.put('STARTED')
        index.main(self.arguments)


#----------------------------------------------------------


class TestDatabaseIndexation(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(TestDatabaseIndexation, self).__init__(methodName)
        self.databases_indexation_process = None
        self.working_dir = None
        self.cache_root = None


    def setUp(self):
        self.shutdown_everything()  # In case another test failed badly during its setUp()
        self.working_dir = tempfile.mkdtemp(prefix=__name__)
        self.cache_root = tempfile.mkdtemp(prefix=__name__)


    def tearDown(self):
        self.shutdown_everything()

        shutil.rmtree(self.working_dir)
        shutil.rmtree(self.cache_root)

        self.working_dir = None
        self.cache_root = None
        self.data_source = None


    def shutdown_everything(self):
        if self.databases_indexation_process is not None:
            self.databases_indexation_process.terminate()
            self.databases_indexation_process.join()
            del self.databases_indexation_process
            self.databases_indexation_process = None


    def process(self, database, protocol_name=None, set_name=None):
        args = [
            prefix,
            self.cache_root,
            database,
        ]

        if protocol_name is not None:
            args.append(protocol_name)

            if set_name is not None:
                args.append(set_name)

        self.databases_indexation_process = IndexationProcess(multiprocessing.Queue(), args)
        self.databases_indexation_process.start()

        self.databases_indexation_process.queue.get()

        self.databases_indexation_process.join()
        del self.databases_indexation_process
        self.databases_indexation_process = None


    def test_one_set(self):
        self.process('integers_db/1', 'double', 'double')

        expected_files = [
            hashDataset('integers_db/1', 'double', 'double')
        ]

        for filename in expected_files:
            self.assertTrue(os.path.exists(os.path.join(self.cache_root,
                                                        toPath(filename, suffix='.db'))
            ))


    def test_one_protocol(self):
        self.process('integers_db/1', 'two_sets')

        expected_files = [
            hashDataset('integers_db/1', 'two_sets', 'double'),
            hashDataset('integers_db/1', 'two_sets', 'triple')
        ]

        for filename in expected_files:
            self.assertTrue(os.path.exists(os.path.join(self.cache_root,
                                                        toPath(filename, suffix='.db'))
            ))


    def test_whole_database(self):
        self.process('integers_db/1')

        expected_files = [
            hashDataset('integers_db/1', 'double', 'double'),
            hashDataset('integers_db/1', 'triple', 'triple'),
            hashDataset('integers_db/1', 'two_sets', 'double'),
            hashDataset('integers_db/1', 'two_sets', 'triple'),
            hashDataset('integers_db/1', 'labelled', 'labelled'),
            hashDataset('integers_db/1', 'different_frequencies', 'double'),
        ]

        for filename in expected_files:
            self.assertTrue(os.path.exists(os.path.join(self.cache_root,
                                                        toPath(filename, suffix='.db'))
            ))


    def test_error(self):
        self.process('crash/1', 'protocol', 'index_crashes')

        unexpected_files = [
            hashDataset('crash/1', 'protocol', 'index_crashes'),
        ]

        for filename in unexpected_files:
            self.assertFalse(os.path.exists(os.path.join(self.cache_root,
                                                         toPath(filename, suffix='.db'))
            ))

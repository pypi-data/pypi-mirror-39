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


import unittest
import tempfile
import shutil
import os

from ..database import Database

from . import prefix


#----------------------------------------------------------


class MyExc(Exception):
    pass


#----------------------------------------------------------


class TestDatabaseViewRunner(unittest.TestCase):

    def setUp(self):
        self.cache_root = tempfile.mkdtemp(prefix=__name__)


    def tearDown(self):
        shutil.rmtree(self.cache_root)


    def test_syntax_error(self):
        db = Database(prefix, 'syntax_error/1')
        self.assertTrue(db.valid)

        with self.assertRaises(SyntaxError):
            view = db.view('protocol', 'set')


    def test_unknown_view(self):
        db = Database(prefix, 'integers_db/1')
        self.assertTrue(db.valid)

        with self.assertRaises(KeyError):
            view = db.view('protocol', 'does_not_exist')


    def test_valid_view(self):
        db = Database(prefix, 'integers_db/1')
        self.assertTrue(db.valid)

        view = db.view('double', 'double')
        self.assertTrue(view is not None)


    def test_indexing_crash(self):
        db = Database(prefix, 'crash/1')
        self.assertTrue(db.valid)

        view = db.view('protocol', 'index_crashes', MyExc)

        with self.assertRaises(MyExc):
            view.index(os.path.join(self.cache_root, 'data.db'))


    def test_get_crash(self):
        db = Database(prefix, 'crash/1')
        self.assertTrue(db.valid)

        view = db.view('protocol', 'get_crashes', MyExc)
        view.index(os.path.join(self.cache_root, 'data.db'))
        view.setup(os.path.join(self.cache_root, 'data.db'))

        with self.assertRaises(MyExc):
            view.get('a', 0)


    def test_not_setup(self):
        db = Database(prefix, 'crash/1')
        self.assertTrue(db.valid)

        view = db.view('protocol', 'get_crashes', MyExc)

        with self.assertRaises(MyExc):
            view.get('a', 0)


    def test_success(self):
        db = Database(prefix, 'integers_db/1')
        self.assertTrue(db.valid)

        view = db.view('double', 'double', MyExc)
        view.index(os.path.join(self.cache_root, 'data.db'))
        view.setup(os.path.join(self.cache_root, 'data.db'))

        self.assertTrue(view.data_sources is not None)
        self.assertEqual(len(view.data_sources), 3)

        for i in range(0, 9):
            self.assertEqual(view.get('a', i)['value'], i + 1)
            self.assertEqual(view.get('b', i)['value'], (i + 1) * 10)
            self.assertEqual(view.get('sum', i)['value'], (i + 1) * 10 + i + 1)


    def test_success_using_keywords(self):
        db = Database(prefix, 'python_keyword/1')
        self.assertTrue(db.valid)

        view = db.view('keyword', 'keyword', MyExc)
        view.index(os.path.join(self.cache_root, 'data.db'))
        view.setup(os.path.join(self.cache_root, 'data.db'))

        self.assertTrue(view.data_sources is not None)
        self.assertEqual(len(view.data_sources), 3)

        for i in range(0, 9):
            self.assertEqual(view.get('class', i)['value'], i + 1)
            self.assertEqual(view.get('def', i)['value'], (i + 1) * 10)
            self.assertEqual(view.get('sum', i)['value'], (i + 1) * 10 + i + 1)

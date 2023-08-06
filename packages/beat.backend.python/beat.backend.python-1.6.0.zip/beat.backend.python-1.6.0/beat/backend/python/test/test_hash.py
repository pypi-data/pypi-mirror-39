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


import nose.tools
import six

from .. import hash


#----------------------------------------------------------


def test_path_from_username():
    path = hash.toUserPath('johndoe')

    assert path is not None
    assert isinstance(path, str)
    assert len(path) > 0

    parts = path.split('/')

    nose.tools.eq_(len(parts), 3)

    for folder in parts[:-1]:
        nose.tools.eq_(len(folder), 2)

    nose.tools.eq_(parts[-1], 'johndoe')


#----------------------------------------------------------


def test_basic_hash():
    nose.tools.eq_(hash._sha256('123456'),
        '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92')


#----------------------------------------------------------


def test_accented_hash():
    if six.PY2:
        ref = '4cb6985f5b4ec0ad4ce46904364f374194386426996a56683dc1c8d2944272ce'
    else:
        ref = '477993339861be6552873127471f9da6ae443991d5aced735f51140c34cd7599'

    nose.tools.eq_(hash._sha256('áéçü'), ref)


#----------------------------------------------------------


def test_unicode_hash():
    nose.tools.eq_(hash._sha256(u'áéçü'),
        '477993339861be6552873127471f9da6ae443991d5aced735f51140c34cd7599')


#----------------------------------------------------------


def test_dataset_hash():

    h = hash.hashDataset('some_database/1', 'some_protocol',' some_set')
    assert h is not None
    assert isinstance(h, str)
    assert len(h) > 0


#----------------------------------------------------------


def test_dataset_hash_repeatability():

    h1 = hash.hashDataset('some_database/1', 'some_protocol',' some_set')
    h2 = hash.hashDataset('some_database/1', 'some_protocol',' some_set')
    nose.tools.eq_(h1, h2)


#----------------------------------------------------------


def test_different_dataset_hashes():

    h1 = hash.hashDataset('some_database/1', 'some_protocol',' some_set1')
    h2 = hash.hashDataset('some_database/1', 'some_protocol',' some_set2')
    assert h1 != h2, "%r != %r" % (h1, h2)

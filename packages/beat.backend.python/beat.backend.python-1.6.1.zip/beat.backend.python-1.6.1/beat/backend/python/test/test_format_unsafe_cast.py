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


import six
import nose.tools

from ..dataformat import DataFormat

from . import prefix


number42L = long(42) if six.PY2 else int(42)


#----------------------------------------------------------


def doit(format, key, value):

    df = DataFormat(prefix, format)
    assert df.valid
    obj = df.type()
    setattr(obj, key, value)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_single_integer():
    doit('user/single_integer/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_single_unsigned_integer():
    doit('user/single_unsigned_integer/1', 'value', -number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_single_unsigned_integer64():
    doit('user/single_unsigned_integer64/1', 'value', -number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_single_float():
    doit('user/single_float/1', 'value', complex(4,6))


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_single_boolean():
    doit('user/single_boolean/1', 'value', 42)


#----------------------------------------------------------


@nose.tools.nottest #string conversion is always possible
@nose.tools.raises(TypeError)
def test_single_string():
    doit('user/single_string/1', 'value', False)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_single_object_fields():
    doit('user/single_object/1', 'obj', dict(value1='abc', value2=False))


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_hierarchy_of_objects():
    doit('user/hierarchy_of_objects/1', 'obj1',
            dict(obj2=dict(obj3={'value':3.4}))
            )


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_hierarchy_of_objects_fields():
    doit('user/hierarchy_of_objects/1', 'obj1',
            dict(obj2=dict(obj3=dict(value=number42L)))
            )


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_empty_1d_array_of_integers():
    doit('user/empty_1d_array_of_integers/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_empty_2d_array_of_integers():
    doit('user/empty_2d_array_of_integers/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_empty_3d_array_of_integers():
    doit('user/empty_3d_array_of_integers/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_1d_array_of_integers():
    doit('user/1d_array_of_integers/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_2d_array_of_integers():
    doit('user/2d_array_of_integers/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_3d_array_of_integers():
    doit('user/3d_array_of_integers/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_empty_1d_array_of_objects():
    doit('user/empty_1d_array_of_objects/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_empty_1d_array_of_objects4():
    doit('user/empty_1d_array_of_objects4/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_empty_2d_array_of_objects():
    doit('user/empty_2d_array_of_objects/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_empty_3d_array_of_objects():
    doit('user/empty_3d_array_of_objects/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_1d_array_of_objects():
    doit('user/1d_array_of_objects/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_2d_array_of_objects():
    doit('user/2d_array_of_objects/1', 'value', number42L)


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_3d_array_of_objects():
    doit('user/3d_array_of_objects/1', 'value', number42L)


#----------------------------------------------------------


def doit_array(format, key, value, index):

    df = DataFormat(prefix, format)
    assert df.valid
    obj = df.type()
    array = getattr(obj, key)
    array[index] = value


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_1d_array_of_strings_content():
    obj = doit_array('user/1d_array_of_strings/1', 'value', 42, (2,))


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_1d_array_of_objects_contents():
    doit_array('user/1d_array_of_objects/1', 'value', {'value': number42L}, (5,))


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_2d_array_of_objects_contents():
    doit_array('user/2d_array_of_objects/1', 'value', {'value': number42L}, (5, 3))


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_3d_array_of_objects_contents():
    doit_array('user/3d_array_of_objects/1', 'value', {'value': number42L}, (5, 3, 0))


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_empty_1d_array_of_dataformat():
    doit_array('user/empty_1d_array_of_dataformat/1', 'value', {})


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_empty_2d_array_of_dataformat():
    doit_array('user/empty_2d_array_of_dataformat/1', 'value', {})


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_empty_3d_array_of_dataformat():
    doit_array('user/empty_3d_array_of_dataformat/1', 'value', {})


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_1d_array_of_dataformat():
    doit_array('user/1d_array_of_dataformat/1', 'value', {'value8': number42L}, (5,))


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_2d_array_of_dataformat():
    doit_array('user/2d_array_of_dataformat/1', 'value', {'value8': number42L}, (5, 3))


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_3d_array_of_dataformat():
    doit_array('user/3d_array_of_dataformat/1', 'value',  {'value8': number42L}, (5, 3, 0))


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_1d_array_of_dataformat_content():
    doit_array('user/1d_array_of_dataformat/1', 'value', {'value8': number42L}, (5,))


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_2d_array_of_dataformat_content():
    doit_array('user/2d_array_of_dataformat/1', 'value', {'value8': number42L}, (5, 3))


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_3d_array_of_dataformat_content():
    doit_array('user/3d_array_of_dataformat/1', 'value', {'value8': number42L}, (5, 3, 0))

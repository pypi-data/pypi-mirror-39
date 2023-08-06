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

from ..dataformat import DataFormat

from . import prefix


#----------------------------------------------------------


def doit(format, data):

    df = DataFormat(prefix, format)
    assert df.valid
    obj = df.type()
    obj.from_dict(data, casting='unsafe', add_defaults=False)


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_single_integer():
    doit('user/single_integer/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_single_float():
    doit('user/single_float/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_single_boolean():
    doit('user/single_boolean/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_single_string():
    doit('user/single_string/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_single_object():
    doit('user/single_object/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_single_object_field():
    doit('user/single_object/1', dict(obj={}))


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_hierarchy_of_objects():
    doit('user/hierarchy_of_objects/1', dict(obj1=dict(obj2={})))


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_hierarchy_of_objects_field():
    doit('user/hierarchy_of_objects/1', dict(obj1=dict(obj2=dict(obj3={}))))


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_empty_1d_array_of_integers():
    doit('user/empty_1d_array_of_integers/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_empty_2d_array_of_integers():
    doit('user/empty_2d_array_of_integers/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_empty_3d_array_of_integers():
    doit('user/empty_3d_array_of_integers/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_1d_array_of_integers():
    doit('user/1d_array_of_integers/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_2d_array_of_integers():
    doit('user/2d_array_of_integers/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_3d_array_of_integers():
    doit('user/3d_array_of_integers/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_empty_1d_array_of_objects():
    doit('user/empty_1d_array_of_objects/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_empty_1d_array_of_objects4():
    doit('user/empty_1d_array_of_objects4/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_empty_2d_array_of_objects():
    doit('user/empty_2d_array_of_objects/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_empty_3d_array_of_objects():
    doit('user/empty_3d_array_of_objects/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_1d_array_of_objects():
    doit('user/1d_array_of_objects/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_2d_array_of_objects():
    doit('user/2d_array_of_objects/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_3d_array_of_objects():
    doit('user/3d_array_of_objects/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_empty_1d_array_of_dataformat():
    doit('user/empty_1d_array_of_dataformat/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_empty_2d_array_of_dataformat():
    doit('user/empty_2d_array_of_dataformat/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_empty_3d_array_of_dataformat():
    doit('user/empty_3d_array_of_dataformat/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_1d_array_of_dataformat():
    doit('user/1d_array_of_dataformat/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_2d_array_of_dataformat():
    doit('user/2d_array_of_dataformat/1', {})


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_3d_array_of_dataformat():
    doit('user/3d_array_of_dataformat/1', {})

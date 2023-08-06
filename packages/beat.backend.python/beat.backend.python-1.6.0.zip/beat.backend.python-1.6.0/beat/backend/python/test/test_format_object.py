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


import numpy
import nose.tools

from ..dataformat import DataFormat

from . import prefix


#----------------------------------------------------------


def test_single_object():

    df = DataFormat(prefix, 'user/single_object/1')
    assert df.valid
    ftype = df.type

    # checks object creation
    obj = ftype(obj=dict(value1=numpy.int32(32), value2=True))
    assert isinstance(obj, ftype)
    assert isinstance(obj.obj.value1, numpy.int32)
    nose.tools.eq_(obj.obj.value1, 32)
    assert isinstance(obj.obj.value2, numpy.bool_)
    nose.tools.eq_(obj.obj.value2, True)

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


def test_two_objects():

    df = DataFormat(prefix, 'user/two_objects/1')
    assert df.valid
    ftype = df.type

    # checks object creation
    obj = ftype(
            obj1=dict(value1=numpy.int32(32), value2=True),
            obj2=dict(value1=numpy.float32(3.14), value2='123'),
            )
    assert isinstance(obj, ftype)
    assert isinstance(obj.obj1.value1, numpy.int32)
    nose.tools.eq_(obj.obj1.value1, 32)
    assert isinstance(obj.obj1.value2, numpy.bool_)
    nose.tools.eq_(obj.obj1.value2, True)
    assert isinstance(obj.obj2.value1, numpy.float32)
    assert numpy.isclose(obj.obj2.value1, 3.14)
    assert isinstance(obj.obj2.value2, str)
    nose.tools.eq_(obj.obj2.value2, '123')

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


def test_hierarchy_of_objects():

    df = DataFormat(prefix, 'user/hierarchy_of_objects/1')
    assert df.valid
    ftype = df.type

    # checks object creation
    obj = ftype(obj1=dict(obj2=dict(obj3=dict(value=numpy.int32(32)))))

    assert isinstance(obj, ftype)
    assert isinstance(obj.obj1.obj2.obj3.value, numpy.int32)
    nose.tools.eq_(obj.obj1.obj2.obj3.value, 32)

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


def test_array_of_dict_objects():

    df = DataFormat(prefix, 'user/1d_array_of_objects3/1')
    assert df.valid
    ftype = df.type

    # checks object creation
    obj = ftype(value=[
        dict(
            id=numpy.int32(17),
            coordinates=dict(x=numpy.int32(15), y=numpy.int32(21)),
            ),
        dict(
            id=numpy.int32(4),
            coordinates=dict(x=numpy.int32(3), y=numpy.int32(-5)),
            ),
        ])

    assert isinstance(obj, ftype)
    assert isinstance(obj.value[0].id, numpy.int32)
    nose.tools.eq_(obj.value[0].id, 17)
    assert isinstance(obj.value[0].coordinates.x, numpy.int32)
    nose.tools.eq_(obj.value[0].coordinates.x, 15)
    assert isinstance(obj.value[0].coordinates.y, numpy.int32)
    nose.tools.eq_(obj.value[0].coordinates.y, 21)
    nose.tools.eq_(obj.value[1].id, 4)
    assert isinstance(obj.value[1].coordinates.x, numpy.int32)
    nose.tools.eq_(obj.value[1].coordinates.x, 3)
    assert isinstance(obj.value[1].coordinates.y, numpy.int32)
    nose.tools.eq_(obj.value[1].coordinates.y, -5)

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


def test_array_of_dict_complex_objects():

    df = DataFormat(prefix, 'user/1d_array_of_objects4/1')
    assert df.valid
    ftype = df.type

    # checks object creation
    obj = ftype(value=[
        dict(
            id=numpy.int32(17),
            name='abc',
            value=complex(1.2, -3.5),
            ),
        dict(
            id=numpy.int32(42),
            name='123',
            value=complex(-0.2, 47.4),
            ),
        ])

    assert isinstance(obj, ftype)
    assert isinstance(obj.value[0].id, numpy.int32)
    nose.tools.eq_(obj.value[0].id, 17)
    assert isinstance(obj.value[0].name, str)
    nose.tools.eq_(obj.value[0].name, 'abc')
    assert isinstance(obj.value[0].value, numpy.complex128)
    assert numpy.isclose(obj.value[0].value, complex(1.2, -3.5))
    assert isinstance(obj.value[1].id, numpy.int32)
    nose.tools.eq_(obj.value[1].id, 42)
    assert isinstance(obj.value[1].name, str)
    nose.tools.eq_(obj.value[1].name, '123')
    assert isinstance(obj.value[1].value, numpy.complex128)
    assert numpy.isclose(obj.value[1].value, complex(-0.2, 47.4))

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


def test_differs():

    df = DataFormat(prefix, 'user/1d_array_of_objects4/1')
    assert df.valid
    ftype = df.type

    # checks object creation
    obj1 = ftype(value=[
        dict(
            id=numpy.int32(17),
            name='abc',
            value=complex(1.2, -3.5),
            ),
        dict(
            id=numpy.int32(42),
            name='123',
            value=complex(-0.2, 47.4),
            ),
        ])

    obj2 = obj1.copy()
    obj3 = obj1.copy()
    obj3.value[1].value = complex(-0.2, 47.5)

    assert obj1.isclose(obj2), '%s != %s' % (obj1, obj2)
    assert not obj1.isclose(obj3), '%s == %s' % (obj1, obj3)

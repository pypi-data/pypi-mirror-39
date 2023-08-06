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


def test_integers():

    df = DataFormat(prefix, 'user/integers/1')
    assert df.valid

    ftype = df.type

    assert numpy.issubdtype(ftype.value8, numpy.int8)
    assert numpy.issubdtype(ftype.value16, numpy.int16)
    assert numpy.issubdtype(ftype.value32, numpy.int32)
    assert numpy.issubdtype(ftype.value64, numpy.int64)

    obj = ftype(
            value8=numpy.int8(2**6),
            value16=numpy.int16(2**14),
            value32=numpy.int32(2**30),
            value64=numpy.int64(2**62),
            )

    nose.tools.eq_(obj.value8.dtype, numpy.int8)
    nose.tools.eq_(obj.value8, 2**6)

    nose.tools.eq_(obj.value16.dtype, numpy.int16)
    nose.tools.eq_(obj.value16, 2**14)

    nose.tools.eq_(obj.value32.dtype, numpy.int32)
    nose.tools.eq_(obj.value32, 2**30)

    nose.tools.eq_(obj.value64.dtype, numpy.int64)
    nose.tools.eq_(obj.value64, 2**62)

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_integers_unsafe_cast():

    df = DataFormat(prefix, 'user/integers/1')
    assert df.valid

    ftype = df.type

    obj = ftype()
    obj.from_dict(dict(value8=2**6), casting='safe', add_defaults=True)


#----------------------------------------------------------


def test_unsigned_integers():
    df = DataFormat(prefix, 'user/unsigned_integers/1')
    assert df.valid

    ftype = df.type

    assert numpy.issubdtype(ftype.value8, numpy.uint8)
    assert numpy.issubdtype(ftype.value16, numpy.uint16)
    assert numpy.issubdtype(ftype.value32, numpy.uint32)
    assert numpy.issubdtype(ftype.value64, numpy.uint64)

    obj = ftype(
            value8=numpy.uint8(2**6),
            value16=numpy.uint16(2**14),
            value32=numpy.uint32(2**30),
            value64=numpy.uint64(2**62),
            )

    nose.tools.eq_(obj.value8.dtype, numpy.uint8)
    nose.tools.eq_(obj.value8, 2**6)

    nose.tools.eq_(obj.value16.dtype, numpy.uint16)
    nose.tools.eq_(obj.value16, 2**14)

    nose.tools.eq_(obj.value32.dtype, numpy.uint32)
    nose.tools.eq_(obj.value32, 2**30)

    nose.tools.eq_(obj.value64.dtype, numpy.uint64)
    nose.tools.eq_(obj.value64, 2**62)

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_unsigned_integers_unsafe_cast():

    df = DataFormat(prefix, 'user/unsigned_integers/1')
    assert df.valid

    ftype = df.type

    obj = ftype()
    obj.from_dict(dict(value8=2**6), casting='safe', add_defaults=True)


#----------------------------------------------------------


@nose.tools.raises(AttributeError)
def test_unsigned_integers_missing_attributes():

    df = DataFormat(prefix, 'user/unsigned_integers/1')
    assert df.valid

    ftype = df.type

    obj = ftype()
    obj.from_dict(dict(value8=2**6), casting='safe', add_defaults=False)


#----------------------------------------------------------


def test_floats():
    df = DataFormat(prefix, 'user/floats/1')
    assert df.valid

    ftype = df.type

    assert numpy.issubdtype(ftype.value32, numpy.float32)
    assert numpy.issubdtype(ftype.value64, numpy.float64)

    obj = ftype(
            value32=numpy.float32(3.0),
            value64=3.14,
            )

    nose.tools.eq_(obj.value32.dtype, numpy.float32)
    assert numpy.isclose(obj.value32, 3.0)

    nose.tools.eq_(obj.value64.dtype, numpy.float64)
    assert numpy.isclose(obj.value64, 3.14)

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


@nose.tools.raises(TypeError)
def test_floats_unsafe_cast():
    df = DataFormat(prefix, 'user/floats/1')
    assert df.valid

    ftype = df.type

    assert numpy.issubdtype(ftype.value32, numpy.float32)
    assert numpy.issubdtype(ftype.value64, numpy.float64)

    obj = ftype()
    obj.from_dict(
            dict(value32=numpy.float64(32.0)),
            casting='safe',
            add_defaults=True,
            )


#----------------------------------------------------------


def test_complexes():
    df = DataFormat(prefix, 'user/complexes/1')
    assert df.valid

    ftype = df.type

    assert numpy.issubdtype(ftype.value64, numpy.complex64)
    assert numpy.issubdtype(ftype.value128, numpy.complex128)

    obj = ftype(
            value64=numpy.complex64(complex(1, 2)),
            value128=numpy.complex64(complex(1.4, 2.2)),
            )

    nose.tools.eq_(obj.value64.dtype, numpy.complex64)
    assert numpy.isclose(obj.value64, complex(1, 2))

    nose.tools.eq_(obj.value128.dtype, numpy.complex128)
    assert numpy.isclose(obj.value128, complex(1.4, 2.2))

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


def test_boolean():
    df = DataFormat(prefix, 'user/single_boolean/1')
    assert df.valid

    ftype = df.type

    assert numpy.issubdtype(ftype.value, numpy.bool_)

    obj = ftype(value=True)

    nose.tools.eq_(obj.value.dtype, numpy.bool_)
    assert obj.value #must be True

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


def test_string():
    df = DataFormat(prefix, 'user/single_string/1')
    assert df.valid

    ftype = df.type

    assert numpy.issubdtype(ftype.value, numpy.dtype(str).type)

    obj = ftype(value='123')

    assert isinstance(obj.value, str)
    nose.tools.eq_(obj.value, '123')

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

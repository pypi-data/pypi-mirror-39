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


def doit(format):

    df = DataFormat(prefix, format)
    assert df.valid, df.errors
    ftype = df.type

    obj = ftype()
    assert isinstance(obj.value, numpy.ndarray)
    nose.tools.eq_(obj.value.ndim, len(ftype.value)-1)
    nose.tools.eq_(obj.value.shape, tuple(ftype.value[:-1]))

    if ftype.value[-1] != str:
        nose.tools.eq_(obj.value.dtype, ftype.value[-1])
    else:
        assert issubclass(obj.value.dtype.type, object) #element for strings

    # checks JSON enconding
    copy = ftype(**obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


def test_empty_1d_array_of_integers():
    doit('user/empty_1d_array_of_integers/1')


#----------------------------------------------------------


def test_empty_2d_array_of_integers():
    doit('user/empty_2d_array_of_integers/1')


#----------------------------------------------------------


def test_empty_3d_array_of_integers():
    doit('user/empty_3d_array_of_integers/1')


#----------------------------------------------------------


def test_empty_fixed_2d_array_of_integers():
    doit('user/empty_2d_fixed_array_of_integers/1')


#----------------------------------------------------------


def test_1d_array_of_integers():
    doit('user/1d_array_of_integers/1')


#----------------------------------------------------------


def test_2d_array_of_integers():
    doit('user/2d_array_of_integers/1')


#----------------------------------------------------------


def test_3d_array_of_integers():
    doit('user/3d_array_of_integers/1')


#----------------------------------------------------------


def test_3d_array_of_integers_pack_unpack():

    df = DataFormat(prefix, 'user/3d_array_of_integers/1')
    assert df.valid, df.errors
    ftype = df.type

    obj = ftype()
    limits = numpy.iinfo(obj.value.dtype)
    obj.value = numpy.random.randint(low=limits.min, high=limits.max,
        size=obj.value.shape).astype(obj.value.dtype)

    # checks JSON enconding
    copy = ftype(**obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


def test_3d_array_of_floats_pack_unpack():

    df = DataFormat(prefix, 'user/3d_array_of_floats/1')
    assert df.valid, df.errors
    ftype = df.type

    obj = ftype()
    obj.value = numpy.random.rand(15, 72, 3).astype(float)

    # checks JSON enconding
    copy = ftype(**obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


def test_3d_array_of_complexes_pack_unpack():

    df = DataFormat(prefix, 'user/3d_array_of_complexes/1')
    assert df.valid, df.errors
    ftype = df.type

    obj = ftype()
    obj.value.real = numpy.random.rand(*obj.value.shape).astype(float)
    obj.value.imag = numpy.random.rand(*obj.value.shape).astype(float)

    # checks JSON enconding
    copy = ftype(**obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())


#----------------------------------------------------------


def test_empty_1d_array_of_objects():
    doit('user/empty_1d_array_of_objects/1')


#----------------------------------------------------------


def test_empty_2d_array_of_objects():
    doit('user/empty_2d_array_of_objects/1')


#----------------------------------------------------------


def test_empty_3d_array_of_objects():
    doit('user/empty_3d_array_of_objects/1')


#----------------------------------------------------------


def test_empty_fixed_2d_array_of_objects():
    doit('user/empty_2d_fixed_array_of_objects/1')


#----------------------------------------------------------


def test_1d_array_of_objects():
    doit('user/1d_array_of_objects/1')


#----------------------------------------------------------


def test_2d_array_of_objects():
    doit('user/2d_array_of_objects/1')


#----------------------------------------------------------


def test_3d_array_of_objects():
    doit('user/3d_array_of_objects/1')


#----------------------------------------------------------


def test_empty_1d_array_of_external_reference():
    doit('user/empty_1d_array_of_dataformat/1')


#----------------------------------------------------------


def test_empty_2d_array_of_external_reference():
    doit('user/empty_2d_array_of_dataformat/1')


#----------------------------------------------------------


def test_empty_3d_array_of_external_reference():
    doit('user/empty_3d_array_of_dataformat/1')


#----------------------------------------------------------


def test_empty_fixed_2d_array_of_external_reference():
    doit('user/empty_2d_fixed_array_of_dataformat/1')


#----------------------------------------------------------


def test_1d_array_of_external_reference():
    doit('user/1d_array_of_dataformat/1')


#----------------------------------------------------------


def test_2d_array_of_external_reference():
    doit('user/2d_array_of_dataformat/1')


#----------------------------------------------------------


def test_3d_array_of_external_reference():
    doit('user/3d_array_of_dataformat/1')


#----------------------------------------------------------


def test_empty_1d_array_of_external_reference_with_empty_array_of_objects():
    doit('user/empty_1d_array_of_dataformat_with_empty_array_of_objects/1')


#----------------------------------------------------------


def test_empty_1d_array_of_external_reference_with_array_of_objects():
    doit('user/empty_1d_array_of_dataformat_with_array_of_objects/1')


#----------------------------------------------------------


def test_1d_array_of_strings():
    doit('user/1d_array_of_strings/1')

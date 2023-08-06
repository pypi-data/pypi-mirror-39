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
    assert df.valid, '\n  * %s' % '\n  * '.join(df.errors)
    ftype = df.type

    obj = ftype()

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    return obj


#----------------------------------------------------------


def test_valid():
    obj = doit('user/extended/1')

    assert hasattr(obj, 'value')
    assert isinstance(obj.value, numpy.int32)
    assert hasattr(obj, 'value2')
    assert isinstance(obj.value2, numpy.bool_)


#----------------------------------------------------------


def test_extension_of_extended():
    obj = doit('user/extended2/1')

    assert hasattr(obj, 'value')
    assert isinstance(obj.value, numpy.int32)
    assert hasattr(obj, 'value2')
    assert isinstance(obj.value2, numpy.bool_)
    assert hasattr(obj, 'value3')
    assert isinstance(obj.value3, numpy.float32)


#----------------------------------------------------------


def test_issubclass():
    first = DataFormat(prefix, 'user/single_integer/1')
    assert first.valid, '\n  * %s' % '\n  * '.join(first.errors)

    middle = DataFormat(prefix, 'user/extended/1')
    assert middle.valid, '\n  * %s' % '\n  * '.join(middle.errors)

    last = DataFormat(prefix, 'user/extended2/1')
    assert last.valid, '\n  * %s' % '\n  * '.join(last.errors)

    assert first.isparent(middle)
    assert middle.isparent(last)
    assert first.isparent(last) #two hops

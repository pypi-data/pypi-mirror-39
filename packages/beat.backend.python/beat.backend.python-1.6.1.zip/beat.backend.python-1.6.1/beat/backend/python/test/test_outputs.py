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
import numpy
import nose.tools

from .mocks import MockDataSink

from ..outputs import Output, OutputList, SynchronizationListener
from ..dataformat import DataFormat
from beat.backend.python.baseformat import baseformat

from . import prefix


#----------------------------------------------------------


def test_creation_without_synchronization_listener():

    dataformat = DataFormat(prefix, 'user/single_integer/1')
    assert dataformat.valid
    data_sink = MockDataSink(dataformat)

    output = Output('test', data_sink)

    nose.tools.eq_(output.name, 'test')
    nose.tools.eq_(output.last_written_data_index, -1)
    nose.tools.eq_(output.nb_data_blocks_written, 0)
    assert output._synchronization_listener is None


#----------------------------------------------------------


def test_creation_with_synchronization_listener():

    dataformat = DataFormat(prefix, 'user/single_integer/1')
    assert dataformat.valid
    data_sink = MockDataSink(dataformat)

    synchronization_listener = SynchronizationListener()

    output = Output('test', data_sink, synchronization_listener)

    nose.tools.eq_(output.name, 'test')
    nose.tools.eq_(output.last_written_data_index, -1)
    nose.tools.eq_(output.nb_data_blocks_written, 0)
    assert output._synchronization_listener is not None
    nose.tools.eq_(output._synchronization_listener, synchronization_listener)


#----------------------------------------------------------


def test_data_creation():

    dataformat = DataFormat(prefix, 'user/single_integer/1')
    assert dataformat.valid
    data_sink = MockDataSink(dataformat)

    output = Output('test', data_sink)

    data = output._createData()
    assert data is not None
    assert isinstance(data, baseformat)
    nose.tools.eq_(data.value, 0)


#----------------------------------------------------------


def test_data_writting():

    dataformat = DataFormat(prefix, 'user/single_integer/1')
    assert dataformat.valid
    data_sink = MockDataSink(dataformat)

    synchronization_listener = SynchronizationListener()

    output = Output('test', data_sink, synchronization_listener)

    for i in six.moves.range(0, 5):
        synchronization_listener.onIntervalChanged(i, i)

        output.write({'value': numpy.int32(i*i)})
        nose.tools.eq_(output.last_written_data_index, i)
        nose.tools.eq_(output.nb_data_blocks_written, i + 1)
        assert not output.isDataMissing()

    nose.tools.eq_(len(data_sink.written), 5)

    for i in six.moves.range(0, 5):
        nose.tools.eq_(data_sink.written[i].data.value, i * i)
        nose.tools.eq_(data_sink.written[i].start, i)
        nose.tools.eq_(data_sink.written[i].end, i)


#----------------------------------------------------------


@nose.tools.raises(IOError)
def test_data_writting_failure():

    dataformat = DataFormat(prefix, 'user/single_integer/1')
    assert dataformat.valid
    data_sink = MockDataSink(dataformat)

    synchronization_listener = SynchronizationListener()

    output = Output('test', data_sink, synchronization_listener)

    synchronization_listener.onIntervalChanged(0, 0)

    output.write({'value': numpy.int32(42)})
    nose.tools.eq_(output.last_written_data_index, 0)
    nose.tools.eq_(output.nb_data_blocks_written, 1)
    assert not output.isDataMissing()

    data_sink.can_write = False

    synchronization_listener.onIntervalChanged(1, 1)

    output.write({'value': numpy.int32(42)}) #this should raise


#----------------------------------------------------------


def test_data_delaying():

    dataformat = DataFormat(prefix, 'user/single_integer/1')
    assert dataformat.valid
    data_sink = MockDataSink(dataformat)

    synchronization_listener = SynchronizationListener()

    output = Output('test', data_sink, synchronization_listener)

    for i in six.moves.range(0, 5):
        synchronization_listener.onIntervalChanged(i * 2, i * 2 + 1)
        output.write({'value': numpy.int32(i*i)})
        nose.tools.eq_(output.last_written_data_index, i * 2 + 1)
        nose.tools.eq_(output.nb_data_blocks_written, i + 1)
        assert not output.isDataMissing()

    nose.tools.eq_(len(data_sink.written), 5)

    for i in six.moves.range(0, 5):
        nose.tools.eq_(data_sink.written[i].data.value, i * i)
        nose.tools.eq_(data_sink.written[i].start, i * 2)
        nose.tools.eq_(data_sink.written[i].end, i * 2 + 1)


#----------------------------------------------------------


def test_data_writting_with_explicit_end_index():

    dataformat = DataFormat(prefix, 'user/single_integer/1')
    assert dataformat.valid
    data_sink = MockDataSink(dataformat)

    synchronization_listener = SynchronizationListener()

    output = Output('test', data_sink, synchronization_listener)

    for i in six.moves.range(0, 5):
        synchronization_listener.onIntervalChanged(i * 3, i * 3 + 2)

        output.write({'value': numpy.int32(i*i)}, i * 3 + 1)
        nose.tools.eq_(output.last_written_data_index, i * 3 + 1)
        nose.tools.eq_(output.nb_data_blocks_written, i + 1)
        assert output.isDataMissing()

    nose.tools.eq_(len(data_sink.written), 5)

    for i in six.moves.range(0, 5):
        nose.tools.eq_(data_sink.written[i].data.value, i * i)
        nose.tools.eq_(data_sink.written[i].start, max(i * 3 - 1, 0))
        nose.tools.eq_(data_sink.written[i].end, i * 3 + 1)


#----------------------------------------------------------


@nose.tools.raises(KeyError)
def test_data_writting_failure_with_explicit_end_index_too_low():

    dataformat = DataFormat(prefix, 'user/single_integer/1')
    assert dataformat.valid
    data_sink = MockDataSink(dataformat)

    synchronization_listener = SynchronizationListener()

    output = Output('test', data_sink, synchronization_listener)

    synchronization_listener.onIntervalChanged(0, 2)
    output.write({'value': numpy.int32(42)})

    synchronization_listener.onIntervalChanged(3, 5)

    # this must raise
    output.write({'value': numpy.int32(42)}, 1)


#----------------------------------------------------------


@nose.tools.raises(KeyError)
def test_data_writting_failure_with_explicit_end_index_too_high():

    dataformat = DataFormat(prefix, 'user/single_integer/1')
    assert dataformat.valid
    data_sink = MockDataSink(dataformat)

    synchronization_listener = SynchronizationListener()

    output = Output('test', data_sink, synchronization_listener)

    synchronization_listener.onIntervalChanged(0, 2)

    # this must raise
    output.write({'value': numpy.int32(42)}, 4)


#----------------------------------------------------------


def test_list_creation():
    outputs = OutputList()
    nose.tools.eq_(len(outputs), 0)


#----------------------------------------------------------


def test_output_list_addition():

    integer_format = DataFormat(prefix, 'user/single_integer/1')
    assert integer_format.valid
    integer_data_sink = MockDataSink(integer_format)

    float_format = DataFormat(prefix, 'user/single_float/1')
    assert float_format.valid
    float_data_sink = MockDataSink(float_format)

    synchronization_listener = SynchronizationListener()
    outputs = OutputList()

    outputs.add(Output('output1', integer_data_sink, synchronization_listener))

    nose.tools.eq_(len(outputs), 1)
    assert outputs[0] is not None
    nose.tools.eq_(outputs[0].name, 'output1')
    nose.tools.eq_(outputs[0]._synchronization_listener, synchronization_listener)
    assert outputs['output1'] is not None

    outputs.add(Output('output2', float_data_sink, synchronization_listener))

    nose.tools.eq_(len(outputs), 2)
    assert outputs[1] is not None
    nose.tools.eq_(outputs[1].name, 'output2')
    nose.tools.eq_(outputs[1]._synchronization_listener, synchronization_listener)
    assert outputs['output2'] is not None

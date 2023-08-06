#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/           #
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

import logging

from collections import namedtuple

from ..data import DataSource
from ..data import DataSink


class MockDataSource(DataSource):

    def __init__(self, data_and_indices):
        super(MockDataSource, self).__init__()
        self.infos = [ (x[1], x[2]) for x in data_and_indices ]
        self.data = [ x[0] for x in data_and_indices ]

    def __getitem__(self, index):
        return (self.data[index], self.infos[index][0], self.infos[index][1])


#----------------------------------------------------------


class CrashingDataSource(DataSource):

    def __init__(self):
        super(CrashingDataSource, self).__init__()

        Infos = namedtuple('Infos', ['start_index', 'end_index'])
        self.infos = [Infos(0, 0)]

    def __getitem__(self, index):
        a = b
        return (None, None, None)


#----------------------------------------------------------


class MockDataSink(DataSink):

    class WrittenData:
        def __init__(self, data, start, end):
            self.data = data
            self.start = start
            self.end = end

    def __init__(self, dataformat):
        self.written = []
        self.can_write = True
        self.dataformat = dataformat

    def write(self, data, start_data_index, end_data_index):
        if not(self.can_write): raise IOError
        self.written.append(
            MockDataSink.WrittenData(data, start_data_index, end_data_index)
        )

    def isConnected(self):
        return True

# Based on https://stackoverflow.com/a/20553331/5843716
class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs.

    Messages are available from an instance's ``messages`` dict, in order,
    indexed by a lowercase log level string (e.g., 'debug', 'info', etc.).
    """

    def __init__(self, *args, **kwargs):
        self.messages = {
            'debug': [], 'info': [],
            'warning': [], 'error': [],
            'critical': [], 'extra': []
        }
        super(MockLoggingHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        "Store a message from ``record`` in the instance's ``messages`` dict."
        try:
            self.messages[record.levelname.lower()].append(record.getMessage())
        except Exception:
            self.handleError(record)

    def reset(self):
        self.acquire()
        try:
            for message_list in self.messages.values():
                message_list.clear()
        finally:
            self.release()

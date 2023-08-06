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

import random
import numpy
from collections import namedtuple
from beat.backend.python.database import View


class Double(View):

    def index(self, root_folder, parameters):
        Entry = namedtuple('Entry', ['a', 'b', 'sum'])

        return [
            Entry(1, 10, 11),
            Entry(2, 20, 22),
            Entry(3, 30, 33),
            Entry(4, 40, 44),
            Entry(5, 50, 55),
            Entry(6, 60, 66),
            Entry(7, 70, 77),
            Entry(8, 80, 88),
            Entry(9, 90, 99),
        ]


    def get(self, output, index):
        obj = self.objs[index]

        if output == 'a':
            return {
                'value': numpy.int32(obj.a)
            }

        elif output == 'b':
            return {
                'value': numpy.int32(obj.b)
            }

        elif output == 'sum':
            return {
                'value': numpy.int32(obj.sum)
            }
        elif output == 'class':
            return {
                'value': numpy.int32(obj.cls)
            }


#----------------------------------------------------------


class Triple(View):

    def index(self, root_folder, parameters):
        Entry = namedtuple('Entry', ['a', 'b', 'c', 'sum'])

        return [
            Entry(1, 10, 100, 111),
            Entry(2, 20, 200, 222),
            Entry(3, 30, 300, 333),
            Entry(4, 40, 400, 444),
            Entry(5, 50, 500, 555),
            Entry(6, 60, 600, 666),
            Entry(7, 70, 700, 777),
            Entry(8, 80, 800, 888),
            Entry(9, 90, 900, 999),
        ]


    def get(self, output, index):
        obj = self.objs[index]

        if output == 'a':
            return {
                'value': numpy.int32(obj.a)
            }

        elif output == 'b':
            return {
                'value': numpy.int32(obj.b)
            }

        elif output == 'c':
            return {
                'value': numpy.int32(obj.c)
            }

        elif output == 'sum':
            return {
                'value': numpy.int32(obj.sum)
            }


#----------------------------------------------------------


class Labelled(View):

    def index(self, root_folder, parameters):
        Entry = namedtuple('Entry', ['label', 'value'])

        return [
            Entry('A', 1),
            Entry('A', 2),
            Entry('A', 3),
            Entry('A', 4),
            Entry('A', 5),
            Entry('B', 10),
            Entry('B', 20),
            Entry('B', 30),
            Entry('B', 40),
            Entry('B', 50),
            Entry('C', 100),
            Entry('C', 200),
            Entry('C', 300),
            Entry('C', 400),
            Entry('C', 500),
        ]


    def get(self, output, index):
        obj = self.objs[index]

        if output == 'label':
            return {
                'value': obj.label
            }

        elif output == 'value':
            return {
                'value': numpy.int32(obj.value)
            }


#----------------------------------------------------------


class DifferentFrequencies(View):

    def index(self, root_folder, parameters):
        Entry = namedtuple('Entry', ['a', 'b'])

        return [
            Entry(1, 10),
            Entry(1, 20),
            Entry(1, 30),
            Entry(1, 40),
            Entry(2, 50),
            Entry(2, 60),
            Entry(2, 70),
            Entry(2, 80),
        ]


    def get(self, output, index):
        obj = self.objs[index]

        if output == 'a':
            return {
                'value': numpy.int32(obj.a)
            }

        elif output == 'b':
            return {
                'value': numpy.int32(obj.b)
            }

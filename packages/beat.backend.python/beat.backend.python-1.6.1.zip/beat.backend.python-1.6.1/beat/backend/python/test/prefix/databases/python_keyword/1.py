#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2018 Idiap Research Institute, http://www.idiap.ch/           #
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


class Keyword(View):
    def __init__(self):
        super(Keyword, self)
        self.output_member_map = {
            'class': 'cls',
            'def': 'definition'
        }

    def index(self, root_folder, parameters):
        Entry = namedtuple('Entry', ['cls', 'definition', 'sum'])

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

        if output == 'class':
            return {
                'value': numpy.int32(obj.cls)
            }
        elif output == 'def':
            return {
                'value': numpy.int32(obj.definition)
            }
        elif output == 'sum':
            return {
                'value': numpy.int32(obj.sum)
            }



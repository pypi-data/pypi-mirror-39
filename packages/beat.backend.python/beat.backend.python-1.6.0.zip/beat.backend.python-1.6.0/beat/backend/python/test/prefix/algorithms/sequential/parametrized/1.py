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

class Algorithm:

    def setup(self, parameters):
        self.int8_value      = parameters['int8_value']
        self.int8_range      = parameters['int8_range']
        self.int8_choices    = parameters['int8_choices']
        self.int16_value     = parameters['int16_value']
        self.int16_range     = parameters['int16_range']
        self.int16_choices   = parameters['int16_choices']
        self.int32_value     = parameters['int32_value']
        self.int32_range     = parameters['int32_range']
        self.int32_choices   = parameters['int32_choices']
        self.int64_value     = parameters['int64_value']
        self.int64_range     = parameters['int64_range']
        self.int64_choices   = parameters['int64_choices']
        self.uint8_value     = parameters['uint8_value']
        self.uint8_range     = parameters['uint8_range']
        self.uint8_choices   = parameters['uint8_choices']
        self.uint16_value    = parameters['uint16_value']
        self.uint16_range    = parameters['uint16_range']
        self.uint16_choices  = parameters['uint16_choices']
        self.uint32_value    = parameters['uint32_value']
        self.uint32_range    = parameters['uint32_range']
        self.uint32_choices  = parameters['uint32_choices']
        self.uint64_value    = parameters['uint64_value']
        self.uint64_range    = parameters['uint64_range']
        self.uint64_choices  = parameters['uint64_choices']
        self.float32_value   = parameters['float32_value']
        self.float32_range   = parameters['float32_range']
        self.float32_choices = parameters['float32_choices']
        self.float64_value   = parameters['float64_value']
        self.float64_range   = parameters['float64_range']
        self.float64_choices = parameters['float64_choices']
        self.bool_value      = parameters['bool_value']
        self.string_value    = parameters['string_value']
        return True

    def process(self, inputs, data_loaders, outputs):
        return True

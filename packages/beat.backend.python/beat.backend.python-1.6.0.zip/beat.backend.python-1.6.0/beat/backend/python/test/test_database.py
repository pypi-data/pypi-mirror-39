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
from ..database import Database

from . import prefix


#----------------------------------------------------------


def load(database_name):

    database = Database(prefix, database_name)
    assert database.valid
    return database


#----------------------------------------------------------


def test_load_valid_database():

    database = Database(prefix, 'integers_db/1')
    assert database.valid, '\n  * %s' % '\n  * '.join(database.errors)

    nose.tools.eq_(len(database.sets("double")), 1)
    nose.tools.eq_(len(database.sets("triple")), 1)
    nose.tools.eq_(len(database.sets("two_sets")), 2)


#----------------------------------------------------------


def test_load_protocol_with_one_set():

    database = Database(prefix, 'integers_db/1')

    protocol = database.protocol("double")
    nose.tools.eq_(len(protocol['sets']), 1)

    set = database.set("double", "double")

    nose.tools.eq_(set['name'], 'double')
    nose.tools.eq_(len(set['outputs']), 3)

    assert set['outputs']['a'] is not None
    assert set['outputs']['b'] is not None
    assert set['outputs']['sum'] is not None


#----------------------------------------------------------


def test_load_protocol_with_two_sets():

    database = Database(prefix, 'integers_db/1')

    protocol = database.protocol("two_sets")
    nose.tools.eq_(len(protocol['sets']), 2)

    set = database.set("two_sets", "double")

    nose.tools.eq_(set['name'], 'double')
    nose.tools.eq_(len(set['outputs']), 3)

    assert set['outputs']['a'] is not None
    assert set['outputs']['b'] is not None
    assert set['outputs']['sum'] is not None

    set = database.set("two_sets", "triple")

    nose.tools.eq_(set['name'], 'triple')
    nose.tools.eq_(len(set['outputs']), 4)

    assert set['outputs']['a'] is not None
    assert set['outputs']['b'] is not None
    assert set['outputs']['c'] is not None
    assert set['outputs']['sum'] is not None

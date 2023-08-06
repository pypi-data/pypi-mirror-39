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


import sys
import os
import platform
import collections
import simplejson


def main():

    # resolve package name
    name = 'environment'
    if len(sys.argv) > 1:
        name = sys.argv[1]

    # resolve version
    version = '1'
    if len(sys.argv) > 2:
        version = sys.argv[2]

    # use a configuration file if one exists
    databases = None
    capabilities = None
    if os.path.exists('/etc/beat/environment.json'):
        with open('/etc/beat/environment.json', 'r') as config_file:
            config = simplejson.load(config_file)
            name = config.get('name', name)
            version = config.get('version', version)
            databases = config.get('databases', None)
            capabilities = config.get('capabilities', None)

    # print the result
    retval = collections.OrderedDict()
    retval['name'] = name
    retval['version'] = version
    retval['os'] = platform.uname()

    if databases is not None:
        retval['databases'] = databases

    if capabilities is not None:
        retval['capabilities'] = capabilities

    print(simplejson.dumps(retval, indent=2))

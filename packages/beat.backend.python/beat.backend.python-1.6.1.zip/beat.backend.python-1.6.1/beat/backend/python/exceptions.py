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


"""
==========
exceptions
==========

Custom exceptions
"""

class RemoteException(Exception):
    """Exception happening on a remote location"""

    def __init__(self, kind, message):
        super(RemoteException, self).__init__()

        if kind == 'sys':
            self.system_error = message
            self.user_error = ''
        else:
            self.system_error = ''
            self.user_error = message

    def __str__(self):
        if self.system_error:
            return '(sys) {}'.format(self.system_error)
        else:
            return '(usr) {}'.format(self.user_error)


class UserError(Exception):
    """User exception"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

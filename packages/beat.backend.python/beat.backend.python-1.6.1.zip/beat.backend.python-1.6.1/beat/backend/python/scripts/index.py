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


"""Executes some database views. (%(version)s)

usage:
  %(prog)s [--debug] [--uid=UID] [--db_root_folder=root_folder] <prefix> <cache> <database> [<protocol> [<set>]]
  %(prog)s (--help)
  %(prog)s (--version)


arguments:
  <prefix>   Path to the prefix
  <cache>    Path to the cache
  <database> Full name of the database


options:
  -h, --help                    Shows this help message and exit
  -V, --version                 Shows program's version number and exit
  -d, --debug                   Runs in debugging mode
  --uid=UID                     UID to run as
  --db_root_folder=root_folder  Root folder to use for the database data (overrides the
                                one declared by the database)

"""

import logging

import os
import sys
import docopt
import pwd

from ..database import Database
from ..hash import hashDataset
from ..hash import toPath


#----------------------------------------------------------


def main(arguments=None):

    # Parse the command-line arguments
    if arguments is None:
        arguments = sys.argv[1:]

    package = __name__.rsplit('.', 2)[0]
    version = package + ' v' + \
              __import__('pkg_resources').require(package)[0].version

    prog = os.path.basename(sys.argv[0])

    args = docopt.docopt(
        __doc__ % dict(prog=prog, version=version),
        argv=arguments,
        version=version
    )


    # Setup the logging system
    formatter = logging.Formatter(fmt="[%(asctime)s - index.py - " \
                                      "%(name)s] %(levelname)s: %(message)s",
                                  datefmt="%d/%b/%Y %H:%M:%S")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger('beat.backend.python')
    root_logger.addHandler(handler)

    if args['--debug']:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    logger = logging.getLogger(__name__)


    if args['--uid']:
        uid = int(args['--uid'])

        # First create the user (if it doesn't exists)
        try:
            user = pwd.getpwuid(uid)
        except:
            import subprocess
            retcode = subprocess.call(['adduser', '--uid', str(uid),
                                       '--no-create-home', '--disabled-password',
                                       '--disabled-login', '--gecos', '""', '-q',
                                       'beat-nobody'])
            if retcode != 0:
                logger.error('Failed to create an user with the UID %d' % uid)
                return 1

        # Change the current user
        try:
            os.setgid(uid)
            os.setuid(uid)
        except:
            import traceback
            logger.error(traceback.format_exc())
            return 1


    # Check the paths
    if not os.path.exists(args['<prefix>']):
        logger.error('Invalid prefix path: %s' % args['<prefix>'])
        return 1

    if not os.path.exists(args['<cache>']):
        logger.error('Invalid cache path: %s' % args['<cache>'])
        return 1


    # Indexing
    try:
        database = Database(args['<prefix>'], args['<database>'])

        if args['<protocol>'] is None:
            protocols = database.protocol_names
        else:
            protocols = [ args['<protocol>'] ]

        for protocol in protocols:

            if args['<set>'] is None:
                sets = database.set_names(protocol)
            else:
                sets = [ args['<set>'] ]

            for set_name in sets:
                filename = toPath(hashDataset(args['<database>'], protocol, set_name),
                                  suffix='.db')

                view = database.view(protocol, set_name, root_folder=args['--db_root_folder'])
                view.index(os.path.join(args['<cache>'], filename))

    except Exception as e:
        import traceback
        logger.error(traceback.format_exc())
        return 1

    return 0



if __name__ == '__main__':
    sys.exit(main())

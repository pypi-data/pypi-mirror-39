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


"""
======
loader
======

This modules implements a simple loader for Python code as well as safe
executor. Safe in this context means that if the method raises an
exception, it will catch it and return in a suitable form to the caller.
"""

import sys
import six
import imp


# ----------------------------------------------------------


def load_module(name, path, uses):
    """Loads the Python file as module, returns  a proper Python module


    Parameters:

      name (str): The name of the Python module to create. Must be a valid
        Python symbol name

      path (str): The full path of the Python file to load the module contents
        from

      uses (dict): A mapping which indicates the name of the library to load
        (as a module for the current library) and the full-path and use
        mappings of such modules.


    Returns:

      :std:term:`module`: A valid Python module you can use in an Algorithm or
          Library.
    """

    retval = imp.new_module(name)

    # loads used modules
    for k, v in uses.items():
        retval.__dict__[k] = load_module(k, v['path'], v['uses'])

    # execute the module code on the context of previously import modules
    exec(compile(open(path, "rb").read(), path, 'exec'), retval.__dict__)

    return retval


# ----------------------------------------------------------


def run(obj, method, exc=None, *args, **kwargs):
    """Runs a method on the object and protects its execution

    In case an exception is raised, it is caught and transformed into the
    exception class the user passed.

    Parameters:

      obj (object): The python object in which execute the method

      method (str): The method name to execute on the object

      exc (:std:term:`class`, Optional): The class to use as base exception
        when translating the exception from the user code. If you set it to
        ``None``, then just re-throws the user raised exception.

      *args: Arguments to the object method, passed unchanged

      **kwargs: Arguments to the object method, passed unchanged

    Returns:

      object: whatever ``obj.method()`` is bound to return.

    """

    try:
        if method == '__new__':
            return obj(*args, **kwargs)

        return getattr(obj, method)(*args, **kwargs)
    except Exception:
        if exc is not None:
            type, value, traceback = sys.exc_info()
            six.reraise(exc, exc(value), traceback)
        else:
            raise  # just re-raise the user exception

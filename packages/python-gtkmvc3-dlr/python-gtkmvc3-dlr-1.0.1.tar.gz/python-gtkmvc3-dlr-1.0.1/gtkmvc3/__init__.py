#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2005-2015 by Roberto Cavada
#
#  gtkmvc3 is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  gtkmvc3 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on gtkmvc3 see <https://github.com/roboogle/gtkmvc3>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <https://github.com/roboogle/gtkmvc3/issues>
#  or to <roboogle@gmail.com>.

"""
Shortcuts are provided to the following classes defined in submodules:

.. class:: Model
   :noindex:
.. class:: TreeStoreModel
   :noindex:
.. class:: ListStoreModel
   :noindex:
.. class:: TextBufferModel
   :noindex:
.. class:: ModelMT
   :noindex:
.. class:: Controller
   :noindex:
.. class:: View
   :noindex:
.. class:: Observer
   :noindex:
.. class:: Observable
   :noindex:

The following two functions are not exported by default, you have to prefix
identifiers with the module name:
"""

__version = (1,0,1)

# Only import packages that do not import gtk
# => allows to use gtkmvc without GTK (useful for Observer/Observable classes)

# visible classes
from gtkmvc3.observer import Observer
from gtkmvc3.observable import Observable, Signal


def get_version():
    """
    Return the imported version of this framework as a tuple of integers.
    """
    return __version


def require(request):
    """
    Raise :exc:`AssertionError` if gtkmvc3 version is not compatible.

    *request* a dotted string or iterable of string or integers representing the
    minimum version you need. ::

     require("1.0")
     require(("1", "2", "2"))
     require([1,99,0])

    .. note::

       For historical reasons this does not take all API changes into account.
       Some are caught by the argument checks in View and Controller
       constructors.
    """
    try:
        request = request.split(".")
    except AttributeError:
        pass
    request = [int(x) for x in request]

    provide = list(__version)

    if request > provide:
        raise AssertionError("gtkmvc3 required version %s, found %s" % (
            request, provide))

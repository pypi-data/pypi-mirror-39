#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.core module of the BEAT platform.             #
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
=====
utils
=====

Helper methods

Forward imports from :py:mod:`beat.backend.python.utils`
"""


import os
import sys
import tempfile
import socket
import contextlib
import string
import random

import numpy
import simplejson

from beat.backend.python.utils import *

from . import hash

# ----------------------------------------------------------


def temporary_directory(prefix='beat_'):
    """Generates a temporary directory"""

    if sys.platform == 'darwin':
        return tempfile.mkdtemp(prefix=prefix, dir='/tmp')
    else:
        return tempfile.mkdtemp(prefix=prefix)


# ----------------------------------------------------------


def uniq(seq):
    '''Order preserving (very fast) uniq function for sequences'''

    seen = set()
    result = []
    for item in seq:
        if item in seen: continue
        seen.add(item)
        result.append(item)

    return result


# ----------------------------------------------------------


def send_multipart(socket, parts):
    """
    Send the parts through the socket after having encoded them if
    necessary.
    """

    for index, item in enumerate(parts):
        if isinstance(item, six.string_types):
            parts[index] = item.encode('utf-8')

    socket.send_multipart(parts)


# ----------------------------------------------------------


def find_free_port():
    '''Returns the value of a free random port'''

    with contextlib.closing(socket.socket(socket.AF_INET,
      socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


#----------------------------------------------------------


def find_free_port_in_range(min_port, max_port):
    '''Returns the value of a free port in range'''

    for port in range(min_port, max_port):
        with contextlib.closing(socket.socket(socket.AF_INET,
            socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(('', port))
            except socket.error as e:
                continue
            else:
                return sock.getsockname()[1]


#----------------------------------------------------------


def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """ Simple id generator based on
    https://stackoverflow.com/a/2257449/5843716
    """
    return ''.join(random.choice(chars) for _ in range(size))



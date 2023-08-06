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
====
data
====

Forward importing from :py:mod:`beat.backend.python.data`:
:py:func:`beat.backend.python.data.mixDataIndices`
:py:func:`beat.backend.python.data.getAllFilenames`
:py:class:`beat.backend.python.data.DataSource`
:py:class:`beat.backend.python.data.CachedDataSource`
:py:class:`beat.backend.python.data.DatabaseOutputDataSource`
:py:class:`beat.backend.python.data.RemoteDataSource`
:py:class:`beat.backend.python.data.DataSink`
:py:class:`beat.backend.python.data.CachedDataSink`
:py:class:`beat.backend.python.data.StdoutDataSink`
:py:func:`beat.backend.python.data.load_data_index`
:py:func:`beat.backend.python.data.load_data_index_db`
:py:func:`beat.backend.python.data.foundSplitRanges`
"""

from beat.backend.python.data import mixDataIndices
from beat.backend.python.data import getAllFilenames
from beat.backend.python.data import DataSource
from beat.backend.python.data import CachedDataSource
from beat.backend.python.data import DatabaseOutputDataSource
from beat.backend.python.data import RemoteDataSource
from beat.backend.python.data import DataSink
from beat.backend.python.data import CachedDataSink
from beat.backend.python.data import StdoutDataSink
from beat.backend.python.data import load_data_index
from beat.backend.python.data import load_data_index_db
from beat.backend.python.data import foundSplitRanges

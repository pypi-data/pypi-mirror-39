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


from ..data import DataSource
from ..data import DataSink


class MockDataSource(DataSource):

    def __init__(self, data, indexes):
        self.data = list(data)
        self.indexes = list(indexes)
        self.current = 0

    def next(self):
        result = (self.data[self.current], self.indexes[self.current][0], self.indexes[self.current][1])
        self.current += 1
        return result

    def hasMoreData(self):
        return self.current < sum(1 for i in self.data)


#----------------------------------------------------------


class MockDataSink(DataSink):

    class WrittenData:
        def __init__(self, data, start, end):
            self.data = data
            self.start = start
            self.end = end

    def __init__(self, dataformat):
        self.written = []
        self.can_write = True
        self.dataformat = dataformat

    def write(self, data, start_data_index, end_data_index):
        if not(self.can_write): raise IOError
        self.written.append(
                MockDataSink.WrittenData(data, start_data_index, end_data_index)
                )

    def isConnected(self):
        return True


#----------------------------------------------------------


class MockDataSource_Crash(DataSource):

    def next(self):
        a = b

    def hasMoreData(self):
        a = b
        return False

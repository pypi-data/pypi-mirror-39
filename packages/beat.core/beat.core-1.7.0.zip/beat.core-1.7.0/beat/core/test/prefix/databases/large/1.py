#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2017 Idiap Research Institute, http://www.idiap.ch/           #
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

import numpy
from collections import namedtuple
from beat.backend.python.database import View


#----------------------------------------------------------


class LargeView(View):

    def __init__(self):
        super(LargeView, self).__init__()
        numpy.random.seed(0)  # So it is kept reproducible


    def index(self, root_folder, parameters):
        Entry = namedtuple('Entry', ['out'])

        entries = []
        for i in range(0, 1000):
            entries.append(numpy.int32(numpy.random.randint(100, size=(1000,))))

        return entries


    def get(self, output, index):
        obj = self.objs[index]

        if output == 'out':
            return {
                'value': obj.out
            }


#----------------------------------------------------------


class SmallView(View):

    def __init__(self):
        super(SmallView, self).__init__()
        numpy.random.seed(0)  # So it is kept reproducible


    def index(self, root_folder, parameters):
        Entry = namedtuple('Entry', ['out'])

        entries = []
        for i in range(0, 1000):
            entries.append(numpy.int32(numpy.random.randint(0, 100)))

        return entries


    def get(self, output, index):
        obj = self.objs[index]

        if output == 'out':
            return {
                'value': obj.out
            }

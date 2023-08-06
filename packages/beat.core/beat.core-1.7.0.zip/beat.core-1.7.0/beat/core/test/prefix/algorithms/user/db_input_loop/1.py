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

import numpy as np

class Algorithm:

    def __init__(self):
        self.threshold = None
        self.max = 0

    def setup(self, parameters):
        self.threshold = parameters['threshold']
        return True

    def prepare(self, data_loaders):
        data_loader = data_loaders.loaderOf('in')

        for i in range(data_loader.count()):
            view = data_loader.view('in', i)
            (data, _, _) = view[view.count() - 1]
            value = data['in'].value
            self.max += value

        return True

    def validate(self, result):
        value = result.value
        result = value > self.threshold and value < self.max
        delta = self.max - value
        return (result, {'value': np.int32(delta)})

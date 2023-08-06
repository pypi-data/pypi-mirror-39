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


import nose.tools
from ..toolchain import Toolchain

from . import prefix

def test_integers_addition_1():

    toolchain = Toolchain(prefix, 'user/integers_addition/1')
    assert toolchain.valid

    order = toolchain.execution_order()
    nose.tools.eq_(list(order.keys()), ['addition', 'analysis'])
    nose.tools.eq_(order['addition'], set())
    nose.tools.eq_(order['analysis'], set(['addition']))

def test_integers_addition_2():

    toolchain = Toolchain(prefix, 'user/integers_addition/2')
    assert toolchain.valid

    order = toolchain.execution_order()
    nose.tools.eq_(list(order.keys()), ['addition1', 'addition2', 'analysis'])
    nose.tools.eq_(order['addition1'], set())
    nose.tools.eq_(order['addition2'], set(['addition1']))
    nose.tools.eq_(order['analysis'], set(['addition2']))

def test_integers_addition_3():

    toolchain = Toolchain(prefix, 'user/integers_addition/3')
    assert toolchain.valid

    order = toolchain.execution_order()
    nose.tools.eq_(list(order.keys()), ['addition1', 'addition2', 'addition3', 'analysis'])
    nose.tools.eq_(order['addition1'], set())
    nose.tools.eq_(order['addition2'], set())
    nose.tools.eq_(order['addition3'], set(['addition1', 'addition2']))
    nose.tools.eq_(order['analysis'], set(['addition3']))

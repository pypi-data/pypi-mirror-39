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


import six
import nose.tools

from ..algorithm import Algorithm

from . import prefix, tmp_prefix
from .utils import cleanup


#----------------------------------------------------------


def test_load_default_algorithm():

    algorithm = Algorithm(prefix, data=None)
    assert algorithm.valid, '\n  * %s' % '\n  * '.join(algorithm.errors)


#----------------------------------------------------------


def test_missing_inputs():

    algorithm = Algorithm(prefix, 'user/no_inputs_declarations/1')
    assert algorithm.valid is False
    assert algorithm.errors[0].find("'inputs' is a required property") != -1


#----------------------------------------------------------


def test_missing_outputs():

    algorithm = Algorithm(prefix, 'user/no_outputs_declarations/1')
    assert algorithm.valid is False
    assert algorithm.errors[0].find("'outputs' is a required property") != -1


#----------------------------------------------------------


def test_invalid_loop_channel():

    algorithm = Algorithm(prefix, 'schema/invalid_loop_channel/1')
    assert algorithm.valid is False
    assert algorithm.errors[0].find("'request' is a required property") != -1


#----------------------------------------------------------


def test_v2():

    algorithm = Algorithm(prefix, 'user/integers_add_v2/1')
    assert algorithm.valid, '\n  * %s' % '\n  * '.join(algorithm.errors)


def test_analyzer_v2():

    algorithm = Algorithm(prefix, 'user/integers_echo_analyzer_v2/1')
    assert algorithm.valid, '\n  * %s' % '\n  * '.join(algorithm.errors)


def test_v3():

    algorithm = Algorithm(prefix, 'autonomous/loop/1')
    assert algorithm.valid, '\n  * %s' % '\n  * '.join(algorithm.errors)


    algorithm = Algorithm(prefix, 'autonomous/loop_user/1')
    assert algorithm.valid, '\n  * %s' % '\n  * '.join(algorithm.errors)


def test_invalid_v3():
    algorithm = Algorithm(prefix, 'schema/invalid_loop_output/1')
    assert not algorithm.valid

    algorithm = Algorithm(prefix, 'schema/invalid_loop_type/1')
    assert not algorithm.valid

    algorithm = Algorithm(prefix, 'schema/invalid_loop_user_type/1')
    assert not algorithm.valid


#----------------------------------------------------------


@nose.tools.with_setup(teardown=cleanup)
def test_export():

    name = 'user/for_dep/1'
    obj = Algorithm(prefix, name)
    assert obj.valid, '\n  * %s' % '\n  * '.join(obj.errors)

    obj.export(tmp_prefix)

    # load from tmp_prefix and validates
    exported = Algorithm(tmp_prefix, name)
    assert exported.valid, '\n  * %s' % '\n  * '.join(exported.errors)

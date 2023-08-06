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
from ..experiment import Experiment

from . import prefix, tmp_prefix
from .utils import cleanup

def test_load_valid_experiment():

    experiment = Experiment(prefix, 'user/integers_addition/1/integers_addition')

    assert experiment.valid, '\n  * %s' % '\n  * '.join(experiment.errors)
    nose.tools.eq_(experiment.label,
            'user/user/integers_addition/1/integers_addition')

    assert experiment.toolchain.valid, '\n  * %s' % '\n  * '.join(experiment.toolchain.errors)
    nose.tools.eq_(experiment.toolchain.name, 'user/integers_addition/1')

    nose.tools.eq_(len(experiment.datasets), 1)
    assert 'integers' in experiment.datasets
    nose.tools.eq_(len(experiment.databases), 1)
    nose.tools.eq_(len(experiment.blocks), 1)
    nose.tools.eq_(len(experiment.analyzers), 1)

    nose.tools.eq_(len(experiment.algorithms), 2)
    assert 'user/sum/1' in experiment.algorithms
    assert experiment.algorithms['user/sum/1'].valid
    assert 'user/integers_analysis/1' in experiment.algorithms
    assert experiment.algorithms['user/integers_analysis/1'].valid

def test_load_one_dataset_two_blocks_toolchain():

    experiment = Experiment(prefix, 'user/integers_addition/2/integers_addition')
    assert experiment.valid, '\n  * %s' % '\n  * '.join(experiment.errors)
    nose.tools.eq_(experiment.label,
            'user/user/integers_addition/2/integers_addition')

    assert experiment.toolchain.valid, '\n  * %s' % '\n  * '.join(experiment.toolchain.errors)
    nose.tools.eq_(experiment.toolchain.name, 'user/integers_addition/2')

    nose.tools.eq_(len(experiment.datasets), 1)
    assert 'integers' in experiment.datasets
    nose.tools.eq_(len(experiment.databases), 1)
    nose.tools.eq_(len(experiment.blocks), 2)
    nose.tools.eq_(len(experiment.analyzers), 1)

    nose.tools.eq_(len(experiment.algorithms), 2)
    assert 'user/sum/1' in experiment.algorithms
    assert experiment.algorithms['user/sum/1'].valid
    assert 'user/integers_analysis/1' in experiment.algorithms
    assert experiment.algorithms['user/integers_analysis/1'].valid

def test_load_two_datasets_three_blocks_toolchain():

    experiment = Experiment(prefix, 'user/integers_addition/3/integers_addition')
    assert not experiment.valid
    nose.tools.eq_(experiment.label,
            'user/user/integers_addition/3/integers_addition')
    assert experiment.errors[0].find("mismatch in input/output") != -1

    assert experiment.toolchain.valid
    nose.tools.eq_(experiment.toolchain.name, 'user/integers_addition/3')

    nose.tools.eq_(len(experiment.datasets), 2)
    assert 'integers1' in experiment.datasets
    assert 'integers2' in experiment.datasets
    nose.tools.eq_(len(experiment.databases), 1)
    nose.tools.eq_(len(experiment.blocks), 3)
    nose.tools.eq_(len(experiment.analyzers), 1)

    nose.tools.eq_(len(experiment.algorithms), 2)
    assert 'user/sum/1' in experiment.algorithms
    assert experiment.algorithms['user/sum/1'].valid
    assert 'user/integers_analysis/1' in experiment.algorithms
    assert experiment.algorithms['user/integers_analysis/1'].valid

def test_no_description():

    experiment = Experiment(prefix, 'user/integers_addition/1/integers_addition')
    assert experiment.valid, '\n  * %s' % '\n  * '.join(experiment.errors)
    assert experiment.description is None
    assert experiment.documentation is None

    description = 'This is my descriptor'
    experiment.description = description
    assert isinstance(experiment.description, six.string_types)
    nose.tools.eq_(experiment.description, description)


@nose.tools.with_setup(teardown=cleanup)
def test_export():

    name = 'user/integers_addition/1/integers_addition'
    obj = Experiment(prefix, name)
    assert obj.valid, '\n  * %s' % '\n  * '.join(obj.errors)

    obj.export(tmp_prefix)

    # load from tmp_prefix and validates
    exported = Experiment(tmp_prefix, name)
    assert exported.valid, '\n  * %s' % '\n  * '.join(exported.errors)

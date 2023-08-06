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

def count_errors(l, e):
    """Makes sure a given string is present in one of the errors"""
    return sum([int(k.find(e) != -1) for k in l])

def test_load_default():

    toolchain = Toolchain(prefix, data=None)
    assert toolchain.valid, '\n  * %s' % '\n  * '.join(toolchain.errors)

def test_load_unknown_toolchain():

    toolchain = Toolchain(prefix, 'user/unknown/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, 'file not found'), 1)

def test_load_invalid_toolchain():

    toolchain = Toolchain(prefix, 'user/invalid/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, 'invalid JSON'), 1)

def test_load_toolchain_without_blocks_list():

    toolchain = Toolchain(prefix, 'user/missing_blocks/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "'blocks' is a required property"), 1)

def test_load_toolchain_with_missing_block_name():

    toolchain = Toolchain(prefix, 'user/missing_block_name/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "'name' is a required property"), 1)

def test_load_toolchain_with_missing_block_inputs():

    toolchain = Toolchain(prefix, 'user/missing_block_inputs/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "'inputs' is a required property"), 1)

def test_load_toolchain_with_missing_block_outputs():

    toolchain = Toolchain(prefix, 'user/missing_block_outputs/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "'outputs' is a required property"), 1)

def test_load_toolchain_without_datasets_list():

    toolchain = Toolchain(prefix, 'user/missing_datasets/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "'datasets' is a required property"), 1)

def test_load_toolchain_with_missing_dataset_name():

    toolchain = Toolchain(prefix, 'user/missing_dataset_name/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "'name' is a required property"), 1)

def test_load_toolchain_with_missing_dataset_outputs():

    toolchain = Toolchain(prefix, 'user/missing_dataset_outputs/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "'outputs' is a required property"), 1)

def test_load_toolchain_with_missing_connection_from():

    toolchain = Toolchain(prefix, 'user/missing_connection_from/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "'from' is a required property"), 1)

def test_load_toolchain_with_missing_connection_to():

    toolchain = Toolchain(prefix, 'user/missing_connection_to/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "'to' is a required property"), 1)

def test_load_toolchain_referencing_unknown_block_input():

    toolchain = Toolchain(prefix, 'user/unknown_block_input/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "invalid input endpoint 'addition.c'"), 1)

def test_load_toolchain_referencing_unknown_dataset_output():

    toolchain = Toolchain(prefix, 'user/unknown_dataset_output/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "invalid output endpoint 'integers.timestamps'"), 1)

def test_load_toolchain_referencing_unknown_block_output():

    toolchain = Toolchain(prefix, 'user/unknown_block_output/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "invalid output endpoint 'addition.unknown'"), 1)

def test_load_toolchain_referencing_unknown_analyzer_input():

    toolchain = Toolchain(prefix, 'user/unknown_analyzer_input/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "invalid input endpoint 'analysis.unknown'"), 1)

def test_load_toolchain_unconnected_input():

    toolchain = Toolchain(prefix, 'user/unconnected_input/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "input(s) `addition.b' remain unconnected"), 1)

def test_load_toolchain_double_connected_input():

    toolchain = Toolchain(prefix, 'user/double_connected_input/1')
    assert toolchain.valid is False
    nose.tools.eq_(count_errors(toolchain.errors, "ending on the same input as"), 1)

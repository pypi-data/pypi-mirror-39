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


import os

import six
import numpy
import nose.tools

from ..dataformat import DataFormat

from . import prefix, tmp_prefix
from .utils import cleanup

def test_load_default_format():

    df = DataFormat(prefix, data=None)
    assert df.valid, '\n  * %s' % '\n  * '.join(df.errors)

def test_load_unknown_format():

    df = DataFormat(prefix, 'user/unknown/1')
    assert df.valid is False
    assert df.errors
    nose.tools.eq_(len(df.errors), 1)
    assert df.errors[0].find('file not found') != -1

def test_load_invalid_format():

    df = DataFormat(prefix, 'user/invalid/1')
    assert df.valid is False
    assert df.errors
    nose.tools.eq_(len(df.errors), 1)
    assert df.errors[0].find('invalid JSON code') != -1

def test_load_valid_format():

    df = DataFormat(prefix, 'user/single_integer/1')
    assert df.valid, '\n  * %s' % '\n  * '.join(df.errors)
    nose.tools.eq_(len(df.errors), 0)

@nose.tools.raises(RuntimeError)
def test_fail_to_create_data_of_unknown_format():

    df = DataFormat(prefix, 'user/unknown/1')
    assert df.valid is False
    assert df.type

def test_fail_to_load_format_with_several_invalid_types():

    df = DataFormat(prefix, 'user/errors/1')
    assert df.valid is False
    nose.tools.eq_(len(df.errors), 1)
    assert df.errors[0].find('is not valid under any of the given schemas') != -1

def test_load_valid_format_from_JSON_declaration():

    df = DataFormat(prefix, dict(value='int32'))
    assert df.valid, '\n  * %s' % '\n  * '.join(df.errors)
    assert df.name == '__unnamed_dataformat__'

def test_load_versioned_format():

    df1 = DataFormat(prefix, 'user/versioned/1')
    assert df1.valid, '\n  * %s' % '\n  * '.join(df1.errors)
    nose.tools.eq_(df1.name, 'user/versioned/1')

    df2 = DataFormat(prefix, 'user/versioned/2')
    assert df2.valid, '\n  * %s' % '\n  * '.join(df2.errors)
    nose.tools.eq_(df2.name, 'user/versioned/2')

    ftype = df2.type
    instance = ftype(value=numpy.float32(32))
    assert isinstance(instance.value, numpy.float32)

def test_no_description():

    df = DataFormat(prefix, 'user/versioned/1')
    assert df.valid, '\n  * %s' % '\n  * '.join(df.errors)
    assert df.description is None
    assert df.documentation is None

    description = 'This is my descriptor'
    df.description = description
    assert isinstance(df.description, six.string_types)
    nose.tools.eq_(df.description, description)

def test_with_description():

    df = DataFormat(prefix, 'user/versioned/2')
    assert df.valid, '\n  * %s' % '\n  * '.join(df.errors)
    assert isinstance(df.description, six.string_types)
    assert len(df.description) != 0
    assert df.documentation is None

def test_description_does_not_affect_hash():

    df2 = DataFormat(prefix, 'user/versioned/2')
    assert df2.valid, '\n  * %s' % '\n  * '.join(df2.errors)
    df3 = DataFormat(prefix, 'user/versioned/3') #the same, but no description
    assert df3.valid, '\n  * %s' % '\n  * '.join(df3.errors)
    assert df2.hash() == df3.hash()

def test_load_direct_recursion():

    df = DataFormat(prefix, 'user/direct_recursion/1')
    assert df.valid is False
    assert df.errors
    assert df.errors[0].find('recursion for') != -1
    assert df.errors[0].find('user/direct_recursion/1') != -1

def test_load_indirect_recursion():

    df = DataFormat(prefix, 'user/indirect_recursion_top/1')
    assert df.valid is False
    assert df.errors
    nose.tools.eq_(len(df.errors), 1)
    assert df.errors[0].find('is invalid') != -1
    assert df.errors[0].find('user/indirect_recursion_bottom/1') != -1

@nose.tools.with_setup(teardown=cleanup)
def test_export():

    name = 'user/composed/1'
    obj = DataFormat(prefix, name)
    assert obj.valid, '\n  * %s' % '\n  * '.join(obj.errors)

    obj.export(tmp_prefix)

    # load from tmp_prefix and validates
    exported = DataFormat(tmp_prefix, name)
    assert exported.valid, '\n  * %s' % '\n  * '.join(exported.errors)

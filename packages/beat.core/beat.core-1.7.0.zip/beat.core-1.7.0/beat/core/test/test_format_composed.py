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

import numpy
import nose.tools

from ..dataformat import DataFormat

from . import prefix

def test_valid():

    df = DataFormat(prefix, 'user/composed/1')
    assert df.valid

    ftype = df.type

    assert numpy.issubdtype(ftype.integers.value8, numpy.int8)
    assert numpy.issubdtype(ftype.integers.value16, numpy.int16)
    assert numpy.issubdtype(ftype.integers.value32, numpy.int32)
    assert numpy.issubdtype(ftype.integers.value64, numpy.int64)
    assert numpy.issubdtype(ftype.floats.value32, numpy.float32)
    assert numpy.issubdtype(ftype.floats.value64, numpy.float64)

    obj = ftype(
            integers=dict(
                value8=numpy.int8(2**6),
                value16=numpy.int16(2**14),
                value32=numpy.int32(2**30),
                value64=numpy.int64(2**62),
                ),
            floats=dict(
                value32=numpy.float32(3.14),
                value64=numpy.float64(2.78),
                ),
            )

    nose.tools.eq_(obj.integers.value8.dtype, numpy.int8)
    nose.tools.eq_(obj.integers.value8, 2**6)

    nose.tools.eq_(obj.integers.value16.dtype, numpy.int16)
    nose.tools.eq_(obj.integers.value16, 2**14)

    nose.tools.eq_(obj.integers.value32.dtype, numpy.int32)
    nose.tools.eq_(obj.integers.value32, 2**30)

    nose.tools.eq_(obj.integers.value64.dtype, numpy.int64)
    nose.tools.eq_(obj.integers.value64, 2**62)

    nose.tools.eq_(obj.floats.value32.dtype, numpy.float32)
    assert numpy.isclose(obj.floats.value32, 3.14)

    nose.tools.eq_(obj.floats.value64.dtype, numpy.float64)
    assert numpy.isclose(obj.floats.value64, 2.78)

    # checks JSON enconding
    copy = ftype()
    copy.from_dict(obj.as_dict())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

    # checks binary encoding
    copy = ftype()
    copy.unpack(obj.pack())
    assert copy.isclose(obj), "%r is not close enough to %r" % (copy.as_dict(), obj.as_dict())

def test_invalid():

    df = DataFormat(prefix, 'user/composed_unknown/1')
    assert df.valid is False
    assert df.errors[0].find('referred dataformat') != -1
    assert df.errors[0].find('invalid') != -1

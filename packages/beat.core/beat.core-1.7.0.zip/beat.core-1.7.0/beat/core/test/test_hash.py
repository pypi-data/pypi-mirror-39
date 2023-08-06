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
from .. import hash


#----------------------------------------------------------


def test_block_output_hash():

    h = hash.hashBlockOutput(
            'some_block',
            'some_algorithm',
            '12345',
            { "param1": 100 },
            { "name": "environment", "version": "1" },
            { "some_input": hash.hashDataset('some_database/1',
                'some_protocol',' some_set') },
            'some_output',
            )
    assert h is not None
    assert isinstance(h, str)
    assert len(h) > 0


#----------------------------------------------------------


def test_block_output_hash_repeatability():

    h1 = hash.hashBlockOutput(
            'some_block',
            'some_algorithm',
            '12345',
            { "param1": 100 },
            { "name": "environment", "version": "1" },
            { "some_input": hash.hashDataset('some_database/1',
                'some_protocol',' some_set') },
            'some_output',
            )

    h2 = hash.hashBlockOutput('some_block',
            'some_algorithm',
            '12345',
            { "param1": 100 },
            { "name": "environment", "version": "1" },
            { "some_input": hash.hashDataset('some_database/1',
                'some_protocol',' some_set') },
            'some_output',
            )

    nose.tools.eq_(h1, h2)


#----------------------------------------------------------


def test_different_block_output_hash():

    h1 = hash.hashBlockOutput(
            'some_block',
            'some_algorithm',
            '12345', { "param1": 100 },
            { "name": "environment", "version": "1" },
            { "some_input": hash.hashDataset('some_database/1',
                'some_protocol',' some_set') },
            'output1',
            )

    h2 = hash.hashBlockOutput(
            'some_block',
            'some_algorithm',
            '12345',
            { "param1": 100 },
            { "name": "environment", "version": "1" },
            { "some_input": hash.hashDataset('some_database/1',
                'some_protocol',' some_set') },
            'output2'
            )

    assert h1 != h2, "%r != %r" % (h1, h2)


#----------------------------------------------------------


def test_analyzer_hash():

    h = hash.hashAnalyzer(
            'some_block',
            'some_algorithm',
            '12345',
            { "param1": 100 },
            { "name": "environment", "version": "1" },
            { "some_input": hash.hashDataset('some_database/1',
                'some_protocol',' some_set') },
            )

    assert h is not None
    assert isinstance(h, str)
    assert len(h) > 0


#----------------------------------------------------------


def test_analyzer_hash_repeatability():

    h1 = hash.hashAnalyzer(
            'some_block',
            'some_algorithm',
            '12345',
            { "param1": 100 },
            { "name": "environment", "version": "1" },
            { "some_input": hash.hashDataset('some_database/1',
                'some_protocol',' some_set') },
            )

    h2 = hash.hashAnalyzer(
            'some_block',
            'some_algorithm',
            '12345',
            { "param1": 100 },
            { "name": "environment", "version": "1" },
            { "some_input": hash.hashDataset('some_database/1',
                'some_protocol',' some_set') },
            )

    nose.tools.eq_(h1, h2)


#----------------------------------------------------------


def test_different_analyzer_hash():

    h1 = hash.hashAnalyzer(
            'some_block',
            'some_algorithm',
            '12345',
            { "param1": 100 },
            { "name": "environment", "version": "1" },
            { "some_input": hash.hashDataset('some_database/1',
                'some_protocol',' some_set') },
            )

    h2 = hash.hashAnalyzer(
            'some_block',
            'some_algorithm',
            '67890',
            { "param1": 100 },
            { "name": "environment", "version": "1" },
            { "some_input": hash.hashDataset('some_database/1',
                'some_protocol',' some_set') },
            )

    assert h1 != h2, "%r != %r" % (h1, h2)


#----------------------------------------------------------


def test_path_from_hash():

    h = hash.hashDataset('some_database/1', 'some_protocol',' some_set')
    path = hash.toPath(h)

    assert path is not None
    assert isinstance(path, str)
    assert len(path) > 0

    parts = path.split('/')

    assert len(parts) > 1

    for folder in parts[:-1]:
        nose.tools.eq_(len(folder), 2)

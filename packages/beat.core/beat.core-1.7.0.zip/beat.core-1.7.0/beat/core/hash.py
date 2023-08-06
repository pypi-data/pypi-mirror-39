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


"""
====
hash
====

Various functions for hashing platform contributions and others

Also forward importing from :py:mod:`beat.backend.python.hash`
"""

import collections

import simplejson

from beat.backend.python.hash import *
from beat.backend.python.hash import _sha256
from beat.backend.python.hash import _stringify
from beat.backend.python.hash import _compact


# ----------------------------------------------------------


def hashBlockOutput(block_name, algorithm_name, algorithm_hash,
                    parameters, environment, input_hashes, output_name):
    """Generate a hash for a given block output

    Parameters:
        :param str block_name: Name of the block (unused)

        :param str algorithm_name: Name of the algorithm used by the block
        (parameter unused)

        :param str algorithm_hash: Hash of the algorithm used by the block

        :param dict parameters: Configured parameters

        :param dict environment: Environment parameters

        :param dict input_hashes: Dictionary containing the input's hashes

        :param str output_name: Name of the output
    """

    # Note: 'block_name' and 'algorithm_name' aren't used to compute the hash,
    # but are useful when an application wants to implement its own hash
    # function
    s = _compact("""{
        "algorithm": "%s",
        "parameters": %s,
        "environment": %s,
        "inputs": %s,
        "output": "%s"
}""") % (algorithm_hash, _stringify(parameters), _stringify(environment),
           _stringify(input_hashes), output_name)
    return hash(s)


# ----------------------------------------------------------


def hashAnalyzer(analyzer_name, algorithm_name, algorithm_hash,
                 parameters, environment, input_hashes):
    """Generate a hash for a given analyzer

    Parameters:
        :param str analyzer_name: Name of the analyzer (unused)

        :param str algorithm_name: Name of the algorithm used by the analyzer

        :param str algorithm_hash: Hash of the algorithm used by the analyzer

        :param dict parameters: Configured parameters

        :param dict environment: Environment parameters

        :param dict input_hashes: Dictionary containing the inputs's hashes
    """

    # Note: 'analyzer_name' isn't used to compute the hash, but is useful when
    # an applications want to implement its own hash function
    s = _compact("""{
        "algorithm_name": "%s",
        "algorithm": "%s",
        "parameters": %s,
        "environment": %s,
        "inputs": %s
}""") % (algorithm_name, algorithm_hash, _stringify(parameters),
          _stringify(environment), _stringify(input_hashes))
    return hash(s)


# ----------------------------------------------------------


def hashJSONStr(contents, description):
    """Hashes the JSON string contents using ``hashlib.sha256``

    Excludes description changes
    """

    try:
        return hashJSON(simplejson.loads(contents,
          object_pairs_hook=collections.OrderedDict), description)  # preserve order
    except simplejson.JSONDecodeError:
        # falls back to normal file content hashing
        return hash(contents)

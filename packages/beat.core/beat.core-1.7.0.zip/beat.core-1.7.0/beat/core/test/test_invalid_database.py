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
from ..database import Database

from . import prefix

import logging
logger = logging.getLogger(__name__)


def doit(filename, error_msg):
    database = Database(prefix, filename)
    assert database.errors
    logger.error(error_msg)
    found = False

    for msg in database.errors:
        logger.error('%s %s', msg, error_msg)
        if msg.find(error_msg) != -1:
            found = True
            break

    assert found, "cannot find message `%s' on error list (%s) from loading database file `%s'" % (error_msg, database.errors, filename)

def test_load_unknown_database():
    doit('unknown/1', 'file not found')

def test_load_invalid_database():
    doit('invalid/1', 'invalid JSON code')

def test_load_database_without_protocols_list():
    doit('missing_protocols/1', "%r is a required property" % u'protocols')

def test_load_database_with_empty_protocols_list():
    doit('empty_protocols/1', "/protocols: [] is too short")

def test_load_database_with_missing_protocol_name():
    doit('missing_protocol_name/1', "/protocols/0: %r is a required property" % u'name')

def test_load_database_with_mixed_protocol_names():
    doit('mixed_protocol_names/1', "None is not of type %r" % u'string')

def test_load_database_with_same_protocol_names():
    doit('same_protocol_names/1', "found different protocols with the same name:")

def test_load_database_with_missing_protocol_sets():
    doit('missing_protocol_sets/1', "%r is a required property" % u'sets')

def test_load_database_with_empty_protocol_sets():
    doit('empty_protocol_sets/1', 'rule: /properties/protocols/items/properties/sets/minItems')

def test_load_database_with_missing_set_name():
    doit('missing_set_name/1', "%r is a required property" % u'name')

def test_load_database_with_mixed_set_names():
    doit('mixed_set_names/1', "name: None is not of type %r" % u'string')

def test_load_database_with_same_set_names():
    doit('same_set_names/1', "found different sets with the same name")

def test_load_database_with_missing_set_view():
    doit('missing_set_view/1', "%r is a required property" % u'view')

def test_load_database_with_missing_set_outputs_list():
    doit('missing_set_outputs/1', "%r is a required property" % u'outputs')

def test_load_database_with_empty_set_outputs_list():
    doit('empty_set_outputs/1', 'outputs: OrderedDict() does not have enough properties')

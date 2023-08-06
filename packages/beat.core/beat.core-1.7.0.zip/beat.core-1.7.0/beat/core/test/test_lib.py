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


import sys
import types

import nose.tools

from . import prefix, tmp_prefix
from .utils import cleanup
from ..library import Library, Storage


def test_valid():

    l = Library(prefix, 'user/valid/1')
    assert l.valid, '\n  * %s' % '\n  * '.join(l.errors)
    nose.tools.eq_(len(l.uses), 0)
    nose.tools.eq_(len(l.libraries), 0)

    # tries to call the function `f()' on that library
    module = l.load()
    assert isinstance(module, types.ModuleType)
    nose.tools.eq_(module.f(), 'OK')
    nose.tools.eq_(module.pyver(), '%d.%d' % sys.version_info[:2])


def test_nested_1():

    l = Library(prefix, 'user/nest1/1')
    assert l.valid, '\n  * %s' % '\n  * '.join(l.errors)
    nose.tools.eq_(len(l.uses), 1)
    nose.tools.eq_(len(l.libraries), 1)

    # tries to call the function `f()' on that library
    module = l.load()
    assert isinstance(module, types.ModuleType)
    nose.tools.eq_(module.f('-extra'), 'OK-extra')
    nose.tools.eq_(module.pyver('-extra'), '%d.%d-extra' % sys.version_info[:2])


def test_nested_2():

    l = Library(prefix, 'user/nest2/1')
    assert l.valid, '\n  * %s' % '\n  * '.join(l.errors)
    nose.tools.eq_(len(l.uses), 1)
    nose.tools.eq_(len(l.libraries), 1)

    # tries to call the function `f()' on that library
    module = l.load()
    assert isinstance(module, types.ModuleType)
    nose.tools.eq_(module.f('-x'), 'OK-x-x')
    nose.tools.eq_(module.pyver('-x'), '%d.%d-x-x' % sys.version_info[:2])


def test_direct_recursion():

    l = Library(prefix, 'user/direct_recursion/1')
    assert not l.valid
    nose.tools.eq_(len(l.errors), 1)
    assert l.errors[0].find('recursion for library') != -1
    assert l.errors[0].find(l.name) != -1


def test_indirect_recursion():

    l = Library(prefix, 'user/indirect_recursion/1')
    assert not l.valid
    nose.tools.eq_(len(l.errors), 1)
    assert l.errors[0].find('referred library') != -1
    assert l.errors[0].find('user/indirect_recursion_next/1') != -1


def test_invalid_mix():

    l = Library(prefix, 'user/invalid_mix/1')
    assert not l.valid
    nose.tools.eq_(len(l.errors), 1)
    assert l.errors[0].find('differs from current language') != -1


@nose.tools.with_setup(teardown=cleanup)
def test_dependencies():

    name = 'user/for_dep/1'
    dep_name = 'user/dep/1'

    l = Library(prefix, name)
    assert l.valid, '\n  * %s' % '\n  * '.join(l.errors)
    nose.tools.eq_(len(l.uses), 0)
    nose.tools.eq_(len(l.libraries), 0)

    # Save to temporary storage, so we can test modifications on it
    new_storage = Storage(tmp_prefix, name)
    l.write(new_storage)

    l_dep = Library(prefix, dep_name)
    assert l_dep.valid
    new_dep_storage = Storage(tmp_prefix, dep_name)
    l_dep.write(new_dep_storage)

    # Reload
    l = Library(tmp_prefix, name)
    assert l.valid, '\n  * %s' % '\n  * '.join(l.errors)
    l_dep = Library(tmp_prefix, dep_name)
    assert l_dep.valid

    l.uses['dep1'] = l_dep.name
    l.write() #rewrite

    # Re-validate
    l = Library(tmp_prefix, name)
    assert l.valid, '\n  * %s' % '\n  * '.join(l.errors)

    nose.tools.eq_(len(l.uses), 1)
    nose.tools.eq_(len(l.libraries), 1)
    nose.tools.eq_(list(l.uses.keys())[0], 'dep1')
    nose.tools.eq_(list(l.uses.values())[0], 'user/dep/1')

    l.uses = {} #reset
    l.uses['mod1'] = l_dep.name
    l.write() #rewrite

    # Re-validate
    l = Library(tmp_prefix, name)
    assert l.valid, '\n  * %s' % '\n  * '.join(l.errors)

    nose.tools.eq_(len(l.uses), 1)
    nose.tools.eq_(len(l.libraries), 1)
    nose.tools.eq_(list(l.uses.keys())[0], 'mod1')
    nose.tools.eq_(list(l.uses.values())[0], 'user/dep/1')

    l.uses = {} #reset
    l.write() #rewrite

    # Re-validate
    l = Library(tmp_prefix, name)
    assert l.valid, '\n  * %s' % '\n  * '.join(l.errors)

    nose.tools.eq_(len(l.uses), 0)
    nose.tools.eq_(len(l.libraries), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_adding_self():
    name = 'user/for_dep/1'

    l = Library(prefix, name)
    assert l.valid, '\n  * %s' % '\n  * '.join(l.errors)
    nose.tools.eq_(len(l.uses), 0)
    nose.tools.eq_(len(l.libraries), 0)

    l.uses['dep'] = l.name
    new_storage = Storage(tmp_prefix, name)
    l.write(new_storage) #rewrite

    # Re-validate
    l = Library(tmp_prefix, name)
    assert not l.valid
    assert l.errors[0].find('recursion') != -1


@nose.tools.with_setup(teardown=cleanup)
def test_invalid_dependencies():

    name = 'user/for_dep/1'
    dep_name = 'user/invalid_dep/1'

    l = Library(prefix, name)
    assert l.valid, '\n  * %s' % '\n  * '.join(l.errors)
    nose.tools.eq_(len(l.uses), 0)
    nose.tools.eq_(len(l.libraries), 0)

    # Save to temporary storage, so we can test modifications on it
    new_storage = Storage(tmp_prefix, name)
    l.write(new_storage)

    l_dep = Library(prefix, dep_name)
    assert l_dep.valid
    new_dep_storage = Storage(tmp_prefix, dep_name)
    l_dep.write(new_dep_storage)

    # Reload
    l = Library(tmp_prefix, name)
    assert l.valid, '\n  * %s' % '\n  * '.join(l.errors)
    l_dep = Library(tmp_prefix, dep_name)
    assert l_dep.valid

    l.uses['dep1'] = l_dep.name
    l.write() #rewrite

    # Re-validate
    l = Library(tmp_prefix, name)
    assert not l.valid
    assert l.errors[0].find('differs from current language') != -1

@nose.tools.with_setup(teardown=cleanup)
def test_export():

    name = 'user/nest2/1'
    obj = Library(prefix, name)
    assert obj.valid, '\n  * %s' % '\n  * '.join(obj.errors)

    obj.export(tmp_prefix)

    # load from tmp_prefix and validates
    exported = Library(tmp_prefix, name)
    assert exported.valid, '\n  * %s' % '\n  * '.join(exported.errors)

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

from ..algorithm import Algorithm, Storage
from ..library import Library, Storage as LibraryStorage
from ..dataformat import DataFormat, Storage as DataFormatStorage

from . import prefix, tmp_prefix
from .utils import cleanup

def copy_objects(algo, lib):

    a = Algorithm(prefix, algo)
    storage = Storage(tmp_prefix, a.name)
    a.write(storage)

    for d in a.dataformats:
        storage = DataFormatStorage(tmp_prefix, d)
        a.dataformats[d].write(storage)

    l = Library(prefix, lib)
    storage = LibraryStorage(tmp_prefix, l.name)
    l.write(storage)


@nose.tools.with_setup(teardown=cleanup)
def test_dependencies():
    name = 'user/for_dep/1'
    dep_name = 'user/dep/1'

    copy_objects(name, dep_name)

    a = Algorithm(tmp_prefix, name)
    assert a.valid, '\n  * %s' % '\n  * '.join(a.errors)
    nose.tools.eq_(len(a.uses), 0)
    nose.tools.eq_(len(a.libraries), 0)

    l_dep = Library(tmp_prefix, dep_name)
    assert l_dep.valid, '\n  * %s' % '\n  * '.join(l_dep.errors)

    # check modification
    a.uses['dep1'] = dep_name
    a.write()
    a = Algorithm(tmp_prefix, name)
    assert a.valid, '\n  * %s' % '\n  * '.join(a.errors)

    nose.tools.eq_(len(a.uses), 1)
    nose.tools.eq_(len(a.libraries), 1)
    nose.tools.eq_(list(a.uses.keys())[0], 'dep1')
    nose.tools.eq_(list(a.uses.values())[0], 'user/dep/1')

    a.uses = {}
    a.uses['mod1'] = dep_name
    a.write()
    a = Algorithm(tmp_prefix, name)
    assert a.valid, '\n  * %s' % '\n  * '.join(a.errors)

    nose.tools.eq_(len(a.uses), 1)
    nose.tools.eq_(len(a.libraries), 1)
    nose.tools.eq_(list(a.uses.keys())[0], 'mod1')
    nose.tools.eq_(list(a.uses.values())[0], 'user/dep/1')

    a.uses = {}
    a.write()
    a = Algorithm(tmp_prefix, name)
    assert a.valid, '\n  * %s' % '\n  * '.join(a.errors)

    nose.tools.eq_(len(a.uses), 0)
    nose.tools.eq_(len(a.libraries), 0)


@nose.tools.with_setup(teardown=cleanup)
def test_invalid_dependencies():

    name = 'user/for_dep/1'
    dep_name = 'user/invalid_dep/1'

    copy_objects(name, dep_name)

    a = Algorithm(tmp_prefix, name)
    assert a.valid, '\n  * %s' % '\n  * '.join(a.errors)
    nose.tools.eq_(len(a.uses), 0)
    nose.tools.eq_(len(a.libraries), 0)

    l_dep = Library(tmp_prefix, 'user/invalid_dep/1')
    assert l_dep.valid, '\n  * %s' % '\n  * '.join(l_dep.errors)

    a.uses['dep'] = dep_name
    a.write()
    a = Algorithm(tmp_prefix, name)
    assert not a.valid
    assert a.errors[0].find('differs from current language') != -1

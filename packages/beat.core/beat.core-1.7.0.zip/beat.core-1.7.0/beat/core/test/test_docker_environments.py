#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2018 Idiap Research Institute, http://www.idiap.ch/           #
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

import unittest

from ..dock import Host

from .. import environments

from .utils import slow


class EnvironmentTest(unittest.TestCase):

    def setUp(self):
        self.host = Host(raise_on_errors=False)
        self.test_environment = \
            self.host.full_environment_name('Cxx development environment')

    def tearDown(self):
        self.host.teardown()
        assert not self.host.containers  # All containers are gone

    @slow
    def test_package_enumeration(self):
        package_list = environments.enumerate_packages(self.host,
                                                       self.test_environment)

        self.assertTrue(len(package_list) > 0)

        for package in package_list:
            self.assertListEqual(sorted(list(package.keys())),
                                 sorted(['version', 'name']))

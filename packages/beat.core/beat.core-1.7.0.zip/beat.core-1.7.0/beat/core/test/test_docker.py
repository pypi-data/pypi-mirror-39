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


"""Asynchronous process I/O with the Subprocess module
"""

import os
import sys
import time
import unittest
import pkg_resources
import time

import requests
import nose

from tempfile import TemporaryDirectory

from ..dock import Host

from . import tmp_prefix
from .utils import slow
from .utils import skipif

from . import network_name
from . import DOCKER_NETWORK_TEST_ENABLED

class NoDiscoveryTests(unittest.TestCase):
    """Test cases that don't require the discovery of database and runtime
    environments.
    """

    @classmethod
    def setUpClass(cls):
        cls.host = Host(raise_on_errors=False, discover=False)


    @classmethod
    def tearDownClass(cls):
        cls.host.teardown()


    def tearDown(self):
        self.host.teardown()
        assert not self.host.containers # All containers are gone


class NetworkTest(NoDiscoveryTests):

    @slow
    @skipif(not DOCKER_NETWORK_TEST_ENABLED, "Network test disabled")
    def test_network(self):
        string = "hello world"
        container = self.host.create_container('debian:8.4', ["echo", string])
        container.network_name = network_name

        try:
            self.host.start(container)
            status = self.host.wait(container)
        except Exception as e:
            network.remove()
            raise

        self.assertEqual(status, 0)
        self.assertEqual(self.host.logs(container), string + '\n')


    @slow
    @skipif(not DOCKER_NETWORK_TEST_ENABLED, "Network test disabled")
    def test_non_existing_network(self):

        string = "hello world"
        network_name = 'beat.core.fake'
        container = self.host.create_container('debian:8.4', ["echo", string])
        container.network_name = network_name

        try:
            self.host.start(container)
        except RuntimeError as e:
            self.assertTrue(str(e).find('network %s not found' % network_name) >= 0)


class UserTest(NoDiscoveryTests):

    @slow
    def test_user(self):
        """Test that the uid property is correctly used.
        """

        container = self.host.create_container('debian:8.4', ["id"])
        container.uid = 10000

        self.host.start(container)
        status = self.host.wait(container)

        self.assertEqual(status, 0)
        self.assertTrue(self.host.logs(container).startswith('uid={0} gid={0}'.format(container.uid)))


class EnvironmentVariableTest(NoDiscoveryTests):

    @slow
    def test_environment_variable(self):
        """Test that the uid property is correctly used.
        """

        container = self.host.create_container('debian:8.4', ["env"])
        container.add_environment_variable('DOCKER_TEST', 'good')

        self.host.start(container)
        status = self.host.wait(container)

        self.assertEqual(status, 0)
        self.assertTrue('DOCKER_TEST=good' in self.host.logs(container))


class WorkdirTest(NoDiscoveryTests):

    @slow
    def test_workdir(self):
        """Test that the workdir property is correctly used.
        """

        with TemporaryDirectory() as tmp_folder:
            test_file = "test.txt"
            container = self.host.create_container('debian:8.4', ["cp", "/etc/debian_version", test_file])
            container.add_volume(tmp_folder, '/test_workdir', read_only=False)
            container.set_workdir('/test_workdir')

            self.host.start(container)
            status = self.host.wait(container)
            if status != 0:
                print(self.host.logs(container))

            self.assertEqual(status, 0)

            with open(os.path.join(tmp_folder, test_file), "rt") as file:
                content = file.read()
                self.assertEqual(content, "8.4\n")


class EntrypointTest(NoDiscoveryTests):

    @slow
    def test_entrypoint(self):
        """Test that the entrypoint property is correctly used.
        """

        container = self.host.create_container('debian:8.4', ["42"])
        container.set_entrypoint('echo')

        self.host.start(container)
        status = self.host.wait(container)
        logs = self.host.logs(container)
        if status != 0:
            print(logs)

        self.assertEqual(status, 0)
        self.assertEqual(logs, "42\n")


class AsyncTest(NoDiscoveryTests):

    @slow
    def test_echo(self):

        string = "hello, world"

        container = self.host.create_container('debian:8.4', ["echo", string])
        self.host.start(container)
        status = self.host.wait(container)

        self.assertEqual(status, 0)
        self.assertEqual(self.host.logs(container), string + '\n')

    @slow
    def test_non_existing(self):

        container = self.host.create_container('debian:8.4', ["sdfsdfdsf329909092"])

        try:
            self.host.start(container)
        except Exception as e:
            self.assertTrue(str(e).find('Failed to create the container') >= 0)

        self.assertFalse(self.host.containers) # All containers are gone


    @slow
    def test_timeout(self):

        sleep_for = 100 # seconds

        container = self.host.create_container('debian:8.4', ["sleep", str(sleep_for)])
        self.host.start(container)

        retval = self.host.wait(container, timeout=0.5)
        self.assertTrue(retval is None)

        self.host.kill(container)

        retval = self.host.wait(container)

        self.assertEqual(self.host.status(container), 'exited')
        self.assertEqual(retval, 137)
        self.assertEqual(self.host.logs(container), '')


    @slow
    def test_does_not_timeout(self):

        sleep_for = 0.5 # seconds

        container = self.host.create_container('debian:8.4', ["sleep", str(sleep_for)])
        self.host.start(container)

        status = self.host.wait(container, timeout=5) # Should not timeout

        self.assertEqual(self.host.status(container), 'exited')
        self.assertEqual(status, 0)
        self.assertEqual(self.host.logs(container), '')



class AsyncWithEnvironmentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = Host(raise_on_errors=False)
        cls.test_environment = cls.host.full_environment_name('Python 2.7')


    @classmethod
    def tearDownClass(cls):
        cls.host.teardown()


    def tearDown(self):
        self.host.teardown()
        assert not self.host.containers # All containers are gone

    @slow
    def test_memory_limit(self):

        cmd = ['python', '-c', '; '.join([
            "print('Before')",
            "import sys; sys.stdout.flush()",
            "d = '0' * (10 * 1024 * 1024)",
            "import time; time.sleep(5)",
            "print('After')",
          ])
        ]

        container = self.host.create_container(self.test_environment, cmd)
        self.host.start(container, virtual_memory_in_megabytes=4)

        time.sleep(2)

        stats = self.host.statistics(container)

        status = self.host.wait(container)

        self.assertEqual(self.host.status(container), 'exited')
        self.assertEqual(status, 137)
        self.assertEqual(self.host.logs(container).strip(), 'Before')


    @slow
    def test_memory_limit2(self):

        cmd = ['python', '-c', '; '.join([
            "print('Before')",
            "import sys; sys.stdout.flush()",
            "d = '0' * (10 * 1024 * 1024)",
            "import time; time.sleep(5)",
            "print('After')",
          ])
        ]

        container = self.host.create_container(self.test_environment, cmd)
        self.host.start(container, virtual_memory_in_megabytes=100)

        time.sleep(2)

        stats = self.host.statistics(container)

        status = self.host.wait(container)

        assert stats['memory']['percent'] > 10, 'Memory check failed, ' \
            '%d%% <= 10%%' % stats['memory']['percent']

        assert stats['memory']['percent'] < 15, 'Memory check failed, ' \
            '%d%% >= 15%%' % stats['memory']['percent']

        self.assertEqual(self.host.status(container), 'exited')
        self.assertEqual(status, 0)
        self.assertEqual(self.host.logs(container).strip(), 'Before\nAfter')


    def _run_cpulimit(self, processes, max_cpu_percent, sleep_time):

        program = pkg_resources.resource_filename(__name__, 'cpu_stress.py')
        dst_name = os.path.join('/tmp', os.path.basename(program))

        container = self.host.create_container(self.test_environment,
                                               ['python', dst_name, str(processes)])

        container.add_volume(program, os.path.join('/tmp', 'cpu_stress.py'))

        self.host.start(container, max_cpu_percent=max_cpu_percent)

        time.sleep(sleep_time)

        stats = self.host.statistics(container)

        self.assertEqual(self.host.status(container), 'running')

        percent = stats['cpu']['percent']
        assert percent < (1.1 * max_cpu_percent), \
               "%.2f%% is more than 20%% off the expected ceiling at %d%%!" % (percent, max_cpu_percent)

        # make sure nothing is there anymore
        self.host.kill(container)
        self.assertEqual(self.host.wait(container), 137)


    @slow
    def test_cpulimit_at_20percent(self):
        # runs 1 process that should consume at most 20% of the host CPU
        self._run_cpulimit(1, 20, 3)


    @slow
    def test_cpulimit_at_100percent(self):
        # runs 4 processes that should consume 50% of the host CPU
        self._run_cpulimit(4, 100, 3)



class HostTest(unittest.TestCase):

    def setUp(self):
        Host.images_cache = {}


    @slow
    def test_images_cache(self):
        self.assertEqual(len(Host.images_cache), 0)

        # Might take some time
        start = time.time()

        host = Host(raise_on_errors=False)
        host.teardown()

        stop = time.time()

        nb_images = len(Host.images_cache)
        self.assertTrue(nb_images > 0)

        self.assertTrue(stop - start > 2.0)

        # Should be instantaneous
        start = time.time()

        host = Host(raise_on_errors=False)
        host.teardown()

        stop = time.time()

        self.assertEqual(len(Host.images_cache), nb_images)

        self.assertTrue(stop - start < 1.0)


    @slow
    def test_images_cache_file(self):
        self.assertEqual(len(Host.images_cache), 0)

        # Might take some time
        start = time.time()

        host = Host(images_cache=os.path.join(tmp_prefix, 'images_cache.json'),
                    raise_on_errors=False)
        host.teardown()

        stop = time.time()

        nb_images = len(Host.images_cache)
        self.assertTrue(nb_images > 0)

        self.assertTrue(stop - start > 2.0)

        Host.images_cache = {}

        # Should be instantaneous
        start = time.time()

        host = Host(images_cache=os.path.join(tmp_prefix, 'images_cache.json'),
                    raise_on_errors=False)
        host.teardown()

        stop = time.time()

        self.assertEqual(len(Host.images_cache), nb_images)

        self.assertTrue(stop - start < 1.0)

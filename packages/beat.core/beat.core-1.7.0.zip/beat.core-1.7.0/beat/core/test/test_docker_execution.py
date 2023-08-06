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


# Tests for experiment execution within Docker containers

import os
import subprocess

from ..dock import Host
from ..execution import DockerExecutor

from .utils import cleanup
from .utils import slow
from .utils import skipif

from .test_execution import BaseExecutionMixIn

from . import network_name
from . import prefix_folder
from . import DOCKER_NETWORK_TEST_ENABLED

BUILDER_IMAGE = "docker.idiap.ch/beat/beat.env.client:2.0.0r0"

#----------------------------------------------------------


class TestDockerExecution(BaseExecutionMixIn):

    @classmethod
    def setup_class(cls):
        cls.host = Host(raise_on_errors=False)


    @classmethod
    def teardown_class(cls):
        cls.host.teardown()
        cleanup()


    def teardown(self):
        self.host.teardown()


    def create_executor(self, prefix, configuration, tmp_prefix, dataformat_cache,
                        database_cache, algorithm_cache):
        executor = DockerExecutor(self.host, prefix, configuration, tmp_prefix,
                                  dataformat_cache, database_cache, algorithm_cache)

        executor.debug = os.environ.get("DOCKER_TEST_DEBUG", False) == "True"
        return executor


    def build_algorithm(self, algorithm):
        test_folder = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        scripts_folder = os.path.abspath(os.path.join(test_folder, 'scripts'))
        sources_folder = os.path.abspath(os.path.join(test_folder, algorithm))
        cmd = ['/build.sh']
        builder_container = self.host.create_container(BUILDER_IMAGE, cmd)
        builder_container.add_volume("%s/build.sh" % scripts_folder, "/build.sh")
        builder_container.add_volume(sources_folder, "/sources", read_only=False)
        builder_container.uid = os.getuid()
        builder_container.set_workdir("/sources")
        builder_container.set_entrypoint("bash")

        self.host.start(builder_container)
        status = self.host.wait(builder_container)
        if status != 0:
            print(self.host.logs(builder_container))

        self.host.rm(builder_container)
        assert status == 0

        # Update the tmp prefix with the latest content
        subprocess.check_call(['rsync',
                               '-arz',
                               '--exclude="*"',
                               '--include="*.so"',
                               os.path.join(test_folder, 'prefix'),
                               prefix_folder])


    @slow
    @skipif(not DOCKER_NETWORK_TEST_ENABLED, "Network test disabled")
    def test_custom_network(self):
        result = self.execute('user/user/integers_addition/1/integers_addition',
                [{'sum': 495, 'nb': 9}], network_name=network_name)

        assert result is None

    @slow
    def test_custom_port_range(self):
        result = self.execute('user/user/integers_addition/1/integers_addition',
                [{'sum': 495, 'nb': 9}], port_range="50000:50100")

        assert result is None

    @slow
    def test_single_1_prepare_error(self):
        result = self.execute('user/user/single/1/prepare_error', [None])

        assert result['status'] == 1
        assert result['user_error'] == "'Could not prepare algorithm (returned False)'"

    @slow
    def test_single_1_setup_error(self):
        result = self.execute('user/user/single/1/setup_error', [None])

        assert result['status'] == 1
        assert result['user_error'] == "'Could not setup algorithm (returned False)'"

    # NOT COMPATIBLE YET WITH THE NEW API
    # @slow
    # def test_cxx_double_1(self):
    #     assert self.execute('user/user/double/1/cxx_double', [{'out_data': 42}]) is None

    @slow
    def test_cxx_double_legacy(self):
        datasets_uid = os.getuid()
        self.build_algorithm("prefix/algorithms/user/cxx_integers_echo_legacy")

        result = self.execute('user/user/double/1/cxx_double_legacy', [{'out_data': 42}], datasets_uid=datasets_uid)
        assert result is None

    @slow
    def test_cxx_double_sequential(self):
        datasets_uid = os.getuid()
        self.build_algorithm("prefix/algorithms/user/cxx_integers_echo_sequential")

        assert self.execute('user/user/double/1/cxx_double_sequential', [{'out_data': 42}], datasets_uid=datasets_uid) is None

    @slow
    def test_cxx_double_autonomous(self):
        datasets_uid = os.getuid()
        self.build_algorithm("prefix/algorithms/user/cxx_integers_echo_autonomous")

        assert self.execute('user/user/double/1/cxx_double_autonomous', [{'out_data': 42}], datasets_uid=datasets_uid) is None

    @slow
    def test_cxx_analyzer_error(self):
        datasets_uid = os.getuid()
        needed_alorithms = [
            "cxx_integers_echo_sequential",
            "cxx_integers_echo_analyzer"
        ]

        for algorithm in needed_alorithms:
            self.build_algorithm("prefix/algorithms/user/%s" % algorithm)


        result = self.execute('user/user/double/1/cxx_analyzer_error', [{'out_data': 42}], datasets_uid=datasets_uid)

        assert result['status'] == 255
        assert "[sys] C++ algorithm can't be analyzers" in result['stderr']

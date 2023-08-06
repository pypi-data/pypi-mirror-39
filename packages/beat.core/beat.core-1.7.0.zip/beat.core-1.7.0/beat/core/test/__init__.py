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


# Basic setup for slow tests

import os
import sys
import subprocess
import shutil
import tempfile
import pkg_resources
import logging

if sys.platform == 'darwin':
    tmp_prefix = tempfile.mkdtemp(prefix=__name__,
                                  suffix='.tmpdir',
                                  dir='/tmp')
    prefix_folder = tempfile.mkdtemp(prefix=__name__,
                                     suffix='.prefix',
                                     dir='/tmp')
else:
    tmp_prefix = tempfile.mkdtemp(prefix=__name__,
                                  suffix='.tmpdir')
    prefix_folder = tempfile.mkdtemp(prefix=__name__,
                                     suffix='.prefix')


prefix = os.path.join(prefix_folder, 'prefix')

DOCKER_NETWORK_TEST_ENABLED = os.environ.get('DOCKER_NETWORK_TEST_ENABLED', False) == 'True'
network_name = os.environ.get('DOCKER_TEST_NETWORK', 'beat_core_test_network')
network = None

# Setup the logging system
VERBOSE_TEST_LOGGING = os.environ.get('VERBOSE_TEST_LOGGING', False) == 'True'

if VERBOSE_TEST_LOGGING:
    formatter = logging.Formatter(fmt="[%(asctime)s - TESTS - "
                                      "%(name)s] %(levelname)s: %(message)s",
                                  datefmt="%d/%b/%Y %H:%M:%S")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    for logger_name in ['beat.core', 'beat.backend.python']:
      logger = logging.getLogger(logger_name)
      logger.setLevel(logging.DEBUG)
      logger.addHandler(handler)


def setup_package():
    prefixes = [
        pkg_resources.resource_filename('beat.backend.python.test', 'prefix'),
        pkg_resources.resource_filename('beat.core.test', 'prefix')
    ]

    for path in prefixes:
        subprocess.check_call(['rsync', '-arz', path, prefix_folder])

    if DOCKER_NETWORK_TEST_ENABLED:
        import docker
        client = docker.from_env()
        try:
            network = client.networks.get(network_name)
        except docker.errors.NotFound:
            subnet = os.environ.get('DOCKER_TEST_SUBNET', '193.169.0.0/24')
            gateway = os.environ.get('DOCKER_TEST_GATEWAY', '193.169.0.254')
            ipam_pool = docker.types.IPAMPool(subnet=subnet,
                                          gateway=gateway)

            ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])

            network = client.networks.create(network_name,
                                             driver="bridge",
                                             ipam=ipam_config)

def teardown_package():
    if os.path.exists(tmp_prefix):
        shutil.rmtree(tmp_prefix)

    shutil.rmtree(prefix_folder)

    if DOCKER_NETWORK_TEST_ENABLED:
        if network:
            network.remove()

#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2017 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.backend.python module of the BEAT platform.   #
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


# Tests for experiment execution

import os
import sys

import logging
logger = logging.getLogger(__name__)

import unittest
import simplejson
import multiprocessing
import tempfile
import shutil
import zmq
from time import time
from time import sleep

from beat.backend.python.scripts import databases_provider
from beat.backend.python.database import Database
from beat.backend.python.data import RemoteDataSource
from beat.backend.python.data import RemoteException

from ..dock import Host
from ..utils import find_free_port

from . import prefix
from . import tmp_prefix


#----------------------------------------------------------


CONFIGURATION = {
    'queue': 'queue',
    'inputs': {
        'in_data': {
            'set': 'double',
            'protocol': 'double',
            'database': 'integers_db/1',
            'output': 'a',
            'path': 'ec/89/e5/6e161d2cb012ef6ac8acf59bf453a6328766f90dc9baba9eb14ea23c55',
            'endpoint': 'a',
            'hash': 'ec89e56e161d2cb012ef6ac8acf59bf453a6328766f90dc9baba9eb14ea23c55',
            'channel': 'integers'
        }
    },
    'algorithm': 'user/integers_echo/1',
    'parameters': {},
    'environment': {
        'name': 'Python 2.7',
        'version': '1.2.0'
    },
    'outputs': {
        'out_data': {
            'path': '20/61/b6/2df3c3bedd5366f4a625c5d87ffbf5a26007c46c456e9abf21b46c6681',
            'endpoint': 'out_data',
            'hash': '2061b62df3c3bedd5366f4a625c5d87ffbf5a26007c46c456e9abf21b46c6681',
            'channel': 'integers'
        }
    },
    'nb_slots': 1,
    'channel': 'integers'
}


#----------------------------------------------------------


class TestDatabasesProvider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.host = Host(raise_on_errors=False)


    def setUp(self):
        if sys.platform == 'darwin':
            self.working_dir = tempfile.mkdtemp(prefix=__name__, dir='/tmp')
            self.cache_root = tempfile.mkdtemp(prefix=__name__, dir='/tmp')
        else:
            self.working_dir = tempfile.mkdtemp(prefix=__name__)
            self.cache_root = tempfile.mkdtemp(prefix=__name__)

        self.data_source = None
        self.client_context = None
        self.client_socket = None
        self.databases_container = None


    def tearDown(self):
        self.stop_databases_provider()

        shutil.rmtree(self.working_dir)
        shutil.rmtree(self.cache_root)

        self.working_dir = None
        self.cache_root = None
        self.data_source = None

        if self.client_socket is not None:
            self.client_socket.setsockopt(zmq.LINGER, 0)
            self.client_socket.close()
            self.client_context.destroy()

        self.host.teardown()


    def start_databases_provider(self, configuration):
        with open(os.path.join(self.working_dir, 'configuration.json'), 'wb') as f:
            data = simplejson.dumps(configuration, indent=4)
            f.write(data.encode('utf-8'))

        working_prefix = os.path.join(self.working_dir, 'prefix')
        if not os.path.exists(working_prefix):
            os.makedirs(working_prefix)

        input_name, input_cfg = list(configuration['inputs'].items())[0]

        database = Database(prefix, input_cfg['database'])
        database.export(working_prefix)

        view = database.view(input_cfg['protocol'], input_cfg['set'])
        view.index(os.path.join(self.cache_root, input_cfg['path']))

        port = find_free_port()
        cmd = [
            'databases_provider',
            '--debug',
            '0.0.0.0:%i' % port,
            '/beat/prefix',
            '/beat/cache',
        ]

        databases_environment = self.host.db2docker([ input_cfg['database'] ])

        self.databases_container = self.host.create_container(databases_environment, cmd)

        self.databases_container.add_volume(self.working_dir, '/beat/prefix')
        self.databases_container.add_volume('/tmp', os.path.join('/beat/datasets', input_cfg['database']))
        self.databases_container.add_volume(self.cache_root, '/beat/cache')

        self.databases_container.add_port(port, port, host_address=self.host.ip)

        self.host.start(self.databases_container)

        self.client_context = zmq.Context()
        self.client_socket = self.client_context.socket(zmq.PAIR)
        self.client_socket.connect('tcp://{}:{}'.format(self.host.ip, port))

        dataformat_name = database.set(input_cfg['protocol'], input_cfg['set'])['outputs'][input_cfg['output']]

        self.data_source = RemoteDataSource()
        self.data_source.setup(self.client_socket, input_name, dataformat_name, prefix)


    def stop_databases_provider(self):
        if self.databases_container is not None:
            self.host.kill(self.databases_container)
            self.host.wait(self.databases_container)
            self.databases_container = None


    def test_success(self):
        self.start_databases_provider(CONFIGURATION)

        self.assertEqual(len(self.data_source), 9)

        for i in range(0, 9):
            (data, start_index, end_index) = self.data_source[i]
            self.assertEqual(start_index, i)
            self.assertEqual(end_index, i)
            self.assertEqual(data.value, i + 1)

#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2017 Idiap Research Institute, http://www.idiap.ch/           #
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
=====
local
=====

Execution utilities
"""


import os
import sys
import tempfile
import shutil
import zmq
import time

import logging
logger = logging.getLogger(__name__)

import simplejson

from .base import BaseExecutor

from beat.backend.python.helpers import create_inputs_from_configuration
from beat.backend.python.helpers import create_outputs_from_configuration
from beat.backend.python.helpers import AccessMode

from beat.backend.python.execution import AlgorithmExecutor
from beat.backend.python.execution import MessageHandler
from beat.backend.python.execution import LoopExecutor
from beat.backend.python.execution import LoopMessageHandler


class LocalExecutor(BaseExecutor):
    """LocalExecutor runs the code given an execution block information


    Parameters:

      prefix (str): Establishes the prefix of your installation.

      data (dict, str): The piece of data representing the block to be executed.
        It must validate against the schema defined for execution blocks. If a
        string is passed, it is supposed to be a fully qualified absolute path to
        a JSON file containing the block execution information.

      cache (:py:class:`str`, Optional): If your cache is not located under
        ``<prefix>/cache``, then specify a full path here. It will be used
        instead.

      dataformat_cache (:py:class:`dict`, Optional): A dictionary mapping
        dataformat names to loaded dataformats. This parameter is optional and,
        if passed, may greatly speed-up database loading times as dataformats
        that are already loaded may be re-used. If you use this parameter, you
        must guarantee that the cache is refreshed as appropriate in case the
        underlying dataformats change.

      database_cache (:py:class:`dict`, Optional): A dictionary mapping
        database names to loaded databases. This parameter is optional and, if
        passed, may greatly speed-up database loading times as databases that
        are already loaded may be re-used. If you use this parameter, you must
        guarantee that the cache is refreshed as appropriate in case the
        underlying databases change.

      algorithm_cache (:py:class:`dict`, Optional): A dictionary mapping
        algorithm names to loaded algorithms. This parameter is optional and,
        if passed, may greatly speed-up database loading times as algorithms
        that are already loaded may be re-used. If you use this parameter, you
        must guarantee that the cache is refreshed as appropriate in case the
        underlying algorithms change.

      library_cache (:py:class:`dict`, Optional): A dictionary mapping library
        names to loaded libraries. This parameter is optional and, if passed,
        may greatly speed-up library loading times as libraries that are
        already loaded may be re-used. If you use this parameter, you must
        guarantee that the cache is refreshed as appropriate in case the
        underlying libraries change.

      custom_root_folders (:py:class:`dict`, Optional): A dictionary where the
        keys are database identifiers (``<db_name>/<version>``) and the values
        are paths to the given database's files. These values will override the
        value found in the database's metadata.


    Attributes:

      cache (str): The path to the cache currently being used

      errors (list): A list containing errors found while loading this execution
        block.

      data (dict): The original data for this executor, as loaded by our JSON
        decoder.

      algorithm (.algorithm.Algorithm): An object representing the
        algorithm to be run.

      databases (dict): A dictionary in which keys are strings with database
        names and values are :py:class:`.database.Database`, representing the
        databases required for running this block. The dictionary may be empty
        in case all inputs are taken from the file cache.

      views (dict): A dictionary in which the keys are tuples pointing to the
        ``(<database-name>, <protocol>, <set>)`` and the value is a setup view
        for that particular combination of details. The dictionary may be empty
        in case all inputs are taken from the file cache.

      input_list (beat.backend.python.inputs.InputList): A list of inputs that
        will be served to the algorithm.

      output_list (beat.backend.python.outputs.OutputList): A list of outputs
        that the algorithm will produce.

      data_sources (list): A list with all data-sources created by our execution
        loader.

      data_sinks (list): A list with all data-sinks created by our execution
        loader. These are useful for clean-up actions in case of problems.

      custom_root_folders (dict): A dictionary where the keys are database
        identifiers (`<db_name>/<version>`) and the values are paths to the
        given database's files. These values will override the value found
        in the database's metadata.

    """

    def __init__(self, prefix, data, cache=None, dataformat_cache=None,
            database_cache=None, algorithm_cache=None, library_cache=None,
            custom_root_folders=None):

        super(LocalExecutor, self).__init__(prefix, data, cache=cache,
                                            dataformat_cache=dataformat_cache,
                                            database_cache=database_cache,
                                            algorithm_cache=algorithm_cache,
                                            library_cache=library_cache,
                                            custom_root_folders=custom_root_folders)

        self.working_dir = None
        self.executor = None
        self.message_handler = None
        self.executor_socket = None

        self.loop_executor = None
        self.loop_message_handler = None
        self.loop_socket = None

        self.zmq_context = None


    def __cleanup(self):
        if self.loop_executor:
            self.loop_executor.wait()

        for handler in [self.message_handler, self.loop_message_handler]:
            if handler:
                handler.kill()
                handler.join()
                handler.destroy()

        for socket in [self.executor_socket, self.loop_socket]:
            if socket:
                socket.setsockopt(zmq.LINGER, 0)
                socket.close()

        if self.zmq_context is not None:
            self.zmq_context.destroy()

        if self.working_dir is not None:
            shutil.rmtree(self.working_dir)


    def process(self, virtual_memory_in_megabytes=0, max_cpu_percent=0,
                timeout_in_minutes=0):
        """Executes the user algorithm code

        Parameters:

          virtual_memory_in_megabytes (:py:class:`int`, Optional): The amount
            of virtual memory (in Megabytes) available for the job. If set to
            zero, no limit will be applied.

          max_cpu_percent (:py:class:`int`, Optional): The maximum amount of
            CPU usage allowed in a system. This number must be an integer
            number between 0 and ``100*number_of_cores`` in your system. For
            instance, if your system has 2 cores, this number can go between 0
            and 200. If it is <= 0, then we don't track CPU usage.

          timeout_in_minutes (int): The number of minutes to wait for the user
            process to execute. After this amount of time, the user process is
            killed with ``signal.SIGKILL``. If set to zero, no timeout will be
            applied.

        Returns:

          dict: A dictionary which is JSON formattable containing the summary of
            this block execution.

        """

        def _create_result(status, error_message=''):
            return {
                'status': status,
                'statistics': {
                    'data': self.io_statistics,
                    'cpu': {
                        'user': 0.0,
                        'system': 0.0,
                        'total': 0.0,
                        'percent': 0.0,
                        'processors': 1,
                    },
                    'memory': {
                        'rss': 0,
                        'limit': 0,
                        'percent': 0.0,
                    },
                },
                'stderr': '',
                'stdout': '',
                'system_error': '',
                'user_error': error_message,
                'timed_out': False
            }

        def _process_exception(exception, prefix, contribution_kind):
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.extract_tb(exc_traceback)

            contributions_prefix = os.path.join(prefix, contribution_kind) + os.sep

            for first_line, line in enumerate(tb):
                if line[0].startswith(contributions_prefix):
                    break

            if first_line == len(tb):
                first_line = 0

            s = ''.join(traceback.format_list(tb[first_line:]))
            s = s.replace(contributions_prefix, '').strip()

            return "%s\n%s: %s" % (s, type(exception).__name__, exception)


        if not self.valid:
            raise RuntimeError("execution information is bogus:\n  * %s" % \
                    '\n  * '.join(self.errors))

        self.message_handler = MessageHandler('127.0.0.1')
        self.message_handler.start()

        self.zmq_context = zmq.Context()
        self.executor_socket = self.zmq_context.socket(zmq.PAIR)
        self.executor_socket.connect(self.message_handler.address)

        self.working_dir = tempfile.mkdtemp(prefix=__name__)
        working_prefix = os.path.join(self.working_dir, 'prefix')

        self.dump_runner_configuration(self.working_dir)
        self.algorithm.export(working_prefix)

        if self.loop_algorithm:
            self.loop_algorithm.export(working_prefix)
            self.loop_message_handler = LoopMessageHandler('127.0.0.1')
            self.loop_socket = self.zmq_context.socket(zmq.PAIR)
            self.loop_socket.connect(self.loop_message_handler.address)

            self.loop_executor = LoopExecutor(self.loop_message_handler,
                                              self.working_dir,
                                              database_cache=self.databases,
                                              cache_root=self.cache)

            retval = self.loop_executor.setup()
            if not retval:
                self.__cleanup()
                raise RuntimeError("Loop algorithm setup failed")

            prepared = self.loop_executor.prepare()
            if not prepared:
                self.__cleanup()
                raise RuntimeError("Loop algorithm prepare failed")

            self.loop_executor.process()

        self.executor = AlgorithmExecutor(self.executor_socket,
                                          self.working_dir,
                                          database_cache=self.databases,
                                          cache_root=self.cache,
                                          loop_socket=self.loop_socket)

        retval = self.executor.setup()
        if not retval:
            self.__cleanup()
            raise RuntimeError("Algorithm setup failed")

        prepared = self.executor.prepare()
        if not prepared:
            self.__cleanup()
            raise RuntimeError("Algorithm prepare failed")

        _start = time.time()

        try:
            processed = self.executor.process()
        except Exception as e:
            message = _process_exception(e, self.prefix, 'databases')
            self.__cleanup()
            return _create_result(1, message)

        if not processed:
            self.__cleanup()
            raise RuntimeError("Algorithm process failed")

        proc_time = time.time() - _start

        # some local information
        logger.debug("Total processing time was %.3f seconds" , proc_time)

        self.__cleanup()

        return _create_result(0)

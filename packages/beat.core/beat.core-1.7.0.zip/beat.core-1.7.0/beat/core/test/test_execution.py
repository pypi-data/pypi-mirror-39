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


# Tests for experiment execution

import os
import glob
import logging
logger = logging.getLogger(__name__)

import numpy
import unittest

from ..experiment import Experiment
from ..execution import LocalExecutor
from ..execution import SubprocessExecutor
from ..hash import hashFileContents
from ..hash import hashDataset
from ..hash import toPath
from ..data import CachedDataSource

from . import prefix, tmp_prefix
from .utils import cleanup
from .utils import slow

import nose.tools


#----------------------------------------------------------

class BaseExecutionMixIn(object):

    def check_output(self, prefix, path):
        '''Checks if a given output exists, together with its indexes and checksums
        '''

        finalpath = os.path.join(prefix, path)
        datafiles = glob.glob(finalpath + '*.data')
        datachksums = glob.glob(finalpath + '*.data.checksum')
        indexfiles = glob.glob(finalpath + '*.index')
        indexchksums = glob.glob(finalpath + '*.index.checksum')

        assert datafiles
        nose.tools.eq_(len(datafiles), len(indexfiles))
        for k in datafiles + indexfiles:
            checksum_file = k + '.checksum'
            assert checksum_file in datachksums + indexchksums
            stored_checksum = None
            with open(checksum_file, 'rt') as f: stored_checksum = f.read().strip()
            current_checksum = hashFileContents(k)
            nose.tools.eq_(current_checksum, stored_checksum)


    def load_result(self, executor):
        '''Loads the result of an experiment, in a single go'''

        f = CachedDataSource()
        assert f.setup(os.path.join(executor.cache, executor.data['result']['path'] + '.data'),
                       executor.prefix)
        data, start, end = f[0]
        nose.tools.eq_(start, 0)
        assert end >= start
        f.close()
        return data


    def execute(self, label, expected_result, **kwargs):
        """Executes the full experiment, block after block, returning results. If an
        error occurs, returns information about the err'd block. Otherwise, returns
        ``None``.

        This bit of code mimics the scheduler, but does everything on the local
        machine. It borrows some code from the package ``beat.cmdline``.
        """

        dataformat_cache = {}
        database_cache = {}
        algorithm_cache = {}

        experiment = Experiment(prefix, label, dataformat_cache, database_cache,
                                algorithm_cache)

        assert experiment.valid, '\n  * %s' % '\n  * '.join(experiment.errors)

        for block_name, infos in experiment.datasets.items():
            view = infos['database'].view(infos['protocol'], infos['set'])
            filename = toPath(hashDataset(infos['database'].name, infos['protocol'], infos['set']), suffix='.db')
            view.index(os.path.join(tmp_prefix, filename))

        scheduled = experiment.setup()

        # can we execute it?
        results = []
        for key, value in scheduled.items():
            configuration = {**value['configuration'], **kwargs}

            executor = self.create_executor(prefix, configuration, tmp_prefix,
                                            dataformat_cache, database_cache, algorithm_cache)
            assert executor.valid, '\n  * %s' % '\n  * '.join(executor.errors)

            with executor:
                result = executor.process(timeout_in_minutes=3)
                assert result
                assert 'status' in result
                assert 'stdout' in result
                assert 'stderr' in result
                assert 'timed_out' in result
                assert 'system_error' in result
                assert 'user_error' in result
                if result['status'] != 0:
                    logger.warn("status: %i", result['status'])
                    logger.warn("(eventual) system errors: %s", result['system_error'])
                    logger.warn("(eventual) user errors: %s", result['user_error'])
                    logger.warn("stdout: %s", result['stdout'])
                    logger.warn("stderr: %s", result['stderr'])
                    return result
                if result['system_error']:
                    logger.warn("system errors: %s", result['system_error'])
                    return result
                assert result['status'] == 0

                if 'statistics' in result:
                    assert isinstance(result['statistics'], dict)

            if executor.analysis:
                self.check_output(tmp_prefix, executor.data['result']['path'])
                results.append(self.load_result(executor))
            else:
                for name, details in executor.data['outputs'].items():
                    self.check_output(tmp_prefix, details['path'])

        # compares all results
        assert results

        for k, result in enumerate(results):
            expected = result.__class__()
            expected.from_dict(expected_result[k], casting='unsafe') #defaults=False

            assert result.isclose(expected), "%r is not close enough to %r" % (result.as_dict(), expected.as_dict())


    @slow
    def test_integers_addition_1(self):
        assert self.execute('user/user/integers_addition/1/integers_addition',
                [{'sum': 495, 'nb': 9}]) is None

    @slow
    def test_integers_addition_2(self):
        assert self.execute('user/user/integers_addition/2/integers_addition',
                [{'sum': 4995, 'nb': 9}]) is None

    @slow
    def test_single_1_single(self):
        assert self.execute('user/user/single/1/single', [{'out_data': 42}]) is None

    @slow
    def test_single_1_add(self):
        assert self.execute('user/user/single/1/single_add', [{'out_data': 43}]) is None

    @slow
    def test_single_1_add2(self):
        assert self.execute('user/user/single/1/single_add2', [{'out_data': 44}]) is None

    @slow
    def test_single_1_error(self):
        result = self.execute('user/user/single/1/single_error', [None])
        assert result
        nose.tools.eq_(result['status'], 1)
        assert result['user_error']
        assert 'NameError' in result['user_error']
        nose.tools.eq_(result['system_error'], '')

    @slow
    def test_single_1_crash(self):
        result = self.execute('user/user/single/1/single_crash', [None])
        assert result
        nose.tools.eq_(result['status'], 1)
        assert result['user_error']
        assert 'NameError' in result['user_error']
        nose.tools.eq_(result['system_error'], '')

    @slow
    def test_single_1_db_crash(self):
        result = self.execute('user/user/single/1/single_db_crash', [None])
        assert result
        assert result['status'] != 0
        assert result['user_error']
        assert 'a = b' in result['user_error']
        nose.tools.eq_(result['system_error'], '')

    @slow
    def test_single_1_large(self):
        assert self.execute('user/user/single/1/single_large', [{'out_data': 2.0}]) is None

    @slow
    def test_double_1(self):
        assert self.execute('user/user/double/1/double', [{'out_data': 42}]) is None

    @slow
    def test_triangle_1(self):
        assert self.execute('user/user/triangle/1/triangle', [{'out_data': 42}]) is None

    @slow
    def test_too_many_nexts(self):
        result = self.execute('user/user/triangle/1/too_many_nexts', [None])
        assert result
        assert result['status'] != 0
        assert result['user_error']
        assert 'no more data' in result['user_error']

    @slow
    def test_double_triangle_1(self):
        assert self.execute('user/user/double_triangle/1/double_triangle', [{'out_data': 42}]) is None

    @slow
    def test_inputs_mix_1(self):
        assert self.execute('user/user/inputs_mix/1/test', [{'sum': 495, 'nb': 9}]) is None

    @slow
    def test_inputs_mix_2(self):
        assert self.execute('user/user/inputs_mix/2/test', [{'sum': 495, 'nb': 9}]) is None

    @slow
    def test_inputs_mix_3(self):
        assert self.execute('user/user/inputs_mix/3/test', [{'sum': 945, 'nb': 9}]) is None

    @slow
    def test_inputs_mix_3b(self):
        assert self.execute('user/user/inputs_mix/3/test2', [{'sum': 954, 'nb': 9}]) is None

    @slow
    def test_inputs_mix_4(self):
        assert self.execute('user/user/inputs_mix/4/test', [{'sum': 990, 'nb': 9}]) is None

    @slow
    def test_inputs_mix_4b(self):
        assert self.execute('user/user/inputs_mix/4/test2', [{'sum': 1008, 'nb': 9}]) is None

    @slow
    def test_integers_labelled_1(self):
        assert self.execute('user/user/integers_labelled/1/test', [
            {
                'nb_data_units': 3,
                'indices': '0 - 4\n5 - 9\n10 - 14\n'
            }
        ]) is None

    @slow
    def test_preprocessing_1(self):
        assert self.execute('user/user/preprocessing/1/different_frequencies', [{'sum': 363, 'nb': 8}]) is None

    @slow
    def test_single_1_prepare_success(self):
        assert self.execute('user/user/single/1/prepare_success', [{'out_data': 42}]) is None

    @slow
    def test_loop_1(self):
        assert self.execute('user/user/loop/1/loop', [{'sum': 504, 'nb': 9}]) is None

    # For benchmark purposes
    # @slow
    # def test_double_1_large(self):
    #     import time
    #     start = time.time()
    #     assert self.execute('user/user/double/1/large', [{'out_data': 49489830}]) is None
    #     print(time.time() - start)

    # For benchmark purposes
    # @slow
    # def test_double_1_large2(self):
    #     import time
    #     start = time.time()
    #     assert self.execute('user/user/double/1/large2', [{'out_data': 21513820}]) is None
    #     print(time.time() - start)


#----------------------------------------------------------


class TestLocalExecution(BaseExecutionMixIn):

    def create_executor(self, prefix, configuration, tmp_prefix, dataformat_cache,
                        database_cache, algorithm_cache):
        return LocalExecutor(prefix, configuration, tmp_prefix,
                             dataformat_cache, database_cache, algorithm_cache)

    @slow
    def test_single_1_prepare_error(self):
        with nose.tools.assert_raises(RuntimeError) as context:
            result = self.execute('user/user/single/1/prepare_error', [None])

            assert 'Algorithm prepare failed' in context.exception

    @slow
    def test_single_1_setup_error(self):
        with nose.tools.assert_raises(RuntimeError) as context:
            result = self.execute('user/user/single/1/setup_error', [None])

            assert 'Algorithm setup failed' in context.exception


#----------------------------------------------------------


class TestSubprocessExecution(BaseExecutionMixIn):

    def create_executor(self, prefix, configuration, tmp_prefix, dataformat_cache,
                        database_cache, algorithm_cache):
        return SubprocessExecutor(prefix, configuration, tmp_prefix,
                                  dataformat_cache, database_cache, algorithm_cache)

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

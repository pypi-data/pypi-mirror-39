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


'''Decorators for test units'''

import os
import shutil

import nose
import docker

#----------------------------------------------------------


def slow(t):
    """
    Label a test as 'slow'.

    The exact definition of a slow test is obviously both subjective and
    hardware-dependent, but in general any individual test that requires more
    than a second or two should be labeled as slow (the whole suite consists of
    thousands of tests, so even a second is significant).

    Parameters
    ----------
    t : callable
        The test to label as slow.

    Returns
    -------
    t : callable
        The decorated test `t`.

    Examples
    --------
    The `numpy.testing` module includes ``import decorators as dec``.
    A test can be decorated as slow like this::

      from numpy.testing import *

      @dec.slow
      def test_big(self):
        print('Big, slow test')

    """

    t.slow = True
    return t


#----------------------------------------------------------


def skipif(skip_condition, msg=None):
    """
    Make function raise SkipTest exception if a given condition is true.

    If the condition is a callable, it is used at runtime to dynamically
    make the decision. This is useful for tests that may require costly
    imports, to delay the cost until the test suite is actually executed.

    Parameters
    ----------
    skip_condition : bool or callable
        Flag to determine whether to skip the decorated test.
    msg : str, optional
        Message to give on raising a SkipTest exception. Default is None.

    Returns
    -------
    decorator : function
        Decorator which, when applied to a function, causes SkipTest
        to be raised when `skip_condition` is True, and the function
        to be called normally otherwise.

    Notes
    -----
    The decorator itself is decorated with the ``nose.tools.make_decorator``
    function in order to transmit function name, and various other metadata.

    """

    def skip_decorator(f):

        # Allow for both boolean or callable skip conditions.
        if callable(skip_condition):
            skip_val = lambda: skip_condition()
        else:
            skip_val = lambda: skip_condition

        # We need to define *two* skippers because Python doesn't allow both
        # return with value and yield inside the same function.
        def skipper_func(*args, **kwargs):
            """Skipper for normal test functions."""
            if skip_val():
                raise nose.SkipTest(msg)
            else:
                return f(*args, **kwargs)

        def skipper_gen(*args, **kwargs):
            """Skipper for test generators."""
            if skip_val():
                raise nose.SkipTest(msg)
            else:
                for x in f(*args, **kwargs):
                    yield x

        # Choose the right skipper to use when building the actual decorator.
        if nose.util.isgenerator(f):
            skipper = skipper_gen
        else:
            skipper = skipper_func

        return nose.tools.make_decorator(f)(skipper)

    return skip_decorator


#----------------------------------------------------------


def cleanup():

    from . import prefix, tmp_prefix

    cache_path = os.path.join(prefix, 'cache')
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)

    beat_path = os.path.join(prefix, '.beat')
    if os.path.exists(beat_path):
        shutil.rmtree(beat_path)

    if os.path.exists(tmp_prefix):
        os.makedirs(tmp_prefix + '.new')
        shutil.copymode(tmp_prefix, tmp_prefix + '.new')
        shutil.rmtree(tmp_prefix)
        shutil.move(tmp_prefix + '.new', tmp_prefix)


#----------------------------------------------------------


def create_network(network_name):
    """ Create a docker network with the given name"""

    ipam_pool = docker.types.IPAMPool(subnet='193.169.0.0/24',
                                      gateway='193.169.0.254')

    ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])

    client = docker.from_env()
    network = client.networks.create(network_name,
                                     driver="bridge",
                                     ipam=ipam_config)
    return network

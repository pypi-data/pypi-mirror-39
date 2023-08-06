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

"""
=====
stats
=====

A class that can read, validate and update statistical information

Forward impored from :py:mod:`beat.backend.python.stats`:
:py:func:`beat.backend.python.stats.io_statistics`
:py:func:`beat.backend.python.stats.update`
"""


import os
import copy

import simplejson

from . import schema
from . import prototypes

from beat.backend.python.stats import io_statistics
from beat.backend.python.stats import update


class Statistics(object):
    """Statistics define resource usage for algorithmic code runs


    Parameters:

      data (:py:class:`object`, Optional): The piece of data representing the
        statistics the be read, it must validate against our pre-defined
        execution schema. If the input is ``None`` or empty, then start a new
        statistics from scratch.


    Attributes:

      errors (list of str): A list containing errors found while loading this
        statistics information.

      data (dict): The original data for these statistics

    """

    def __init__(self, data=None):

        self.errors = []

        if data:
            self._load(data)  # also runs validation
        else:
            self._data, self.errors = prototypes.load('statistics')  # also validates

    def _load(self, data):
        """Loads the statistics

        Parameters:

          data (object, str, file): The piece of data to load. The input can be
            a valid python object that represents a JSON structure, a file,
            from which the JSON contents will be read out or a string. See
            :py:func:`schema.validate` for more details.
        """

        # reset
        self._data = None
        self.errors = []

        if not isinstance(data, dict):  # user has passed a file pointer
            if not os.path.exists(data):
                self.errors.append('File not found: %s' % data)
                return

        # this runs basic validation, including JSON loading if required
        self._data, self.errors = schema.validate('statistics', data)
        if self.errors: return  # don't proceed with the rest of validation


    @property
    def schema_version(self):
        """Returns the schema version"""

        return self.data.get('schema_version', 1)


    @property
    def cpu(self):
        """Returns only CPU information"""

        return self._data['cpu']

    @cpu.setter
    def cpu(self, data):
        """Sets the CPU information"""

        for key in ('user', 'system', 'total'):
            self._data['cpu'][key] = data[key]

        for key in ('voluntary', 'involuntary'):
            self._data['cpu']['context_switches'][key] = data['context_switches'][key]


    @property
    def memory(self):
        """Returns only memory information"""

        return self._data['memory']


    @memory.setter
    def memory(self, data):
        """Sets only the memory information"""

        for key in ('rss',): self._data['memory'][key] = data[key]


    @property
    def data(self):
        """Returns only I/O information"""

        return self._data['data']


    @data.setter
    def data(self, data):
        """Sets only the I/O information"""

        for key in ('volume', 'blocks', 'time'):
            self._data['data'][key]['read'] = data[key]['read']
            self._data['data'][key]['write'] = data[key]['write']

        self._data['data']['files'] = list(data['files'])
        self._data['network'] = data['network']


    @property
    def valid(self):
        """A boolean that indicates if this executor is valid or not"""

        return not bool(self.errors)


    def __add__(self, other):
        """Adds two statistics data blocks"""

        retval = Statistics(copy.deepcopy(self._data))
        retval += other
        return retval


    def __iadd__(self, other):
        """Self-add statistics from another block"""

        if not isinstance(other, Statistics): return NotImplemented

        for key in ('user', 'system', 'total'):
            self._data['cpu'][key] += other._data['cpu'][key]

        for key in ('voluntary', 'involuntary'):
            self._data['cpu']['context_switches'][key] += \
                    other._data['cpu']['context_switches'][key]

        for key in ('rss', ): #gets the maximum between the two
            self._data['memory'][key] = max(other._data['memory'][key],
                self._data['memory'][key])

        for key in ('volume', 'blocks', 'time'):
            self._data['data'][key]['read'] += other._data['data'][key]['read']
            self._data['data'][key]['write'] += other._data['data'][key]['write']

        self._data['data']['files'] += other._data['data']['files']

        self._data['data']['network']['wait_time'] += \
                other._data['data']['network']['wait_time']

        return self


    def __str__(self):

        return self.as_json(2)


    def as_json(self, indent=None):
        """Returns self as as JSON

        Parameters:
            :param indent int: Indentation to use for the JSON generation

        Returns:
            dict: JSON representation
        """

        return simplejson.dumps(self._data, indent=indent)


    def as_dict(self):
        """Returns self as a dictionary"""

        return self._data


    def write(self, f):
        """Writes contents to a file-like object"""

        if hasattr(f, 'write'): f.write(str(self))
        else:
            with open(f, 'wt') as fobj: fobj.write(str(self))


# ----------------------------------------------------------


def cpu_statistics(start, end):
    """Summarizes current CPU usage

    This method should be used when the currently set algorithm is the only one
    executed through the whole process. It is done for collecting resource
    statistics on separate processing environments. It follows the recipe in:
    http://stackoverflow.com/questions/30271942/get-docker-container-cpu-usage-as-percentage

    Returns:

      dict: A dictionary summarizing current CPU usage

    """

    if 'system_cpu_usage' not in end:
        return {
                'user': 0.0,
                'system': 0.0,
                'total': 0.0,
                'percent': 0.0,
                'processors': 1,
               }

    if start is not None:
        user_cpu = end['cpu_usage']['total_usage'] - \
            start['cpu_usage']['total_usage']
        total_cpu = end['system_cpu_usage'] - start['system_cpu_usage']

    else:
        user_cpu = end['cpu_usage']['total_usage']
        total_cpu = end['system_cpu_usage']

    user_cpu /= 1000000000.  # in seconds
    total_cpu /= 1000000000.  # in seconds
    processors = len(end['cpu_usage']['percpu_usage']) if \
        end['cpu_usage']['percpu_usage'] is not None else 1

    return {
            'user': user_cpu,
            'system': 0.,
            'total': total_cpu,
            'percent': 100.*processors*user_cpu/total_cpu if total_cpu else 0.,
            'processors': processors,
           }


# ----------------------------------------------------------


def memory_statistics(data):
    """Summarizes current memory usage

    This method should be used when the currently set algorithm is the only one
    executed through the whole process. It is done for collecting resource
    statistics on separate processing environments.

    Returns:

      dict: A dictionary summarizing current memory usage

    """

    limit = float(data['limit'])
    memory = float(data['max_usage'])

    return {
            'rss': memory,
            'limit': limit,
            'percent': 100.*memory/limit if limit else 0.,
           }

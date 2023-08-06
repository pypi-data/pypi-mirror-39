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
=========
algorithm
=========

Validation for algorithms

Forward importing from :py:mod:`beat.backend.python.algorithm`
:py:class:`beat.backend.python.algorithm.Storage`
:py:class:`beat.backend.python.algorithm.Runner`
"""


import six
import numpy

from . import dataformat
from . import library
from . import schema
from . import prototypes
from . import utils

from beat.backend.python.algorithm import Storage
from beat.backend.python.algorithm import Runner
from beat.backend.python.algorithm import Algorithm as BackendAlgorithm


class Algorithm(BackendAlgorithm):
    """Algorithms represent runnable components within the platform.

    This class can only parse the meta-parameters of the algorithm (i.e., input
    and output declaration, grouping, synchronization details, parameters and
    splittability). The actual algorithm is not directly treated by this class.
    It can, however, provide you with a loader for actually running the
    algorithmic code (see :py:meth:`.runner`).


    Parameters:

      prefix (str): Establishes the prefix of your installation.

      data (:py:class:`object`, Optional): The piece of data representing the
        algorithm. It must validate against the schema defined for algorithms.
        If a string is passed, it is supposed to be a valid path to an
        algorithm in the designated prefix area. If a tuple is passed (or a
        list), then we consider that the first element represents the algorithm
        declaration, while the second, the code for the algorithm (either in
        its source format or as a binary blob). If ``None`` is passed, loads
        our default prototype for algorithms (source code will be in Python).

      dataformat_cache (:py:class:`dict`, Optional): A dictionary mapping
        dataformat names to loaded dataformats. This parameter is optional and,
        if passed, may greatly speed-up algorithm loading times as dataformats
        that are already loaded may be re-used.

      library_cache (:py:class:`dict`, Optional): A dictionary mapping library
        names to loaded libraries. This parameter is optional and, if passed,
        may greatly speed-up library loading times as libraries that are
        already loaded may be re-used.


    Attributes:

      name (str): The algorithm name

      description (str): The short description string, loaded from the JSON
        file if one was set.

      documentation (str): The full-length docstring for this object.

      storage (object): A simple object that provides information about file
        paths for this algorithm

      dataformats (dict): A dictionary containing all pre-loaded dataformats
        used by this algorithm. Data format objects will be of type
        :py:class:`beat.core.dataformat.DataFormat`.

      libraries (dict): A mapping object defining other libraries this
        algorithm needs to load so it can work properly.

      uses (dict): A mapping object defining the required library import name
        (keys) and the full-names (values).

      parameters (dict): A dictionary containing all pre-defined parameters
        that this algorithm accepts.

      splittable (bool): A boolean value that indicates if this algorithm is
        automatically parallelizeable by our backend.

      input_map (dict): A dictionary where the key is the input name and the
        value, its type. All input names (potentially from different groups)
        are comprised in this dictionary.

      output_map (dict): A dictionary where the key is the output name and the
        value, its type. All output names (potentially from different groups)
        are comprised in this dictionary.

      results (dict): If this algorithm is actually an analyzer (i.e., there
        are no formal outputs, but results that must be saved by the platform),
        then this dictionary contains the names and data types of those
        elements.

      groups (dict): A list containing dictionaries with inputs and outputs
        belonging to the same synchronization group.

      errors (list): A list containing errors found while loading this
        algorithm.

      data (dict): The original data for this algorithm, as loaded by our JSON
        decoder.

      code (str): The code that is associated with this algorithm, loaded as a
        text (or binary) file.

    """

    def __init__(self, prefix, data, dataformat_cache=None, library_cache=None):
        super(Algorithm, self).__init__(prefix, data, dataformat_cache, library_cache)


    def _load(self, data, dataformat_cache, library_cache):
        """Loads the algorithm"""

        self.errors = []
        self.data = None
        self.code = None

        self._name = None
        self.storage = None
        self.dataformats = {}  # preloaded dataformats
        self.libraries = {}  # preloaded libraries
        code = None

        if data is None:  # loads prototype and validates it

            data = None
            code = None

        elif isinstance(data, (tuple, list)):  # user has passed individual info

            data, code = data  # break down into two components


        if isinstance(data, six.string_types):  # user has passed a file pointer

            self._name = data
            self.storage = Storage(self.prefix, self._name)
            if not self.storage.json.exists():
                self.errors.append('Algorithm declaration file not found: %s' % data)
                return

            data = self.storage.json.path  # loads data from JSON declaration


        # At this point, `data' can be a dictionary or ``None``
        if data is None:  # loads the default declaration for an algorithm
            self.data, self.errors = prototypes.load('algorithm')
            assert not self.errors, "\n  * %s" % "\n  *".join(self.errors)
        else:  # just assign it
            # this runs basic validation, including JSON loading if required
            self.data, self.errors = schema.validate('algorithm', data)


        if self.errors: return  # don't proceed with the rest of validation

        if self.storage is not None:  # loading from the disk, check code
            if not self.storage.code.exists():
                if self.data['language'] != 'cxx':
                    self.errors.append('Algorithm code not found: %s' % \
                            self.storage.code.path)
                    return
            else:
                code = self.storage.code.load()


        # At this point, `code' can be a string (or a binary blob) or ``None``
        if code is None:  # loads the default code for an algorithm
            self.code = prototypes.binary_load('algorithm.py')
            self.data['language'] = 'python'

        else:  # just assign it - notice that in this case, no language is set
            self.code = code


        if self.errors: return  # don't proceed with the rest of validation


        # if no errors so far, make sense out of the declaration data
        self.groups = self.data['groups']

        # now we check for consistence
        self._check_endpoint_uniqueness()

        # create maps for easy access to data
        self.input_map = dict([(k,v['type']) for g in self.groups \
                for k,v in g['inputs'].items()])
        self.output_map = dict([(k,v['type']) for g in self.groups \
                for k,v in g.get('outputs', {}).items()])
        self.loop_map = dict([(k,v['type']) for g in self.groups \
                for k,v in g.get('loop', {}).items()])

        self._validate_required_dataformats(dataformat_cache)
        self._convert_parameter_types()

        # finally, the libraries
        self._validate_required_libraries(library_cache)
        self._check_language_consistence()


    def _check_endpoint_uniqueness(self):
        """Checks for name clashes accross input/output groups
        """

        all_input_names = []
        for group in self.groups: all_input_names.extend(group['inputs'].keys())
        if len(set(all_input_names)) != len(all_input_names):
            self.errors.append("repeated input name in algorithm `%s' " \
                    "declaration: %s" % (self.name, ', '.join(all_input_names)))

        # all outputs must have unique names
        all_output_names = []
        for group in self.groups:
            if 'outputs' not in group: continue
            all_output_names.extend(group['outputs'].keys())
        if len(set(all_output_names)) != len(all_output_names):
            self.errors.append("repeated output name in algorithm `%s' " \
                    "declaration: %s" % (self.name, ', '.join(all_output_names)))


    def _validate_required_dataformats(self, dataformat_cache):
        """Makes sure we can load all requested formats
        """

        for group in self.groups:

            for name, input in group['inputs'].items():
                if input['type'] in self.dataformats: continue

                if dataformat_cache and input['type'] in dataformat_cache:  # reuse
                    thisformat = dataformat_cache[input['type']]
                else:  # load it
                    thisformat = dataformat.DataFormat(self.prefix, input['type'])
                    if dataformat_cache is not None:  # update it
                        dataformat_cache[input['type']] = thisformat

                self.dataformats[input['type']] = thisformat

                if thisformat.errors:
                    self.errors.append("found error validating data format `%s' " \
                            "for input `%s' on algorithm `%s': %s" % \
                            (input['type'], name, self.name,
                                '\n'.join(thisformat.errors)))

            if 'outputs' not in group: continue

            for name, output in group['outputs'].items():
                if output['type'] in self.dataformats: continue

                if dataformat_cache and output['type'] in dataformat_cache:  # reuse
                    thisformat = dataformat_cache[output['type']]
                else:  # load it
                    thisformat = dataformat.DataFormat(self.prefix, output['type'])
                    if dataformat_cache is not None:  # update it
                        dataformat_cache[output['type']] = thisformat

                self.dataformats[output['type']] = thisformat

                if thisformat.errors:
                    self.errors.append("found error validating data format `%s' " \
                            "for output `%s' on algorithm `%s': %s" % \
                            (output['type'], name, self.name,
                                '\n'.join(thisformat.errors)))

        if self.results:

            for name, result in self.results.items():

                if result['type'].find('/') != -1:

                    if result['type'] in self.dataformats: continue

                    if dataformat_cache and result['type'] in dataformat_cache:  # reuse
                        thisformat = dataformat_cache[result['type']]
                    else:
                        thisformat = dataformat.DataFormat(self.prefix, result['type'])
                        if dataformat_cache is not None:  # update it
                            dataformat_cache[result['type']] = thisformat

                    self.dataformats[result['type']] = thisformat

                    if thisformat.errors:
                        self.errors.append("found error validating data format `%s' " \
                                "for result `%s' on algorithm `%s': %s" % \
                                (result['type'], name, self.name,
                                    '\n'.join(thisformat.errors)))


    def _convert_parameter_types(self):
        """Converts types to numpy equivalents, checks defaults, ranges and
        choices
        """

        def _try_convert(name, tp, value, desc):
            try:
                return tp.type(value)
            except Exception as e:
                self.errors.append("%s for parameter `%s' cannot be cast to type " \
                        "`%s': %s" % (desc, name, tp.name, e))

        if self.parameters is None: return

        for name, parameter in self.parameters.items():
            if parameter['type'] == 'string':
                parameter['type'] = numpy.dtype('str')
            else:
                parameter['type'] = numpy.dtype(parameter['type'])

            if 'range' in parameter:
                parameter['range'][0] = _try_convert(name, parameter['type'],
                    parameter['range'][0], 'start of range')
                parameter['range'][1] = _try_convert(name, parameter['type'],
                    parameter['range'][1], 'end of range')
                if parameter['range'][0] >= parameter['range'][1]:
                    self.errors.append("range for parameter `%s' has a start greater " \
                            "then the end value (%r >= %r)" % \
                            (name, parameter['range'][0], parameter['range'][1]))

            if 'choice' in parameter:
                for i, choice in enumerate(parameter['choice']):
                    parameter['choice'][i] = _try_convert(name, parameter['type'],
                        parameter['choice'][i], 'choice[%d]' % i)

            if 'default' in parameter:
                parameter['default'] = _try_convert(name, parameter['type'],
                    parameter['default'], 'default')

                if 'range' in parameter:  # check range
                    if parameter['default'] < parameter['range'][0] or \
                            parameter['default'] > parameter['range'][1]:
                        self.errors.append("default for parameter `%s' (%r) is not " \
                          "within parameter range [%r, %r]" % (name, parameter['default'],
                              parameter['range'][0], parameter['range'][1]))

                if 'choice' in parameter:  # check choices
                    if parameter['default'] not in parameter['choice']:
                        self.errors.append("default for parameter `%s' (%r) is not " \
                          "a valid choice `[%s]'" % (name, parameter['default'],
                              ', '.join(['%r' % k for k in parameter['choice']])))


    def _validate_required_libraries(self, library_cache):

        # all used libraries must be loadable; cannot use self as a library

        if self.uses:

            for name, value in self.uses.items():

                self.libraries[value] = library_cache.setdefault(value,
                        library.Library(self.prefix, value, library_cache))

                if not self.libraries[value].valid:
                    self.errors.append("referred library `%s' (%s) is not valid" % \
                            (self.libraries[value].name, name))


    def _check_language_consistence(self):

        # all used libraries must be programmed with the same language
        if self.language == 'unknown': return  # bail out on unknown language

        if self.uses:

            for name, library in self.uses.items():

                if library not in self.libraries: continue  # invalid

                if self.libraries[library].data is None:
                    self.errors.append("language for used library `%s' cannot be " \
                            "inferred as the library was not properly loaded" % \
                            (library,))
                    continue

                if self.libraries[library].language != self.language:
                    self.errors.append("language for used library `%s' (`%s') " \
                            "differs from current language for this algorithm (`%s')" % \
                            (library, self.libraries[library].language, self.language))

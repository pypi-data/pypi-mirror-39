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
========
database
========

Validation of databases

Forward importing from :py:mod:`beat.backend.python.database`:
:py:class:`beat.backend.python.database.Storage`
"""

import os

import six

from . import schema

from .dataformat import DataFormat
from . import prototypes

from beat.backend.python.database import Storage
from beat.backend.python.database import Database as BackendDatabase


class Database(BackendDatabase):
    """Databases define the start point of the dataflow in an experiment.


    Parameters:

      prefix (str): Establishes the prefix of your installation.

      data (dict, str): The piece of data representing the database. It must
        validate against the schema defined for databases. If a string is
        passed, it is supposed to be a valid path to an database in the
        designated prefix area.

      dataformat_cache (:py:class:`dict`, Optional): A dictionary mapping
        dataformat names to loaded dataformats. This parameter is optional and,
        if passed, may greatly speed-up database loading times as dataformats
        that are already loaded may be re-used. If you use this parameter, you
        must guarantee that the cache is refreshed as appropriate in case the
        underlying dataformats change.


    Attributes:

      name (str): The full, valid name of this database

      description (str): The short description string, loaded from the JSON
        file if one was set.

      documentation (str): The full-length docstring for this object.

      storage (object): A simple object that provides information about file
        paths for this database

      errors (list): A list containing errors found while loading this
        database.

      data (dict): The original data for this database, as loaded by our JSON
        decoder.

    """

    def __init__(self, prefix, data, dataformat_cache=None):
        super(Database, self).__init__(prefix, data, dataformat_cache)


    def _load(self, data, dataformat_cache):
        """Loads the database"""

        self._name = None
        self.storage = None
        self.dataformats = {}  # preloaded dataformats
        code = None

        if isinstance(data, (tuple, list)):  # user has passed individual info

            data, code = data  # break down into two components

        if isinstance(data, six.string_types):  # user has passed a file pointer

            self._name = data
            self.storage = Storage(self.prefix, self._name)
            data = self.storage.json.path
            if not self.storage.json.exists():
                self.errors.append('Database declaration file not found: %s' % data)
                return


        # this runs basic validation, including JSON loading if required
        self.data, self.errors = schema.validate('database', data)
        if self.errors: return  # don't proceed with the rest of validation

        if self.storage is not None:  # loading from the disk, check code
            if not self.storage.code.exists():
                self.errors.append('Database view code not found: %s' % \
                        self.storage.code.path)
                return
            else:
                code = self.storage.code.load()


        # At this point, `code' can be a string (or a binary blob) or ``None``
        if code is None:  # loads the default code for an algorithm
            self.code = prototypes.binary_load('view.py')

        else: # just assign it - notice that in this case, no language is set
            self.code = code


        if self.errors: return  # don't proceed with the rest of validation

        self._validate_semantics(dataformat_cache)


    def _validate_semantics(self, dataformat_cache):
        """Validates all sematical aspects of the database"""

        # all protocol names must be unique
        protocol_names = [k['name'] for k in self.data['protocols']]
        if len(protocol_names) != len(set(protocol_names)):
            self.errors.append(
                    "found different protocols with the same name: %s" % \
                            (protocol_names,)
                            )

        # all set names within a protocol must be unique
        for protocol in self.data['protocols']:
            set_names = [k['name'] for k in protocol['sets']]
            if len(set_names) != len(set(set_names)):
                self.errors.append(
                        "found different sets with the same name at protocol " \
                                "`%s': %s" % (protocol['name'], set_names),
                                )

            # all outputs must have valid data types
            for _set in protocol['sets']:

                for key, value in _set['outputs'].items():

                    if value in self.dataformats: continue

                    if value in dataformat_cache:  # re-use
                        dataformat = dataformat_cache[value]
                    else:
                        dataformat = DataFormat(self.prefix, value)
                        dataformat_cache[value] = dataformat

                    self.dataformats[value] = dataformat

                    if dataformat.errors:
                        self.errors.append("found error validating data format `%s' " \
                                "for output `%s' on set `%s' of protocol `%s': %s" % \
                                (value, key, _set['name'], protocol['name'],
                                    "\n".join(dataformat.errors))
                                )

                # all view names must be relative to the database root path
                if _set['view'].find('.') != -1 or _set['view'].find(os.sep) != -1:
                    self.errors.append("dataset views are required to sit inside the " \
                            "database root folder, but `%s' is either in a " \
                            "subdirectory or points to a python module, what is " \
                            "unsupported by this version" % (_set['view'],)
                            )

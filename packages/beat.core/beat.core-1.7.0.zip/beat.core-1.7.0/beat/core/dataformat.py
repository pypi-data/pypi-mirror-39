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
==========
dataformat
==========

Validation and parsing for dataformats

Forward importing from :py:mod:`beat.backend.python.dataformat`:
:py:class:`beat.backend.python.dataformat.Storage`
"""

import os
import copy

import six
import simplejson

from . import schema
from . import prototypes
from . import utils
from .baseformat import baseformat

from beat.backend.python.dataformat import Storage
from beat.backend.python.dataformat import DataFormat as BackendDataFormat



class DataFormat(BackendDataFormat):
    """Data formats define the chunks of data that circulate between blocks.

    Parameters:

      prefix (str): Establishes the prefix of your installation.

      data (:py:class:`object`, Optional): The piece of data representing the
        data format. It must validate against the schema defined for data
        formats. If a string is passed, it is supposed to be a valid path to an
        data format in the designated prefix area. If ``None`` is passed, loads
        our default prototype for data formats.

      parent (:py:class:`tuple`, Optional): The parent DataFormat for this
        format. If set to ``None``, this means this dataformat is the first one
        on the hierarchy tree. If set to a tuple, the contents are
        ``(format-instance, field-name)``, which indicates the originating
        object that is this object's parent and the name of the field on that
        object that points to this one.

      dataformat_cache (:py:class:`dict`, Optional): A dictionary mapping
        dataformat names to loaded dataformats. This parameter is optional and,
        if passed, may greatly speed-up data format loading times as
        dataformats that are already loaded may be re-used. If you use this
        parameter, you must guarantee that the cache is refreshed as
        appropriate in case the underlying dataformats change.

    Attributes:

      name (str): The full, valid name of this dataformat

      description (str): The short description string, loaded from the JSON
        file if one was set.

      documentation (str): The full-length docstring for this object.

      storage (object): A simple object that provides information about file
        paths for this dataformat

      errors (list of str): A list containing errors found while loading this
        dataformat.

      data (dict): The original data for this dataformat, as loaded by our JSON
        decoder.

      resolved (dict): A dictionary similar to :py:attr:`data`, but with
        references fully resolved.

      referenced (dict): A dictionary pointing to all loaded dataformats.

      parent (beat.core.dataformat.DataFormat): The pointer to the
        dataformat to which the current format is part of. It is useful for
        internal error reporting.

    """

    def __init__(self, prefix, data, parent=None, dataformat_cache=None):
        super(DataFormat, self).__init__(prefix, data, parent, dataformat_cache)


    def _load(self, data, dataformat_cache):
        """Loads the dataformat"""

        self._name = None
        self.storage = None
        self.referenced = {}
        self.resolved = None
        self.errors = []
        self.data = None

        if data is None: #loads prototype and validates it

            self.data, self.errors = prototypes.load('dataformat')
            assert not self.errors, "\n  * %s" % "\n  *".join(self.errors)

        else:

            if not isinstance(data, dict): #user has passed a file pointer
                # make sure to log this into the cache (avoids recursion)
                dataformat_cache[data] = None

                self._name = data
                self.storage = Storage(self.prefix, data)
                data = self.storage.json.path
                if not self.storage.exists():
                    self.errors.append('Dataformat declaration file not found: %s' % data)
                    return

            # this runs basic validation, including JSON loading if required
            self.data, self.errors = schema.validate('dataformat', data)

        self.resolved = copy.deepcopy(self.data)

        # remove reserved fields
        def is_reserved(x):
            '''Returns if the field name is a reserved name'''
            return (x.startswith('__') and x.endswith('__')) or \
                    x in ('#description', '#schema_version')

        for key in list(self.resolved):
            if is_reserved(key): del self.resolved[key]

        if self.errors:
            #don't proceed with the rest of validation
            self.errors = utils.uniq(self.errors)
            return

        def maybe_load_format(name, obj, dataformat_cache):
            """Tries to load a given dataformat from its relative path"""

            if isinstance(obj, six.string_types) and obj.find('/') != -1: #load it

                if obj in dataformat_cache: #reuse

                    if dataformat_cache[obj] is None: #recursion detected
                        self.errors.append("recursion for dataformat `%s' detected" % obj)
                        return self

                    self.referenced[obj] = dataformat_cache[obj]

                else: #load it
                    self.referenced[obj] = DataFormat(self.prefix, obj, (self, name),
                            dataformat_cache)

                if not self.referenced[obj].valid:
                    self.errors.append("referred dataformat `%s' is invalid" % obj)

                return self.referenced[obj]

            elif isinstance(obj, dict): #can cache it, must load from scratch
                return DataFormat(self.prefix, obj, (self, name), dataformat_cache)

            elif isinstance(obj, list):
                retval = copy.deepcopy(obj)
                retval[-1] = maybe_load_format(field, obj[-1], dataformat_cache)
                return retval

            return obj

        # now checks that every referred dataformat also validates, and accumulates
        # errors
        for field, value in self.data.items():
            if field in ('#description', '#schema_version'):
                continue #skip the description and schema version meta attributes
            self.resolved[field] = maybe_load_format(field, value, dataformat_cache)
            if isinstance(self.resolved[field], DataFormat):
                if not self.resolved[field].valid:
                    self.errors.append("referred dataformat `%s' is invalid" % value)

        # at this point, there should be no more external references in
        # ``self.resolved``. We treat the "#extends" property, which requires a
        # special handling, given its nature.
        if '#extends' in self.resolved:

            ext = self.data['#extends']
            self.referenced[ext] = maybe_load_format(self.name, ext, dataformat_cache)
            basetype = self.resolved['#extends']

            # before updating, checks there is no name clash if basetype.valid:
            if basetype.valid:
                for attrname in self.resolved:
                    if attrname == '#extends': continue
                    if attrname in basetype.resolved:
                        self.errors.append("the attribute `%s' in `%s' clashes with an " \
                                "attribute with the same name on the extended class " \
                                "`%s'" %  (attrname, self.name, basetype.name))
                tmp = self.resolved
                self.resolved = basetype.resolved
                self.resolved.update(tmp)
                del self.resolved['#extends'] #avoids infinite recursion

            else:
                self.errors.append("referred dataformat `%s' is invalid" % ext)

        # all references are resolved at this point and the final model is built
        # you can lookup the original data in ``self.data`` and the final model
        # in ``self.resolved``.
        if self.errors:
            self.errors = utils.uniq(self.errors)

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


'''Schema validation for BEAT JSON I/O'''


import os
import collections
import pkg_resources

import six
import simplejson
import jsonschema


def maybe_load_json(s):
  """Maybe loads the JSON from a string or filename"""

  # if it is a string
  if isinstance(s, six.string_types):
    # if it is a valid path
    if os.path.exists(s):
      with open(s, 'rt') as f:
        return maybe_load_json(f)
    else:
      return simplejson.loads(s, object_pairs_hook=collections.OrderedDict)

  # if it is a 'file-like' object
  if hasattr(s, 'read'):
    return maybe_load_json(s.read())

  return s


def load_schema(schema_name, version=1):
  """Returns a JSON validator for the schema given the relative name


  Parameters:

    schema_name (str): the name of the schema to load. This value corresponds
      to the filename inside our schema directory (where this file is located)
      and should *exclude* the extension ``.json``.

    version (int): the version of the schema to use.


  Returns:

    jsonschema.Draft4Validator: An instance of a JSON schema draft-4 validator.


  Raises:

    jsonschema.SchemaError: If there is an error on the schema.

  """

  fname = pkg_resources.resource_filename(__name__,
          os.path.join(schema_name, '%d.json' % version))

  with open(fname, 'rb') as f:
    data = f.read().decode()
    schema = simplejson.loads(data)

  basedir = os.path.realpath(os.path.dirname(fname))
  resolver = jsonschema.RefResolver('file://' + basedir + '/', schema)

  # now we load it
  return jsonschema.Draft4Validator(schema, resolver=resolver)


def validate(schema_name, data):
  """Validates the input data using the schema

  This function handles schema versionning in the context of BEAT transparently
  by first peeking the schema version required by the JSON data and then
  validating the JSON data against the proper schema version for the respective
  type.


  Example:

    .. code-block:: python

       try:
           cleaned_data, error_list = validate('toolchain', '/to/my/file.json')
       except simplejson.JSONDecodeError as e:
           print(e)


  Parameters:

    schema_name (str): The relative path to the schema to use for validation.
      For example, to validate a toolchain, use ``'toolchain'``.

    data (object, str, file): The piece of data to validate. The input can be a
      valid python object that represents a JSON structure, a file, from which
      the JSON contents will be read out or a string.

      If ``data`` is a string and represents a valid filesystem path, the
      relevant file will be opened and read as with
      :py:func:`simplejson.load``. Otherwise, it will be considered to be
      string containing a valid JSON structure that will be loaded as with
      :py:func:`simplejson.loads`.

      Note that if the file is opened and read internally using
      :py:func:`simplejson.load`, exceptions may be thrown by that subsystem,
      concerning the file structure. Consult the manual page for
      :py:mod:`simplejson` for details.


  Returns:

    A tuple with two elements: the cleaned JSON data structure, after
    processing and a list of errors found by ``jsonschema``. If no errors
    occur, then returns an empty list for the second element of the tuple.

  Raises:

    jsonschema.SchemaError: If there is an error on the schema.

  """

  try:
    data = maybe_load_json(data)
  except simplejson.JSONDecodeError as e:
    return data, ["invalid JSON code: %s" % str(e)]

  # handles the schema version
  if schema_name != 'dataformat': version = data.get('schema_version', 1)
  else: version = data.get('#schema_version', 1)

  validator = load_schema(schema_name, version)

  def encode_error(error, indent=''):
    abspath = '/'.join([''] + ([str(k) for k in error.absolute_path] or ['']))
    schpath = '/'.join([''] + ([str(k) for k in error.schema_path] or ['']))
    retval = indent + '%s: %s (rule: %s)' % (abspath, error.message, schpath)
    for another_error in error.context:
      retval += '\n' + encode_error(another_error, indent + '  ')
    return retval

  errorlist = [encode_error(k) for k in \
          sorted(validator.iter_errors(data), key=lambda e: e.path)]

  return data, errorlist

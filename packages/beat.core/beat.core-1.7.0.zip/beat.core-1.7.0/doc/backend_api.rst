
.. Copyright (c) 2016 Idiap Research Institute, http://www.idiap.ch/          ..
.. Contact: beat.support@idiap.ch                                             ..
..                                                                            ..
.. This file is part of the beat.core module of the BEAT platform.            ..
..                                                                            ..
.. Commercial License Usage                                                   ..
.. Licensees holding valid commercial BEAT licenses may use this file in      ..
.. accordance with the terms contained in a written agreement between you     ..
.. and Idiap. For further information contact tto@idiap.ch                    ..
..                                                                            ..
.. Alternatively, this file may be used under the terms of the GNU Affero     ..
.. Public License version 3 as published by the Free Software and appearing   ..
.. in the file LICENSE.AGPL included in the packaging of this file.           ..
.. The BEAT platform is distributed in the hope that it will be useful, but   ..
.. WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY ..
.. or FITNESS FOR A PARTICULAR PURPOSE.                                       ..
..                                                                            ..
.. You should have received a copy of the GNU Affero Public License along     ..
.. with the BEAT platform. If not, see http://www.gnu.org/licenses/.          ..


.. _beat-core-backend-api:

============
Backend API
============

As it is currently setup, user code at toolchain blocks running on the platform
consumes data stored on disk and produces data which is stored on disk so that
subsequent code running on the following blocks can operate on the same
principles. This approach allows users to potentially configure experiments
with a hybrid set of algorithms that execute on different backends. Each
backend can be implemented in a different programming language and contain any
number of (pre-installed) libraries users can call on their algorithms.

The requirements for BEAT when reading/writing data are:

  * Ability to manage large and complex data
  * Portability to allow the use of heterogeneous environments

Based on our experience and on these requirements, we investigated
the use of HDF5. Unfortunately, HDF5 is not convenient to handle
structures such as arrays of variable-size elements, for instance,
array of strings.
Therefore, we decided to rely on our own binary format.


This document describes the binary formats in BEAT and the API required by BEAT to handle multiple backend implementations. The
package `beat.env.python27`_ provides the *reference* Python backend
implementation based on `Python 2.7`_.


Binary Format
-------------

Our binary format does *not* contains information about the format of the data
itself, and it is hence necessary to know this format a priori. This means that
the format cannot be inferred from the content of a file.

We rely on the following fundamental C-style formats:

  * int8
  * int16
  * int32
  * int64
  * uint8
  * uint16
  * uint32
  * uint64
  * float32
  * float64
  * complex64 (first real value, and then imaginary value)
  * complex128 (first real value, and then imaginary value)
  * bool (written as a byte)
  * string

An element of such a basic format is written in the C-style way, using
little-endian byte ordering.

Besides, dataformats always consist of arrays or dictionary of such fundamental
formats or compound formats.

An array of elements is saved as followed. First, the shape of the array is
saved using an *uint64* value for each dimension. Next, the elements of the
arrays are saved in C-style order.

A dictionary of elements is saved as followed. First, the key are ordered
according to the lexicographic ordering. Then, the values associated to each of
these keys are saved following this ordering.

The platform is data-driven and always processes chunks of data.  Therefore,
data are always written by chunks, each chunk being preceded by a text-formated
header indicated the start- and end- indices followed by the size (in bytes) of
the chunck.

Considering the Python backend of the platform, this binary format has been
successfully implemented using the ``struct``  module.


Filesystem Organization
-----------------------

At the filesystem level, each backend shall be organized so it is fully
contained in a single-rooted directory tree. The backend installer should not
make assumptions about the directory structure of the target operating systems,
except, possibly, for the use of stock files. For example:

.. code-block:: sh

   $ ls /path/to/beat.env.python27
   -rw-r--r-- 1 beat beat  2829 Jul 20 19:57 LICENSE
   -rw-r--r-- 1 beat beat  7268 Jul 20 19:57 Makefile
   -rw-r--r-- 1 beat beat  1852 Jul 20 19:57 README.md
   drwxr-xr-x 2 beat beat  4096 Jul 28 16:19 bin/
   drwxr-xr-x 2 beat beat  4096 Jul 28 16:19 usr/
   drwxr-xr-x 2 beat beat  4096 Jul 28 16:19 src/
   ...

There is a minimal set of required files in each environment:

1. ``Makefile``: A make file or equivalent script should be present to
   **fully** build the environment from scratch. This allows BEAT platform
   administrators to install the environment on a target machine.

2. ``bin/describe``: This is an executable that takes no arguments and
   describes the current environment, providing its name, version and a list of
   pre-installed libraries, toolboxes or any other information that may be
   relevant to users implementing algorithms for this backend. The output of
   the ``describe`` command should be a parseable JSON string. For example, our
   reference `beat.env.python27`_ environment returns the following for a call
   to ``bin/describe``:

   .. code-block:: json

      {
        "name": "Scientific Python 2.7",
        "version": "0.0.4",
        "os": [
          "Linux",
          "extatix03",
          "3.12.14-1-idiap-generic",
          "#20140313 SMP Thu Mar 13 15:12:40 CET 2014",
          "x86_64",
          ""
        ],
        "packages": {
          "beat.core": "0.9.4",
          "bob": "1.2.2",
          "matplotlib": "1.4.3",
          "numpy": "1.9.2",
          "oset": "0.1.3"
        }
      }

   Each pair of ``name`` and ``version`` for an environment must be unique so
   that platform users can uniquely select them.

3. ``bin/execute``: This is an executable that is called by the BEAT
   infrastructure to execute user code. The executable must be able to receive
   2 arguments that correspond to a I/O server address and  (temporary)
   directory containing the following files:

   .. code-block:: sh

      $ ls -1 /tmp/beat.A976xy1/
      configuration.json  #the configuration for the algorithm in JSON format
      prefix              #the prefix with algorithm/libraries/formats required

   Optional flags may be provided for administrative purposes, but will not be
   using for running user code. For example, the reference implementation of
   ``bin/execute`` responds this way when passed the ``-h`` optional flag:

   .. code-block:: sh

      $ /path/to/beat.env.python27/bin/execute -h
      Executes a single algorithm.

      usage:
        execute [--debug] <addr> <dir>
        execute (--help)


      arguments:
        <addr>  Address of the server for I/O requests
        <dir>   Directory containing all configuration required to run the user
                algorithm


      options:
        -h, --help   Shows this help message and exit
        -d, --debug  Runs executor in debugging mode


   You should **strongly** consider implemeting similar functionality on your
   backend to ease debugging in case of problems.


Further to those files, it is prudent to include:

1. ``README.rst``: a file containing installation and management instructions.
   It should preferrably be written using a markup language such as MarkDown
   (``.md`` extension) or reStructuredText (``.rst`` extension). By reading
   this file, it should be possible for a remote party with a working knowledge
   of the target operating system, to completely install the environment
   without external help.

   The README should also include contact points and, if possible, a
   bug-tracking link where users can submit bug/update requests.

2. ``LICENSE``: a file that describes the usage license for the backend.


Message Passing
---------------

The BEAT infrastructure communicates with the ``bin/execute`` process via `Zero
Message Queue`_ or ZMQ for short. ZMQ_ provides a portable bidirectional
communication layer between the BEAT infrastructure and the target backend,
with many `language bindings`_, including `python bindings`_.

The user process, which manages the data readout of a given algorithm, sends
commands back to the infrastructure for requesting data when needed.

.. code-block:: text

   "command"
   "argument1"
   "..."
   "argumentn"

Where ``command`` is the command name to be executed and ``argument*`` are the
corresponding arguments, sent using separate ``zmq.send()`` calls using the
multipart sending technique (as with ``zmq.SNDMORE``). In order to simplify
representation, we denote multi-message commands in a single line. So, the
command above will be represented in this document such as:

.. code-block:: text

   "command" "argument1" "..." "argumentn"

Commands may also exchange binary data. In such a case, we represent it in this
manual using ``<binary>``. The binary data format is the one defined by our
``BaseFormat`` class at the package ``beat.backend.python``.

The next diagram represents some possible states between the BEAT
infrastructure and the ``execute`` process in case of a successful execution:


.. _beat-core-backend-msc:
.. figure:: ./img/execute.*

   Message Sequence Chart between BEAT agents and user containers/algorithms


In the remainder of this section, we describe the various commands, which are
supported by this communication protocol.


Command: has-more-data (hmd)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command asks the infrastructure, whether there is more input data in a
given input or not. The format of this command is:

.. code-block:: text

   "hmd channel [name]"

where ``name`` refers to the input name and is optional.

The BEAT infrastructure will answer by writing the following into the input
pipe.

.. code-block:: text

   "boolean"

where `boolean` is a boolean indicating whether there is more data to process
or not. The values may be ``tru``, for True and ``fal``, for False.


Command: is-dataunit-done (idd)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command asks the infrastructure, whether the current chunk of data is
going to change or not, next time the current data index is increased. The
format of this command is:

.. code-block:: text

   "idd channel name"

The infrastructure will answer by writing the following into the input pipe.

.. code-block:: text

   "boolean"

where `boolean` is a boolean indicating whether there is more data to process
or not. The values may be ``tru``, for True and ``fal``, for False.


Command: next (nxt)
~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command asks the infrastructure to provide the next data on a given
channel and/or input. If no input ``name`` is provided, then the infrastructure
will return the data on all inputs of the given ``channel``. The format of this
command is:

.. code-block:: text

   "nxt channel [name]"

where ``name`` refers to the input name and is optional.

If an input ``name`` is provided, the infrastructure will answer by writing the
following into the input pipe:

.. code-block:: text

   "dat N name1 <bin1> .. nameN-1 <binN-1>"

where ``N`` refers to the number of data chunks in the reply, ``name`` is the
name of a given channel, and ``<bin>`` corresponds to the binary representation
of the data contents. The binary data format uses the same format for disk
storage used by the infrastructure so as to optimize I/O performance. Our
reference backend implementation at `beat.backend.python`_ contains
implementation details about the binary data format. As a backend developer,
you must ensure your backend is fully capable of **correctly** interpreting the
contents of the binary stream given the data formats associated with each input
and output of the algorithm.


Command: write (wrt)
~~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command asks the infrastructure to write data on a given output. The
format of this command is:

.. code-block:: text

   "wrt name <bin>"

The ``name`` identifies the output on which to write the data. The message
`<bin>` is the raw data to write on the output, pre-encoded in the same binary
data format as the one used for the input. The contents of the binary stream
sent to the infrastructure will be checked again before being written to disk.
In case of problems, a system error will be issued and the processing will
stop. It is the task of the backend developer to insure conformity in order to
avoid such errors.

The infrastructure acknowledges with:

.. code-block:: text

   "ack"

In case all is OK or with the keyword ``err``, if there was an error
interpreting the binary data back. In such cases, the UP is expected to stop
processing and issue a ``done`` command, waiting to be gracefully stopped by
the infrastructure. If the UP does not issue the ``done`` command next, the UP
is forcibly terminated with a operating system level signal.


Command: is-data-missing (idm)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command asks the infrastructure whether there is missing data on a given
output, by looking at the synchronization information. The format of this
command is:

.. code-block:: text

   "idm name"

The infrastructure will answer by writing the following into the input pipe.

.. code-block:: text

   "boolean"

where `boolean` is a boolean indicating whether there is more data to process
or not. The values may be ``tru``, for True and ``fal``, for False.


Command: output-is-connected (oic)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command asks the infrastructure, whether a given output is connected or
not. The format of this command is:

.. code-block:: text

   "ict name\n"

The infrastructure will answer by writing the following into the input pipe.

.. code-block:: text

   "boolean"

where `boolean` is a boolean indicating whether there is more data to process
or not. The values may be ``tru``, for True and ``fal``, for False.


Command: done (don)
~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command notifies the infrastructure that the execution of the user process
has completed (i.e. it will not read or write any further data).

.. code-block:: text

   "done float"

Where ``float`` is a valid floating point number that represents the time
wasted waiting for I/O on the user process. This number composes the statistics
for processes.

Once the UP has sent this command, the infrastructure will retrieve the
statistics (I/O, CPU and memory) and it will acknowlegde the UP, once this is
done with:

.. code-block:: text

   "ack"

At this point, the UP is expected to gracefully terminate.


Command: error (err)
~~~~~~~~~~~~~~~~~~~~

(User Process -> Infrastructure)


This command notifies the infrastructure that the execution of the user process
has err and will not request any further data. A message explaining the error
condition is attached.

.. code-block:: text

   "err type message"

Once the UP has sent this command, the infrastructure will retrieve the
statistics (I/O, CPU and memory) and it will acknowlegde the UP, once this is
done with:

.. code-block:: text

   "ack"

At this point, the UP is expected to gracefully terminate. The value for
``type`` maybe set to ``usr``, indicating the error occurred inside the user
code or anything else, indicating it was a system error (and must be reported
to system administrators). In this case, the user only gets a generic message
indicating a problem with the infrastructure was detected and that system
administrators were informed.


.. include:: links.rst

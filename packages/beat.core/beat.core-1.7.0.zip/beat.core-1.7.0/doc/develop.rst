.. vim: set fileencoding=utf-8 :

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

.. _beat-core-local-development:

===================
 Local Development
===================

Go through the following sequence of commands:


.. code-block:: sh

   $ git checkout https://gitlab.idiap.ch/bob/bob.admin
   $ #install miniconda (version 4.4 or above required)
   $ conda activate base
   $ cd beat.backend.python #cd into this package's sources
   $ ../bob.admin/conda/conda-bootstrap.py --overwrite --python=3.6 beat-core-dev
   $ conda activate beat-core-dev
   $ #n.b.: docker must be installed on your system (see next section)
   $ buildout -c develop.cfg

These commands should download and install all non-installed dependencies and
get you a fully operational test and development environment.


Docker
------

This package depends on Docker_ and may use it to run user algorithms in a
container with the required software stack. You must install the Docker_ engine
and make sure the user running tests has access to it.

In particular, this package controls memory and CPU utilisation of the
containers it launches. You must make sure to enable those functionalities on
your installation.


Docker Setup
============

Make sure you have the ``docker`` command available on your system. For certain
operating systems, it is necessary to install ``docker`` via an external
virtual machine (a.k.a. the *docker machine*). Follow the instructions at `the
docker website <https://docs.docker.com/engine/installation/>` before trying to
execute algorithms or experiments.

We use specific docker images to run user algorithms. Download the following
base images before you try to run tests or experiments on your computer::

  $ docker pull docker.idiap.ch/beat/beat.env.system.python:1.3.0
  $ docker pull docker.idiap.ch/beat/beat.env.db.examples:1.4.0
  $ docker pull docker.idiap.ch/beat/beat.env.client:2.0.0
  $ docker pull docker.idiap.ch/beat/beat.env.cxx:2.0.0

Optionally, also download the following images to be able to re-run experiments
downloaded from the BEAT platform (not required for unit testing). These docker
images corresponds to the python environment available on the platform. Keep in
mind that at the moment you cannot use different environments to run each block
when you are using BEAT locally (meaning not using the Docker executor)::

  $ docker pull docker.idiap.ch/beat/beat.env.python:1.1.0
  $ docker pull docker.idiap.ch/beat/beat.env.python:2.0.0
  $ docker pull docker.idiap.ch/beat/beat.env.db:1.4.0

Before pulling these images, you should check the registry as there might have
been new release (i.e. rX versions).

To run an experiment using docker you should specify the docker image when defining the experiment, then use the `--docker` flag when using `beat.cmdline`::

  $ beat experiment run --docker <experiment name>

You can find more information about running experiments locally using different executors in `here <https://www.idiap.ch/software/beat/docs/beat/docs/master/beat.cmdline/doc/experiments.html#how-to-run-an-experiment>`_.


Documentation
-------------

To build the documentation, just do:

.. code-block:: sh

   $ ./bin/sphinx-build doc sphinx



Testing
-------

After installation, it is possible to run our suite of unit tests. To do so,
use ``nose``:

.. code-block:: sh

   $ ./bin/nosetests -sv


.. note::

  Some of the tests for our command-line toolkit require a running BEAT
  platform web-server, with a compatible ``beat.core`` installed (preferably
  the same).  By default, these tests will be skipped. If you want to run
  them, you must setup a development web server and set the environment
  variable ``BEAT_CORE_TEST_PLATFORM`` to point to that address. For example::

   $ export BEAT_CORE_TEST_PLATFORM="http://example.com/platform/"
   $ ./bin/nosetests -sv

  .. warning::

    Do **NOT** run tests against a production web server.


If you want to skip slow tests (at least those pulling stuff from our servers)
or executing lengthy operations, just do::

  $ ./bin/nosetests -sv -a '!slow'


To measure the test coverage, do the following::

  $ ./bin/nosetests -sv --with-coverage --cover-package=beat.core


Our documentation is also interspersed with test units. You can run them using
sphinx::

    $ ./bin/sphinx -b doctest doc sphinx

Other Bits
==========

Profiling
---------

In order to profile the test code, try the following::

  $ ./bin/python -mcProfile -oprof.data ./bin/nosetests -sv ...

This will dump the profiling data at ``prof.data``. You can dump its contents
in different ways using another command::

  $ ./bin/python -mpstats prof.data

This will allow you to dump and print the profiling statistics as you may find
fit.


.. include:: links.rst

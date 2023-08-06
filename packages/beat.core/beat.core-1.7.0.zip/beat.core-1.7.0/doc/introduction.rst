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


.. _beat-core-introduction:

==============
 Introduction
==============

A typical BEAT experiment is composed of several building blocks. Datasets that provide data to the system, algorithms that handles the functions introduced by user, analyzers that is in charge of interpreting the output result and producing the appropriate results and figures, and toolchains that determines the data flow between the blocks from datasets to the final results. In addition, each block accepts specific data formats and the data is synchronized between blocks neatly without users need to interfere. These basic functionalities that are introduced in `Getting Started with BEAT`_ are all defined and managed by ``beat.core``. For example, as it is explained in `Algorithms`_, algorithm objects should be derived from the class
``Algorithm`` when using Python or in case of C++, they should be derived from ``IAlgorithmLagacy``, ``IAlgorithmSequential``, or ``IAlgorithmAutonomous`` depending of the algorithm type. All these parent classes are defined in ``beat.core`` package.

The rest of this document includes information about the backend api used to handle data through the BEAT ecosystem. For developers and advanced user there is information for local development of the package. 


.. include:: links.rst

#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2018 Idiap Research Institute, http://www.idiap.ch/           #
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
===========
environment
===========

Helper functions related to environment management
"""

import re
import logging


logger = logging.getLogger(__name__)


def enumerate_packages(host, environment_name):
    """
    Enumerate the packages installed in given environment.
    """

    packages = []

    if environment_name not in host.processing_environments:
        logger.error('Environment "{}" not found'.format(environment_name))
        return packages

    cmd = ["conda", "list"]
    container = host.create_container(environment_name, cmd)

    try:
        host.start(container)
    except RuntimeError:
        logger.exception("Failed to list packages")
        return packages

    status = host.wait(container)
    if status != 0:
        logger.error('Command error: {}'.format(status))
        return packages

    output = host.logs(container)

    package_lines = output.split("\n")

    for package_line in package_lines:
        information = re.split('\s+', package_line)
        if len(information) == 4:
            packages.append({
                'name': information[0],
                'version': information[1]
            })

    host.rm(container)
    return packages

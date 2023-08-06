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

import six
import numpy
import itertools

# Make sure we won't require an X11 connection
import matplotlib
matplotlib.use('Agg')

from matplotlib.figure import Figure
import matplotlib.pyplot as pyplot


class Plotter:

    def setup(self, parameters):

        self.xlabel = parameters['xlabel']
        self.xaxis_multiplier = parameters['xaxis_multiplier']
        self.xaxis_log = parameters['xaxis_log']
        self.ylabel = parameters['ylabel']
        self.yaxis_multiplier = parameters['yaxis_multiplier']
        self.yaxis_log = parameters['yaxis_log']
        self.title  = parameters['title']
        self.line_attributes = parameters['line_attributes'].split('&')
        self.legend = parameters['legend'].split('&')
        self.grid = parameters['grid']
        self.mimetype = parameters['mimetype']

        return True

    def process(self, inputs):

        # Creates the image to return
        fig = Figure()
        ax = fig.add_subplot(111)

        if not isinstance(inputs, (list,tuple)):
            inputs = [inputs]
        if not isinstance(self.legend, (list,tuple)):
            self.legend = [self.legend]
        if not isinstance(self.line_attributes, (list,tuple)):
            self.line_attributes = [self.line_attributes]

        try:
            Z = itertools.izip
        except AttributeError:
            Z = zip

        C = itertools.cycle

        for input, attributes, label  in Z(inputs, C(self.line_attributes), C(self.legend)):

            # Massages the input data
            final_data = numpy.array([(k.x, k.y) for k in input.data])
            x = final_data[:,0]
            y = final_data[:,1]
            x *= self.xaxis_multiplier
            y *= self.yaxis_multiplier

            args = (x, y)
            if attributes: args = args + (attributes,)
            kwargs = {}
            if label: kwargs['label'] = label

            # Plots
            ax.plot(*args, **kwargs)

        # Sets plot attributes
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.title)
        ax.grid(self.grid)
        if self.xaxis_log: ax.set_xscale('log')
        if self.yaxis_log: ax.set_yscale('log')
        if any(self.legend): ax.legend()

        # Returns the image
        if six.PY2:
            sio = six.StringIO()
        else:
            sio = six.BytesIO()

        if self.mimetype == 'image/png':
            pyplot.savefig(sio, format='png')
        elif self.mimetype == 'image/jpeg':
            pyplot.savefig(sio, format='jpeg')
        elif self.mimetype == 'application/pdf':
            from matplotlib.backends.backend_pdf import FigureCanvasPdf
            canvas = FigureCanvasPdf(fig)
            canvas.print_figure(sio)

        return sio.getvalue()

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


import imghdr

import numpy
import six

import nose.tools

from ..plotter import Plotter

from . import prefix

def test_default():

    p = Plotter(prefix, data=None)
    assert not p.valid


def test_scatter():

    p = Plotter(prefix, 'user/scatter/1')
    assert p.valid, '\n  * %s' % '\n  * '.join(p.errors)


def do_plot(mimetype):

    p = Plotter(prefix, 'user/scatter/1')
    assert p.valid

    runnable = p.runner()
    assert runnable.ready is False
    runnable.setup({
        'xlabel': 'Temperature in C',
        'ylabel': 'Icecream Sales in $',
        'title': 'Temperature versus icecream sales',
        'mimetype': mimetype
        })
    assert runnable.ready

    # now produce the plot
    data = p.dataformat.type(data=[
        # temperature in C against icecream sales day-by-day
        { 'x': 11.9, 'y': 185 },
        { 'x': 14.2, 'y': 215 },
        { 'x': 15.2, 'y': 332 },
        { 'x': 16.4, 'y': 325 },
        { 'x': 17.2, 'y': 408 },
        { 'x': 18.1, 'y': 421 },
        { 'x': 19.4, 'y': 412 },
        { 'x': 18.5, 'y': 406 },
        { 'x': 22.1, 'y': 522 },
        { 'x': 22.6, 'y': 445 },
        { 'x': 23.4, 'y': 544 },
        { 'x': 25.1, 'y': 614 },
        ])

    return runnable.process(data)


def test_plot_png():
    fig = do_plot('image/png')
    nose.tools.eq_(imghdr.what('test.png', fig), 'png')
    #with open('test.png', 'wb') as f: f.write(fig)


def test_plot_jpeg():
    fig = do_plot('image/jpeg')
    nose.tools.eq_(imghdr.what('test.jpg', fig), 'jpeg')
    #with open('test.jpg', 'wb') as f: f.write(fig)


def test_plot_pdf():
    fig = do_plot('application/pdf')

    if six.PY2:
        assert fig.startswith('%PDF')
    else:
        assert fig.startswith(b'%PDF')
    #with open('test.pdf', 'wb') as f: f.write(fig)

def test_plot_many_lines():

    p = Plotter(prefix, 'user/scatter/1')
    assert p.valid

    data1 = p.dataformat.type(data=[
        # temperature in C against icecream sales day-by-day
        { 'x': 0, 'y': 0 },
        { 'x': 1, 'y': 1 },
        { 'x': 2, 'y': 2 },
        { 'x': 3, 'y': 3 },
        { 'x': 4, 'y': 4 },
        { 'x': 5, 'y': 5 },
        { 'x': 6, 'y': 6 },
        { 'x': 7, 'y': 7 },
        { 'x': 8, 'y': 8 },
        { 'x': 9, 'y': 9 },
        ])

    data2 = p.dataformat.type(data=[
        # temperature in C against icecream sales day-by-day
        { 'x': 0, 'y': 1 },
        { 'x': 1, 'y': 3 },
        { 'x': 2, 'y': 5 },
        { 'x': 3, 'y': 7 },
        { 'x': 4, 'y': 9 },
        { 'x': 5, 'y': 11 },
        { 'x': 6, 'y': 13 },
        { 'x': 7, 'y': 15 },
        { 'x': 8, 'y': 17 },
        { 'x': 9, 'y': 19 },
        ])

    runnable = p.runner()
    assert runnable.ready is False
    runnable.setup({
        'title': 'Test plot',
        'grid': True,
        'legend': '&'.join(['Dashed red line with cross', 'Blue circles with line']),
        'line_attributes': '&'.join(['r+--', 'bo-']),
        'mimetype': 'image/png',
        })
    assert runnable.ready

    fig = runnable.process([data1, data2])
    nose.tools.eq_(imghdr.what('test.png', fig), 'png')
    #with open('test2.png', 'wb') as f: f.write(fig)

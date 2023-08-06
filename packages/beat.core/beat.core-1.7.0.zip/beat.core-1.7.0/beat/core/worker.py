#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2017 Idiap Research Institute, http://www.idiap.ch/           #
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
======
worker
======

Worker implementation
"""

import logging

import zmq
import socket
import simplejson

from .utils import send_multipart

logger = logging.getLogger(__name__)


class WorkerController(object):
    """Implements the controller that will handle the workers allocated.

    Constants:
        Status:
            :py:const:`READY`
            :py:const:`EXIT`
            :py:const:`DONE`
            :py:const:`JOB_ERROR`
            :py:const:`ERROR`
            :py:const:`CANCELLED`

        Commands:
            :py:const:`EXECUTE`
            :py:const:`CANCEL`
            :py:const:`ACK`
            :py:const:`SCHEDULER_SHUTDOWN`
    """


    # Status code
    READY = b'rdy'  #: The worker is ready to be used
    EXIT = b'ext'  #: The worker has exited
    DONE = b'don'  #: The worker as successfully finished its task
    JOB_ERROR = b'erj'  #: The worker failed to finish its task
    ERROR = b'err'  #: The worker encountered an error
    CANCELLED = b'cld'  #: The worker's task has been canceled

    # Commands
    EXECUTE = b'exe'  #: Execute the given job
    CANCEL = b'cnl'  #: Cancel the given job
    ACK = b'ack'  #: Acknowledge
    SCHEDULER_SHUTDOWN = b'shd'  #: Shutdown the scheduler


    class Callbacks(object):
        """Set of callbacks used when a worker is ready or went away"""

        def __init__(self):
            self.onWorkerReady = None
            self.onWorkerGone = None


    def __init__(self, address, port, callbacks=None):
        self.context = zmq.Context()
        self.context.setsockopt(socket.SO_REUSEADDR, 1)

        self.socket = self.context.socket(zmq.ROUTER)

        if port is not None:
            self.address = 'tcp://%s:%d' % (address, port)
            self.socket.bind(self.address)
        else:
            self.address = 'tcp://%s' % address
            port = self.socket.bind_to_random_port(self.address, min_port=50000)
            self.address += ':%d' % port

        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

        self.workers = []

        if callbacks is None:
            callbacks = {}

        self.callbacks = WorkerController.Callbacks()
        for k, v in callbacks.items():
            setattr(self.callbacks, k, v)


    def destroy(self):
        for worker in self.workers:
            parts = [
              worker,
              WorkerController.SCHEDULER_SHUTDOWN,
            ]
            send_multipart(self.socket, parts)

        self.workers = []

        self.poller.unregister(self.socket)
        self.poller = None

        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.socket = None

        self.context.destroy()
        self.context = None


    def execute(self, worker, job_id, configuration):
        """Executes the given job by the given worker using passed
        configuration

        Parameters:
            :param str worker: Address of the worker
            :param int job_id: Identifier of the job to execute
            :param dict configuration: Configuration for the job
        """

        parts = [
          worker,
          WorkerController.EXECUTE,
          b'%d' % job_id,
          simplejson.dumps(configuration)
        ]
        send_multipart(self.socket, parts)


    def cancel(self, worker, job_id):
        """Cancels the given job on the given worker

        Parameters:
            :param str worker: Address of the worker
            :param int job_id: Identifier of the job to execute
        """

        parts = [
          worker,
          WorkerController.CANCEL,
          b'%d' % job_id,
        ]
        send_multipart(self.socket, parts)


    def ack(self, worker):
        """Send acknowledge to worker

        Parameters:
            :param str worker: Address of the worker
        """

        parts = [
          worker,
          WorkerController.ACK
        ]
        send_multipart(self.socket, parts)


    def process(self, timeout=0):
        """Processing loop

        Gets processing information through ZeroMQ and acts accordingly.

        Parameters:
            :param int timeout: Maximum time allocate for processing

        Returns:
            tuple: Returns a tuple containing the worker address, job_id and
                corresponding data if any or None in case of error.
        """


        while True:
            socks = dict(self.poller.poll(timeout))
            if not (self.socket in socks) or (socks[self.socket] != zmq.POLLIN):
                return None

            (address, status, data) = self._receive()

            if status == WorkerController.READY:
                if address not in self.workers:
                    self.workers.append(address)
                    self.ack(address)

                    if self.callbacks.onWorkerReady is not None:
                        self.callbacks.onWorkerReady(address)

                    timeout = 0

            elif status == WorkerController.EXIT:
                try:
                    self.workers.remove(address)
                except:
                    logger.error('Unknown worker: %s' % address)
                    return None

                if self.callbacks.onWorkerGone is not None:
                    self.callbacks.onWorkerGone(address)

                timeout = 0

            elif status in [ WorkerController.DONE, WorkerController.JOB_ERROR,
                             WorkerController.CANCELLED ]:
                job_id = int(data[0])
                return (address, status, job_id, data[1:])

            elif (status == WorkerController.ERROR) and (len(data) >= 2):
                job_id = int(data[0])
                return (address, status, job_id, data[1:])

            else:
                job_id = None
                return (address, status, job_id, data)


    def _receive(self):
        parts = self.socket.recv_multipart()
        return parts[0], parts[1], parts[2:]

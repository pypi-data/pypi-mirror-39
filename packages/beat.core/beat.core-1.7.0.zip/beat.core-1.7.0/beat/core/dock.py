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
====
dock
====

Docker helper classes
"""


import os
import simplejson
import socket
import tempfile
import time
import docker
import subprocess as sp
import logging

from beat.core import stats

logger = logging.getLogger(__name__)


class Host(object):
    """An object of this class can connect to the docker host and resolve stuff
    """

    images_cache = {}


    def __init__(self, images_cache=None, raise_on_errors=True, discover=True):

        # Initialisations
        self.raise_on_errors = raise_on_errors
        self.images_cache_filename = images_cache
        self.base_url = None
        self.containers = []
        self.processing_environments = {}
        self.db_environments = {}

        # (If necessary) Load the known infos about the images
        if (self.images_cache_filename is not None) and os.path.exists(self.images_cache_filename):
            with open(self.images_cache_filename, 'r') as f:
                Host.images_cache = simplejson.load(f)

        # Discover the environments
        if discover:
            (self.processing_environments, self.db_environments) = self._discover_environments()

        # (If necessary) Save the known infos about the images
        if self.images_cache_filename is not None:
            with open(self.images_cache_filename, 'w') as f:
                simplejson.dump(Host.images_cache, f, indent=4)


    def __contains__(self, key):
        return (key in self.processing_environments) or (key in self.db_environments)


    def __str__(self):
        s = 'Docker host'

        if self.base_url is not None:
            s += ' (%s)' % self.base_url

        return s


    def env2docker(self, key):
        """Returns a nice docker image name given a BEAT environment key"""

        attrs = self.processing_environments[key]
        return attrs['image']


    def db2docker(self, db_names):
        """Returns a nice docker image name given a database name"""

        def _all_in(db_names, databases):
            return len([ x for x in db_names if x in databases ]) == len(db_names)

        attrs = [ x for x in self.db_environments.values() if _all_in(db_names, x['databases']) ][0]

        return attrs['image']


    def teardown(self):
        for container in self.containers:
            self.rm(container)

        self.containers = []


    def __exit__(self, *exc):
        self.teardown()


    def full_environment_name(self, name):
        try:
            return list(filter(lambda x: x.startswith(name  + ' ('), self.processing_environments.keys()))[0]
        except:
            try:
                return list(filter(lambda x: x.startswith(name  + ' ('), self.db_environments.keys()))[0]
            except:
                return None

    @property
    def ip(self):
        """The IP address of the docker host"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connecting to a UDP address doesn't send packets
        return s.getsockname()[0]


    def _discover_environments(self):
        """Returns a dictionary containing information about docker environments

        Raises:

          RuntimeError: if you set ``raise_on_errors`` in the constructor and I
            found environments that override each other for their description
            keys (``<name>(<version>)``), which should be unique.

        """

        def _describe(image):
            """Tries to run the "describe" app on the image, collect results"""

            if image in Host.images_cache:
                return Host.images_cache[image]

            cmd = [
                'docker',
                'run',
                '--rm=true',
                image,
                'describe'
            ]

            (status, stdout, stderr) = self._exec(cmd)

            if status == 0:
                try:
                    infos = simplejson.loads(stdout)
                    Host.images_cache[image] = infos
                    return infos
                except Exception as e:
                    logger.warn("Ignoring potential environment at `%s' since " \
                            "`describe' output cannot be parsed: %s", image, str(e))
            else:
                logger.warn("Execution failed with status {}: \n"
                            "stdout: '{}'\n"
                            "stderr: '{}'".format(status, stdout, stderr))
            return {}


        def _must_replace(image, environments, key):
            # this check avoids we do a new environment and, by mistake,
            # override it with a previous version or the contrary.
            if self.raise_on_errors:
                raise RuntimeError("Environments at '%s' and '%s' have the " \
                        "same name ('%s'). Distinct environments must be " \
                        "uniquely named. Fix this and re-start." % \
                        (image, environments[key]['image'], key))

            new_version = None
            previous_version = None

            parts = image.split('/')
            if len(parts) > 1:
                parts = parts[-1].split(':')
                if len(parts) > 1:
                    new_version = parts[-1]

            parts = environments[key]['image'].split('/')
            if len(parts) > 1:
                parts = parts[-1].split(':')
                if len(parts) > 1:
                    previous_version = parts[-1]

            replacement = False
            keep = False

            if (new_version is not None) and (previous_version is not None):
                if new_version == 'latest':
                    replacement = True
                elif previous_version == 'latest':
                    keep = True
                else:
                    try:
                        new_version = tuple([ int(x) for x in new_version.split('.') ])

                        try:
                            previous_version = tuple([ int(x) for x in previous_version.split('.') ])

                            if new_version > previous_version:
                                replacement = True
                            else:
                                keep = True
                        except:
                            replacement = True

                    except:
                        keep = True

            elif new_version is not None:
                replacement = True
            elif previous_version is not None:
                keep = True

            if replacement:
                logger.debug("Overriding **existing** environment '%s' in image '%s'", key, environments[key]['image'])
            elif keep:
                logger.debug("Environment '%s' already existing in image '%s', we'll keep it", key, environments[key]['image'])
                return False
            else:
                logger.warn("Overriding **existing** environment '%s' image " \
                        "with '%s'. To avoid this warning make " \
                        "sure your docker images do not contain environments " \
                        "with the same names", key, environments[key]['image'])

            return True


        environments = {}
        db_environments = {}

        cmd = [
            'docker',
            'images',
            '--format',
            '{{.Repository}}:{{.Tag}}',
        ]

        (status, stdout, stderr) = self._exec(cmd)

        if status != 0:
            logger.error("Failed to retrieve the list of docker images, reason:\n\n%s", stderr)
            return (environments, db_environments)

        images = [ x for x in stdout.split('\n') if x.find('beat.env.') >= 0 ]


        for image in images:
            # Call the "describe" application on each existing image
            description = _describe(image)
            if not description:
                continue

            key = description['name'] + ' (' + description['version'] + ')'

            if 'databases' in description:
                if (key in db_environments) and not _must_replace(image, db_environments, key):
                    continue

                db_environments[key] = description
                db_environments[key]['image'] = image
            else:
                if (key in environments) and not _must_replace(image, environments, key):
                    continue

                environments[key] = description
                environments[key]['image'] = image

            logger.info("Registered '%s' -> '%s'", key, image)


        logger.debug("Found %d environments and %d database environments", len(environments),
                     len(db_environments))

        return (environments, db_environments)


    def create_container(self, image, command):

        if image in self:  # Replace by a real image name
            image = self.env2docker(image)

        return Container(image, command)


    def start(self, container, virtual_memory_in_megabytes=0, max_cpu_percent=0):
        """Starts the execution of a container

        The process will be run in the background, and its standard output and
        standard error will be read after it finishes, into a limited size
        circular buffer.


        Parameters:

          container (:py:class:`Container`): The container.

          virtual_memory_in_megabytes (:py:class:`int`, Optional): The maximum
            amount of memory the user process can consume on the host. If not
            specified, a memory limit is not set.

          max_cpu_percent (:py:class:`float`, Optional): The maximum amount of
            CPU the user process may consume on the host. The value ``100``
            equals to using 100% of a single core. If not specified, then a CPU
            limitation is not put in place.
        """

        cmd = [
            'docker',
            'run',
            '-tid',
        ]

        network = container.network
        if network:
            cmd.append(network)

        user = container.user
        if user:
            cmd.append(user)

        name = container.name
        if name:
            cmd.append(name)

        workdir = container.workdir
        if workdir:
            cmd.append(workdir)

        entrypoint = container.entrypoint
        if entrypoint:
            cmd.append(entrypoint)

        if container.image in Host.images_cache:
            image_infos = Host.images_cache[container.image]
            if ('capabilities' in image_infos) and ('gpu' in image_infos['capabilities']):
                cmd.append('--runtime=nvidia')


        if virtual_memory_in_megabytes:
            # For this to work properly, memory swap limitation has to be
            # enabled on the kernel. This typically goes by setting
            # "cgroup_enable=memory" as a boot parameter to kernels which are
            # compiled with this support.
            # More info: https://docs.docker.com/engine/installation/linux/ubuntulinux/#/enable-memory-and-swap-accounting
            logger.debug('Setting maximum memory to %dMB' % virtual_memory_in_megabytes)
            cmd.append('--memory=%dm' % virtual_memory_in_megabytes)
            cmd.append('--memory-swap=%dm' % virtual_memory_in_megabytes)

        if max_cpu_percent:
            # The period corresponds to the scheduling interval for the CFS in
            # Linux. The quota corresponds to a fraction or a multiple of the
            # period, the container will get. A quota that is 2x the period
            # gets the container up to 200% cpu time (2 cores). If the quota is
            # 0.5x the period, the container gets up to 50% the cpu time. Each
            # core represents 100%. A system with 2 cores has 200% computing
            # power.
            #
            # More info:
            # https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt
            #
            # For this to work properly, CPU bandwidth provisioning for the
            # Linux CFS must be enabled on the kernel. More info on how to do
            # it: http://www.blaess.fr/christophe/2012/01/07/linux-3-2-cfs-cpu-bandwidth-english-version/
            #
            # If your system is running on a virtual machine, having more cores
            # available to docker engine normally translates to more precise
            # scheduling.
            period = 100000  # microseconds
            quota = max_cpu_percent / 100.0

            logger.debug('Setting CPU quota to %d%%' % max_cpu_percent)

            cmd.append('--cpu-period=%d' % period)
            cmd.append('--cpu-quota=%d' % int(quota * period))

        # Mount the volumes
        cmd.extend(container.volumes)

        # Expose the ports
        cmd.extend(container.ports)

        # Environment variables
        cmd.extend(container.environment_variables)

        cmd.append(container.image)
        cmd.extend(container.command)


        # Instantiate the container
        logger.debug("Creation and start of a container: image=%s, command=\"%s\"",
                     container.image, ' '.join(container.command))

        logger.debug("Docker command: %s", ' '.join(cmd))

        (status, stdout, stderr) = self._exec(cmd)

        if stdout != '':
            container.id = stdout.replace('\n', '')
            self.containers.append(container)

        if status != 0:
            message = "Failed to create the container, reason:\n\n%s" % stderr
            logger.error(message)

            if container.id is not None:
                self.rm(container)

            raise RuntimeError(message)

        logger.debug("Container ID: '%s'", container.id)


    def wait(self, container, timeout=None):
        """Wait for the container to finish its job

        Parameters:

          timeout (:py:class:`float`, Optional): A timeout in seconds to wait
            for the user process to finish. If a timeout value is not given,
            waits forever.
        """

        (status, stdout, stderr) = self._exec(['docker', 'wait', container.id],
                                              timeout=timeout)
        if status != 0:
            return None

        return int(stdout)


    def status(self, container):
        """Checks the status of a given container"""

        logger.debug("Inspect container %s", container.id)

        (status, stdout, stderr) = self._exec(['docker', 'inspect', container.id])
        if status != 0:
            return None

        try:
            return simplejson.loads(stdout)[0]['State']['Status']
        except:
            return None


    def logs(self, container):
        """Returns the logs of a container"""

        (status, stdout, stderr) = self._exec(['docker', 'logs', container.id])
        if status != 0:
            return ''

        return stdout.replace('\r\n', '\n')


    def statistics(self, container):
        """Returns the statistics about a container"""

        client = docker.APIClient()

        data = client.stats(container.id, stream=False)

        # If CPU statistics can't be retrieved
        if 'system_cpu_usage' not in data['cpu_stats']:
            data['cpu_stats'] = dict(data['precpu_stats'])

        # If memory statistics can't be retrieved
        if len(data['memory_stats']) == 0:
            data['memory_stats'] = dict(
                limit=0,
                max_usage=0
            )

        previous_cpu = container._stats['cpu_stats'] if container._stats else None

        # merge statistics
        retval = dict(
            cpu=stats.cpu_statistics(previous_cpu, data['cpu_stats']),
            memory=stats.memory_statistics(data['memory_stats']),
        )

        container._stats = data

        return retval


    def rm(self, container):
        """Removes a given container. If it is not done, kill it first"""

        if container.id is None:
            return

        status = self.status(container)

        if status not in ('created', 'exited'):
            logger.warn("Killing container '%s' which is on state '%s'", container.id, status)
            self._exec(['docker', 'container', 'stop', container.id])

        logger.debug("Remove container %s", container.id)
        (status, stdout, stderr) = self._exec(['docker', 'rm', container.id])

        self.containers.remove(container)

        container.id = None


    def kill(self, container):
        """Stop a container"""

        if self.status(container) == 'running':
            self._exec(['docker', 'kill', container.id])


    def run(self, image, command):
        """Runs a command and retrieves its status and output"""

        container = None
        try:
            container = self.create_container(image, command)
            self.start(container)
            status = self.wait(container)
            output = self.logs(container)

        except Exception as e:
            return 1, None

        finally:
            if container is not None:
                self.rm(container)

        return status, output


    def get_ipaddress(self, container):
        """ Returns the ip address of the given container"""

        cmd = [
            'docker',
            'inspect',
            '--format',
            '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}',
            container.id
        ]

        (status, stdout, stderr) = self._exec(cmd)

        if status != 0:
            logger.error("Failed to retrieve the ip address of the container, reason:\n\n%s", stderr)
            return None

        return stdout.replace('\n', '')

    def _exec(self, command, timeout=None):
        process_stdout = tempfile.NamedTemporaryFile()
        process_stderr = tempfile.NamedTemporaryFile()

        def _read_streams():
            with open(process_stdout.name, 'r') as f:
                stdout = f.read()

            with open(process_stderr.name, 'r') as f:
                stderr = f.read()

            return (stdout, stderr)

        try:
            process = sp.Popen(command, stdout=process_stdout, stderr=process_stderr)
        except IOError as e:
            if self.raise_on_errors:
                raise

            logger.error("Docker can not be found")
            return (-1, None, e)

        if timeout is None:
            process.communicate()
        else:
            start = time.time()
            while process.poll() is None:
                time.sleep(0.1)
                if time.time() - start >= timeout:
                    process.kill()
                    (stdout, stderr) = _read_streams()
                    return (None, stdout, stderr)

        (stdout, stderr) = _read_streams()

        return (process.returncode, stdout, stderr)


# ----------------------------------------------------------


class Container:
    """This class represents a Docker container with its set of parameters

    Parameters:
        :param str image: Name of the image to use to build the container

        :param str command: Command to execute in the container.
    """


    def __init__(self, image, command):
        self.image = image
        self.command = command
        self.network_name = None
        self.uid = None
        self.id = None
        self._volumes = {}
        self._ports = {}
        self._environment_variables = {}
        self._stats = None
        self._name = None
        self._workdir = None
        self._entrypoint = None


    def set_name(self, name):
        """ Set the name to be used by the container in place of the docker
        auto generated one.
        """
        self._name = name


    def set_workdir(self, workdir):
        """ Set the work folder to be used by the container
        """
        self._workdir = workdir


    def set_entrypoint(self, entrypoint):
        """ Set the entry point to be used by the container
        """
        self._entrypoint = entrypoint


    def add_volume(self, path, mount_path, read_only=True):
        """Add a volume to be mounted on the container

        Parameters:
            :param str path: Source path of the volume on disk

            :param str mount_path: Path of the volume in the container

            :param boolean read_only: Whether the volume will be read only
        """

        self._volumes[path] = {
          'bind': mount_path,
          'mode': 'ro' if read_only else 'rw',
        }


    def add_port(self, container_port, host_port, host_address=None):
        """Add a port binding

        Parameters:
            :param int container_port: Port to bind from the container

            :param int host_port: Port to bind to on the host

            :param str host_address: Address of the host
        """

        if host_address is not None:
            value = (host_address, host_port)
        else:
            value = [host_port]

        self._ports[container_port] = value

    def add_environment_variable(self, name, value):
        """Add an environment variable

        Parameters:
            :param str name: Name of the variable

            :param str value: Content of the variable
        """

        self._environment_variables[name] = value


    def reset_ports(self):
        """Empty the port bindings"""

        self._ports = {}


    @property
    def name(self):
        name = ''
        if self._name:
            name = '--name=%s' % self._name
        return name


    @property
    def workdir(self):
        workdir = ''
        if self._workdir:
            workdir = '--workdir=%s' % self._workdir
        return workdir


    @property
    def entrypoint(self):
        entrypoint = ''
        if self._entrypoint:
            entrypoint = '--entrypoint=%s' % self._entrypoint
        return entrypoint


    @property
    def volumes(self):
        """Returns the volumes of this container in a suitable form to build
        a command to start the container.
        """

        volumes = []
        for k, v in self._volumes.items():
            if k.startswith('nfs://'):
                addr, src = k[6:].split(':')
                volumes.append('--mount=type=volume,'
                                       'dst={dst},'
                                       'volume-driver=local,'
                                       'volume-opt=type=nfs,'
                                       'volume-opt=device=:{src},'
                                       'volume-opt=o=addr={addr}'.format(dst=v['bind'], src=src, addr=addr))
            else:
                if k.startswith('file://'):
                    k = k[6:]
                volumes.append('--volume=%s:%s:%s' % (k, v['bind'], v['mode']))
        return volumes


    @property
    def ports(self):
        """Returns the ports of this container in a suitable form to build
        a command to start the container.
        """

        ports = []
        for k, v in self._ports.items():
            ports.append('-p')
            if isinstance(v, tuple):
                ports.append('%s:%d:%d' % (v[0], v[1], k))
            else:
                ports.append('%d:%d' % (v[0], k))
        return ports


    @property
    def environment_variables(self):
        """Returns the environment variables to set on this container.
        """

        environment_variables = []
        for k, v in self._environment_variables.items():
            environment_variables.append('--env={}={}'.format(k, v))
        return environment_variables


    @property
    def network(self):
        network = ''
        if self.network_name:
            network = '--network=' + self.network_name
        return network

    @property
    def user(self):
        user = ''
        if self.uid:
            user = '--user={0}:{0}'.format(self.uid)
        return user


    @property
    def command_line(self):
        """Returns the complete docker command to start the container and
        execute the specified command.

        Returns:
            str: Command to execute
        """

        cmd = "docker run -ti --rm=true "
        cmd += "%s " % self.network
        cmd += "%s " % self.user
        cmd += ' '.join(self.volumes)
        cmd += ' '.join(self.ports)
        cmd += ' '.join(self.environment_variables)
        cmd += "%s " % self.name
        cmd += "%s " % self.workdir
        cmd += "%s " % self.entrypoint

        cmd += "%s " % self.image

        cmd += '"%s"' % ' '.join(self.command)

        return cmd

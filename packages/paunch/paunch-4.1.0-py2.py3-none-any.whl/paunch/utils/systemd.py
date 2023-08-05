# Copyright 2018 Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import subprocess

from paunch.utils import common


def service_create(container, cconfig, sysdir='/etc/systemd/system/',
                   log=None):
    """Create a service in systemd

    :param container: container name
    :type container: String

    :param cconfig: container configuration
    :type cconfig: Dictionary

    :param sysdir: systemd unit files directory
    :type sysdir: string

    :param log: optional pre-defined logger for messages
    :type log: logging.RootLogger
    """
    log = log or common.configure_logging(__name__)

    wants = " ".join(str(x) + '.service' for x in
                              cconfig.get('depends_on', []))

    restart = cconfig.get('restart', 'always')
    stop_grace_period = cconfig.get('stop_grace_period', '10')
    # SystemD doesn't have the equivalent of docker unless-stopped.
    # Let's force 'always' so containers aren't restarted when stopped by
    # systemd, but restarted when in failure. Also this code is only for
    # podman now, so nothing changed for Docker deployments.
    if restart == 'unless-stopped':
        restart = 'always'

    sysd_unit_f = sysdir + container + '.service'
    log.debug('Creating systemd unit file: %s' % sysd_unit_f)
    s_config = {
        'name': container,
        'wants': wants,
        'restart': restart,
        'stop_grace_period': stop_grace_period,
    }
    with open(sysd_unit_f, 'w') as unit_file:
        os.chmod(unit_file.name, 0o644)
        unit_file.write("""[Unit]
Description=%(name)s container
After=paunch-container-shutdown.service
Wants=%(wants)s
[Service]
Restart=%(restart)s
ExecStart=/usr/bin/podman start -a %(name)s
ExecStop=/usr/bin/podman stop -t %(stop_grace_period)s %(name)s
KillMode=process
[Install]
WantedBy=multi-user.target""" % s_config)
    subprocess.call(['systemctl', 'enable', '--now', container])
    subprocess.call(['systemctl', 'daemon-reload'])


def service_delete(container, log=None):
    """Delete a service in systemd

    :param container: container name
    :type container: String

    :param log: optional pre-defined logger for messages
    :type log: logging.RootLogger
    """
    log = log or common.configure_logging(__name__)

    sysd_unit_f = '/etc/systemd/system/' + container + '.service'
    if os.path.isfile(sysd_unit_f):
        log.debug('Stopping and disabling systemd service for %s' % container)
        subprocess.call(['systemctl', 'stop', container])
        subprocess.call(['systemctl', 'disable', container])
        log.debug('Removing systemd unit file %s' % sysd_unit_f)
        os.remove(sysd_unit_f)
        subprocess.call(['systemctl', 'daemon-reload'])
    else:
        log.warning('No systemd unit file was found for %s' % container)

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

import mock
import os
import tempfile

from paunch.tests import base
from paunch.utils import systemd


class TestUtilsSystemd(base.TestCase):

    @mock.patch('subprocess.call', autospec=True)
    @mock.patch('os.chmod')
    def test_service_create(self, mock_chmod, mock_subprocess_call):
        container = 'my_app'
        cconfig = {'depends_on': ['something'], 'restart': 'unless-stopped',
                   'stop_grace_period': '15'}
        tempdir = tempfile.mkdtemp()
        systemd.service_create(container, cconfig, tempdir)

        sysd_unit_f = tempdir + container + '.service'
        unit = open(sysd_unit_f, 'rt').read()
        self.assertIn('Wants=something.service', unit)
        self.assertIn('Restart=always', unit)
        self.assertIn('ExecStop=/usr/bin/podman stop -t 15 my_app', unit)
        mock_chmod.assert_has_calls([mock.call(sysd_unit_f, 420)])

        mock_subprocess_call.assert_has_calls([
            mock.call(['systemctl', 'enable', '--now', container]),
            mock.call(['systemctl', 'daemon-reload']),
        ])

        os.rmdir(tempdir)

    @mock.patch('os.remove', autospec=True)
    @mock.patch('os.path.isfile', autospec=True)
    @mock.patch('subprocess.call', autospec=True)
    def test_service_delete(self, mock_subprocess_call, mock_isfile, mock_rm):
        mock_isfile.return_value = True
        container = 'my_app'
        systemd.service_delete(container)
        mock_subprocess_call.assert_has_calls([
            mock.call(['systemctl', 'stop', container]),
            mock.call(['systemctl', 'disable', container]),
            mock.call(['systemctl', 'daemon-reload']),
        ])

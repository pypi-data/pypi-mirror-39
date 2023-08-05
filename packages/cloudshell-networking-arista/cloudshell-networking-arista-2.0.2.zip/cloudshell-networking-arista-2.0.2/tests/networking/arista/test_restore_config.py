from mock import patch, MagicMock

from cloudshell.networking.arista.runners.arista_configuration_runner import \
    AristaConfigurationRunner
from tests.networking.arista.base_test import BaseAristaTestCase, CliEmulator, Command, \
    ENABLE_PROMPT


@patch('cloudshell.cli.session.ssh_session.paramiko', MagicMock())
@patch('cloudshell.cli.session.ssh_session.SSHSession._clear_buffer', MagicMock(return_value=''))
class TestRestoreConfig(BaseAristaTestCase):
    def _setUp(self, attrs=None):
        super(TestRestoreConfig, self)._setUp(attrs)
        self.runner = AristaConfigurationRunner(
            self.logger, self.resource_config, self.api, self.cli_handler)

    def setUp(self):
        self._setUp({
            'Backup Location': 'Test-running-081018-215424',
            'Backup Type': AristaConfigurationRunner.DEFAULT_FILE_SYSTEM,
        })

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_restore_running_override(self, send_mock, recv_mock):
        self._setUp()
        host = '192.168.122.10'
        file_name = 'Test-running-100418-163658'
        remote_path = 'ftp://{}/{}'.format(host, file_name)
        configuration_type = 'running'

        emu = CliEmulator([
            Command('configure replace {}'.format(remote_path), ENABLE_PROMPT)
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.restore(remote_path, configuration_type)

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_restore_running_append(self, send_mock, recv_mock):
        self._setUp()
        host = '192.168.122.10'
        file_name = 'Test-running-100418-163658'
        remote_path = 'ftp://{}/{}'.format(host, file_name)
        configuration_type = 'running'

        emu = CliEmulator([
            Command(
                'copy {} {}-config'.format(remote_path, configuration_type),
                'Copy completed successfully.\n'
                '{}'.format(ENABLE_PROMPT),
            )
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.restore(remote_path, configuration_type, 'append')

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_restore_startup(self, send_mock, recv_mock):
        self._setUp()
        host = '192.168.122.10'
        file_name = 'Test-startup-100418-163658'
        remote_path = 'ftp://{}/{}'.format(host, file_name)
        configuration_type = 'startup'

        emu = CliEmulator([
            Command(
                'copy {} {}-config'.format(remote_path, configuration_type),
                'Copy completed successfully.\n'
                '{}'.format(ENABLE_PROMPT),
            )
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.restore(remote_path, configuration_type)

        emu.check_calls()

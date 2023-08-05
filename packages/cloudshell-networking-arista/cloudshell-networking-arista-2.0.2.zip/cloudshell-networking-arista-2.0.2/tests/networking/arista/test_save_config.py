from mock import patch, MagicMock

from cloudshell.networking.arista.runners.arista_configuration_runner import \
    AristaConfigurationRunner
from tests.networking.arista.base_test import BaseAristaTestCase, CliEmulator, Command, \
    ENABLE_PROMPT, VRF_PROMPT


@patch('cloudshell.cli.session.ssh_session.paramiko', MagicMock())
@patch('cloudshell.cli.session.ssh_session.SSHSession._clear_buffer', MagicMock(return_value=''))
class TestSaveConfig(BaseAristaTestCase):

    def _setUp(self, attrs=None):
        super(TestSaveConfig, self)._setUp(attrs)
        self.runner = AristaConfigurationRunner(
            self.logger, self.resource_config, self.api, self.cli_handler)

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_save_anonymous(self, send_mock, recv_mock):
        self._setUp()
        host = '192.168.122.10'
        ftp_path = 'ftp://{}'.format(host)
        configuration_type = 'running'

        emu = CliEmulator([
            Command(
                '^copy {0} {1}/Arista-{0}-\d+-\d+$'.format(configuration_type, ftp_path),
                'Copy complete\n'
                '{}'.format(ENABLE_PROMPT),
                regexp=True,
            ),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.save(ftp_path, configuration_type)

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_save_ftp(self, send_mock, recv_mock):
        self._setUp()
        user = 'user'
        password = 'password'
        host = '192.168.122.10'
        ftp_path = 'ftp://{}:{}@{}'.format(user, password, host)
        configuration_type = 'running'

        emu = CliEmulator([
            Command(
                '^copy {0} {1}/Arista-{0}-\d+-\d+$'.format(configuration_type, ftp_path),
                'Copy complete\n'
                '{}'.format(ENABLE_PROMPT),
                regexp=True
            )
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.save(ftp_path, configuration_type)

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_save_with_vrf(self, send_mock, recv_mock):
        vrf_name = 'vrf_name'
        self._setUp({'VRF Management Name': vrf_name})
        user = 'user'
        password = 'password'
        host = '192.168.122.10'
        ftp_path = 'ftp://{}:{}@{}'.format(user, password, host)
        configuration_type = 'running'

        emu = CliEmulator([
            Command(
                'routing-context vrf {}'.format(vrf_name),
                VRF_PROMPT.format(vrf_name=vrf_name)
            ),
            Command(
                '^copy {0} {1}/Arista-{0}-\d+-\d+$'.format(configuration_type, ftp_path),
                'Copy complete\n'
                '{}'.format(VRF_PROMPT.format(vrf_name=vrf_name)),
                regexp=True
            ),
            Command('routing-context vrf default', ENABLE_PROMPT),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.save(ftp_path, configuration_type)

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_save_startup(self, send_mock, recv_mock):
        self._setUp()
        user = 'user'
        password = 'password'
        host = '192.168.122.10'
        ftp_path = 'ftp://{}:{}@{}'.format(user, password, host)
        configuration_type = 'startup'

        emu = CliEmulator([
            Command(
                '^copy {0} {1}/Arista-{0}-\d+-\d+$'.format(configuration_type, ftp_path),
                'Copy complete\n'
                '{}'.format(ENABLE_PROMPT),
                regexp=True
            )
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.save(ftp_path, configuration_type)

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_fail_to_save(self, send_mock, recv_mock):
        self._setUp()
        host = '192.168.122.10'
        ftp_path = 'ftp://{}'.format(host)
        configuration_type = 'running'

        emu = CliEmulator([
            Command(
                '^copy {0} {1}/Arista-{0}-\d+-\d+$'.format(configuration_type, ftp_path),
                'Error\n'
                '{}'.format(ENABLE_PROMPT),
                regexp=True,
            )
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.assertRaisesRegexp(
            Exception,
            'Copy Command failed',
            self.runner.save,
            ftp_path,
            configuration_type,
        )

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_save_to_device(self, send_mock, recv_mock):
        self._setUp({
            'Backup Location': '',
            'Backup Type': AristaConfigurationRunner.DEFAULT_FILE_SYSTEM,
        })
        path = ''
        configuration_type = 'running'

        emu = CliEmulator([
            Command(
                r'copy {0} flash:/Arista-{0}-\d+-\d+'.format(configuration_type),
                'Copy complete\n'
                '{}'.format(ENABLE_PROMPT),
                regexp=True,
            )
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.save(path, configuration_type)

        emu.check_calls()

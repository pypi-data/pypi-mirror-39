from mock import patch, MagicMock

from cloudshell.networking.arista.runners.arista_autoload_runner import AristaAutoloadRunner
from cloudshell.networking.arista.snmp.arista_snmp_handler import AristaSnmpHandler
from tests.networking.arista.base_test import BaseAristaTestCase, CliEmulator, Command, \
    ENABLE_PROMPT, CONFIG_PROMPT


@patch('cloudshell.devices.snmp_handler.QualiSnmp', MagicMock())
@patch('cloudshell.networking.arista.flows.arista_autoload_flow.AristaSNMPAutoload', MagicMock())
@patch('cloudshell.cli.session.ssh_session.paramiko', MagicMock())
@patch('cloudshell.cli.session.ssh_session.SSHSession._clear_buffer', MagicMock(return_value=''))
class TestEnableDisableSnmp(BaseAristaTestCase):

    def _setUp(self, attrs=None):
        attrs = attrs or {}
        snmp_attrs = {
            'SNMP Version': 'v2c',
            'SNMP Read Community': 'public',
            'SNMP V3 User': 'quali_user',
            'SNMP V3 Password': 'password',
            'SNMP V3 Private Key': 'private_key',
            'SNMP V3 Authentication Protocol': 'No Authentication Protocol',
            'SNMP V3 Privacy Protocol': 'No Privacy Protocol',
            'Enable SNMP': 'True',
            'Disable SNMP': 'False',
        }
        snmp_attrs.update(attrs)
        super(TestEnableDisableSnmp, self)._setUp(snmp_attrs)
        self.snmp_handler = AristaSnmpHandler(
            self.resource_config, self.logger, self.api, self.cli_handler)
        self.runner = AristaAutoloadRunner(self.resource_config, self.logger, self.snmp_handler)

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v2(self, send_mock, recv_mock):
        self._setUp()

        emu = CliEmulator([
            Command('configure terminal', CONFIG_PROMPT),
            Command('show snmp community', CONFIG_PROMPT),
            Command('snmp-server community public ro', CONFIG_PROMPT),
            Command(
                'show snmp community',
                'Community name: public\n'
                'Community access: read-only\n'
                '{}'.format(CONFIG_PROMPT),
            ),
            Command('end', ENABLE_PROMPT),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v2_with_vrf(self, send_mock, recv_mock):
        self._setUp({
            'VRF Management Name': 'management',
        })

        emu = CliEmulator([
            Command('configure terminal', CONFIG_PROMPT),
            Command(
                'show snmp',
                '0 SNMP packets input\n'
                '    0 Bad SNMP version errors\n'
                '    0 Unknown community name\n'
                '    0 Illegal operation for community name supplied\n'
                '    0 Encoding errors\n'
                '    0 Number of requested variables\n'
                '    0 Number of altered variables\n'
                '    0 Get-request PDUs\n'
                '    0 Get-next PDUs\n'
                '    0 Set-request PDUs\n'
                '...\n'
                'SNMP logging: disabled\n'
                'SNMP agent enabled in VRFs: default\n'
                '{}'.format(CONFIG_PROMPT),
            ),
            Command('snmp-server vrf management', CONFIG_PROMPT),
            Command('show snmp community', CONFIG_PROMPT),
            Command('snmp-server community public ro', CONFIG_PROMPT),
            Command(
                'show snmp community',
                'Community name: public\n'
                'Community access: read-only\n'
                '{}'.format(CONFIG_PROMPT),
            ),
            Command('end', ENABLE_PROMPT),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v2_with_vrf_already_enabled(self, send_mock, recv_mock):
        self._setUp({
            'VRF Management Name': 'management',
        })

        emu = CliEmulator([
            Command('configure terminal', CONFIG_PROMPT),
            Command(
                'show snmp',
                '0 SNMP packets input\n'
                '    0 Bad SNMP version errors\n'
                '    0 Unknown community name\n'
                '    0 Illegal operation for community name supplied\n'
                '    0 Encoding errors\n'
                '    0 Number of requested variables\n'
                '    0 Number of altered variables\n'
                '    0 Get-request PDUs\n'
                '    0 Get-next PDUs\n'
                '    0 Set-request PDUs\n'
                '...\n'
                'SNMP logging: disabled\n'
                'SNMP agent enabled in VRFs: default, management\n'
                '{}'.format(CONFIG_PROMPT),
            ),
            Command('show snmp community', CONFIG_PROMPT),
            Command('snmp-server community public ro', CONFIG_PROMPT),
            Command(
                'show snmp community',
                'Community name: public\n'
                'Community access: read-only\n'
                '{}'.format(CONFIG_PROMPT),
            ),
            Command('end', ENABLE_PROMPT),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v2_already_enabled(self, send_mock, recv_mock):
        self._setUp()

        emu = CliEmulator([
            Command('configure terminal', CONFIG_PROMPT),
            Command(
                'show snmp community',
                'Community name: public\n'
                'Community access: read-only\n'
                '{}'.format(CONFIG_PROMPT),
            ),
            Command('end', ENABLE_PROMPT),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v2_not_enabled(self, send_mock, recv_mock):
        self._setUp()

        emu = CliEmulator([
            Command('configure terminal', CONFIG_PROMPT),
            Command('show snmp community', CONFIG_PROMPT),
            Command('snmp-server community public ro', CONFIG_PROMPT),
            Command('show snmp community', CONFIG_PROMPT),
            Command('end', ENABLE_PROMPT),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        with self.assertRaisesRegexp(Exception, 'Failed to create SNMP community'):
            self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v2_write_community(self, send_mock, recv_mock):
        self._setUp({'SNMP Write Community': 'private'})

        emu = CliEmulator([
            Command('configure terminal', CONFIG_PROMPT),
            Command('show snmp community', CONFIG_PROMPT),
            Command('snmp-server community private ro', CONFIG_PROMPT),
            Command(
                'show snmp community',
                'Community name: private\n'
                'Community access: read-only\n'
                '{}'.format(CONFIG_PROMPT),
            ),
            Command('end', ENABLE_PROMPT),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('tests.networking.arista.base_test.AristaCliHandler')
    def test_enable_snmp_without_community(self, cli_handler_mock):
        self._setUp({'SNMP Read Community': ''})

        with self.assertRaisesRegexp(Exception, 'SNMP community cannot be empty'):
            self.runner.discover()

        cli_handler_mock.get_cli_service.assert_not_called()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_disable_snmp_v2(self, send_mock, recv_mock):
        self._setUp({
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
        })

        emu = CliEmulator([
            Command('configure terminal', CONFIG_PROMPT),
            Command('no snmp-server community public', CONFIG_PROMPT),
            Command('show snmp community', CONFIG_PROMPT),
            Command('end', ENABLE_PROMPT),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('tests.networking.arista.base_test.AristaCliHandler')
    def test_disable_snmp_without_community(self, cli_handler_mock):
        self._setUp({
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
            'SNMP Read Community': '',
        })

        with self.assertRaisesRegexp(Exception, 'SNMP community cannot be empty'):
            self.runner.discover()

        cli_handler_mock.get_cli_service.assert_not_called()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_disable_snmp_v2_already_disabled(self, send_mock, recv_mock):
        self._setUp({
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
        })

        emu = CliEmulator([
            Command('configure terminal', CONFIG_PROMPT),
            Command('no snmp-server community public', CONFIG_PROMPT),
            Command('show snmp community', CONFIG_PROMPT),
            Command('end', ENABLE_PROMPT),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_disable_snmp_v2_is_not_disabled(self, send_mock, recv_mock):
        self._setUp({
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
        })

        emu = CliEmulator([
            Command('configure terminal', CONFIG_PROMPT),
            Command('no snmp-server community public', CONFIG_PROMPT),
            Command(
                'show snmp community',
                'Community name: public\n'
                'Community access: read-only\n'
                '{}'.format(CONFIG_PROMPT),
            ),
            Command('end', ENABLE_PROMPT),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        with self.assertRaisesRegexp(Exception, 'Failed to remove SNMP community'):
            self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_disable_snmp_v2_write_community(self, send_mock, recv_mock):
        self._setUp({
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
            'SNMP Write Community': 'private',
        })

        emu = CliEmulator([
            Command('configure terminal', CONFIG_PROMPT),
            Command('no snmp-server community private', CONFIG_PROMPT),
            Command('show snmp community', CONFIG_PROMPT),
            Command('end', ENABLE_PROMPT),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('tests.networking.arista.base_test.AristaCliHandler')
    def test_enable_snmp_v3(self, cli_handler_mock):
        cli_instance_mock = MagicMock()
        cli_handler_mock.return_value = cli_instance_mock
        self._setUp({'SNMP Version': 'v3'})

        with self.assertRaisesRegexp(Exception, 'Do not support SNMP V3'):
            self.runner.discover()

        cli_instance_mock.get_cli_service.assert_not_called()

    @patch('tests.networking.arista.base_test.AristaCliHandler')
    def test_disable_snmp_v3(self, cli_handler_mock):
        cli_instance_mock = MagicMock()
        cli_handler_mock.return_value = cli_instance_mock
        self._setUp({
            'SNMP Version': 'v3',
            'SNMP V3 Authentication Protocol': 'SHA',
            'SNMP V3 Privacy Protocol': 'AES-128',
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
        })

        with self.assertRaisesRegexp(Exception, 'Do not support SNMP V3'):
            self.runner.discover()

        cli_instance_mock.get_cli_service.assert_not_called()

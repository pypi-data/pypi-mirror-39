import re
from collections import deque
from unittest import TestCase

from cloudshell.devices.driver_helper import get_cli
from cloudshell.devices.standards.networking.configuration_attributes_structure import \
    create_networking_resource_from_context
from cloudshell.shell.core.driver_context import ResourceCommandContext, ResourceContextDetails
from mock import create_autospec, MagicMock

from cloudshell.networking.arista.cli.arista_cli_handler import AristaCliHandler


DEFAULT_PROMPT = 'Arista>'
ENABLE_PROMPT = 'Arista#'
CONFIG_PROMPT = 'Arista(config)#'
VRF_PROMPT = 'Arista(vrf:{vrf_name})#'

ENABLE_PASSWORD = 'enable_password'


class Command(object):
    def __init__(self, request, response, regexp=False):
        self.request = request
        self.response = response
        self.regexp = regexp

    def is_equal_to_request(self, request):
        return (not self.regexp and self.request == request
                or self.regexp and re.search(self.request, request))

    def __repr__(self):
        return 'Command({!r}, {!r}, {!r})'.format(self.request, self.response, self.regexp)


class CliEmulator(object):
    def __init__(self, commands=None):
        self.request = None

        self.commands = deque([
            Command(None, DEFAULT_PROMPT),
            Command('', DEFAULT_PROMPT),
            Command('enable', 'Password:'),
            Command(ENABLE_PASSWORD, ENABLE_PROMPT),
            Command('terminal length 0', ENABLE_PROMPT),
            Command('terminal width 300', ENABLE_PROMPT),
            Command('terminal no exec prompt timestamp', ENABLE_PROMPT),
            Command('configure terminal', CONFIG_PROMPT),
            Command('no logging console', CONFIG_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command('', ENABLE_PROMPT),
        ])

        if commands:
            self.commands.extend(commands)

        self.unexpected_requests = []

    def _get_response(self):
        try:
            command = self.commands.popleft()
        except IndexError:
            self.unexpected_requests.append(self.request)
            raise IndexError('Not expected requests - "{}"'.format(self.unexpected_requests))

        if not command.is_equal_to_request(self.request):
            self.unexpected_requests.append(self.request)
            raise KeyError('Unexpected request - "{}"\n'
                           'Expected - "{}"'.format(self.unexpected_requests, command.request))

        if isinstance(command.response, Exception):
            raise command.response
        else:
            return command.response

    def receive_all(self, timeout, logger):
        return self._get_response()

    def send_line(self, command, logger):
        self.request = command

    def check_calls(self):
        if self.commands:
            commands = '\n'.join('\t\t- {}'.format(command.request) for command in self.commands)
            raise ValueError('Not executed commands: \n{}'.format(commands))


class BaseAristaTestCase(TestCase):
    SHELL_NAME = ''

    def create_context(self, attrs=None):
        context = create_autospec(ResourceCommandContext)
        context.resource = create_autospec(ResourceContextDetails)
        context.resource.name = 'Arista'
        context.resource.fullname = 'Arista'
        context.resource.family = 'CS_Router'
        context.resource.address = 'host'
        context.resource.attributes = {}

        attributes = {
            'User': 'admin',
            'Password': 'password',
            'Enable Password': ENABLE_PASSWORD,
            'host': 'host',
            'CLI Connection Type': 'ssh',
            'Sessions Concurrency Limit': '1',
        }
        attributes.update(attrs or {})

        for key, val in attributes.items():
            context.resource.attributes['{}{}'.format(self.SHELL_NAME, key)] = val

        return context

    def _setUp(self, attrs=None):
        if attrs is None:
            attrs = {}

        self.resource_config = create_networking_resource_from_context(
            self.SHELL_NAME, ['EOS'], self.create_context(attrs))
        self._cli = get_cli(int(self.resource_config.sessions_concurrency_limit))

        self.logger = MagicMock()
        self.api = MagicMock(DecryptPassword=lambda password: MagicMock(Value=password))

        self.cli_handler = AristaCliHandler(self._cli, self.resource_config, self.logger, self.api)

    def tearDown(self):
        self._cli._session_pool._session_manager._existing_sessions = []

        while not self._cli._session_pool._pool.empty():
            self._cli._session_pool._pool.get()

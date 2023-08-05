import re

from cloudshell.cli.cli_service_impl import CliServiceImpl as CliService
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor

from cloudshell.networking.arista.command_templates.arista_configuration_templates import \
    ENABLE_SNMP, \
    SHOW_SNMP_COMMUNITY, DISABLE_SNMP, SHOW_SNMP, ENABLE_VRF_FOR_SNMP


class EnableDisableSnmpActions(object):
    def __init__(self, cli_service, logger):
        """
        Reboot actions
        :param cli_service: config mode cli service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """
        self._cli_service = cli_service
        self._logger = logger

    def is_configured(self, snmp_community):
        """
        Check snmp community configured
        :param snmp_community:
        :return:
        """
        output = CommandTemplateExecutor(self._cli_service, SHOW_SNMP_COMMUNITY).execute_command()
        return snmp_community in output

    def enable_snmp(self, snmp_community):
        """
        Enable snmp on the device
        :return:
        """

        return CommandTemplateExecutor(
            self._cli_service,
            ENABLE_SNMP
        ).execute_command(snmp_community=snmp_community)

    def disable_snmp(self, snmp_community):
        """
        Disable SNMP
        :return:
        """
        return CommandTemplateExecutor(
            self._cli_service,
            DISABLE_SNMP
        ).execute_command(snmp_community=snmp_community)

    def is_configured_vrf(self, vrf_name):
        """Check that vrf name is enabled for SNMP agent.

        :param str vrf_name:
        :rtype: bool
        """
        output = CommandTemplateExecutor(
            self._cli_service,
            SHOW_SNMP,
        ).execute_command()

        vrfs = re.search(r'^SNMP agent enabled in VRFs:\s(.+)$', output, re.MULTILINE)
        vrfs = map(str.strip, vrfs.group(1).split(','))

        return vrf_name in vrfs

    def enable_vrf_for_snmp_server(self, vrf_name):
        """Enable vrf for SNMP server.

        :param str vrf_name:
        """
        return CommandTemplateExecutor(
            self._cli_service,
            ENABLE_VRF_FOR_SNMP,
        ).execute_command(vrf_name=vrf_name)

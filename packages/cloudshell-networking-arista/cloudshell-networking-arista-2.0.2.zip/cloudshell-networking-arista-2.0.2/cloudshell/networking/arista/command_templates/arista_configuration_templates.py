from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

BOOT_SYSTEM_FILE = CommandTemplate("boot system flash:{firmware_file_name}")
SHOW_BOOT = CommandTemplate("show boot")

ERROR_MAP = OrderedDict([(r'[Ee]rror:', 'Command error')])

SHOW_SNMP_COMMUNITY = CommandTemplate('show snmp community', error_map=ERROR_MAP)
ENABLE_SNMP = CommandTemplate('snmp-server community {snmp_community} ro', error_map=ERROR_MAP)
DISABLE_SNMP = CommandTemplate('no snmp-server community {snmp_community}', error_map=ERROR_MAP)

SHOW_SNMP = CommandTemplate('show snmp')
ENABLE_VRF_FOR_SNMP = CommandTemplate('snmp-server vrf {vrf_name}')

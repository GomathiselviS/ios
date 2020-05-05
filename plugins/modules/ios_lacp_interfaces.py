#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
"""
The module file for ios_lacp_interfaces
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {"metadata_version": "1.1", "supported_by": "Ansible"}

DOCUMENTATION = """
module: ios_lacp_interfaces
short_description: LACP interfaces resource module
description: This module provides declarative management of LACP on Cisco IOS network devices lacp_interfaces.
version_added: 1.0.0
author: Sumit Jaiswal (@justjais)
notes:
- Tested against Cisco IOSv Version 15.2 on VIRL.
- This module works with connection C(network_cli), See L(IOS Platform Options,../network/user_guide/platform_ios.html).
options:
  config:
    description: A dictionary of LACP lacp_interfaces option
    type: list
    elements: dict
    suboptions:
      name:
        description:
        - Name of the Interface for configuring LACP.
        type: str
        required: true
      port_priority:
        description:
        - LACP priority on this interface.
        - Refer to vendor documentation for valid port values.
        type: int
      fast_switchover:
        description:
        - LACP fast switchover supported on this port channel.
        type: bool
      max_bundle:
        description:
        - LACP maximum number of ports to bundle in this port channel.
        - Refer to vendor documentation for valid port values.
        type: int
  running_config:
    description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the VyOS device by executing
        the command B(show configuration commands | grep interfaces).
      - The state I(parsed) reads the configuration from C(running_config) option and transforms
        it into Ansible structured data as per the resource module's argspec and the value is then
        returned in the I(parsed) key within the result.
  state:
    description:
    - The state of the configuration after module completion
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - rendered
    - gathered
    - parsed
    default: merged
"""

EXAMPLES = """
# Using merged
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
# interface GigabitEthernet0/2
#  shutdown
# interface GigabitEthernet0/3
#  shutdown

- name: Merge provided configuration with device configuration
  cisco.ios.ios_lacp_interfaces:
    config:
    - name: GigabitEthernet0/1
      port_priority: 10
    - name: GigabitEthernet0/2
      port_priority: 20
    - name: GigabitEthernet0/3
      port_priority: 30
    - name: Port-channel10
      fast_switchover: true
      max_bundle: 5
    state: merged

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
#  lacp fast-switchover
#  lacp max-bundle 5
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  lacp port-priority 10
# interface GigabitEthernet0/2
#  shutdown
#  lacp port-priority 20
# interface GigabitEthernet0/3
#  shutdown
#  lacp port-priority 30

# Using overridden
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
#  lacp fast-switchover
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  lacp port-priority 10
# interface GigabitEthernet0/2
#  shutdown
#  lacp port-priority 20
# interface GigabitEthernet0/3
#  shutdown
#  lacp port-priority 30

- name: Override device configuration of all lacp_interfaces with provided configuration
  cisco.ios.ios_lacp_interfaces:
    config:
    - name: GigabitEthernet0/1
      port_priority: 20
    - name: Port-channel10
      max_bundle: 2
    state: overridden

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
#  lacp max-bundle 2
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  lacp port-priority 20
# interface GigabitEthernet0/2
#  shutdown
# interface GigabitEthernet0/3
#  shutdown

# Using replaced
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
#  lacp max-bundle 5
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  lacp port-priority 10
# interface GigabitEthernet0/2
#  shutdown
#  lacp port-priority 20
# interface GigabitEthernet0/3
#  shutdown
#  lacp port-priority 30

- name: Replaces device configuration of listed lacp_interfaces with provided configuration
  cisco.ios.ios_lacp_interfaces:
    config:
    - name: GigabitEthernet0/3
      port_priority: 40
    - name: Port-channel10
      fast_switchover: true
      max_bundle: 2
    state: replaced

# After state:
# ------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
#  lacp fast-switchover
#  lacp max-bundle 2
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  lacp port-priority 10
# interface GigabitEthernet0/2
#  shutdown
#  lacp port-priority 20
# interface GigabitEthernet0/3
#  shutdown
#  lacp port-priority 40

# Using Deleted
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
#  flowcontrol receive on
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  lacp port-priority 10
# interface GigabitEthernet0/2
#  shutdown
#  lacp port-priority 20
# interface GigabitEthernet0/3
#  shutdown
#  lacp port-priority 30

- name: "Delete LACP attributes of given interfaces (Note: This won't delete the interface itself)"
  cisco.ios.ios_lacp_interfaces:
    config:
    - name: GigabitEthernet0/1
    state: deleted

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
# interface GigabitEthernet0/2
#  shutdown
#  lacp port-priority 20
# interface GigabitEthernet0/3
#  shutdown
#  lacp port-priority 30

# Using Deleted without any config passed
# "(NOTE: This will delete all of configured LLDP module attributes)"
#
# Before state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
#  lacp fast-switchover
# interface Port-channel20
#  lacp max-bundle 2
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
#  lacp port-priority 10
# interface GigabitEthernet0/2
#  shutdown
#  lacp port-priority 20
# interface GigabitEthernet0/3
#  shutdown
#  lacp port-priority 30

- name: "Delete LACP attributes for all configured interfaces (Note: This won't delete the interface itself)"
  cisco.ios.ios_lacp_interfaces:
    state: deleted

# After state:
# -------------
#
# vios#show running-config | section ^interface
# interface Port-channel10
# interface Port-channel20
# interface Port-channel30
# interface GigabitEthernet0/1
#  shutdown
# interface GigabitEthernet0/2
#  shutdown
# interface GigabitEthernet0/3
#  shutdown
<<<<<<< HEAD
=======

# Using Gathered

# Before state:
# -------------
#
# vios#sh running-config | section ^interface
# interface Port-channel10
#  lacp fast-switchover
#  lacp max-bundle 2
# interface Port-channel40
#  lacp max-bundle 5
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  lacp port-priority 30
# interface GigabitEthernet0/2
#  lacp port-priority 20

- name: Gather listed LACP interfaces with provided configurations
  cisco.ios.ios_lacp_interfaces:
    config:
    state: gathered

# Module Execution Result:
# ------------------------
#
# "gathered": [
#         {
#             "fast_switchover": true,
#             "max_bundle": 2,
#             "name": "Port-channel10"
#         },
#         {
#             "max_bundle": 5,
#             "name": "Port-channel40"
#         },
#         {
#             "name": "GigabitEthernet0/0"
#         },
#         {
#             "name": "GigabitEthernet0/1",
#             "port_priority": 30
#         },
#         {
#             "name": "GigabitEthernet0/2",
#             "port_priority": 20
#         }
#     ]

# After state:
# ------------
#
# vios#sh running-config | section ^interface
# interface Port-channel10
#  lacp fast-switchover
#  lacp max-bundle 2
# interface Port-channel40
#  lacp max-bundle 5
# interface GigabitEthernet0/0
# interface GigabitEthernet0/1
#  lacp port-priority 30
# interface GigabitEthernet0/2
#  lacp port-priority 20

# Using Rendered

- name: Render the commands for provided  configuration
  cisco.ios.ios_lacp_interfaces:
    config:
      - name: GigabitEthernet0/1
        port_priority: 10
      - name: GigabitEthernet0/2
        port_priority: 20
      - name: Port-channel10
        fast_switchover: True
        max_bundle: 2
    state: rendered

# Module Execution Result:
# ------------------------
#
# "rendered": [
#         "interface GigabitEthernet0/1",
#         "lacp port-priority 10",
#         "interface GigabitEthernet0/2",
#         "lacp port-priority 20",
#         "interface Port-channel10",
#         "lacp max-bundle 2",
#         "lacp fast-switchover"
#     ]

# Using Parsed

- name: Parse the commands for provided configuration
  cisco.ios.ios_lacp_interfaces:
    running_config:
      "interface GigabitEthernet0/1
       lacp port-priority 10
       interface GigabitEthernet0/2
       lacp port-priority 20
       interface Port-channel10
       lacp max-bundle 2
       slacp fast-switchover"
    state: parsed

# Module Execution Result:
# ------------------------
#
# "parsed": [
#         {
#             "name": "GigabitEthernet0/1",
#             "port_priority": 10
#         },
#         {
#             "name": "GigabitEthernet0/2",
#             "port_priority": 20
#         },
#         {
#             "fast_switchover": true,
#             "max_bundle": 2,
#             "name": "Port-channel10"
#         }
#     ]

>>>>>>> fix lacp interfaces new states
"""
RETURN = """
before:
  description: The configuration as structured data prior to module invocation.
  returned: always
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
after:
  description: The configuration as structured data after module completion.
  returned: when changed
  type: list
  sample: >
    The configuration returned will always be in the same format
     of the parameters above.
commands:
  description: The set of commands pushed to the remote device.
  returned: always
  type: list
  sample: ['interface GigabitEthernet 0/1', 'lacp port-priority 30']
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.lacp_interfaces.lacp_interfaces import (
    Lacp_InterfacesArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.lacp_interfaces.lacp_interfaces import (
    Lacp_Interfaces,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "overridden", ("config",)),
        ("state", "rendered", ("config",)),
        ("state", "parsed", ("running_config",)),
    ]
    mutually_exclusive = [("config", "running_config")]

    module = AnsibleModule(
        argument_spec=Lacp_InterfacesArgs.argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    result = Lacp_Interfaces(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()

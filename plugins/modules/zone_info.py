#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Part of ansible markuman.hetzner_dns collection

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: markuman.hetzner_dns.zone_info
description: Get information about a hetzner dns zone.
'''

EXAMPLES = '''
    - name: fetch zone info
      markuman.hetzner_dns.zone_info:
        name: zone_name
'''

from ansible.module_utils.basic import *
from ansible_collections.markuman.hetzner_dns.plugins.module_utils.helper import HetznerAPIHandler
from ansible_collections.markuman.hetzner_dns.plugins.module_utils.helper import ZoneInfo


def main():
    argument_spec = dict(
        name = dict(required=True, type='str'),
        api_token = dict(required=False, type='str', no_log=True, aliases=['access_token'])
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    module.deprecate("'markuman.hetzner_dns' collection becomes deprecated since 'community.dns' included support for hetzner dns")

    dns = HetznerAPIHandler(module.params, module.fail_json)

    name = module.params.get("name")

    zones = dns.get_zone_info(name)
    zone_id, zone_info = ZoneInfo(zones, name)

    module.exit_json(changed = False, zone_id=zone_id, zone_info=zone_info)


if __name__ == '__main__':
    main()

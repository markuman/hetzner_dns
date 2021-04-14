#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Part of ansible markuman.hetzner_dns collection

DOCUMENTATION = '''
module: markuman.hetzner_dns.zone_info
'''

EXAMPLES = '''
    - name: fetch zone info
      markuman.hetzner_dns.record_info:
        filter:
          - name: fritzbox
            value: 192.168.178.1
            type: A
          - name: fritzbox
            type: AAAA
        zone_name: osuv.de
    
'''

from ansible.module_utils.basic import *
from ansible_collections.markuman.hetzner_dns.plugins.module_utils.helper import HetznerAPIHandler
from ansible_collections.markuman.hetzner_dns.plugins.module_utils.helper import ZoneInfo


def main():
    argument_spec = dict(
        filter = dict(required=False, type='list'),
        zone_id = dict(required=False, type='str'),
        zone_name = dict(required=False, type='str'),
        api_token = dict(required=False, type='str', no_log=True, aliases=['access_token'])
    )
    
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[['zone_id', 'zone_name']],
        supports_check_mode=True
    )

    dns = HetznerAPIHandler(module.params, module.fail_json)

    filters = module.params.get("filter")
    zone_id = module.params.get("zone_id")
    zone_name = module.params.get("zone_name")

    if zone_id is None:
        zones = dns.get_zone_info()
        zone_id = ZoneInfo(zones, zone_name)

    records = dns.get_record_info(zone_id)

    if filters is None:
        retval = records.json()['records']
    else:
        retval = list()
        for record in records.json()['records']:
            for filter in filters:
                if all(item in record.items() for item in filter.items()):
                    retval.append(record)

    

    module.exit_json(changed = False, record_info=retval)
    

if __name__ == '__main__':
    main()
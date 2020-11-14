#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
module: markuman.hetzner_dns.zone_info
'''

EXAMPLES = '''
    - name: fetch zone info
      markuman.hetzner_dns.record_info:
        name: fritzbox
        value: 192.168.178.1
        type: A
        zone_id: abc
        zone_name: osuv.de
    
'''

from ansible.module_utils.basic import *
from ansible_collections.markuman.hetzner_dns.plugins.module_utils.auth import HetznerAPIHandler

def main():
    module = AnsibleModule(
        argument_spec = dict(
            name = dict(required=False, type='str'),
            dns_type = dict(required=False, type='str'),
            value = dict(required=False, type='str'),
            zone_id = dict(required=True, type='str'),
            api_token = dict(required=False, type='str', no_log=True, aliases=['access_token'])
        )
    )

    dns = HetznerAPIHandler(module.params)

    name = module.params.get("name")
    dns_type = module.params.get("dns_type")
    value = module.params.get("value")
    zone_id = module.params.get("zone_id")

    records = dns.get_record_info(zone_id)

    if not any([name, dns_type, value]):
        retval = records.json()['records']
    else:
        retval = list()
        for item in records.json()['records']:
            if item.get('name', '') == name or item.get('type', '') == dns_type or value == item.get('value', ''):
                retval.append(item)
    

    module.exit_json(changed = False, record_info=retval)
    

if __name__ == '__main__':
    main()
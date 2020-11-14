#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
module: markuman.hetzner_dns.zone_info
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
    module = AnsibleModule(
        argument_spec = dict(
            name = dict(required=False, type='str'),
            api_token = dict(required=False, type='str', no_log=True, aliases=['access_token'])
        )
    )

    dns = HetznerAPIHandler(module.params)

    name = module.params.get("name")

    zones = dns.get_zone_info()
    zone_id, zone_info = ZoneInfo(zones, name)
    
    module.exit_json(changed = False, zone_id=zone_id, zone_info=zone_info)
    

if __name__ == '__main__':
    main()
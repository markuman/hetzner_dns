#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Part of ansible markuman.hetzner_dns collection

DOCUMENTATION = '''
module: markuman.hetzner_dns.zone_info
'''

EXAMPLES = '''
    - name: add record
      markuman.hetzner_dns.record:
        zone_name: osuv.de
        name: hetzner_dns_ansible_collection
        value: osuv.de.
        type: CNAME
        ttl: 300
      register: RECORD

    - name: add record no change
      markuman.hetzner_dns.record:
        zone_name: osuv.de
        name: hetzner_dns_ansible_collection
        value: osuv.de.
        type: CNAME
        ttl: 300
      register: RECORD

    - name: add record change
      markuman.hetzner_dns.record:
        zone_name: osuv.de
        name: hetzner_dns_ansible_collection
        value: osuv.de.
        type: CNAME
        ttl: 60
      register: RECORD

    - name: del record
      markuman.hetzner_dns.record:
        zone_name: osuv.de
        name: hetzner_dns_ansible_collection
        type: CNAME
        state: absent
      register: RECORD
'''

from ansible.module_utils.basic import *
from ansible_collections.markuman.hetzner_dns.plugins.module_utils.helper import HetznerAPIHandler
from ansible_collections.markuman.hetzner_dns.plugins.module_utils.helper import ZoneInfo


def main():
    argument_spec = dict(
        zone_id = dict(required=False, type='str'),
        zone_name = dict(required=False, type='str'),
        api_token = dict(required=False, type='str', no_log=True, aliases=['access_token']),
        name = dict(required=True, type='str'),
        value = dict(type='str'),
        ttl = dict(default=300, type='int'),
        type = dict(required=True, type='str', choices=["A","AAAA","NS","MX","CNAME","RP","TXT","SOA","HINFO","SRV","DANE","TLSA","DS","CAA"]),
        state = dict(type='str', default='present', choices=['present', 'absent'])
    )
    
    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[['state', 'present', ['value']]],
        required_one_of=[
            ['zone_id', 'zone_name']
        ],
        supports_check_mode=True
    )

    dns = HetznerAPIHandler(module.params)

    zone_id = module.params.get("zone_id")
    zone_name = module.params.get("zone_name")
    state = module.params.get("state")

    if zone_id is None:
        zones = dns.get_zone_info()
        zone_id, zone_info = ZoneInfo(zones, zone_name)

    future_record = {
        'name': module.params.get("name"),
        'value': module.params.get("value"),
        'type': module.params.get("type"),
        'ttl': int(module.params.get("ttl")),
        'zone_id': zone_id
    }

    find_record = {
        'name': future_record.get('name'),
        'type': future_record.get('type'),
    }

    records = dns.get_record_info(zone_id)

    record_changed = False
    record_exists = False
    change = False
    past_record = None
    for record in records.json()['records']:
        if not record.get('ttl'):
          record['ttl'] = 300
        if all(item in record.items() for item in find_record.items()):
            record_exists = True
            record_id = record.get('id')
            past_record = record
            if not all(item in record.items() for item in future_record.items()):
                record_changed = True
            else:
                this_record = { 'record': record }
            break
    
    if state == 'present':
        if not record_exists:
            record_id = None
            this_record = { 'record': future_record }
            change = True
            if not module.check_mode:
              r = dns.create_record(future_record)
              record_id = r.json()['record']['id']
              this_record = r.json()
        elif record_changed:
            change = True
            this_record = { 'record': future_record }
            if not module.check_mode:
              r = dns.update_record(future_record, record_id)
              this_record = r.json()
            

    if state == 'absent':
        if record_exists:
            change = True
            if not module.check_mode:
              r = dns.delete_record(record_id)
        else:
            change = False
        this_record = { 'record': None }
        record_id = None
            

    module.exit_json(changed = change, record_id=record_id, record_info=this_record, past_record=past_record)
    

if __name__ == '__main__':
    main()
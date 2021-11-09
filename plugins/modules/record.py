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
from ansible.errors import AnsibleError
from ansible_collections.markuman.hetzner_dns.plugins.module_utils.helper import HetznerAPIHandler
from ansible_collections.markuman.hetzner_dns.plugins.module_utils.helper import ZoneInfo, error_codes, UE
import yaml

def main():
    argument_spec = dict(
        zone_id = dict(required=False, type='str'),
        zone_name = dict(required=False, type='str'),
        api_token = dict(required=False, type='str', no_log=True, aliases=['access_token']),
        name = dict(required=True, type='str'),
        value = dict(type='str'),
        ttl = dict(default=300, type='int'),
        type = dict(required=True, type='str', choices=["A","AAAA","NS","MX","CNAME","RP","TXT","SOA","HINFO","SRV","DANE","TLSA","DS","CAA"]),
        state = dict(type='str', default='present', choices=['present', 'absent']),
        purge = dict(required=False, type='bool', default=True, aliases=['replace', 'overwrite', 'solo'])
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[['state', 'present', ['value']]],
        required_one_of=[
            ['zone_id', 'zone_name']
        ],
        supports_check_mode=True
    )

    module.deprecate("'markuman.hetzner_dns' collection becomes deprecated since 'community.dns' included support for hetzner dns")

    dns = HetznerAPIHandler(module.params, module.fail_json)

    zone_id = module.params.get("zone_id")
    zone_name = module.params.get("zone_name")
    state = module.params.get("state")
    purge = module.params.get("purge")

    if zone_id is None:
        zones = dns.get_zone_info(zone_name)
        zone_id, zone_info = ZoneInfo(zones, zone_name)
        if zone_id is None:
          module.fail_json(msg='zone or zone_id: {msg}'.format(msg=error_codes.get(404, UE)))

    future_record = {
        'name': module.params.get("name"),
        'value': module.params.get("value"),
        'type': module.params.get("type"),
        'ttl': int(module.params.get("ttl")),
        'zone_id': zone_id
    }

    find_record = {
        'name': future_record.get('name'),
        'type': future_record.get('type')
    }

    if module.params.get("value") and not purge:
        find_record['value'] = module.params.get("value")

    records = dns.get_record_info(zone_id)

    record_changed = False
    record_exists = False
    change = False
    past_record = []
    record_ids = []
    for record in records.json()['records']:

        if not record.get('ttl'):
          record['ttl'] = 300

        if all(item in record.items() for item in find_record.items()):
            record_exists = True
            record_id = record.get('id')
            record_ids.append(record.get('id'))
            past_record.append(record)

            if not all(item in record.items() for item in future_record.items()):
                record_changed = True
            else:
                this_record = { 'record': record }


    if record_changed and not purge:
        record_exists = False
        record_changed = False

    if state == 'present':
        if purge and len(record_ids) > 1:
            for id in record_ids:
                r = dns.delete_record(id)

        if not record_exists or (purge and len(record_ids) > 1):
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
                if not module.params.get("value"):
                    # when value was not defined, delete all records of this type
                    for id in record_ids:
                        r = dns.delete_record(id)
                else:
                    r = dns.delete_record(record_id)

        else:
            change = False
        this_record = { 'record': {} }
        record_id = None

    for idx in range(len(past_record)):
        past_record[idx].pop('id', None)
        past_record[idx].pop('created', None)
        past_record[idx].pop('modified', None)
        past_record[idx].pop('zone_id', None)

    after_record = [this_record.get('record')]
    if isinstance(after_record[0], dict):
        after_record[0].pop('id', None)
        after_record[0].pop('created', None)
        after_record[0].pop('modified', None)
        after_record[0].pop('zone_id', None)

    diff = dict(
        before=yaml.safe_dump(past_record),
        after=yaml.safe_dump(after_record)
    )

    module.exit_json(changed = change, record_id=record_id, record_info=this_record, past_record=past_record, diff=diff)


if __name__ == '__main__':
    main()

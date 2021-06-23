#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Part of ansible markuman.hetzner_dns collection


from ansible_collections.markuman.hetzner_dns.plugins.module_utils.helper import HetznerAPIHandler
from ansible_collections.markuman.hetzner_dns.plugins.module_utils.helper import ZoneInfo
from ansible.plugins.inventory import BaseInventoryPlugin
import os

DOCUMENTATION = '''
    name: hetzner_dns
    plugin_type: inventory

    options:
        zone_name:
            description: dns zone name.
            required: True
            type: string
        api_token:
            description: api token. if not set, it is read from env HETZNER_DNS_TOKEN
            required: False
            type: string
'''

class InventoryModule(BaseInventoryPlugin):
    NAME = 'markuman.hetzner_dns.hetzner_dns'

    def __init__(self):
        super(InventoryModule, self).__init__()
        # credentials
        self.api_token = self.get_option('api_token') or os.environ.get('HETZNER_DNS_TOKEN')

    def verify_file(self, path):
        return True

    def parse(self, inventory, loader, path, cache=False):

        # call base method to ensure properties are available for use with other helper methods
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        config = self._read_config_data(path)

        params = {'api_token': self.api_token}
        dns = HetznerAPIHandler(params)
        zone_name = self.get_option('zone_name')
        zones = dns.get_zone_info(zone_name)
        zone_id = ZoneInfo(zones, zone_name)

        records = dns.get_record_info(zone_id).json()['records']

        #parse data and create inventory objects:
        for item in records:
            if item.get('type') in ['A', 'AAAA', 'CNAME']:
                name = item.get('name') + '.' + zone_name
                self.inventory.add_host(name)
                self.inventory.set_variable(name, 'ansible_host', item.get('value'))


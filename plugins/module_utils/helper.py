#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Part of ansible markuman.hetzner_dns collection

import os
import requests
import json
from ansible.errors import AnsibleError

error_codes = {
    200: "Successful response.",
    401: "Unauthorized.",
    403: "Forbidden.",
    404: "Not found.",
    406: "Not acceptable.",
    409: "Conflict.",
    422: "Unprocessable entity."
}
UE = "Unkown Error."

def ZoneInfo(zones, name):
    zone_id = None
    zone_info = {}
    for item in zones.json()['zones']:
        if item.get('name') == name:
            zone_id = item.get('id')
            zone_info = item

    return zone_id, zone_info

class HetznerAPIHandler:
    def __init__(self, params, fail_json=None):
        self.fail_json = fail_json
        self.TOKEN = params.get('api_token') or os.environ.get('HETZNER_DNS_TOKEN')
        if self.TOKEN is None:
            self.fail_json(msg='Unable to continue. No Hetzner DNS API Token is given.')

    def get_zone_info(self, zone_name):
        try:
            r = requests.get(
                url="https://dns.hetzner.com/api/v1/zones",
                headers={
                    "Auth-API-Token": self.TOKEN,
                },
                params={
                    "name": zone_name,
                },
            )

            if r.status_code == 200:
                return r
            else:
                self.fail_json(msg='zone_info: {msg}'.format(msg=error_codes.get(r.status_code, UE)))
        except requests.exceptions.RequestException:
            self.fail_json(msg='HTTP Request failed')

    def get_record_info(self, zone_id):
        try:
            r = requests.get(
                url="https://dns.hetzner.com/api/v1/records",
                params={
                    "zone_id": zone_id,
                },
                headers={
                    "Auth-API-Token": self.TOKEN,
                },
            )
            if r.status_code == 200:
                return r
            else:
                self.fail_json(msg='record_info: {msg}'.format(msg=error_codes.get(r.status_code, UE)))
        except requests.exceptions.RequestException:
            self.fail_json(msg='HTTP Request failed')


    def create_record(self, record):
        try:
            r = requests.post(
                url="https://dns.hetzner.com/api/v1/records",
                headers={
                    "Content-Type": "application/json",
                    "Auth-API-Token": self.TOKEN,
                },
                data=json.dumps(record)
            )
            if r.status_code == 200:
                return r
            else:
                raise AnsibleError('create record: {msg}'.format(msg=error_codes.get(r.status_code, UE)))
        except requests.exceptions.RequestException:
            raise AnsibleError('HTTP Request failed')


    def update_record(self, record, record_id):
        try:
            r = requests.put(
                url="https://dns.hetzner.com/api/v1/records/{RecordID}".format(RecordID=record_id),
                headers={
                    "Content-Type": "application/json",
                    "Auth-API-Token": self.TOKEN,
                },
                data=json.dumps(record)
            )

            if r.status_code == 200:
                return r
            else:
                self.fail_json(msg='update record: {msg}'.format(msg=error_codes.get(r.status_code, UE)))
        except requests.exceptions.RequestException:
            self.fail_json(msg='HTTP Request failed')

    def delete_record(self, record_id):
        try:
            r = requests.delete(
                url="https://dns.hetzner.com/api/v1/records/{RecordID}".format(RecordID=record_id),
                headers={
                    "Auth-API-Token": self.TOKEN,
                },
            )
            if r.status_code == 200:
                return r
            else:
                self.fail_json(msg='delete record: {msg}'.format(msg=error_codes.get(r.status_code, UE)))
        except requests.exceptions.RequestException:
            self.fail_json(msg='HTTP Request failed')











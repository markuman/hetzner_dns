# hetzner dns ansible collection

Manage DNS records using ansible. E.g. [set DNS records while creating servers in the same play](https://git.osuv.de/m/hetzner_dns/wiki/Home).  
Or use hetzner DNS as an inventory for your playbooks.

* https://galaxy.ansible.com/markuman/hetzner_dns
* `ansible-galaxy collection install markuman.hetzner_dns`

## Auth

The API token can be set via ansible parameter or ENV variable.

| **Ansible Parameter** | **ENV Variable** |
| --- | --- |
| `api_token` (_alias `access_token`_) | `HETZNER_DNS_TOKEN` |

All modules supports and respects `check_mode: yes`.

## record

* `state: absent` 
    * _deleting_ a record: `name` and `type` are sufficient (_`ttl` doesn't matter_).
    * When `value` is not given, all records that match `name` and `type` will be removed!
    * When `value` is given, only one record will be deleted that matches `name`, `type`, and `value`.
* `state: present`
    * the `ttl` default value is set to `0` (_same as hetzner webinterface did._)
    * Either `zone_id` or `zone_name`  must be given, but not both.  

| parameters | default | comment |
| --- | --- | --- |
| `name` | - | name of a record |
| `purge` | `true` | Wether a existing value should be replaced (`true`) or appended (`false`) to achive multiple DNS records for one name. Alias parameter are: `replace`, `overwrite`, `solo`.
| `value` | - | required with `state: present` |
| `type` | - | type of record. valid records: "A" "AAAA" "NS" "MX" "CNAME" "RP" "TXT" "SOA" "HINFO" "SRV" "DANE" "TLSA" "DS" "CAA" |
| `ttl` | `300` | TTL of a record |
| `zone_id` | - | Required one of `zone_name` or `zone_id` |
| `zone_name` | - | Required one of `zone_name` or `zone_id` |
| `api_token` | - | Can be also set as env variable `HETZNER_DNS_TOKEN` |


```yml
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

- name: add single A record
  markuman.hetzner_dns.record:
    zone_name: osuv.de
    name: dns
    value: 1.1.1.1
    type: A
    ttl: 60

- name: append A record
  markuman.hetzner_dns.record:
    zone_name: osuv.de
    name: dns
    value: 8.8.8.8
    type: A
    purge: no
    ttl: 60

- name: append A record
  markuman.hetzner_dns.record:
    zone_name: osuv.de
    name: dns
    value: 8.8.4.4
    type: A
    purge: no
    ttl: 60

- name: delete single A record
  markuman.hetzner_dns.record:
    zone_name: osuv.de
    name: dns
    value: 8.8.8.8
    type: A
    state: absent

- name: > 
    delete all A records
    when no `value` is given
  markuman.hetzner_dns.record:
    zone_name: osuv.de
    name: dns
    type: A
    state: absent

```

#### mx priority

When dialing with sevaral mx records, the priority must be part of the value.

```yml
- name: take care about mx record
  markuman.hetzner_dns.record:
    api_token: "{{ API }}"
    zone_name: osuv.de
    name: "@"
    value: 10 mail.osuv.de.
    type: MX
    ttl: 300
  register: RECORD
```

## record_info

When no filter is given, all records will be returned.  
Either `zone_id` or `zone_name`  must be given, but not both.  
Parameter `filter` must be a list, where each object supports the same keys as in `record`  module for search.

| parameter | default | comments |
| --- | --- | --- |
| `filter` | - | Apply a list of key/value pairs to search for |
| `zone_id` | - | Required one of `zone_name` or `zone_id` |
| `zone_name` | - | Required one of `zone_name` or `zone_id` |
| `api_token` | - | Can be also set as env variable `HETZNER_DNS_TOKEN` |


```yml
- name: fetch zone info
  markuman.hetzner_dns.record_info:
    filter:
      - name: fritzbox
        value: 192.168.178.1
        type: A
      - name: fritzbox
        type: AAAA
    zone_name: osuv.de
```

## zone_info

To determine the `zone_id`.

```yml
- name: fetch zone info
  markuman.hetzner_dns.zone_info:
    name: zone_name
```

# Dynamic Inventory

`hetzner_dns` collection comes with a dns based dynamic inventory.   
The file ending must be `.hetzner_dns.yml` or `.hetzner_dns.yaml`.

```yml
plugin: markuman.hetzner_dns.inventory
zone_name: osuv.de
```

Can be used with 

`ansible-inventory -i osuv.hetzner_dns.yml --list` or  
`ansible-playbook -i osuv.hetzner_dns.yml some_tasks.yml`

Supported filters are

```yml
plugin: markuman.hetzner_dns.inventory
zone_name: osuv.de
filters:
  type:
    - A
    - CNAME
```

The default type filter is set to `['A', 'AAAA', 'CNAME']`

### SCM

| **host** | **category** |
| --- | --- |
| https://git.osuv.de/m/hetzner_dns | origin |
| https://gitlab.com/markuman/hetzner_dns | pull mirror, issues, MR |
| https://github.com/markuman/hetzner_dns | push mirror, issues, PR |

#### License

GNU General Public License v3.0+  

_Basically I don't care about the license in this case. So I've decided to choose the same license as [official Ansible Hetzner Cloud Collection](https://github.com/ansible-collections/hetzner.hcloud)._

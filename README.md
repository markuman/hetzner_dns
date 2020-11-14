# hetzner dns ansible collection

## Auth

The API token can be set via ansible parameter or ENV variable.

| **Ansible Parameter** | **ENV Variable** |
| --- | --- |
| `api_token` | `HETZNER_DNS_TOKEN` |


## record

When `state: absent` (_deleting_) a record, than `name` and `type` are sufficient (_`value` and `ttl` doesn't matter_).  
When `state: present`, the `ttl` default value  is set to `0`.  
Either `zone_id` or `zone_name`  must be given, but not both.

 | parameters |
 | --- |
 | `name` |
 | `value` |
 | `type` |
 | `ttl` |
 | `zone_id` |
 | `zone_name` |


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
```

## record_info

When no filter is given, all records will be returned.  
Either `zone_id` or `zone_name`  must be given, but not both.  
Parameter `filter` must be a list, where each object supports the same keys as in `record`  module for search.

 | parameters |
 | --- |
 | `filter` |
 | `zone_id` |
 | `zone_name` |

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

### SCM

| **host** | **category** |
| --- | --- |
| https://git.osuv.de/m/hetzner_dns | origin |
| https://gitlab.com/markuman/hetzner_dns | pull mirror |
| https://github.com/markuman/hetzner_dns | push mirror |
# 1.6.0

* Add dynamic inventory for hetzner dns

```yml
plugin: markuman.hetzner_dns.hetzner_dns
zone_name: osuv.de
filters:
  type:
    - A
    - CNAME
```

`ansible-inventory -i osuv.hetzner_dns.yml --list`

# 1.5.0

* fetch only requested `zone_name`
* improve integrationtests (_easier to run against custom domains_)

# 1.4.3

* fix bug. `purge: yes` removes not all existing records

# 1.4.2

* fix bug. even with `purge: yes`, it was always handled as `purge: no` and was always appending values.  
  *  https://git.osuv.de/m/hetzner_dns/commit/c57e5fd8b9a2a9ad8a9a3769a1f98e9664e0e685

# 1.4.1

* minor change (_documentation update_).

# 1.4.0

* add support to add/delete muliple DNS records for one Name
  * new paramter `purge` with alias parameter `replace`, `overwrite` and `solo` to be compatible with other ansible dns modules.


# 1.3.0

* Grafeful error handling
* full `--diff` support

---

# 1.2.0

* keep past record informations (_[Better Check Mode and Diff Support #1](https://github.com/markuman/hetzner_dns/issues/1)_)
* `check_mode` support also for `_info` modules (_[Better Check Mode and Diff Support #1](https://github.com/markuman/hetzner_dns/issues/1)_)
* Add GPL3+ License

---

# 1.1.0

Set default TTL to 300 to detect dns changes correctly. When a record was set manually without setting a TTL, the API does not response a TTL value.
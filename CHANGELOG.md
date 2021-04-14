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
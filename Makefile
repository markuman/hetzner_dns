.PHONY: help test

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: ## build collection localy
	ansible-galaxy collection build -f

install: ## install collection localy
	ansible-galaxy collection install markuman*

remove: ## remove collection localy
	rm -rf markuman* ~/.ansible/collections/ansible_collections/markuman/hetzner_dns

syntax: ## test compile
	python -m py_compile plugins/modules/record.py
	python -m py_compile plugins/modules/record_info.py
	python -m py_compile plugins/modules/zone_info.py
	python -m py_compile plugins/module_utils/helper.py
	python -m py_compile plugins/inventory/inventory.py

whisper: ## verify files
	whisper-ci --exit-code 1

cleanup: ## remove garbage
	rm -rf whispers.log
	find . -type d -name __pycache__ -exec rm -r {} \+

round: ## remove, build install
	$(MAKE) syntax
	$(MAKE) whisper
	$(MAKE) cleanup
	$(MAKE) remove
	$(MAKE) build
	$(MAKE) install

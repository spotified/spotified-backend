SHELL := /bin/sh

PROJECT := config
PROJECT_DIR := $(abspath $(shell pwd))

deploy_production:
	cd deployment/ansible/
	ansible-galaxy install jnv.unattended-upgrades dev-sec.ssh-hardening debops.gunicorn debops.apt_preferences debops.logrotate debops.python
	ansible-playbook common_server_setup.yml --check
	#git checkout master && git pull && git merge develop && git push && git checkout develop && git push;

pre_commit_all:
	pre-commit install
	pre-commit run --all-files

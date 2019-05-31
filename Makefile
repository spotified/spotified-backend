SHELL := /bin/sh

PROJECT := config
PROJECT_DIR := $(abspath $(shell pwd))

deploy_production:
	git push;
	cd deployment/ansible/; ansible-playbook app.yml

pre_commit_all:
	pre-commit install
	pre-commit run --all-files

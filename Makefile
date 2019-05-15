SHELL := /bin/sh

PROJECT := config
PROJECT_DIR := $(abspath $(shell pwd))

deploy_production:
	#git checkout master && git pull && git merge develop && git push && git checkout develop && git push;
	cd deployment/ansible/; ansible-playbook app.yml

pre_commit_all:
	pre-commit install
	pre-commit run --all-files

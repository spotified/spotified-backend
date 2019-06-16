SHELL := /bin/sh

PROJECT := config
PROJECT_DIR := $(abspath $(shell pwd))

deploy_production:
	cd ../spotified-frontend/ && git pull && yarn install && npm run build
	rm -r var/static/*; cp -r ../spotified-frontend/build/* var/static;
	./manage.py collectstatic_js_reverse
	cd deployment/ansible/ && ansible-playbook app.yml
	rsync -azv --delete --rsh=ssh var/static/* root@reverse-proxy-1.spotified.403.io:/opt/spotified/
	git push;

pre_commit_all:
	pre-commit install
	pre-commit run --all-files

test:
	coverage run manage.py test --parallel
	coverage report
	coverage erase

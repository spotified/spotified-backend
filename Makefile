SHELL := /bin/sh

PROJECT := config
PROJECT_DIR := $(abspath $(shell pwd))

deploy_production:
	./manage.py test --parallel
	cd ../spotified-frontend/ && git pull && yarn install && npm run build
	rm -r var/static/*; cp -r ../spotified-frontend/build/* var/static;
	./manage.py collectstatic_js_reverse
	git checkout master && git merge develop && git push && git checkout develop
	cd deployment/ansible/ && ansible-playbook app.yml
	rsync -azv --delete --rsh=ssh var/static/* root@reverse-proxy-1.spotified.403.io:/opt/spotified/

pre_commit_all:
	pre-commit install
	pre-commit run --all-files

test:
	coverage erase
	coverage run --parallel-mode --concurrency=multiprocessing manage.py test --parallel
	coverage combine
	coverage report
	coverage erase

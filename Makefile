.PHONY: docs
SHELL := /bin/bash
.DEFAULT_GOAL := help-default

DOCKERS := $$(docker ps -a -q)
IMAGES := $$(docker images -f "dangling=true" -q)
IMAGES_ALL := $$(docker images)
APP := emenu

define PRINT_HELP_PYSCRIPT
import re, sys
for line in sorted(sys.stdin):
    match = re.match(r'^([a-zA-Z_-]+).*?:.*?##(.*)$$', line)
    if match:
        target, help = match.groups()
        print(f'${GREEN}{target :33s}${NC} ${YELLOW}{help}${NC}')
endef
export PRINT_HELP_PYSCRIPT


init:
	pipenv shell

clean:
	@- docker rm $(APP) -f

help-default:
	@-python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

docker-rmi:  ##  Usuwa błedne obrazy dockera
	@-docker rmi $(IMAGES) -f

docker-rmi-all:  ##  Usuwa błedne obrazy dockera
	@-docker rmi $(IMAGES_ALL) -f

docker-rm:  ##  Usuwa contenery
	@-docker stop ${DOCKERS}
	@-docker rm ${DOCKERS} -f

docker-volumes-down:  ##  Usuwa volumeny
	docker-compose down --volumes

docker-networks-down:  ##  Usuwa netw
	docker-compose down --networks

start-build:  ##  Start Build
	@- export COMPOSE_HTTP_TIMEOUT=10 && docker-compose up -d --build --remove-orphans

start: clean  ##  Start
	@- export COMPOSE_HTTP_TIMEOUT=100 && docker-compose up -d --remove-orphans

stop: clean  ##  Stop
	@- docker-compose stop

#!/usr/bin/make
#
lo_version="7.3"

args = $(filter-out $@,$(MAKECMDGOALS))

all: run
py:=3.9

.PHONY: bootstrap buildout run test cleanall startlibreoffice stoplibreoffice
bootstrap:
	virtualenv -p python$(py) .
	bin/pip install -r requirements.txt

buildout:
	if ! test -f bin/buildout;then make bootstrap;fi
	bin/buildout -Nt 5

run:
	if ! test -f bin/instance;then make buildout;fi
	mkdir -p var/tmp
	make startlibreoffice
	bin/instance fg

test:
	if ! test -f bin/test;then make buildout;fi
	make startlibreoffice
	rm -fr htmlcov
	bin/translation-manage -c
	if test -z "$(args)" ;then bin/test;else bin/test -t $(args);fi
	make stoplibreoffice

cleanall:
	rm -fr bin develop-eggs devel htmlcov include .installed.cfg lib .mr.developer.cfg parts downloads eggs local

startlibreoffice:
	make stoplibreoffice
	docker run -p 2002:2002\
 			   -d \
 			   --rm \
 			   --pull always \
 			   --name="oo_server" \
 			   -v /tmp:/tmp \
 			   -v /var/tmp:/var/tmp \
 			   harbor.imio.be/library/libreoffice:$(lo_version)
	docker ps

stoplibreoffice:
	if docker ps | grep oo_server;then docker stop oo_server;fi

SHELL   := /bin/bash
VERSION := $(shell cat VERSION)
NULL    := /dev/null



all: test


test:
	# python setup.py test -- it does not wokr in python 2.7
	python -m unittest discover -p "test*.py"

clean:
	@rm -rf build dev_mapper.egg-info
	@(find . -name "*.pyc" -exec rm -rf {} \; 2>$(NULL) || true)
	@(find . -name __pycache__ -exec rm -rf {} \; 2>$(NULL) || true)


build: test
	python setup.py sdist bdist_wheel


upload:
	python -m twine upload \
	    dist/dev_mapper-$(VERSION).tar.gz \
	    dist/dev_mapper-$(VERSION)-py2-none-any.whl \
	    dist/dev_mapper-$(VERSION)-py3-none-any.whl

freeze:
	pip freeze > requirement.txt


.PHONY: test clean build upload freeze

SHELL   := /bin/bash
VERSION := $(shell cat VERSION)



all: test


test:
	python -m unittest discover -p "test_*.py"

clean:
	rm -rf build dev_mapper.egg-info dist/*


build:
	python setup.py sdist bdist_wheel


upload:
	python -m twine upload \
	    dist/dev_mapper-$(VERSION)-py2-none-any.whl \
	    dist/dev_mapper-$(VERSION)-py3-none-any.whl


.PHONY: test clean build build.27 build.36 upload.27

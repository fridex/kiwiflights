# Makefile for kiwiflights
# 2016 Fridolin Pokorny <fridex.devel@gmail.com>

TEMPFILE := $(shell mktemp -u)

.PHONY: install clean uninstall venv check devenv test

install:
	pip3 install -r requirements.txt
	python3 setup.py install

uninstall:
	python3 setup.py install --record ${TEMPFILE}
	cat ${TEMPFILE} | xargs rm -rf
	rm -f ${TEMPFILE}

check:
	@# set timeout so we do not wait in infinite loops and such
	py.test -vvl --timeout=2 test
	pylint kiwiflights || true  # ignore pylint, it's not configured as I would like to have it

devenv:
	@echo "Installing latest development requirements"
	pip3 install -U -r dev_requirements.txt

venv:
	python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt
	@echo "Run 'source venv/bin/activate' to enter virtual environment and 'deactivate' to return from it"

clean:
	rm -rf venv build dist kiwiflights.egg-info
	find . -name '*.pyc' -or -name '__pycache__' -print0 | xargs -0 rm -rf

test: check


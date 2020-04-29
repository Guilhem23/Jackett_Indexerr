.PHONY: clean clean-dist clean-build build help

# ==================================================================================================
# Variables
# ==================================================================================================

PACKAGE_NAME=Jackett_Indexerr
EXECUTABLE_NAME:=add_indexer.py

PIPENV:=pipenv
PYTHON:=$(shell which python3)
PIP:=$(PYTHON) -m pip
PIPENV_LOCK_ARGS:= --deploy --ignore-pipfile

PIPENV_VERSION=2018.11.26
PIP_VERSION=20.1

SHELL:=/bin/bash


# ==================================================================================================
# General Functions
# ==================================================================================================

define BROWSER_PYSCRIPT
import os, webbrowser, sys
from urllib.request import pathname2url
webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python3 -c "$$BROWSER_PYSCRIPT"

define PRINT_HELP_PYSCRIPT
import re, sys
for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-30s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


# ==================================================================================================
# help target
# ==================================================================================================

help:  ## This help message
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


# ==================================================================================================
# do-it-all targets
# ==================================================================================================


dev: ensure-pipenv mk-venv pipenv-install-dev requirements  ## Setup dev environment

# ==================================================================================================
# Install targets
# ==================================================================================================

ensure-pipenv:
	$(PIP) install --user --upgrade 'pipenv==$(PIPENV_VERSION)' 'pip==$(PIP_VERSION)'
	@echo "NOTE: ensure your local python install is in your PATH"

pipenv-install-dev:
	# Do not use destructive "--python" or "--three" option if the venv already exists
	# See https://github.com/pypa/pipenv/issues/349
	$(pipenv --venv) \
	if [ $$? -eq 0 ]; then \
		echo "$(PIPENV) install --dev $(PIPENV_LOCK_ARGS)" ; \
		$(PIPENV) install --dev $(PIPENV_LOCK_ARGS) ; \
	else \
		echo "$(PIPENV) install --dev $(PIPENV_LOCK_ARGS) --python $(PYTHON)" ; \
		$(PIPENV) install --dev $(PIPENV_LOCK_ARGS) --python $(PYTHON) ; \
	fi
	$(PIPENV) run pip install -e .

mk-venv: clean-venv
	# use that to configure a symbolic link to the virtualenv in .venv
	mkdir -p .venv

.venv: mk-venv

clean-venv:
	@rm -fr .venv

install-local: install-local-only-deps install-local-only-curpackage

install-local-only-deps:
	# Install only dependencies
	$(PIPENV) install $(PIPENV_LOCK_ARGS)

install-local-only-curpackage:
	# Install current package as well
	$(PIPENV) run pip install .

install-system-only-deps:
	# Do not use --system, it may break on pip updates
	$(PIPENV) install --deploy $(PIPENV_LOCK_ARGS)

install-system-only-curpackage:
	$(PIPENV) run pip install .

pipenv-install:  ## Use it for the first install or update method
	if [ -f Pipfile.lock ]; then \
		$(PIPENV) install --dev --ignore-pipfile; \
	else \
		$(PIPENV) install --dev --skip-lock; \
	fi;
	$(PIPENV) run pip install -e .

pipenv-install-inspect:
	$(PIPENV) install --skip-lock --dev
	$(PIPENV) graph


# ==================================================================================================
# Misc targets
# ==================================================================================================

shell:
	$(PIPENV) shell

update: clean-pipenv mk-venv pipenv-update pipenv-install-dev requirements  ## Update dependencies

pipenv-update:
	$(PIPENV) update --clear

requirements:
	# freeze requirements from lock file for applications, for information purpose
	$(PIPENV) run pipenv_to_requirements
	$(PIPENV) run pipenv_to_requirements --freeze --output requirements.txt


lock:
	$(PIPENV) lock --clear


# ==================================================================================================
# Clean targets
# ==================================================================================================

clean: clean-dist clean-venv clean-pipenv  ## Clean environment
	find . -name '__pycache__'  -exec rm -rf {} \; || true
	find . -name '.cache'  -exec rm -rf {} \; || true
	find . -name '*.egg-info'  -exec rm -rf {} \; || true
	find . -name "*.pyc" -exec rm -f {} \; || true
	rm -rf .pytest_cache || true

clean-pipenv:
	$(PIPENV) --rm || true


# ==================================================================================================
# Run targets
# ==================================================================================================

run:
	# add you run commands here
	$(PIPENV) run python $(EXECUTABLE_NAME)



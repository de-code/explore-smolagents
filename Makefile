#!/usr/bin/make -f

VENV = venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python

MODEL_ID = ollama_chat/llama3.2


venv-clean:
	@if [ -d "$(VENV)" ]; then \
		rm -rf "$(VENV)"; \
	fi

venv-create:
	python3 -m venv $(VENV)

dev-install:
	$(PIP) install --disable-pip-version-check -r requirements.build.txt
	$(PIP) install --disable-pip-version-check \
		-r requirements.txt \
		-r requirements.dev.txt

dev-venv: venv-create dev-install


dev-flake8:
	$(PYTHON) -m flake8 explore_smolagents

dev-pylint:
	$(PYTHON) -m pylint explore_smolagents

dev-mypy:
	$(PYTHON) -m mypy --check-untyped-defs explore_smolagents

dev-lint: dev-flake8 dev-pylint dev-mypy


dev-run:
	$(PYTHON) -m explore_smolagents \
		--model-id=$(MODEL_ID)

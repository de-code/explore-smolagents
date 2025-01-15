#!/usr/bin/make -f

VENV = venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python

MODEL_TYPE = litellm
MODEL_ID = ollama_chat/llama3.2
API_BASE =
API_KEY =


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


dev-start-telemetry-server:
	$(PYTHON) -m phoenix.server.main serve


dev-run:
	$(PYTHON) -m explore_smolagents \
		--model-type=$(MODEL_TYPE) \
		--model-id=$(MODEL_ID) \
		--api-base=$(API_BASE) \
		--api-key=$(API_KEY)


dev-run-with-telemetry:
	$(PYTHON) -m explore_smolagents \
		--model-type=$(MODEL_TYPE) \
		--model-id=$(MODEL_ID) \
		--api-base=$(API_BASE) \
		--api-key=$(API_KEY) \
		--otlp-endpoint="http://0.0.0.0:6006/v1/traces"

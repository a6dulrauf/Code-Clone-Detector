VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: setup web cli demo desktop test docker

setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt -r requirements-dev.txt
	$(PY) -m nltk.downloader -d $(VENV)/nltk_data punkt punkt_tab
	$(PY) manage.py migrate
	$(PY) manage.py seed_demo

web:
	$(PY) manage.py runserver

cli:
	$(PY) cli.py $(ARGS)

demo:
	$(PY) cli.py demo

desktop:
	$(PIP) install -r requirements-desktop.txt
	$(PY) desktop.py

test:
	$(PY) -m pytest -v

docker:
	docker build -t ccd-web . && docker run --rm -e PORT=8000 -e ALLOWED_HOSTS=localhost,127.0.0.1 -p 8000:8000 ccd-web

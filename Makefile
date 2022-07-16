venv_dir = .venv
venv_activate = . $(venv_dir)/bin/activate


install: venv_setup poetry_install
	poetry install

venv_setup:
	python3.10 -m venv $(venv_dir)

poetry_install:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

run:
	poetry run python3 app/app.py

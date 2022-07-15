venv_dir = .venv
venv_activate = . $(venv_dir)/bin/activate


install: venv_setup
	poetry install

venv_setup:
	python3.10 -m venv $(venv_dir)

run:
	poetry run python3 app/app.py

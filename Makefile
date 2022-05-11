.PHONY: test lint

default:
	lint test

pip:
	pip install pip-tools
	pip-compile
	pip-compile dev-requirements.in
	pip-sync dev-requirements.txt requirements.txt

lint:
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

test:
	pytest tests
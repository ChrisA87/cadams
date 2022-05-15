.PHONY: test lint

default: lint test

pip:
	pip install pip-tools
	pip-compile
	pip-compile dev-requirements.in
	pip-sync dev-requirements.txt requirements.txt

lint:
	flake8 . --count --max-complexity=10 --max-line-length=127 --statistics

test:
	coverage run --source app -m pytest tests
	coverage report

make docker-build:
	docker build -t chrisa87/cadams .

make docker-run:
	docker run -p 8000:8000 --rm chrisa87/cadams

make docker: docker-build docker-run
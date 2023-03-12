.PHONY: test lint docker-build docker-run

default: lint test

pip:
	pip install pip-tools
	pip-compile requirements/requirements.in
	pip-compile requirements/dev-requirements.in
	pip-sync requirements/dev-requirements.txt requirements/requirements.txt

lint:
	flake8 . --count --max-complexity=10 --max-line-length=127 --statistics

test:
	coverage run --source app -m pytest tests
	coverage report

docker-build:
	docker build -t chrisa87/cadams .

docker-run:
	docker run -v "$$(pwd)/data-dev.sqlite:/app/data-dev.sqlite" -p 8000:8000 --name cadams-web --rm chrisa87/cadams

docker: docker-build docker-run

run:
	export FLASK_APP=run_app.py; flask run --reload

db-init:
	export FLASK_APP=run_app.py; \
	export PYTHONPATH=".:$$PYTHONPATH"; \
	flask db upgrade; \
	python app/db/setup.py;

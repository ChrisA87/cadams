FROM python:3.10.0-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements/requirements.txt --no-cache-dir

RUN python -m nltk.downloader brown

ENV FLASK_APP run_app.py

ENTRYPOINT [ "gunicorn", "--worker-tmp-dir", "/dev/shm", "--config", "gunicorn_config.py", "run_app:app"]

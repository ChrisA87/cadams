FROM python:3.10.0

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# gunicorn --worker-tmp-dir /dev/shm --config gunicorn_config.py app.app:app
ENTRYPOINT [ "gunicorn", "--worker-tmp-dir", "/dev/shm", "--config", "gunicorn_config.py", "app.app:app"]

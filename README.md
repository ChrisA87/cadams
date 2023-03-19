# Cadams

Source code for [https://cadams.tech](https://cadams.tech)

## Initial Setup
Create and activate a new python [virtualenv](https://pypi.org/project/virtualenv/) with python **3.10.0** interpreter, then to install dependencies and setup the database run:
```
make pip
make db-init
```

then either run **locally** at http://127.0.0.1:5000

```
make run
```

or build and run with **Docker** at http://127.0.0.1:8000

```
make docker
```

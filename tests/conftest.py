import pytest
from app import create_app, db
from app.models.users import User
from app.models.roles import Role


@pytest.fixture
def app():
    app = create_app('test')
    app.config["TESTING"] = True
    yield app


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture
def test_db(app):
    context = app.app_context()
    context.push()
    db.create_all()

    # Import test data
    for name in ['John', 'David', 'Gillian', 'Chris']:
        db.session.add(User(name=name))
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()
    context.pop()

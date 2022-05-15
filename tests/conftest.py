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
def list_users():
    yield [
        User(name='John', password='cat'),
        User(name='Susan', password='dog'),
        User(name='Bob', password='rabbit')
    ]


@pytest.fixture
def test_db(app, list_users):
    context = app.app_context()
    context.push()
    db.create_all()

    # Import test data
    db.session.add_all(list_users)
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()
    context.pop()

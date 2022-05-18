import pytest
from app import create_app, db
from app.models.users import User
from app.models.roles import Role


@pytest.fixture(scope='module')
def app():
    app = create_app('test')
    app.config["TESTING"] = True
    app.app_context().push()
    yield app


@pytest.fixture(scope='module')
def client(app):
    yield app.test_client(use_cookies=True)


@pytest.fixture(scope='module')
def list_users():
    yield [
        User(username='John', email='john@example.com', password='cat', id=1),
        User(username='Susan', email='susan@example.com', password='dog', id=2),
        User(username='Bob', email='bob@example.com', password='rabbit', id=3)
    ]


@pytest.fixture(scope='module')
def test_db(app, list_users):
    db.create_all()

    # Import test data
    db.session.add_all(list_users)
    db.session.commit()
    Role.insert_roles()

    yield db

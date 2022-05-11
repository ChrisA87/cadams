import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app('test')
    app.config["TESTING"] = True
    yield app


@pytest.fixture
def client(app):
    yield app.test_client()


def test_get_index_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Check back soon" in response.data

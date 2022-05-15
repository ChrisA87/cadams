import pytest


def test_get_index_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Check back soon" in response.data


def test_get_test_returns_200(client):
    response = client.get('/test')
    assert response.status_code == 200
    assert b"What is your name" in response.data


def test_post_test_returns_200__no_name(client):
    response = client.post('/test', data={'name': 'test'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'What is your name?' in response.data


def test_post_test_returns_200__with_name(client):
    with client.session_transaction() as sess:
        sess['name'] = 'test'
    response = client.post('/test', data={'name': 'test'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Hey test!' in response.data

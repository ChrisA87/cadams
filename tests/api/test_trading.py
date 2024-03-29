import pytest


def test_api_docs__returns_200(client):
    response = client.get('/api/v1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Cadams APIs' in response.data


def test_health__returns_200(client):
    response = client.get('api/v1/trading/health', follow_redirects=True)
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_stocks__not_authorised_returns_401(client):
    response = client.get('api/v1/trading/stocks', follow_redirects=True)
    assert response.status_code == 401
    assert b'The server could not verify that you are authorized' in response.data


def test_stocks__authorised_public_key_returns_200(client, test_db):
    response = client.get(
        'api/v1/trading/stocks',
        follow_redirects=True,
        headers={'x-api-key': 'public-test-key'})
    assert response.status_code == 200


def test_stock_symbol__not_authorised_returns_401(client):
    response = client.get('api/v1/trading/stock/CADM', follow_redirects=True)
    assert response.status_code == 401
    assert b'The server could not verify that you are authorized' in response.data


def test_stocks__authorised_private_key_returns_200(client, test_db, list_users):
    # Logged in admin user
    *_, admin_user = list_users
    client.post('/auth/login', data={'username': admin_user.username, 'password': 'rabbit'},
                follow_redirects=True)

    response = client.get(
        'api/v1/trading/stock/CADM',
        follow_redirects=True,
        headers={'x-api-key': 'api-key123'})
    assert response.status_code == 200
    assert response.json['result'] == {'id': 1, 'name': 'Cadams, Inc.', 'symbol': 'CADM', 'last_updated': None}


def test_stocks__authorised_not_found_returns_200(client, test_db, list_users):
    # Logged in admin user
    *_, admin_user = list_users
    client.post('/auth/login', data={'username': admin_user.username, 'password': 'rabbit'},
                follow_redirects=True)

    response = client.get(
        'api/v1/trading/stock/FAKEY',
        follow_redirects=True,
        headers={'x-api-key': 'api-key123'})
    assert response.status_code == 200
    assert response.json['result'] == {'result': 'not found', 'symbol': 'FAKEY'}


def test_stockprice_symbol__returns_200(client, test_db):
    response = client.get('api/v1/trading/stock-prices/CADM', follow_redirects=True)
    expected_keys = ['id', 'date', 'symbol', 'open', 'close', 'adj_close', 'high', 'low', 'volume']

    assert response.status_code == 200
    assert len(response.json['result']) == 500
    for key in expected_keys:
        assert key in response.json['result'][0]


def test_stockprice_symbol__not_found_returns_200(client, test_db):
    response = client.get('api/v1/trading/stock-prices/FAKEY', follow_redirects=True)

    assert response.status_code == 200
    assert response.json['result'] == {'result': 'not found', 'symbol': 'FAKEY'}


@pytest.mark.parametrize('strategy, payload', [
    ('sma', {'fast': 42, 'slow': 252}),
    ('momentum', {'period': 3}),
    ('mean-reversion', {'sma': 28, 'threshold': 3}),
    ('ols', {'lags': 7})
])
def test_strategy_suggestion__returns_200(client, test_db, list_users, strategy, payload):
    # Logged in admin user
    *_, admin_user = list_users
    client.post('/auth/login', data={'username': admin_user.username, 'password': 'rabbit'},
                follow_redirects=True)

    response = client.post(f'api/v1/trading/strategy/{strategy}/CADM', json=payload)
    assert response.status_code == 200

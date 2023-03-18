
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
    assert response.json['result'] == [
        {'id': 1, 'name': 'Cadams, Inc.', 'symbol': 'CADM', 'last_updated': None},
        {'id': 2, 'name': 'Apple, Inc.', 'symbol': 'AAPL', 'last_updated': None},
        {'id': 3, 'name': 'Microsoft Corporation', 'symbol': 'MSFT', 'last_updated': None},
        {'id': 4, 'name': 'Amazon.com, Inc.', 'symbol': 'AMZN', 'last_updated': None},
        {'id': 5, 'name': 'Euro / US Dollar Rate', 'symbol': 'EURUSD=X', 'last_updated': None},
        {'id': 6, 'name': 'VanEck Gold Miners ETF', 'symbol': 'GDX', 'last_updated': None},
        {'id': 7, 'name': 'SPDR Gold Trust', 'symbol': 'GLD', 'last_updated': None}]


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

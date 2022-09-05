##################################################################################
# Stocks
def test_get_sample_stocks_returns_200(client, test_db):
    response = client.get('/sample-stocks')
    assert response.status_code == 200
    assert b"Stocks" in response.data
    assert b"These are some sample stocks" in response.data


def test_valid_get_stocks_page_returns_200(client, test_db):
    response = client.get('/stocks/CADM')
    assert response.status_code == 200
    assert b"Cadams, Inc. (CADM) Trading Stategies" in response.data


def test_invalid_get_stocks_page_returns_404(client, test_db):
    response = client.get('/stocks/test')
    assert response.status_code == 404
    assert b"Not Found" in response.data


def test_get_stocks_redirects_to_login__logged_out(client, test_db):
    response = client.get('/stocks', follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data


def test_get_stocks_returns_200__logged_in(client, test_db):
    # Log in
    client.post('auth/login', data={'username': 'John', 'password': 'cat'}, follow_redirects=True)
    response = client.get('/stocks')
    assert response.status_code == 200
    assert b"Stocks" in response.data
    assert b"These are some sample stocks" not in response.data


##################################################################################
# SMA
def test_valid_get_sma_strategy_returns_200(client, test_db):
    response = client.get('/stocks/CADM/simple-moving-average')
    assert response.status_code == 200
    assert b"Simple Moving Average Strategy For CADM" in response.data


def test_valid_post_sma_strategy_returns_200(client, test_db):
    response = client.post('/stocks/CADM/simple-moving-average',
                           data={'fast': 15,
                                 'slow': 100,
                                 'duration': '10Y'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Simple Moving Average Strategy For CADM' in response.data


def test_invalid_post_sma_strategy_flashes_message(client, test_db):
    response = client.post('/stocks/CADM/simple-moving-average',
                           data={'fast': 100,
                                 'slow': 10,
                                 'duration': '10Y'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'invalid input' in response.data


##################################################################################
# Momentum
def test_valid_get_momentum_strategy_returns_200(client, test_db):
    response = client.get('/stocks/CADM/momentum')
    assert response.status_code == 200
    assert b"Momentum Strategy For CADM" in response.data


def test_valid_post_momentum_strategy_returns_200(client, test_db):
    response = client.post('/stocks/CADM/momentum',
                           data={'period': 5,
                                 'duration': '10Y'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Momentum Strategy For CADM' in response.data


##################################################################################
# Mean Reversion
def test_valid_get_mean_reversion_strategy_returns_200(client, test_db):
    response = client.get('/stocks/CADM/mean-reversion')
    assert response.status_code == 200
    assert b"Mean Reversion Strategy For CADM" in response.data


def test_valid_post_mean_reversion_strategy_returns_200(client, test_db):
    response = client.post('/stocks/CADM/mean-reversion',
                           data={'sma': 15,
                                 'threshold': 7.5,
                                 'duration': '10Y'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Mean Reversion Strategy For CADM' in response.data

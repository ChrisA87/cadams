
def test_get_stocks_returns_200(client, test_db):
    response = client.get('/sample-stocks')
    assert response.status_code == 200
    assert b"Stocks" in response.data


def test_valid_get_stocks_page_returns_200(client, test_db):
    response = client.get('/stocks/CADM')
    assert response.status_code == 200
    assert b"Cadams, Inc. (CADM) Trading Stategies" in response.data


def test_invalid_get_stocks_page_returns_404(client, test_db):
    response = client.get('/stocks/test')
    assert response.status_code == 404
    assert b"Not Found" in response.data


def test_valid_get_sma_strategy_returns_200(client, test_db):
    response = client.get('/stocks/CADM/simple-moving-average')
    assert response.status_code == 200
    assert b"Simple Moving Average Strategy For CADM" in response.data


def test_valid_get_momentum_strategy_returns_200(client, test_db):
    response = client.get('/stocks/CADM/momentum')
    assert response.status_code == 200
    assert b"Momentum Strategy For CADM" in response.data


def test_valid_get_mean_reversion_strategy_returns_200(client, test_db):
    response = client.get('/stocks/CADM/mean-reversion')
    assert response.status_code == 200
    assert b"Mean Reversion Strategy For CADM" in response.data

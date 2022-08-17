
def test_get_index_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Check back soon" in response.data


def test_get_stocks_returns_200(client, test_db):
    response = client.get('/sample-stocks')
    assert response.status_code == 200
    assert b"Stocks" in response.data


def test_valid_get_stocks_plot_returns_200(client, test_db):
    response = client.get('/stocks/CADM')
    assert response.status_code == 200
    assert b"Trading Strategy For CADM" in response.data


def test_invalid_get_stocks_plot_returns_404(client, test_db):
    response = client.get('/stocks/test')
    assert response.status_code == 404
    assert b"Not Found" in response.data


def test_get_index_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Check back soon" in response.data


def test_get_stocks_returns_200(client):
    response = client.get('/stocks')
    assert response.status_code == 200
    assert b"Available Stocks" in response.data


def test_get_stocks_plot_returns_200(client):
    response = client.get('/stocks/test')
    assert response.status_code == 200
    assert b"Trading Strategy For TEST" in response.data

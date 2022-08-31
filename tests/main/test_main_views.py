
def test_get_index_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Check back soon" in response.data

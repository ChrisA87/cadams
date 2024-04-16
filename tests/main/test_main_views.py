def test_get_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Trading Ideas" in response.data


def test_get_about_returns_200(client):
    response = client.get("/about-me")
    assert response.status_code == 200
    assert b"About" in response.data

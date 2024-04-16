def test_wordle_suggestions__unauthorized_returns_401(client):
    response = client.post(
        "/api/v1/wordle/suggest",
        json={"pattern": "___", "exclude_letters": "e", "include_letters": "a"},
        follow_redirects=True,
    )
    assert response.status_code == 401
    assert b"The server could not verify that you are authorized" in response.data


def test_wordle_suggestions__authorized_valid_returns_200(client, list_users, test_db):
    # Logged in admin user
    *_, admin_user = list_users
    client.post(
        "/auth/login",
        data={"username": admin_user.username, "password": "rabbit"},
        follow_redirects=True,
    )

    response = client.post(
        "/api/v1/wordle/suggest",
        json={"pattern": "___", "exclude_letters": "e", "include_letters": "a"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert response.json["result"]
    for value in response.json["result"]:
        assert len(value) == 3
        assert "e" not in value
        assert "a" in value

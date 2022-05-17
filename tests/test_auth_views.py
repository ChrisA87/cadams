
def test_get_login_returns_200(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b"Log In" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data


def test_get_register_returns_200(client):
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b"Sign Up" in response.data
    assert b"Username" in response.data
    assert b"Confirm Password" in response.data


def test_post_register_returns_returns_302(client, test_db):
    response = client.post('/auth/register',
                           data={'username': 'joe',
                                 'email': 'joe@example.com',
                                 'password': 'foo',
                                 'password2': 'foo'},
                           follow_redirects=False)
    assert response.status_code == 302


def test_post_register_returns_returns_200__username_taken(client, test_db):
    client.post('/auth/register',
                data={'username': 'joe',
                      'email': 'joe@example.com',
                      'password': 'foo',
                      'password2': 'foo'},
                      follow_redirects=True)
    response = client.post('/auth/register',
                           data={'username': 'joe',
                                 'email': 'joe@example.com',
                                 'password': 'foo',
                                 'password2': 'foo'},
                           follow_redirects=True)
    print(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert b'Username is already taken' in response.data


def test_logout_when_not_logged_in(client, test_db):
    response = client.get('/auth/logout', follow_redirects=True)
    print(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert b'Please log in to access this page' in response.data


def test_post_login_returns_200__valid(client, test_db):
    response = client.post('/auth/login', data={'username': 'John', 'password': 'cat'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome Back John' in response.data


def test_post_login_returns_200__invalid(client, test_db):
    response = client.post('/auth/login', data={'username': 'John', 'password': 'wrong-password'}, follow_redirects=True)
    print(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data


def test_logout_when_logged_in(client, test_db):
    client.post('auth/login', data={'username': 'John', 'password': 'cat'}, follow_redirects=True)
    response = client.get('/auth/logout', follow_redirects=True)
    print(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert b'You have been logged out' in response.data

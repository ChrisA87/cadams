from app.models.users import User


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


def test_post_register_returns_302(client, test_db):
    response = client.post('/auth/register',
                           data={'username': 'joe',
                                 'email': 'joe@example.com',
                                 'password': 'foo',
                                 'password2': 'foo'},
                           follow_redirects=False)
    assert response.status_code == 302


def test_post_register_returns_200__username_taken(client, test_db):
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


def test_user_confirm_token__valid(client, test_db):
    # Register new user
    new_user = User(username='steve', password='password1', email='steve@test.com')
    client.post('/auth/register',
                data={'username': new_user.username,
                      'email': new_user.email,
                      'password': 'password1',
                      'password2': 'password1'},
                follow_redirects=True)

    # Login
    client.post('/auth/login', data={'username': new_user.username, 'password': 'password1'},
                follow_redirects=False)

    # Verify account
    token = new_user.generate_verify_token()
    response = client.get(f'auth/verify/{token}', follow_redirects=True)
    assert response.status_code == 200


def test_user_confirm_token__invalid(client, test_db):
    # Register new user
    new_user = User(username='Billy', password='bar', email='billy@test.com')
    client.post('/auth/register',
                data={'username': new_user.username,
                      'email': new_user.email,
                      'password': 'bar',
                      'password2': 'bar'},
                follow_redirects=True)

    # Login
    client.post('/auth/login', data={'username': new_user.username, 'password': 'bar'},
                follow_redirects=False)

    # Verify account
    existing_user = User.query.first()
    token = existing_user.generate_verify_token()
    response = client.get(f'auth/verify/{token}', follow_redirects=True)
    assert response.status_code == 200
    assert b'The confirmation link is invalid' in response.data


def test_admin_page__not_logged_in_redirected_to_login(client, test_db):
    response = client.get('/auth/admin', follow_redirects=True)
    assert response.status_code == 200
    assert b'Log In' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


def test_admin_page__logged_in_but_not_admin_redirected_to_login(client, test_db, list_users):
    non_admin, *_ = list_users
    client.post('/auth/login', data={'username': non_admin.username, 'password': 'cat'},
                follow_redirects=True)
    response = client.get('/auth/admin', follow_redirects=True)
    assert response.status_code == 200
    assert b'Log In' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


def test_admin_page__logged_in_admin_user_gets_admin_panel(client, test_db, list_users):
    *_, admin_user = list_users
    client.post('/auth/login', data={'username': admin_user.username, 'password': 'rabbit'},
                follow_redirects=True)

    response = client.get('/auth/admin', follow_redirects=True)
    assert response.status_code == 200
    assert b'Home - Admin' in response.data

    response = client.get('/auth/admin/user', follow_redirects=True)
    assert response.status_code == 200
    for user in list_users:
        assert user.email.encode() in response.data

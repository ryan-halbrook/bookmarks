from bookmarks.db import get_cursor
from werkzeug.security import check_password_hash
from tests.headers import request_headers, unauthorized_test


def test_add_user(client, app):
    email = 'bob@example.com'
    password = '1234'
    post_json = {
        'email': email,
        'password': password
    }
    response = client.post('/users', json=post_json)
    assert response.status_code == 200
    assert response.json['email'] == email

    with app.app_context():
        cur = get_cursor()
        cur.execute(
            'SELECT id, password FROM users WHERE username = %s',
            (email,))
        result = cur.fetchone()
        cur.close()
        assert check_password_hash(result['password'], password)

    # Email taken
    new_user = {
        'email': email,
        'password': '5678'
    }
    response = client.post('/users', json=new_user)
    assert response.status_code == 422

    # Check password is not changed
    with app.app_context():
        cur = get_cursor()
        cur.execute(
            'SELECT id, password FROM users WHERE username = %s',
            (email,))
        result = cur.fetchone()
        cur.close()
    assert check_password_hash(result['password'], password)


def test_update_user(client, app, authenticated_user):
    # Change email and password
    new_email = 'newemail@example.com'
    new_password = 'newpassword'
    new_json = {
        'email': new_email,
        'password': new_password,
    }
    response = client.put('/users', json=new_json,
                          headers=request_headers(authenticated_user))
    assert response.status_code == 200
    assert response.json['email'] == new_email

    with app.app_context():
        cur = get_cursor()
        cur.execute(
            'SELECT password FROM users WHERE username = %s',
            (new_email,))
        result = cur.fetchone()
        cur.close()
        assert check_password_hash(result['password'], new_password)


def test_update_user_unauthorized(client, app):
    unauthorized_test(client, '/users', method='PUT',
                      json={'email': 'update@example.com'},
                      test_other_user=False)


def test_login_user(client, app):
    # Create the user
    email = 'bob@example.com'
    password = '1234'
    post_json = {
        'email': email,
        'password': password
    }
    response = client.post('/users', json=post_json)
    assert response.status_code == 200
    assert response.json['email'] == email

    # Login
    response = client.post('/users/login', json=post_json)
    assert response.status_code == 200
    assert response.json['token']

    wrong_password = {
        'email': email,
        'password': '5678'
    }
    response = client.post('/users/login', json=wrong_password)
    assert response.status_code == 401

    wrong_email = {
        'email': 'alice@example.com',
        'password': password
    }
    response = client.post('/users/login', json=wrong_email)
    assert response.status_code == 401

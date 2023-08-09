from bookmarks.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash


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
    user_id = response.json['id']

    with app.app_context():
        result = get_db().execute(
            'SELECT id, password FROM users WHERE id = ?', (user_id,)).fetchone()
    assert check_password_hash(result['password'], password)


def test_update_user(client, app):
    email = 'bob@example.com'
    password = '1234'
    post_json = {
        'email': email,
        'password': password
    }
    response = client.post('/users', json=post_json)
    assert response.status_code == 200

    response = client.post('/users/login', json=post_json)
    assert response.status_code == 200

    new_email = 'alice@example.com'
    new_password = '5678'
    new_json = {
        'email': new_email,
        'password': new_password,
        'token': response.json['token']
    }
    response = client.put('/users', json=new_json)
    assert response.status_code == 200
    assert response.json['email'] == new_email
    user_id = response.json['id']

    with app.app_context():
        result = get_db().execute(
            'SELECT password FROM users WHERE id = ?',
            (user_id,)).fetchone()
    assert check_password_hash(result['password'], new_password)


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
    user_id = response.json['id']

    # Login
    response = client.post('/users/login', json=post_json)
    assert response.status_code == 200
    assert response.json['id'] == user_id
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

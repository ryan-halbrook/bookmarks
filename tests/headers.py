import jwt


def request_headers(authenticated_user):
    return {'Authorization': 'bearer ' + authenticated_user.user_token.token}


def invalid_auth_headers():
    invalid_token = jwt.encode(
        {'user': 'nil@example.com'}, 'secret', algorithm='HS256')
    return {'Authorization': 'bearer ' + invalid_token}


def other_user_headers(client):
    new_user_name = 'newuser@example.com'
    new_user = {
        'email': new_user_name,
        'password': 'newuser'
    }
    client.post('/users', json=new_user)
    response = client.post('/users/login', json=new_user)
    new_user_token = response.json['token']
    new_user_headers = {'Authorization': 'bearer ' + new_user_token}
    return new_user_headers


def unauthorized_test(client, url, method='GET',
                      json=None, test_other_user=True):
    # No auth header
    response = client.open(url, method=method, json=json)
    assert response.status_code == 401

    if test_other_user:
        response = client.open(
            url,
            method=method,
            json=json,
            headers=other_user_headers(client))
        assert response.status_code == 404

    # Invalid authorization
    response = client.open(
        url,
        method=method,
        json=json,
        headers=invalid_auth_headers())
    assert response.status_code == 401

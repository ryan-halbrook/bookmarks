from bookmarks.db import get_cursor
from tests.headers import request_headers, unauthorized_test


def test_create(client, app, authenticated_user):
    name = 'New test collection'
    response = client.post(
        '/collections',
        json={'name': name},
        headers=request_headers(authenticated_user))

    assert response.status_code == 200
    assert response.json['name'] == name
    assert response.json['user_id'] == authenticated_user.user.id

    # name field missing in json
    response = client.post(
        '/collections',
        json={'nameX': name},
        headers=request_headers(authenticated_user))
    assert response.status_code == 400


def test_create_unauthorized(client, app):
    name = 'New test collection'
    unauthorized_test(client, '/collections', method='POST',
                      json={'name': name}, test_other_user=False)

    # Check database
    with app.app_context():
        query = 'SELECT COUNT(id) FROM collections WHERE name=%s'
        cur = get_cursor()
        cur.execute(query, (name,))
        count = cur.fetchone()[0]
        cur.close()
        assert count == 0


def test_get(client, app, authenticated_user):
    response = client.get(
        '/collections',
        headers=request_headers(authenticated_user))

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['name'] == 'test collection'
    assert response.json[1]['name'] == 'another collection'


def test_get_unauthorized(client, app):
    unauthorized_test(client, '/collections', test_other_user=False)

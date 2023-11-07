from bookmarks.db import get_cursor
from tests.headers import request_headers, unauthorized_test


def example_bookmark(new_type=False):
    return {
        'name': 'new bookmark',
        'type': 'new type' if new_type else 'test type',
        'link': 'http://example.com',
        'description': 'lorem ipsum...'
    }


def test_create(client, app, authenticated_user):
    client.post('/collections/1/bookmarks',
                json=example_bookmark(),
                headers=request_headers(authenticated_user))

    with app.app_context():
        cur = get_cursor()
        cur.execute('SELECT COUNT(id) FROM bookmarks')
        count = cur.fetchone()[0]
        cur.close()
        assert count == 4


def test_create_unauthorized(client, app):
    for use_new_type in [False, True]:
        unauthorized_test(client, '/collections/1/bookmarks',
                          method='POST',
                          json=example_bookmark(new_type=use_new_type))

    # Check database
    with app.app_context():
        query = 'SELECT COUNT(id) FROM bookmarks WHERE name=%s'
        cur = get_cursor()
        cur.execute(query, (example_bookmark()['name'],))
        count = cur.fetchone()[0]
        cur.close()
        assert count == 0


def test_create_with_new_type(client, app, authenticated_user):
    client.post('/collections/1/bookmarks',
                json=example_bookmark(new_type=True),
                headers=request_headers(authenticated_user))

    with app.app_context():
        try:
            cur = get_cursor()
            cur.execute('SELECT COUNT(id) FROM bookmarks')
            count = cur.fetchone()[0]
            assert count == 4
        finally:
            cur.close()


def test_get(client, app, authenticated_user):
    response = client.get('/collections/1/bookmarks',
                          headers=request_headers(authenticated_user))
    assert response.status_code == 200
    assert len(response.json) == 3
    assert 'test bookmark' == response.json[0]['name']
    assert 'another test bookmark' == response.json[1]['name']
    bookmark = response.json[0]
    assert 'id' in bookmark
    assert 'created' in bookmark
    assert 'name' in bookmark
    assert 'link' in bookmark
    assert 'description' in bookmark
    bookmark_type = bookmark['type']
    assert 'id' in bookmark_type
    assert 'name' in bookmark_type


def test_get_unauthorized(client):
    unauthorized_test(client, '/collections/1/bookmarks')


def test_get_by_name(client, authenticated_user):
    response = client.get(
        '/collections/1/bookmarks?query=test%20bookmark&match=name',
        headers=request_headers(authenticated_user))
    assert response.status_code == 200
    print(response.json)
    assert len(response.json) == 2


def test_get_by_name_unauthorized(client):
    unauthorized_test(
        client,
        '/collections/1/bookmarks?query=test%20bookmark&match=name')


def test_get_by_description(client, authenticated_user):
    response = client.get(
        '/collections/1/bookmarks?query=another&match=description',
        headers=request_headers(authenticated_user))
    assert response.status_code == 200
    assert len(response.json) == 2


def test_get_by_description_unauthorized(client):
    unauthorized_test(
        client,
        '/collections/1/bookmarks?query=another&match=description')


def test_get_by_id(client, app, authenticated_user):
    response = client.get('/collections/1/bookmarks/1',
                          headers=request_headers(authenticated_user))
    assert response.status_code == 200
    assert 'test bookmark' == response.json['name']

    response = client.get('/collections/1/bookmarks/2',
                          headers=request_headers(authenticated_user))
    assert response.status_code == 200
    assert 'another test bookmark' == response.json['name']


def test_get_by_id_unauthorized(client):
    unauthorized_test(client, '/collections/1/bookmarks/1')


def test_delete(client, app, authenticated_user):
    client.delete('/collections/1/bookmarks/1',
                  headers=request_headers(authenticated_user))

    with app.app_context():
        try:
            cur = get_cursor()
            cur.execute('SELECT id FROM bookmarks WHERE id=1')
            assert cur.fetchone() is None
        finally:
            cur.close()


def test_delete_unauthorized(client, app):
    unauthorized_test(client, '/collections/1/bookmarks/1', method='DELETE')

    # Check database
    with app.app_context():
        try:
            query = 'SELECT COUNT(id) FROM bookmarks WHERE id=%s'
            cur = get_cursor()
            cur.execute(query, (1,))
            count = cur.fetchone()[0]
            assert count == 1
        finally:
            cur.close()


def test_update(client, app, authenticated_user):
    client.patch(
        '/collections/1/bookmarks/1', json={'name': 'New Name'},
        headers=request_headers(authenticated_user))

    with app.app_context():
        try:
            cur = get_cursor()
            cur.execute('SELECT name FROM bookmarks WHERE id=1')
            result = cur.fetchone()
            assert result['name'] == 'New Name'
        finally:
            cur.close()


def test_update_unauthorized(client, app):
    new_name = 'New Name'
    unauthorized_test(client,
                      '/collections/1/bookmarks/1',
                      'PATCH',
                      json={'name': new_name})

    # Check database
    with app.app_context():
        try:
            cur = get_cursor()
            cur.execute('SELECT COUNT(id) FROM bookmarks WHERE name=%s',
                        (new_name,))
            result = cur.fetchone()[0]
            assert result == 0
        finally:
            cur.close()


def test_update_type(client, app, authenticated_user):
    existing_type = 'another type'
    new_type = 'new type'

    for type_name in [existing_type, new_type]:
        client.patch(
            '/collections/1/bookmarks/1', json={'type': type_name},
            headers=request_headers(authenticated_user))

        with app.app_context():
            try:
                cur = get_cursor()
                cur.execute(
                    'SELECT types.name as type FROM bookmarks,'
                    'types WHERE bookmarks.id=1 AND bookmarks.type_id=types.id'
                    )
                result = cur.fetchone()
                assert result['type'] == type_name
            finally:
                cur.close()

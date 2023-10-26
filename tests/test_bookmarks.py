from bookmarks.db import get_db
from tests.headers import unauthorized_test


def example_bookmark(new_type=False):
    return {
        'name': 'new bookmark',
        'type': 'new type' if new_type else 'test type',
        'link': 'http://example.com',
        'description': 'lorem ipsum...'
    }


def test_create(client, app, authenticated_user):
    client.post(
        '/collections/1/bookmarks', json=example_bookmark(),
        headers={'Authorization': 'bearer ' + authenticated_user.token})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM bookmarks').fetchone()[0]
        assert count == 4


def test_create_unauthorized(client, app):
    for use_new_type in [False, True]:
        unauthorized_test(client, '/collections/1/bookmarks',
                          method='POST',
                          json=example_bookmark(new_type=use_new_type))

    # Check database
    with app.app_context():
        query = 'SELECT COUNT(id) FROM bookmarks WHERE name=?'
        count = get_db().execute(
            query, (example_bookmark()['name'],)).fetchone()[0]
        assert count == 0


def test_create_with_new_type(client, app, authenticated_user):
    client.post(
        '/collections/1/bookmarks', json=example_bookmark(new_type=True),
        headers={'Authorization': 'bearer ' + authenticated_user.token})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM bookmarks').fetchone()[0]
        assert count == 4


def test_get(client, app, authenticated_user):
    response = client.get(
        '/collections/1/bookmarks',
        headers={'Authorization': 'bearer ' + authenticated_user.token})
    assert response.status_code == 200
    assert len(response.json) == 3
    assert 'a third bookmark' == response.json[0]['name']
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
        headers={'Authorization': 'bearer ' + authenticated_user.token})
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
        headers={'Authorization': 'bearer ' + authenticated_user.token})
    assert response.status_code == 200
    assert len(response.json) == 2


def test_get_by_description_unauthorized(client):
    unauthorized_test(
        client,
        '/collections/1/bookmarks?query=another&match=description')


def test_get_by_id(client, app, authenticated_user):
    response = client.get(
        '/collections/1/bookmarks/20',
        headers={'Authorization': 'bearer ' + authenticated_user.token})
    assert response.status_code == 200
    assert 'test bookmark' == response.json['name']

    response = client.get(
        '/collections/1/bookmarks/30',
        headers={'Authorization': 'bearer ' + authenticated_user.token})
    assert response.status_code == 200
    assert 'another test bookmark' == response.json['name']


def test_get_by_id_unauthorized(client):
    unauthorized_test(client, '/collections/1/bookmarks/20')


def test_delete(client, app, authenticated_user):
    client.delete(
        '/collections/1/bookmarks/20',
        headers={'Authorization': 'bearer ' + authenticated_user.token})

    with app.app_context():
        db = get_db()
        assert db.execute(
            'SELECT id FROM bookmarks WHERE id=20').fetchone() is None


def test_delete_unauthorized(client, app):
    unauthorized_test(client, '/collections/1/bookmarks/20', method='DELETE')

    # Check database
    with app.app_context():
        query = 'SELECT COUNT(id) FROM bookmarks WHERE id=?'
        count = get_db().execute(query, (20,)).fetchone()[0]
        assert count == 1


def test_update(client, app, authenticated_user):
    client.patch(
        '/collections/1/bookmarks/20', json={'name': 'New Name'},
        headers={'Authorization': 'bearer ' + authenticated_user.token})

    with app.app_context():
        db = get_db()
        result = db.execute(
            'SELECT name FROM bookmarks WHERE id=20').fetchone()
        assert result['name'] == 'New Name'


def test_update_unauthorized(client, app):
    new_name = 'New Name'
    unauthorized_test(client,
                      '/collections/1/bookmarks/20',
                      'PATCH',
                      json={'name': new_name})

    # Check database
    with app.app_context():
        db = get_db()
        result = db.execute(
            'SELECT COUNT(id) FROM bookmarks WHERE name=?',
            (new_name,)).fetchone()[0]
        assert result == 0


def test_update_type(client, app, authenticated_user):
    existing_type = 'another type'
    new_type = 'new type'

    for type_name in [existing_type, new_type]:
        client.patch(
            '/collections/1/bookmarks/20', json={'type': type_name},
            headers={'Authorization': 'bearer ' + authenticated_user.token})

        with app.app_context():
            db = get_db()
            result = db.execute(
                'SELECT types.name as type FROM bookmarks,'
                'types WHERE bookmarks.id=20 AND bookmarks.type_id=types.id'
                ).fetchone()
            assert result['type'] == type_name

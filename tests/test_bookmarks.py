import pytest
from bookmarks.db import get_db


def test_create(client, app, authenticated_user):
    newBookmark = {
        'name': 'new bookmark',
        'type': 'test type',
        'link': 'http://example.com',
        'description': 'lorem ipsum...'
    }
    client.post(
        '/collections/1/bookmarks', json=newBookmark,
        headers={'Authorization': 'bearer ' + authenticated_user.token})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM bookmarks').fetchone()[0]
        assert count == 4


def test_create_new_type(client, app, authenticated_user):
    newBookmark = {
        'name': 'new bookmark',
        'type': 'new type',
        'link': 'http://example.com',
        'description': 'lorem ipsum...'
    }
    client.post(
        '/collections/1/bookmarks', json=newBookmark,
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


def test_get_by_name(client, authenticated_user):
    response = client.get(
        '/collections/1/bookmarks?query=test%20bookmark&match=name',
        headers={'Authorization': 'bearer ' + authenticated_user.token})
    assert response.status_code == 200
    print(response.json)
    assert len(response.json) == 2


def test_get_by_description(client, authenticated_user):
    response = client.get(
        '/collections/1/bookmarks?query=another&match=description',
        headers={'Authorization': 'bearer ' + authenticated_user.token})
    assert response.status_code == 200
    assert len(response.json) == 2


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


def test_delete(client, app, authenticated_user):
    client.delete(
        '/collections/1/bookmarks/20',
        headers={'Authorization': 'bearer ' + authenticated_user.token})

    with app.app_context():
        db = get_db()
        assert db.execute(
            'SELECT id FROM bookmarks WHERE id=20').fetchone() == None


def test_update(client, app, authenticated_user):
    client.patch(
        '/collections/1/bookmarks/20', json={'name': 'New Name'},
        headers={'Authorization': 'bearer ' + authenticated_user.token})

    with app.app_context():
        db = get_db()
        result = db.execute(
            'SELECT name FROM bookmarks WHERE id=20').fetchone()
        assert result['name'] == 'New Name'


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
                'SELECT types.name as type FROM bookmarks, types WHERE bookmarks.id=20 AND bookmarks.type_id=types.id').fetchone()
            assert result['type'] == type_name

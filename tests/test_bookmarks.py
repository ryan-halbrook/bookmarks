import pytest
from flaskr.db import get_db
import json

def test_create(client, app):
    newBookmark = {
            'name': 'Test Bookmark',
            'type': 'Test Type',
            'link': 'http://example.com',
            'description': 'lorem ipsum...'
            }
    client.post('/bookmarks', json=newBookmark)

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM bookmarks').fetchone()[0]
        assert count == 4


def test_get(client, app):
    response = client.get('/bookmarks')
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


def test_get_by_id(client, app):
    response = client.get('/bookmarks/20')
    assert response.status_code == 200
    assert 'test bookmark' == response.json['name']
    
    response = client.get('/bookmarks/30')
    assert response.status_code == 200
    assert 'another test bookmark' == response.json['name']


def test_delete(client, app):
    client.delete('/bookmarks/20')

    with app.app_context():
        db = get_db()
        assert db.execute('SELECT id FROM bookmarks WHERE id=20').fetchone() == None


def test_update(client, app):
    client.patch('/bookmarks/20', json={
        'name': 'New Name'})

    with app.app_context():
        db = get_db()
        result = db.execute('SELECT name FROM bookmarks WHERE id=20').fetchone()
        assert result['name'] == 'New Name'


from bookmarks.db import get_db
from tests.headers import request_headers, unauthorized_test


def test_get(client, authenticated_user):
    response = client.get('/bookmarks/20/tags',
                          headers=request_headers(authenticated_user))
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['bookmark']['name'] == 'another test bookmark'


def test_get_unauthorized(client):
    unauthorized_test(client, '/bookmarks/20/tags')


def test_delete(client, authenticated_user):
    response = client.delete('/bookmarks/20/tags/40',
                             headers=request_headers(authenticated_user))
    assert response.status_code == 200
    assert len(response.json) == 0


def test_delete_unauthorized(client, app):
    unauthorized_test(client, '/bookmarks/20/tags/40', method='DELETE')

    # Check database
    with app.app_context():
        query = 'SELECT COUNT(id) FROM tags WHERE id=40'
        count = get_db().execute(query).fetchone()[0]
        assert count == 1


def test_post(client, app, authenticated_user):
    def get_tag_count(bookmark_id):
        with app.app_context():
            db = get_db()
            query = 'SELECT COUNT(id) FROM tags WHERE bookmark_id = ' + str(
                bookmark_id)
            count = db.execute(query).fetchone()[0]
        return count

    validTag = {
        'tag_bookmark_id': 32
    }
    client.post('/bookmarks/20/tags', json=validTag,
                headers=request_headers(authenticated_user))
    assert get_tag_count(20) == 2

    invalidTag = {
        'tag': 31
    }
    response = client.post('/bookmarks/20/tags', json=invalidTag,
                           headers=request_headers(authenticated_user))
    assert response.status_code == 400
    assert get_tag_count(20) == 2


def test_post_unauthorized(client, app):
    tag_json = {
        'tag_bookmark_id': 50
    }
    unauthorized_test(client, '/bookmarks/20/tags',
                      method='POST', json=tag_json)

    # Check database
    with app.app_context():
        query = 'SELECT COUNT(id) FROM tags WHERE id=50'
        count = get_db().execute(query).fetchone()[0]
        assert count == 0

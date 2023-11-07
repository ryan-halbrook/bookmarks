from bookmarks.db import get_cursor
from tests.headers import request_headers, unauthorized_test


def test_get(client, authenticated_user):
    response = client.get('/bookmarks/1/tags',
                          headers=request_headers(authenticated_user))
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['bookmark']['name'] == 'another test bookmark'


def test_get_unauthorized(client):
    unauthorized_test(client, '/bookmarks/1/tags')


def test_delete(client, authenticated_user):
    response = client.delete('/bookmarks/1/tags/1',
                             headers=request_headers(authenticated_user))
    assert response.status_code == 200
    assert len(response.json) == 0


def test_delete_unauthorized(client, app):
    unauthorized_test(client, '/bookmarks/1/tags/1', method='DELETE')

    # Check database
    with app.app_context():
        query = 'SELECT COUNT(id) FROM tags WHERE id=1'
        cur = get_cursor()
        cur.execute(query)
        count = cur.fetchone()[0]
        cur.close()
        assert count == 1


def test_post(client, app, authenticated_user):
    def get_tag_count(bookmark_id):
        with app.app_context():
            query = 'SELECT COUNT(id) FROM tags WHERE bookmark_id = %s' \
                    % str(bookmark_id)
            cur = get_cursor()
            cur.execute(query)
            count = cur.fetchone()[0]
            cur.close()
            return count

    validTag = {
        'tag_bookmark_id': 3
    }
    client.post('/bookmarks/1/tags', json=validTag,
                headers=request_headers(authenticated_user))
    assert get_tag_count(1) == 2

    invalidTag = {
        'tag_bookmark_id': 4
    }
    response = client.post('/bookmarks/1/tags', json=invalidTag,
                           headers=request_headers(authenticated_user))
    assert response.status_code == 400
    assert get_tag_count(1) == 2


def test_post_unauthorized(client, app):
    tag_json = {
        'tag_bookmark_id': 2
    }
    unauthorized_test(client, '/bookmarks/1/tags',
                      method='POST', json=tag_json)

    # Check database
    with app.app_context():
        query = 'SELECT COUNT(id) FROM tags WHERE id=2'
        cur = get_cursor()
        cur.execute(query)
        count = cur.fetchone()[0]
        cur.close()
        assert count == 0

from bookmarks.db import get_db


def test_get(client, authenticated_user):
    response = client.get('/bookmarks/20/tags',
        headers={'Authorization': 'bearear ' + authenticated_user.token})
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['bookmark']['name'] == 'another test bookmark'


def test_delete(client, authenticated_user):
    response = client.delete('/bookmarks/20/tags/40',
        headers={'Authorization': 'bearear ' + authenticated_user.token})
    assert response.status_code == 200
    assert len(response.json) == 0


def test_post(client, app, authenticated_user):
    def get_tag_count(bookmark_id):
        with app.app_context():
            db = get_db()
            query = 'SELECT COUNT(id) FROM tags WHERE bookmark_id = ' + str(
                bookmark_id)
            count = db.execute(query).fetchone()[0]
            count == 2
        return count

    validTag = {
        'tag_bookmark_id': 32
    }
    client.post(
        '/bookmarks/20/tags', json=validTag,
        headers={'Authorization': 'bearear ' + authenticated_user.token})
    assert get_tag_count(20) == 2

    invalidTag = {
        'tag': 31
    }
    response = client.post(
        '/bookmarks/20/tags', json=invalidTag,
        headers={'Authorization': 'bearear ' + authenticated_user.token})
    assert response.status_code == 400
    assert get_tag_count(20) == 2

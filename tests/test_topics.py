from flaskr.db import get_db


def test_get(client):
    response = client.get('/topics')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'test topic'


def test_update(client, app):
    def get_topic_name(topic_id):
        with app.app_context():
            result = get_db().execute('SELECT name FROM topics WHERE id = ' + str(topic_id)).fetchone()
        return result['name']

    valid_patch_data = {
        'name': 'new topic name'
    }
    client.patch('/topics/10', json=valid_patch_data)
    assert get_topic_name(10) == valid_patch_data['name']

    invalid_patch_data = {
        'nameX': 'X'
    }
    client.patch('/topics/10', json=invalid_patch_data)
    assert get_topic_name(10) == valid_patch_data['name']


def test_delete(client, app):
    client.delete('/topics/10')

    with app.app_context():
        count = get_db().execute('SELECT COUNT(id) FROM topics').fetchone()[0]
        assert count == 0
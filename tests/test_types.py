from bookmarks.db import get_db


def test_get(client):
    response = client.get('/collections/1/types')
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['name'] == 'test type'


def test_update(client, app):
    def get_type_name(type_id):
        with app.app_context():
            result = get_db().execute('SELECT name FROM types WHERE id = ' + str(type_id)).fetchone()
        return result['name']

    valid_patch_data = {
        'name': 'new type name'
    }
    client.patch('/types/10', json=valid_patch_data)
    assert get_type_name(10) == valid_patch_data['name']

    invalid_patch_data = {
        'nameX': 'X'
    }
    client.patch('/types/10', json=invalid_patch_data)
    assert get_type_name(10) == valid_patch_data['name']


def test_delete(client, app):
    client.delete('/types/10')

    with app.app_context():
        count = get_db().execute('SELECT COUNT(id) FROM types').fetchone()[0]
        assert count == 1

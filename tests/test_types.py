from bookmarks.db import get_cursor
from tests.headers import request_headers, unauthorized_test


def get_type_name(app, type_id):
    with app.app_context():
        cur = get_cursor()
        cur.execute(
            'SELECT name FROM types WHERE id = ' + str(type_id)
            )
        result = cur.fetchone()
        cur.close()
    if result is None:
        return None
    return result['name']


def test_get(client, authenticated_user):
    response = client.get(
        '/collections/1/types',
        headers=request_headers(authenticated_user))

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['name'] == 'test type'

    # Unused collection id
    response = client.get(
        '/collections/3/types',
        headers=request_headers(authenticated_user))

    assert response.status_code == 404


def test_get_unauthorized(client):
    unauthorized_test(client, '/collections/1/types')


def test_update(client, app, authenticated_user):
    valid_patch_data = {
        'name': 'new type name'
    }
    response = client.patch('/types/1', json=valid_patch_data,
                            headers=request_headers(authenticated_user))
    assert response.status_code == 200
    assert get_type_name(app, 1) == valid_patch_data['name']

    # Unused type id
    response = client.patch('/types/3', json={'name': 'unused id'},
                            headers=request_headers(authenticated_user))
    assert response.status_code == 404
    assert get_type_name(app, 3) is None
    assert get_type_name(app, 1) == valid_patch_data['name']

    # Incorrect field name in the patch's JSON
    invalid_patch_data = {
        'nameX': 'X'
    }
    response = client.patch('/types/1', json=invalid_patch_data,
                            headers=request_headers(authenticated_user))
    assert response.status_code == 400
    assert get_type_name(app, 1) == valid_patch_data['name']


def test_update_unauthorized(client, app, authenticated_user):
    # No auth header
    new_name = 'new type name'
    unauthorized_test(client, '/types/1', method='PATCH',
                      json={'name': new_name})

    # Check database
    assert get_type_name(app, 1) != new_name


def test_delete(client, app, authenticated_user):
    client.delete('/types/1', headers=request_headers(authenticated_user))
    assert get_type_name(app, 1) is None

    # Unused type ID
    response = client.delete('/types/3',
                             headers=request_headers(authenticated_user))
    assert response.status_code == 404


def test_delete_unauthorized(client, app):
    unauthorized_test(client, '/types/1', method='DELETE')

    # Check database
    assert get_type_name(app, 1)

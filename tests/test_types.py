from bookmarks.db import get_db
from tests.headers import request_headers, unauthorized_test


def get_type_name(app, type_id):
    with app.app_context():
        result = get_db().execute(
                'SELECT name FROM types WHERE id = ' + str(type_id)
                ).fetchone()
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
        '/collections/100/types',
        headers=request_headers(authenticated_user))

    assert response.status_code == 404


def test_get_unauthorized(client):
    unauthorized_test(client, '/collections/1/types')


def test_update(client, app, authenticated_user):
    valid_patch_data = {
        'name': 'new type name'
    }
    response = client.patch('/types/10', json=valid_patch_data,
                            headers=request_headers(authenticated_user))
    assert response.status_code == 200
    assert get_type_name(app, 10) == valid_patch_data['name']

    # Unused type id
    response = client.patch('/types/100', json={'name': 'unused id'},
                            headers=request_headers(authenticated_user))
    assert response.status_code == 404
    assert get_type_name(app, 100) is None
    assert get_type_name(app, 10) == valid_patch_data['name']

    # Incorrect field name in the patch's JSON
    invalid_patch_data = {
        'nameX': 'X'
    }
    response = client.patch('/types/10', json=invalid_patch_data,
                            headers=request_headers(authenticated_user))
    assert response.status_code == 400
    assert get_type_name(app, 10) == valid_patch_data['name']


def test_update_unauthorized(client, app, authenticated_user):
    # No auth header
    new_name = 'new type name'
    unauthorized_test(client, '/types/10', method='PATCH',
                      json={'name': new_name})

    # Check database
    assert get_type_name(app, 10) != new_name


def test_delete(client, app, authenticated_user):
    client.delete('/types/10', headers=request_headers(authenticated_user))
    assert get_type_name(app, 10) is None

    # Unused type ID
    response = client.delete('/types/100',
                             headers=request_headers(authenticated_user))
    assert response.status_code == 404


def test_delete_unauthorized(client, app):
    unauthorized_test(client, '/types/10', method='DELETE')

    # Check database
    assert get_type_name(app, 10)

import pytest


def test_create(client, authenticated_user):
    name = 'New test collection'

    response = client.post(
        '/collections', json={'name': name},
        headers={'Authorization': 'bearear ' + authenticated_user.token})
    
    assert response.status_code == 200
    assert response.json['name'] == name
    assert response.json['user_id'] == authenticated_user.id


def test_get(client, authenticated_user):
    response = client.get(
        '/collections',
        headers={'Authorization': 'bearear ' + authenticated_user.token})
    
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['name'] == 'test collection'
    assert response.json[1]['name'] == 'another collection'

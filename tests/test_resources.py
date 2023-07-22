from bookmarks.db import get_db

def test_get(client):
    response = client.get('/bookmarks/30/resources')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'test bookmark'

    response = client.get('/bookmarks/30/resources?type=another%20type')
    assert response.status_code == 200
    assert len(response.json) == 0

    response = client.get('/bookmarks/30/resources?type=test%20type')
    assert response.status_code == 200
    assert len(response.json) == 1

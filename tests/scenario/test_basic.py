

# Test minimum steps to create a new user and first bookmark.
def test_basic(client):
    user = {
        'email': 'test@example.com',
        'password': '1234'
    }

    coll_name = 'Main'

    bookmark = {
        'name': 'Example',
        'link': 'http://example.com',
        'description': 'Test bookmark',
        'type': 'Example type'
    }

    # Create user and login.
    client.post('/users', json=user)
    response = client.post('/users/login', json=user)
    headers = {'Authorization': 'bearer ' + response.json['token']}

    # Create collection.
    client.post('/collections', json={'name': coll_name}, headers=headers)
    response = client.get('/collections', headers=headers)
    assert len(response.json) == 1
    assert response.json[0]['name'] == coll_name

    # Create bookmark.
    collId = response.json[0]['id']
    client.post('/collections/%s/bookmarks' % collId,
                json=bookmark,
                headers=headers)
    response = client.get('/collections/' + str(collId) + '/types',
                          headers=headers)
    assert len(response.json) == 1
    assert response.json[0]['name'] == bookmark['type']

    # Get bookmarks, verify sole bookmark matches expected.
    response = client.get('/collections/%s/bookmarks' % collId,
                          headers=headers)
    assert len(response.json) == 1
    actual_bookmark = response.json[0]
    assert actual_bookmark['name'] == bookmark['name']
    assert actual_bookmark['link'] == bookmark['link']
    assert actual_bookmark['description'] == bookmark['description']
    assert actual_bookmark['type']['name'] == bookmark['type']

import pytest
from bookmarks.db import get_db
import json

def test_get(client, app):
    response = client.get('/collections')
    assert response.status_code == 200
    assert len(response.json) == 2
    
    assert response.json[0]['name'] == 'test collection'
    assert response.json[1]['name'] == 'another collection'

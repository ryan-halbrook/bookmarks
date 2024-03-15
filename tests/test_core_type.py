import bookmarks.model.bookmark_type as bookmark_type
from bookmarks.db import get_cursor


def test_create(app):
    with app.app_context():
        name = 'Test Type'
        bookmark_type.create(name)

        cur = get_cursor()
        cur.execute('SELECT name FROM types WHERE name = %s', (name,))
        types = cur.fetchall()
        cur.close()
        assert types[0]['name'] == name


def test_fetch(app):
    with app.app_context():
        result = bookmark_type.fetch()[0]
        assert result.id == 1
        assert result.name == 'test type'

        result = bookmark_type.fetch_single()
        assert result.id == 1
        assert result.name == 'test type'


def test_update(app):
    with app.app_context():
        new_name = 'New Type'
        bookmark_type.update(1, name=new_name)

        cur = get_cursor()
        cur.execute('SELECT name FROM types WHERE name = %s', (new_name,))
        types = cur.fetchall()
        cur.close()
        assert types[0]['name'] == new_name


def test_delete(app):
    with app.app_context():
        bookmark_type.delete(1)
        cur = get_cursor()
        cur.execute('SELECT name FROM types WHERE id = %s', (1,))
        types = cur.fetchall()
        cur.close()
        assert not types

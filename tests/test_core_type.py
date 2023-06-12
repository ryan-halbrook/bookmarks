import flaskr.core.bookmark_type as bookmark_type
from flaskr.db import get_db

def test_create(app):
    with app.app_context():
        name = 'Test Type'
        bookmark_type.create(name)

        types = get_db().execute(
                'SELECT name FROM types WHERE name = ?',
                (name,)).fetchall()
        assert types[0]['name'] == name


def test_fetch(app):
    with app.app_context():
        result = bookmark_type.fetch()[0]
        assert result.id == 10
        assert result.name == 'test type'

        result = bookmark_type.fetch_single()
        assert result.id == 10
        assert result.name == 'test type'


def test_update(app):
    with app.app_context():
        new_name = 'New Type'
        bookmark_type.update(10, name=new_name)

        types = get_db().execute(
                'SELECT name FROM types WHERE name = ?',
                (new_name,)).fetchall()
        assert types[0]['name'] == new_name


def test_delete(app):
    with app.app_context():
        bookmark_type.delete(10)
        types = get_db().execute(
                'SELECT name FROM types WHERE id = ?',
                (10,)).fetchall()
        assert not types

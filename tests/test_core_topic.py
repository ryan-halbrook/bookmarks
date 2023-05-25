import flaskr.core.topic as topic
from flaskr.db import get_db

def test_create(app):
    with app.app_context():
        name = 'Test Topic'
        topic.create(name)

        topics = get_db().execute(
                'SELECT name FROM topics WHERE name = ?',
                (name,)).fetchall()
        assert topics[0]['name'] == name


def test_fetch(app):
    with app.app_context():
        result = topic.fetch()[0]
        assert result.id == 10
        assert result.name == 'test topic'

        result = topic.fetch_single()
        assert result.id == 10
        assert result.name == 'test topic'


def test_update(app):
    with app.app_context():
        new_name = 'New Topic'
        topic.update(10, name=new_name)

        topics = get_db().execute(
                'SELECT name FROM topics WHERE name = ?',
                (new_name,)).fetchall()
        assert topics[0]['name'] == new_name


def test_delete(app):
    with app.app_context():
        topic.delete(10)
        topics = get_db().execute(
                'SELECT name FROM topics WHERE id = ?',
                (10,)).fetchall()
        assert not topics

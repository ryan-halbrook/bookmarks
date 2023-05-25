import pytest

from flaskr.db import get_db
import flaskr.core.bookmark as bookmark


def test_create(app):
    with app.app_context():
        name = 'Test Create Bookmark'
        topic_id = 1
        link = 'http://example.com/create'
        description = 'lorem ipsum...'

        bookmark.create(name, topic_id, link, description);
        bookmarks = get_db().execute(
                'SELECT b.id FROM bookmarks as b WHERE'
                ' b.name = ? AND b.topic_id = ? AND b.link = ?'
                ' AND b.description = ?'
                , (name, topic_id, link, description)).fetchall()
        assert len(bookmarks) == 1


def test_fetch_all(app):
    with app.app_context():
        assert len(bookmark.fetch()) == 3


def test_fetch_id(app):
    with app.app_context():
        assert bookmark.fetch_single(20).name == 'test bookmark'


def test_fetch_name(app):
    with app.app_context():
        result = bookmark.fetch_single(name='test bookmark',
                                        topic_name='test topic')
        assert result.name == 'test bookmark'


def test_update(app):
    with app.app_context():
        bookmark.update(20, name='updated bookmark')
        assert bookmark.fetch_single(20).name == 'updated bookmark'
        bookmark.update(20, link='updated link')
        assert bookmark.fetch_single(20).link == 'updated link'
        bookmark.update(20, description='updated desc')
        assert bookmark.fetch_single(20).description == 'updated desc'
        #bookmark.update(20, topic_id=30)
        #assert bookmark.fetch_single(20).topic.id == 30
        

def test_delete(app):
    with app.app_context():
        bookmark.delete(20)
        assert not get_db().execute(
                'SELECT id FROM bookmarks WHERE id = 20'
                ).fetchone()

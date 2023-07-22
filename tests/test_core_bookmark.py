import pytest

from bookmarks.db import get_db
import bookmarks.core.bookmark as bookmark


def test_create(app):
    with app.app_context():
        name = 'Test Create Bookmark'
        type_id = 1
        link = 'http://example.com/create'
        description = 'lorem ipsum...'

        bookmark.create(1, name, type_id, link, description);
        bookmarks = get_db().execute(
                'SELECT b.id FROM bookmarks as b WHERE'
                ' b.name = ? AND b.type_id = ? AND b.link = ?'
                ' AND b.description = ?'
                , (name, type_id, link, description)).fetchall()
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
                                        type_name='test type')
        assert result.name == 'test bookmark'


def test_update(app):
    with app.app_context():
        bookmark.update(20, name='updated bookmark')
        assert bookmark.fetch_single(20).name == 'updated bookmark'
        bookmark.update(20, link='updated link')
        assert bookmark.fetch_single(20).link == 'updated link'
        bookmark.update(20, description='updated desc')
        assert bookmark.fetch_single(20).description == 'updated desc'
        bookmark.update(20, type_id=11)
        assert bookmark.fetch_single(20).bookmark_type.id == 11
        # Verify receiving no update parameters raises
        with pytest.raises(Exception):
            bookmark.update(20)
        # Update multiple parameters
        bookmark.update(20, type_id=10, link='new link')
        updated = bookmark.fetch_single(20)
        assert updated.bookmark_type.id == 10
        assert updated.link == 'new link'
        

def test_delete(app):
    with app.app_context():
        bookmark.delete(20, 1)
        assert not get_db().execute(
                'SELECT id FROM bookmarks WHERE id = 20'
                ).fetchone()

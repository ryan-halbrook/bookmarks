import pytest

from bookmarks.db import get_cursor
import bookmarks.core.bookmark as bookmark
from bookmarks.types import Type


def test_create(app):
    with app.app_context():
        name = 'Test Create Bookmark'
        b_type = Type(1, 'test type', 0)
        link = 'http://example.com/create'
        description = 'lorem ipsum...'
        note = 'sample note'

        bookmark.create(b_type, name, link, description, note=note)
        cur = get_cursor()
        cur.execute(
                'SELECT b.id, b.note, b.note_is_markdown'
                ' FROM bookmarks as b WHERE'
                ' b.name = %s AND b.type_id = %s AND b.link = %s'
                ' AND b.description = %s',
                (name, b_type.id, link, description))
        bookmarks = cur.fetchall()
        cur.close()
        assert len(bookmarks) == 1
        assert bookmarks[0]['note'] == 'sample note'
        assert not bookmarks[0]['note_is_markdown']


def test_fetch_all(app):
    with app.app_context():
        assert len(bookmark.fetch()) == 3


def test_fetch_id(app):
    with app.app_context():
        assert bookmark.fetch_single(1).name == 'test bookmark'


def test_fetch_name(app):
    with app.app_context():
        result = bookmark.fetch_single(name='test bookmark',
                                       type_name='test type')
        assert result.name == 'test bookmark'


def test_update(app):
    with app.app_context():
        bookmark.update(1, name='updated bookmark')
        assert bookmark.fetch_single(1).name == 'updated bookmark'
        bookmark.update(1, link='updated link')
        assert bookmark.fetch_single(1).link == 'updated link'
        bookmark.update(1, description='updated desc')
        assert bookmark.fetch_single(1).description == 'updated desc'
        bookmark.update(1, type_id=2)
        assert bookmark.fetch_single(1).bookmark_type.id == 2
        # Update multiple parameters
        bookmark.update(1, type_id=1, link='new link')
        updated = bookmark.fetch_single(1)
        assert updated.bookmark_type.id == 1
        assert updated.link == 'new link'
        # Update note
        bookmark.update(1, note='new note', note_is_markdown=True)
        updated = bookmark.fetch_single(1)
        assert updated.note == 'new note'
        assert updated.note_is_markdown
        # Update to invalid type
        with pytest.raises(Exception):
            bookmark.update(1, type_id=50)


def test_delete(app):
    with app.app_context():
        bookmark.delete(1)
        cur = get_cursor()
        cur.execute('SELECT id FROM bookmarks WHERE id = 1')
        result = cur.fetchone()
        cur.close()
        assert result is None

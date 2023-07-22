import bookmarks.core.tag as tag
import bookmarks.core.bookmark
from bookmarks.db import get_db
import pytest


def test_create(app):
    with app.app_context():
        # Tag with itself raises
        with pytest.raises(Exception):
            tag.create(20, 20)
        # Recreate existing
        tag.create(20, 30)
        tag.create(30, 20)
        # Tag non-existent bookmark raises
        with pytest.raises(Exception):
            tag.create(20, 21)


def test_fetch(app):
    with app.app_context():
        bookmarks.core.bookmark.create(
                1, 'a third bookmark', 11, 'http://example.com', '')
        tag.create(20, 33)
        assert len(tag.fetch_tags(20)) == 2
        for type_name in ['test type', 'another type']:
            for bookmark in tag.fetch_tags(20, type_name=type_name):
                assert bookmark.bookmark.bookmark_type.name == type_name



def test_delete(app):
    pass

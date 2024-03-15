import bookmarks.model.tag as tag
import bookmarks.model.bookmark
from bookmarks.types import Type
import pytest


def test_create(app):
    with app.app_context():
        # Tag with itself raises
        with pytest.raises(Exception):
            tag.create(1, 1)
        # Recreate existing
        tag.create(1, 2)
        tag.create(2, 1)
        # Tag non-existent bookmark raises
        with pytest.raises(Exception):
            tag.create(1, 21)


def test_fetch(app):
    with app.app_context():
        b_type = Type(1, 'test type', 0)
        bookmark_id = bookmarks.model.bookmark.create(
                b_type, 'a fourth bookmark', 2, 'http://example.com', '').id
        tag.create(1, bookmark_id)

        assert len(tag.fetch_tags(1)) == 2

        for type_name in ['test type', 'another type']:
            for bookmark in tag.fetch_tags(1, type_name=type_name):
                assert bookmark.bookmark.bookmark_type.name == type_name


def test_delete(app):
    pass

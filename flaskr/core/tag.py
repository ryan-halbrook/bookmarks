import flaskr.db as db
from model.types import Bookmark, Tag, Type
from . import bookmark as core_bookmark

# Tag the bookmark with ID = bookmark_id
# with the bookmark with ID = tag_bookmark_id
def create(bookmark_id, tag_bookmark_id):
    if bookmark_id == tag_bookmark_id:
        raise Exception()
    bookmark = core_bookmark.fetch_single(bookmark_id)
    tag_bookmark = core_bookmark.fetch_single(tag_bookmark_id)
    if not (bookmark and tag_bookmark):
        raise Exception()

    db.get_db().execute(
        'INSERT INTO tags (bookmark_id, tag_bookmark_id)'
        ' VALUES (?, ?)',
        (bookmark.id, tag_bookmark.id,)
    )
    db.get_db().commit()


def delete(id):
    db.get_db().execute(
        'DELETE FROM tags WHERE id = ?',
        (id,)
    )
    db.get_db().commit()

# bookmark_id, tag_bookmark_id
def fetch_tags(bookmark_id, type_name=None):
    query = """SELECT ta.name as type_name, a.id as bookmark_id,
               a.created as bookmark_created,
               a.name as bookmark_name, a.link as bookmark_link,
               ta.id as type_id, a.description as bookmark_description,
               t.id as tag_id
               FROM tags as t, bookmarks as a, types as ta
               WHERE a.type_id = ta.id
               AND (
               (t.bookmark_id = ? AND t.tag_bookmark_id = a.id) OR
               (t.bookmark_id = a.id AND t.tag_bookmark_id = ?))"""
    if type_name:
        query += ' AND ta.name = ?'
    params = (bookmark_id, bookmark_id, type_name) if type_name else (bookmark_id, bookmark_id)
    
    fetchResults = db.get_db().execute(query, params).fetchall()

    def bookmark(row):
        return Tag( row['tag_id'],
                    Bookmark(
                        row['bookmark_id'],
                        row['bookmark_created'],
                        row['bookmark_name'],
                        Type(
                            row['type_id'],
                            row['type_name']
                        ),
                        row['bookmark_link'],
                        row['bookmark_description']
                    ))

    return [bookmark(row) for row in fetchResults]


def fetch_resources(bookmark_id, type_name=None):
    if type_name:
        fetchResults = db.get_db().execute(
            'SELECT ta.name as type_name, a.id as bookmark_id,'
            ' a.created as bookmark_created,'
            ' a.name as bookmark_name, a.link as bookmark_link,'
            ' ta.id as type_id, a.description as bookmark_description'
            ' FROM tags as t, bookmarks as a, types as ta'
            ' WHERE a.type_id = ta.id'
            ' AND t.bookmark_id = a.id AND t.tag_bookmark_id = ?'
            ' AND ta.name = ?',
            (bookmark_id, type_name,)
        ).fetchall()
    else:
        fetchResults = db.get_db().execute(
            'SELECT ta.name as type_name, a.id as bookmark_id,'
            ' a.name as bookmark_name, a.link as bookmark_link,'
            ' a.created as bookmark_created,'
            ' ta.id as type_id, a.description as bookmark_description'
            ' FROM tags as t, bookmarks as a, types as ta'
            ' WHERE a.type_id = ta.id'
            ' AND t.bookmark_id = a.id AND t.tag_bookmark_id = ?',
            (bookmark_id,)
        ).fetchall()

    def bookmark(row):
        return Bookmark(
            row['bookmark_id'],
            row['bookmark_created'],
            row['bookmark_name'],
            Type(
                row['type_id'],
                row['type_name']
            ),
            row['bookmark_link'],
            row['bookmark_description']
        )

    return [bookmark(row) for row in fetchResults]

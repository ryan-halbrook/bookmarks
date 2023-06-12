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


# Collection of 'Tag's. Includes tag ID and both bookmarks.
def fetch():
    fetchResults = db.get_db().execute(
        'SELECT t.id as tag_id, t.created as tag_created,'
        ' a.name as bookmark_name, a.id as bookmark_id, a.created as bookmark_created,'
        ' a.link as bookmark_link, a.description as bookmark_description,'
        ' b.name as tag_bookmark_name, b.id as tag_bookmark_id,'
        ' b.created as tag_bookmark_created,'
        ' b.link as tag_bookmark_link, b.description as tag_bookmark_description,'
        ' ta.name as bookmark_type_name, ta.id as bookmark_type_id,'
        ' tb.name as tag_type_name, tb.id as tag_type_id'
        ' FROM tags as t, bookmarks as a, bookmarks as b,'
        ' types as ta, types as tb'
        ' WHERE t.bookmark_id = a.id AND t.tag_bookmark_id = b.id'
        ' AND a.type_id = ta.id AND b.type_id = tb.id'
    ).fetchall()

    tags = []
    for row in fetchResults:
        bookmark = Bookmark(
            row['bookmark_id'],
            row['bookmark_created'],
            row['bookmark_name'],
            Type(
                row['bookmark_type_id'],
                row['bookmark_type_name']
            ),
            row['bookmark_link'],
            row['bookmark_description']
        )
        tag_bookmark = Bookmark(
            row['tag_bookmark_id'],
            row['tag_bookmark_created'],
            row['tag_bookmark_name'],
            Type(
                row['tag_type_id'],
                row['tag_type_name']
            ),
            row['tag_bookmark_link'],
            row['tag_bookmark_description']
        )
        tags.append(
            Tag(
                row['tag_id'],
                row['tag_created'],
                bookmark,
                tag_bookmark
            )
        )
    return tags


def fetch_tags(bookmark_id, type_name=None):
    query = """SELECT ta.name as type_name, a.id as bookmark_id,
               a.created as bookmark_created,
               a.name as bookmark_name, a.link as bookmark_link,
               ta.id as type_id, a.description as bookmark_description
               FROM tags as t, bookmarks as a, types as ta
               WHERE a.type_id = ta.id
               AND t.bookmark_id = ? AND t.tag_bookmark_id = a.id"""
    if type_name:
        query += ' AND ta.name = ?'
    params = (bookmark_id, type_name) if type_name else (bookmark_id,)
    
    fetchResults = db.get_db().execute(query, params).fetchall()

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

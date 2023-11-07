import bookmarks.db as db
from bookmarks.types import Bookmark, Tag, Type
from . import bookmark as core_bookmark


def tag_exists(id1, id2):
    query = """SELECT id FROM tags WHERE (
               (bookmark_id = %s AND tag_bookmark_id = %s) OR
               (bookmark_id = %s AND tag_bookmark_id = %s))"""
    cur = db.get_cursor()
    cur.execute(query, (id1, id2, id2, id1,))
    fetch = cur.fetchone()
    cur.close()
    return bool(fetch)


def create(bookmark_id, tag_bookmark_id):
    if bookmark_id == tag_bookmark_id:
        raise Exception()
    if tag_exists(bookmark_id, tag_bookmark_id):
        return
    bookmark = core_bookmark.fetch_single(bookmark_id)
    tag_bookmark = core_bookmark.fetch_single(tag_bookmark_id)
    if not (bookmark and tag_bookmark):
        raise Exception()

    cur = db.get_cursor()
    cur.execute(
        'INSERT INTO tags (bookmark_id, tag_bookmark_id)'
        ' VALUES (%s, %s)',
        (bookmark.id, tag_bookmark.id,)
    )
    db.get_db().commit()
    cur.close()


def delete(id):
    cur = db.get_cursor()
    cur.execute('DELETE FROM tags WHERE id = %s', (id,))
    db.get_db().commit()
    cur.close()


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
               (t.bookmark_id = %s AND t.tag_bookmark_id = a.id) OR
               (t.bookmark_id = a.id AND t.tag_bookmark_id = %s))"""
    if type_name:
        query += ' AND ta.name = %s'
        params = (bookmark_id, bookmark_id, type_name)
    else:
        params = (bookmark_id, bookmark_id)

    cur = db.get_cursor()
    cur.execute(query, params)
    fetchResults = cur.fetchall()
    cur.close()

    def bookmark(row):
        return Tag(row['tag_id'],
                   Bookmark(
                       row['bookmark_id'],
                       row['bookmark_created'],
                       row['bookmark_name'],
                       Type(
                            row['type_id'],
                            row['type_name'],
                            0
                       ),
                       row['bookmark_link'],
                       row['bookmark_description']
                       ))

    return [bookmark(row) for row in fetchResults]

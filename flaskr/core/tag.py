import flaskr.db as db
from model.types import Bookmark, Tag, Topic
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
        'SELECT t.id as tag_id,'
        ' a.name as bookmark_name, a.id as bookmark_id,'
        ' a.link as bookmark_link, a.description as bookmark_description,'
        ' b.name as tag_bookmark_name, b.id as tag_bookmark_id,'
        ' b.link as tag_bookmark_link, b.description as tag_bookmark_description,'
        ' ta.name as bookmark_topic_name, ta.id as bookmark_topic_id,'
        ' tb.name as tag_topic_name, tb.id as tag_topic_id'
        ' FROM tags as t, bookmarks as a, bookmarks as b,'
        ' topics as ta, topics as tb'
        ' WHERE t.bookmark_id = a.id AND t.tag_bookmark_id = b.id'
        ' AND a.topic_id = ta.id AND b.topic_id = tb.id'
    ).fetchall()

    tags = []
    for row in fetchResults:
        bookmark = Bookmark(
            row['bookmark_id'],
            row['bookmark_name'],
            Topic(
                row['bookmark_topic_id'],
                row['bookmark_topic_name']
            ),
            row['bookmark_link'],
            row['bookmark_description']
        )
        tag_bookmark = Bookmark(
            row['tag_bookmark_id'],
            row['tag_bookmark_name'],
            Topic(
                row['tag_topic_id'],
                row['tag_topic_name']
            ),
            row['tag_bookmark_link'],
            row['tag_bookmark_description']
        )
        tags.append(
            Tag(
                row['tag_id'],
                bookmark,
                tag_bookmark
            )
        )
    return tags


def fetch_tags(bookmark_id, topic_name=None):
    query = """SELECT ta.name as topic_name, a.id as bookmark_id,
               a.name as bookmark_name, a.link as bookmark_link,
               ta.id as topic_id, a.description as bookmark_description
               FROM tags as t, bookmarks as a, topics as ta
               WHERE a.topic_id = ta.id
               AND t.bookmark_id = ? AND t.tag_bookmark_id = a.id"""
    if topic_name:
        query += ' AND ta.name = ?'
    params = (bookmark_id, topic_name) if topic_name else (bookmark_id,)
    
    fetchResults = db.get_db().execute(query, params).fetchall()

    def bookmark(row):
        return Bookmark(
            row['bookmark_id'],
            row['bookmark_name'],
            Topic(
                row['topic_id'],
                row['topic_name']
            ),
            row['bookmark_link'],
            row['bookmark_description']
        )

    return [bookmark(row) for row in fetchResults]


def fetch_resources(bookmark_id, topic_name=None):
    if topic_name:
        fetchResults = db.get_db().execute(
            'SELECT ta.name as topic_name, a.id as bookmark_id,'
            ' a.name as bookmark_name, a.link as bookmark_link,'
            ' ta.id as topic_id, a.description as bookmark_description'
            ' FROM tags as t, bookmarks as a, topics as ta'
            ' WHERE a.topic_id = ta.id'
            ' AND t.bookmark_id = a.id AND t.tag_bookmark_id = ?'
            ' AND ta.name = ?',
            (bookmark_id, topic_name,)
        ).fetchall()
    else:
        fetchResults = db.get_db().execute(
            'SELECT ta.name as topic_name, a.id as bookmark_id,'
            ' a.name as bookmark_name, a.link as bookmark_link,'
            ' ta.id as topic_id, a.description as bookmark_description'
            ' FROM tags as t, bookmarks as a, topics as ta'
            ' WHERE a.topic_id = ta.id'
            ' AND t.bookmark_id = a.id AND t.tag_bookmark_id = ?',
            (bookmark_id,)
        ).fetchall()

    def bookmark(row):
        return Bookmark(
            row['bookmark_id'],
            row['bookmark_name'],
            Topic(
                row['topic_id'],
                row['topic_name']
            ),
            row['bookmark_link'],
            row['bookmark_description']
        )

    return [bookmark(row) for row in fetchResults]

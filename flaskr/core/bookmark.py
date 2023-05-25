import flaskr.db as db
from model.types import Bookmark, Topic
import flaskr.core.utils as utils
import flaskr.core.topic as topic


def create(name, topic_id, link, description):
    db.get_db().execute(
        'INSERT INTO bookmarks (name, topic_id, link, description)'
        ' VALUES (?, ?, ?, ?)',
        (name, topic_id, link, description)
    )
    db.get_db().commit()


def fetch_single(id=None, name=None, topic_id=None, topic_name=None):
    bookmarks = fetch(id=id, name=name, topic_id=topic_id,
                      topic_name=topic_name)
    return bookmarks[0] if bookmarks else None


def fetch(id=None, name=None, topic_id=None, topic_name=None):
    params = { 
              'bookmark_id': id,
              'bookmark_name': name,
              'topic_id': topic_id,
              'topic_name': topic_name,
              }

    query = """SELECT b.id as bookmark_id, b.name as bookmark_name,
               b.link as bookmark_link, t.name as topic_name,
               t.id as topic_id, b.description as bookmark_description
               FROM bookmarks as b, topics as t where b.topic_id = t.id """
    if any(params.values()):
        query += " AND "
    query, values = utils.build_sql_where(query, params=params, add_where=False)
    fetchResult = db.get_db().execute(query, values).fetchall()

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
    return [bookmark(row) for row in fetchResult]


def update(id, name=None, link=None, topic_id=None, description=None):
    if not any([name, link, topic_id, description]):
        raise

    sets = {}
    if name:
        sets['name'] = name
    if link:
        sets['link'] = link
    if topic_id:
        sets['topic_id'] = topic_id
    if description:
        sets['description'] = description

    set_stmt = ' SET '
    set_values = []
    first = True
    for key, value in sets.items():
        if not first:
            set_stmt += ', '
        set_stmt += key + ' = ?'
        set_values.append(value)
        first = False

    db.get_db().execute(
        'UPDATE bookmarks' + set_stmt + ' WHERE id = ?',
        set_values + [id]
    )
    db.get_db().commit()


def delete(id):
    db.get_db().execute(
        'DELETE FROM bookmarks WHERE id = ?',
        (id,)
    )
    db.get_db().commit()

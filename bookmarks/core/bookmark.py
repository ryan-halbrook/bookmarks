import bookmarks.db as db
from bookmarks.types import Bookmark, Type, User
import bookmarks.core.utils as utils
import sqlite3


def create(collection_id, name, type_id, link, description):
    try:
        cur = db.get_db().cursor()
        cur.execute(
            'INSERT INTO bookmarks (name, type_id, link, description)'
            ' VALUES (?, ?, ?, ?)',
            (name, type_id, link, description)
        )
        bookmark_id = cur.lastrowid
        db.get_db().commit()
    except sqlite3.Error:
        return None
    return Bookmark(bookmark_id, None, name, None, link, description)


def fetch_single(id=None, collection_id=None, name=None, type_id=None,
                 type_name=None):
    bookmarks = fetch(
        user_id=None, id=id, collection_id=collection_id, name=name,
        type_id=type_id, type_name=type_name)
    return bookmarks[0] if bookmarks else None


def search(collection_id, match_type, match_string):
    query = """SELECT b.id as bookmark_id, b.created as created,
            b.name as bookmark_name, b.link as bookmark_link,
            t.name as type_name, t.id as type_id,
            b.description as bookmark_description
            FROM bookmarks as b, types as t
            where b.type_id = t.id AND t.collection_id = ?"""
    query += " AND b." + match_type + " LIKE ?"
    fetchResult = db.get_db().execute(
            query, (collection_id, '%' + match_string + '%',)).fetchall()

    def bookmark(row):
        return Bookmark(
            row['bookmark_id'],
            row['created'],
            row['bookmark_name'],
            Type(
                row['type_id'],
                row['type_name'],
                0
            ),
            row['bookmark_link'],
            row['bookmark_description']
        )
    return [bookmark(row) for row in fetchResult]


def fetch(
        user_id=None, id=None, collection_id=None, name=None, type_id=None,
        type_name=None):
    params = {
        'bookmark_id': id,
        'bookmark_name': name,
        'type_id': type_id,
        'type_name': type_name,
        'collection_id': collection_id,
        'user_id': user_id,
    }

    query = """SELECT b.id as bookmark_id, b.created as created,
            b.name as bookmark_name, b.link as bookmark_link,
            t.name as type_name, t.id as type_id,
            t.collection_id as collection_id,
            b.description as bookmark_description,
            c.user_id as user_id
            FROM bookmarks as b, types as t, collections as c
            where b.type_id = t.id AND t.collection_id = c.id"""
    if any(params.values()):
        query += " AND "
    query, values = utils.build_sql_where(
        query, params=params, add_where=False)
    fetchResult = db.get_db().execute(query, values).fetchall()

    def bookmark(row):
        return Bookmark(
            row['bookmark_id'],
            row['created'],
            row['bookmark_name'],
            Type(
                row['type_id'],
                row['type_name'],
                0
            ),
            row['bookmark_link'],
            row['bookmark_description']
        )
    return [bookmark(row) for row in fetchResult]


def update(id, name=None, link=None, type_id=None, description=None):
    if not any([name, link, type_id, description]):
        raise

    sets = {}
    if name:
        sets['name'] = name
    if link:
        sets['link'] = link
    if type_id:
        sets['type_id'] = type_id
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


def bookmark_user(bookmark_id):
    result = db.get_db().execute(
        'SELECT c.user_id as user_id FROM bookmarks as b, types as t, '
        'collections as c WHERE b.type_id = t.id AND t.collection_id = c.id '
        'AND b.id = ?', (bookmark_id,)
    ).fetchone()

    if not result:
        return None
    user_id = result['user_id']

    result = db.get_db().execute(
        'SELECT id, username FROM users WHERE id = ?',
        (user_id,)).fetchone()
    if not result:
        return None

    return User(result['id'], result['username'])


# Convenience for authenticating user access
def bookmark_user_id(bookmark_id):
    user = bookmark_user(bookmark_id)
    if user:
        return user.id
    else:
        return None

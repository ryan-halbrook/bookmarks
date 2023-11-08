import bookmarks.db as db
from bookmarks.types import Bookmark, Type, User, NameInUse
import bookmarks.core.utils as utils
import psycopg2.errors


def create(collection_id, name, type_id, link, description, note=''):
    try:
        cur = db.get_cursor()
        cur.execute(
            'INSERT INTO bookmarks (name, type_id, link, description, note)'
            ' VALUES (%s, %s, %s, %s, %s) RETURNING id',
            (name, type_id, link, description, note)
        )
        result = cur.fetchone()
        if result:
            bookmark_id = result['id']
        else:
            return None
        db.get_db().commit()
    except psycopg2.errors.UniqueViolation:
        raise NameInUse()
    finally:
        cur.close()
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
            where b.type_id = t.id AND t.collection_id = %s"""
    query += " AND b." + match_type + " ILIKE %s"
    cur = db.get_cursor()
    cur.execute(query, (collection_id, '%' + match_string + '%',))
    fetchResult = cur.fetchall()
    cur.close()

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
        'b.id': id,
        'b.name': name,
        'b.type_id': type_id,
        't.name': type_name,
        't.collection_id': collection_id,
        'c.user_id': user_id,
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
    cur = db.get_cursor()
    cur.execute(query, values)
    fetchResult = cur.fetchall()
    cur.close()

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
        set_stmt += key + ' = %s'
        set_values.append(value)
        first = False

    cur = db.get_cursor()
    cur.execute(
        'UPDATE bookmarks' + set_stmt + ' WHERE id = %s',
        set_values + [id]
    )
    db.get_db().commit()
    cur.close()


def delete(id):
    cur = db.get_cursor()
    cur.execute('DELETE FROM bookmarks WHERE id = %s', (id,))
    db.get_db().commit()
    cur.close()


def bookmark_user(bookmark_id):
    cur = db.get_cursor()
    cur.execute(
        'SELECT c.user_id as user_id FROM bookmarks as b, types as t, '
        'collections as c WHERE b.type_id = t.id AND t.collection_id = c.id '
        'AND b.id = %s', (bookmark_id,)
        )
    result = cur.fetchone()
    cur.close()

    if not result:
        return None
    user_id = result['user_id']

    cur = db.get_cursor()
    cur.execute('SELECT id, username FROM users WHERE id = %s', (user_id,))
    result = cur.fetchone()
    cur.close()

    return User(result['id'], result['username'])


# Convenience for authenticating user access
def bookmark_user_id(bookmark_id):
    user = bookmark_user(bookmark_id)
    if user:
        return user.id
    else:
        return None

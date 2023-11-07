from bookmarks import db
from bookmarks.types import Type
import bookmarks.core.utils as utils
import psycopg2.errors


def create(name, collection_id=1):
    try:
        cur = db.get_cursor()
        cur.execute(
            'INSERT INTO types (name, collection_id) VALUES'
            ' (%s, %s)',
            (name, collection_id,)
        )
        db.get_db().commit()
    except psycopg2.errors.UniqueViolation:
        return None
    finally:
        cur.close()


def fetch(id=None, collection_id=None, name=None):
    params = {
                'id': id,
                'name': name,
                'collection_id': collection_id,
             }
    query, values = utils.build_sql_where(
            'SELECT id, created, name, collection_id FROM types',
            params=params)
    try:
        cur = db.get_cursor()
        cur.execute(query, values)
        fetchResult = cur.fetchall()
        return [Type(f['id'],
                     f['name'],
                     f['collection_id'])
                for f in fetchResult]
    finally:
        cur.close()


def fetch_single(id=None, collection_id=None, name=None):
    types = fetch(id=id, collection_id=collection_id, name=name)
    return types[0] if types else None


def update(id, name=None):
    try:
        cur = db.get_cursor()
        cur.execute('UPDATE types SET name = %s WHERE id = %s', (name, id,))
        db.get_db().commit()
    finally:
        cur.close()


def delete(id):
    try:
        cur = db.get_cursor()
        cur.execute('DELETE FROM types WHERE id = %s', (id,))
        db.get_db().commit()
    finally:
        cur.close()

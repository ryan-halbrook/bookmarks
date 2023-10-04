import bookmarks.db as db
from bookmarks.types import Collection
import sqlite3


def create(user_id, name):
    try:
        cur = db.get_db().cursor()
        cur.execute(
            'INSERT INTO collections (name, user_id) VALUES (?, ?)',
            (name, user_id,))
        coll_id = cur.lastrowid
        db.get_db().commit()
    except sqlite3.Error:
        return None
    return Collection(coll_id, None, name, user_id)


def fetch(user_id):
    query = "SELECT id, name, created, user_id FROM collections WHERE user_id = ?"
    fetchResult = db.get_db().execute(query, (user_id,)).fetchall()

    return [Collection(row['id'], row['created'], row['name'], row['user_id']) for row in fetchResult]


def fetch_single(id):
    query = "SELECT id, name, created, user_id FROM collections WHERE id = ?"
    result = db.get_db().execute(query, (id,)).fetchone()
    return Collection(
        result['id'],
        result['created'],
        result['name'],
        result['user_id'])


# Convenience for authenticating collection access.
def collection_user_id(collection_id):
    coll = fetch_single(collection_id)
    if coll:
        return coll.user_id
    else:
        return None


def delete(id):
    try:
        db.get_db().execute("DELETE FROM collections WHERE id = ?", (id,))
        db.get_db().commit()
    except sqlite3.Error:
        return None
    return id
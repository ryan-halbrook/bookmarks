import bookmarks.db as db
from bookmarks.types import Collection, NameInUse
import psycopg2.errors
from typing import List


def create(user_id: int, name: str) -> Collection | None:
    try:
        cur = db.get_cursor()
        cur.execute(
            'INSERT INTO collections (name, user_id) VALUES (%s, %s) '
            'RETURNING id, created',
            (name, user_id,))
        # coll_id = cur.lastrowid
        result = cur.fetchone()
        db.get_db().commit()
        return Collection(result['id'], result['created'], name, user_id)
    except psycopg2.errors.UniqueViolation:
        raise NameInUse()
    finally:
        cur.close()


def fetch(user_id: int) -> List[Collection]:
    query = '''SELECT id, name, created, user_id
               FROM collections WHERE user_id = %s'''
    try:
        cur = db.get_cursor()
        cur.execute(query, (user_id,))
        fetchResult = cur.fetchall()
        return [Collection(row['id'],
                           row['created'],
                           row['name'],
                           row['user_id'])
                for row in fetchResult]
    finally:
        cur.close()


def fetch_single(id: int) -> Collection | None:
    query = "SELECT id, name, created, user_id FROM collections WHERE id = %s"
    try:
        cur = db.get_cursor()
        cur.execute(query, (id,))
        result = cur.fetchone()
        if result:
            return Collection(
                result['id'],
                result['created'],
                result['name'],
                result['user_id'])
    finally:
        cur.close()
    return None


# Convenience for authenticating collection access.
def collection_user_id(collection_id: int) -> int | None:
    coll = fetch_single(collection_id)
    if coll:
        return coll.user_id
    else:
        return None


def delete(id: int) -> int | None:
    try:
        cur = db.get_cursor()
        cur.execute("DELETE FROM collections WHERE id = %s", (id,))
        db.get_db().commit()
        return id
    finally:
        cur.close()

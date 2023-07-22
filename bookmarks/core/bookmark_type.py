from bookmarks import db
from model.types import Type
import bookmarks.core.utils as utils


def create(name, collection_id=1):
    db.get_db().execute(
        'INSERT INTO types (name, collection_id) VALUES'
        ' (?, ?)',
        (name, collection_id,)
    )
    db.get_db().commit()


def fetch(id=None, collection_id=None, name=None):
    params = {
                'id': id,
                'name': name,
                'collection_id': collection_id,
             }
    query, values = utils.build_sql_where(
            'SELECT id, created, name, collection_id FROM types', params=params)
    fetchResult = db.get_db().execute(query, values).fetchall()
    return [Type(f['id'], f['name']) for f in fetchResult]


def fetch_single(id=None, collection_id=None, name=None):
    types = fetch(id=id, collection_id=collection_id, name=name)
    return types[0] if types else None


def update(id, name=None):
    db.get_db().execute(
        'UPDATE types'
        ' SET name = ?'
        ' WHERE id = ?',
        (name, id,)
    )
    db.get_db().commit()
 

def delete(id):
    db.get_db().execute(
        'DELETE FROM types WHERE id = ?',
        (id,)
    )
    db.get_db().commit()

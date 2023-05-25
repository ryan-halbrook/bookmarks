from flaskr import db
from model.types import Topic
import flaskr.core.utils as utils


def create(name):
    db.get_db().execute(
        'INSERT INTO topics (name) VALUES'
        ' (?)',
        (name,)
    )
    db.get_db().commit()


def fetch(id=None, name=None):
    params = { 'id': id, 'name': name }
    query, values = utils.build_sql_where(
            'SELECT id, name FROM topics', params=params)
    print(query)
    print(values)
    fetchResult = db.get_db().execute(query, values).fetchall()
    return [Topic(f['id'], f['name']) for f in fetchResult]


def fetch_single(id=None, name=None):
    topics = fetch(id=id, name=name)
    return topics[0] if topics else None


def update(id, name=None):
    db.get_db().execute(
        'UPDATE topics'
        ' SET name = ?'
        ' WHERE id = ?',
        (name, id,)
    )
    db.get_db().commit()
 

def delete(id):
    db.get_db().execute(
        'DELETE FROM topics WHERE id = ?',
        (id,)
    )
    db.get_db().commit()

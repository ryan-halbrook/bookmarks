import flaskr.db as db
from model.types import Collection


def create(name):
    db.get_db().execute(
            'INSERT INTO collections (name) VALUES (?)',
            (name,))
    db.get_db().commit()


def fetch():
    query = "SELECT id, name, created FROM collections"
    fetchResult = db.get_db().execute(query).fetchall()

    return [Collection(row['id'], row['created'], row['name']) for row in fetchResult]


def delete(id):
    db.get_db().execute(
        'DELETE FROM collections WHERE id = ?',
        (id,))
    db.get_db().commit()

import bookmarks.db as db
from model.types import Collection


def fetch():
    query = "SELECT id, name, created FROM collections"
    fetchResult = db.get_db().execute(query).fetchall()

    return [Collection(row['id'], row['created'], row['name']) for row in fetchResult]

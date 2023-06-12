import flaskr.db as db
from model.types import Bookmark, Type
import flaskr.core.utils as utils


def create(name, type_id, link, description):
    db.get_db().execute(
        'INSERT INTO bookmarks (name, type_id, link, description)'
        ' VALUES (?, ?, ?, ?)',
        (name, type_id, link, description)
    )
    db.get_db().commit()


def fetch_single(id=None, name=None, type_id=None, type_name=None):
    bookmarks = fetch(id=id, name=name, type_id=type_id,
                      type_name=type_name)
    return bookmarks[0] if bookmarks else None


def fetch(id=None, name=None, type_id=None, type_name=None):
    params = { 
              'bookmark_id': id,
              'bookmark_name': name,
              'type_id': type_id,
              'type_name': type_name,
              }

    query = """SELECT b.id as bookmark_id, b.created as created,
               b.name as bookmark_name, b.link as bookmark_link,
               t.name as type_name, t.id as type_id,
               b.description as bookmark_description
               FROM bookmarks as b, types as t where b.type_id = t.id """
    if any(params.values()):
        query += " AND "
    query, values = utils.build_sql_where(query, params=params, add_where=False)
    fetchResult = db.get_db().execute(query, values).fetchall()

    def bookmark(row):
        return Bookmark(
                row['bookmark_id'],
                row['created'],
                row['bookmark_name'],
                Type(
                    row['type_id'],
                    row['type_name']
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

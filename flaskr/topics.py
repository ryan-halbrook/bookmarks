import flaskr.db as db
from flask import Blueprint, request
import flaskr.core as core

bp = Blueprint('topics', __name__, url_prefix='/')

@bp.get('/topics')
def topics():
    return [t.to_json() for t in core.get_topics()]

@bp.post('/topics')
def topics_post():
    data = request.json
    name = data['name']
    db.get_db().execute(
        'INSERT INTO topics (name) VALUES'
        ' (?)',
        (name,)
    )
    db.get_db().commit()
    return data['name']

@bp.delete('/topic/<id>')
def topics_delete(id):
    db.get_db().execute(
        'DELETE FROM topics WHERE id = ?',
        (id,)
    )
    db.get_db().commit()
    return id

@bp.patch('/topic/<id>')
def topics_update(id):
    data = request.json
    name = data['name']
    if not name:
        return 'Failed'
    db.get_db().execute(
        'UPDATE topics'
        ' SET name = ?'
        ' WHERE id = ?',
        (name, id,)
    )
    db.get_db().commit()
    return id
import flaskr.db as db
from flask import Blueprint, request
import flaskr.core.topic as topic

bp = Blueprint('topics', __name__, url_prefix='/')


@bp.get('/topics')
def topics():
    return [t.to_json() for t in topic.fetch()]


@bp.patch('/topics/<id>')
def topics_update(id):
    data = request.json
    name = data.get('name', None)
    if not name:
        return 'Failed'
    topic.update(id, name=name)
    return id


@bp.delete('/topics/<id>')
def topics_delete(id):
    topic.delete(id)
    return id

import flaskr.db as db
from flask import Blueprint, request
import flaskr.core.bookmark_type as bookmark_type

bp = Blueprint('types', __name__, url_prefix='/')

@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,DELETE,PATCH'
    return response


@bp.get('/types')
def types_get():
    return [t.to_json() for t in bookmark_type.fetch()]


@bp.patch('/types/<id>')
def types_update(id):
    data = request.json
    name = data.get('name', None)
    if not name:
        return 'Failed'
    bookmark_type.update(id, name=name)
    return id


@bp.delete('/types/<id>')
def types_delete(id):
    bookmark_type.delete(id)
    return id

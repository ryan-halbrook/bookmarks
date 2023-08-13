import bookmarks.db as db
from flask import Blueprint, request, abort
import bookmarks.core.bookmark_type as bookmark_type
import bookmarks.core.collection as collection
import bookmarks.core.user as user

bp = Blueprint('types', __name__, url_prefix='/')

@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,DELETE,PATCH'
    return response


def abort_if_unauthorized(user_id, collection_id):
    coll = collection.fetch_single(collection_id)
    if not coll:
        abort(404)
    if coll.user_id != user_id:
        abort(401)


def get_authenticated_user(authorization):
    if not authorization:
        print('no auth')
        abort(401)
    print(authorization)
    authenticated_user = user.get_authenticated_user(
        authorization.split(' ')[1])
    if not authenticated_user:
        abort(500)
    return authenticated_user


@bp.get('/collections/<id>/types')
def types_get(id):
    user = get_authenticated_user(request.headers['Authorization'])
    abort_if_unauthorized(user.id, id)
    return [t.to_json() for t in bookmark_type.fetch(collection_id=id)]


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

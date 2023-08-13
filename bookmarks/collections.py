from flask import Blueprint, request, Response, abort
import bookmarks.core.collection as collection
import bookmarks.core.user as user

bp = Blueprint('collections', __name__, url_prefix='/')


@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,DELETE,PATCH'
    return response


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


@bp.get('/collections')
def collections_get():
    print(request.headers['Authorization'])
    user = get_authenticated_user(request.headers['Authorization'])
    return [c.to_json() for c in collection.fetch(user.id)]


@bp.post('/collections')
def collections_post():
    user = get_authenticated_user(request.headers['Authorization'])
    name = request.json['name']
    if not name:
        abort(400)
    return collection.create(user.id, name).to_json()
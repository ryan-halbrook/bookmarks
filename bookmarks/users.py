from flask import Blueprint, request, abort
import bookmarks.core.user as user

bp = Blueprint('users', __name__, url_prefix='/')


@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,DELETE,PATCH'
    return response


@bp.post('/users')
def users():
    email = request.json['email']
    password = request.json['password']
    new_user = user.add_user(email, password)
    if not new_user:
        abort(500)


@bp.put('/users')
def update_user():
    email = request.json['email']
    password = request.json['password']
    token = request.json['token']
    try:
        updated_user = update_user(token, email, password)
    except:
        abort(500)
    return updated_user

@bp.post('/login')
def login():
    email = request.json['email']
    password = request.json['password']
    authenticated_user = user.login(email, password)
    if authenticated_user:
        return authenticated_user
    abort(401)
from flask import Blueprint, request, abort
import bookmarks.core.user as user

bp = Blueprint('users', __name__, url_prefix='/')


@bp.post('/users')
def users():
    email = request.json['email']
    password = request.json['password']
    new_user = user.add_user(email, password)
    if not new_user:
        abort(500)
    return new_user.to_json()


@bp.put('/users')
def update_user():
    email = request.json['email']
    password = request.json['password']
    token = request.json['token']
    try:
        updated_user = user.update_user(token, email, password)
    except Exception as e:
        print(e)
        abort(500)
    if not updated_user:
        abort(500)
    return updated_user.to_json()

@bp.post('/users/login')
def login():
    email = request.json['email']
    password = request.json['password']
    authenticated_user = user.login(email, password)
    if authenticated_user:
        return authenticated_user.to_json()
    abort(401)
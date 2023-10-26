from flask import Blueprint, request, abort, g
import bookmarks.core.user as user
from bookmarks.auth import login_required

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
@login_required
def update_user():
    email = request.json.get('email')
    password = request.json.get('password')
    updated_user = user.update_user(g.user.id, email, password)
    return updated_user.to_json()


@bp.post('/users/login')
def login():
    email = request.json['email']
    password = request.json['password']
    authenticated_user = user.login(email, password)
    if authenticated_user:
        return authenticated_user.to_json()
    abort(401)

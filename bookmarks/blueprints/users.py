from flask import Blueprint, request, abort, g
import bookmarks.core.user as user
from bookmarks.auth import login_required

bp = Blueprint('users', __name__, url_prefix='/')


@bp.post('/users')
def users():
    email = request.json['email']
    password = request.json['password']
    try:
        new_user = user.add_user(email, password)
    except user.EmailTaken:
        abort(422)
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
    try:
        user_token = user.login(email, password)
    except user.InvalidCredentials:
        abort(401)
    return user_token.to_json()

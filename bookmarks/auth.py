from flask import g, abort, request
import bookmarks.model.user as user
import functools
import bookmarks.types as types


def get_authenticated_user() -> user.User:
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        abort(401)
    try:
        username = user.UserToken(auth_header.split(' ')[1]).username()
        return user.get_user(username)
    except types.InvalidToken:
        abort(401)
    except user.UserNotFound:
        abort(401)


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        g.user = get_authenticated_user()
        return view(**kwargs)

    return wrapped_view

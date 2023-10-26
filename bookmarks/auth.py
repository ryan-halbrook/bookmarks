from flask import g, abort, request
import bookmarks.core.user as user
import functools


def get_authenticated_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        abort(401)
    authenticated_user = user.get_authenticated_user(
        auth_header.split(' ')[1])
    if not authenticated_user:
        abort(500)
    return authenticated_user


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        g.user = get_authenticated_user()
        return view(**kwargs)

    return wrapped_view

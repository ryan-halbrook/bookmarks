import bookmarks.db as db
from flask import Blueprint, request, abort
import bookmarks.core.tag as tag
import bookmarks.core.bookmark as bookmark
import bookmarks.core.user as user

bp = Blueprint('tags', __name__, url_prefix='/bookmarks')


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


@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,DELETE,PATCH'
    return response


@bp.post('/<id>/tags')
def bookmark_tags_post(id):
    data = request.json
    bookmark_user = bookmark.bookmark_user(id)
    authenticated_user = get_authenticated_user(request.headers.get('Authorization'))
    if not authenticated_user or authenticated_user.id != bookmark_user.id:
        abort(401)
    tag_bookmark_id = data.get('tag_bookmark_id', None)
    if not tag_bookmark_id:
        abort(400)
    tag.create(id, tag_bookmark_id)
    return ''


@bp.get('/<id>/tags')
def bookmark_tags(id):
    bookmark_user = bookmark.bookmark_user(id)
    authenticated_user = get_authenticated_user(request.headers.get('Authorization'))
    if not authenticated_user or authenticated_user.id != bookmark_user.id:
        abort(401)
    return [t.to_json() for t in tag.fetch_tags(id)]


@bp.delete('/<id>/tags/<tag_id>')
def bookmark_tags_delete(id, tag_id):
    bookmark_user = bookmark.bookmark_user(id)
    authenticated_user = get_authenticated_user(request.headers.get('Authorization'))
    if not authenticated_user or authenticated_user.id != bookmark_user.id:
        abort(401)
    tag.delete(tag_id)
    return []

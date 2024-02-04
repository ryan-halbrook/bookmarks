from flask import Blueprint, request, abort, g
import bookmarks.core.tag as tag
import bookmarks.core.bookmark as bookmark
from bookmarks.auth import login_required

bp = Blueprint('tags', __name__, url_prefix='/bookmarks')


@bp.post('/<id>/tags')
@login_required
def bookmark_tags_post(id):
    data = request.json
    if bookmark.bookmark_user_id(id) != g.user.id:
        abort(404)
    tag_bookmark_id = data.get('tag_bookmark_id', None)
    if not tag_bookmark_id:
        abort(400)
    try:
        tag.create(id, tag_bookmark_id)
    except Exception:
        abort(400)
    return ''


@bp.get('/<id>/tags')
@login_required
def bookmark_tags(id):
    if bookmark.bookmark_user_id(id) != g.user.id:
        abort(404)
    return [t.to_json() for t in tag.fetch_tags(id)]


@bp.delete('/<id>/tags/<tag_id>')
@login_required
def bookmark_tags_delete(id, tag_id):
    if bookmark.bookmark_user_id(id) != g.user.id:
        abort(404)
    tag.delete(tag_id)
    return []

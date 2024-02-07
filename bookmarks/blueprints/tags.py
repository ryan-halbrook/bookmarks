from flask import Blueprint, request, abort, g
import bookmarks.core.tag as tag
import bookmarks.core.bookmark as bookmark
from bookmarks.auth import login_required
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('tags', __name__, url_prefix='/bookmarks')


@bp.post('/<id>/tags')
@login_required
def bookmark_tags_post(id):
    try:
        id = int(id)
    except ValueError:
        logger.error('Bookmark id must be a valid integer.')
        abort(400)

    data = request.json
    if bookmark.bookmark_user_id(id) != g.user.id:
        abort(404)
    tag_bookmark_id = data.get('tag_bookmark_id', None)
    if not tag_bookmark_id:
        logger.error('tag_bookmark_id not found in request.')
        abort(400)
    try:
        tag.create(id, tag_bookmark_id)
        logger.error('Create tag failed.')
    except Exception:
        logger.error('Create tag failed.')
        abort(400)
    return ''


@bp.get('/<id>/tags')
@login_required
def bookmark_tags(id):
    try:
        id = int(id)
    except ValueError:
        abort(400)

    if bookmark.bookmark_user_id(id) != g.user.id:
        abort(404)
    return [t.to_json() for t in tag.fetch_tags(id)]


@bp.delete('/<id>/tags/<tag_id>')
@login_required
def bookmark_tags_delete(id, tag_id):
    try:
        id = int(id)
        tag_id = int(tag_id)
    except ValueError:
        abort(400)

    if bookmark.bookmark_user_id(id) != g.user.id:
        abort(404)
    tag.delete(tag_id)
    return []

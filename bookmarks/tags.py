import bookmarks.db as db
from flask import Blueprint, request, abort
import bookmarks.core.tag as tag

bp = Blueprint('tags', __name__, url_prefix='/bookmarks')


@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,DELETE,PATCH'
    return response


@bp.post('/<id>/tags')
def bookmark_tags_post(id):
    data = request.json
    tag_bookmark_id = data.get('tag_bookmark_id', None)
    if not tag_bookmark_id:
        abort(400)
    tag.create(id, tag_bookmark_id)
    return ''


@bp.get('/<id>/tags')
def bookmark_tags(id):
    return [t.to_json() for t in tag.fetch_tags(id)]

@bp.delete('/<id>/tags/<tag_id>')
def bookmark_tags_delete(id, tag_id):
    tag.delete(tag_id)
    return []

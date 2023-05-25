import flaskr.db as db
from flask import Blueprint, request, abort
import flaskr.core.tag as tag

bp = Blueprint('tags', __name__, url_prefix='/bookmarks')


@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
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

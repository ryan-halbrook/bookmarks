import flaskr.db as db
from flask import Blueprint, request, abort
import flaskr.core as core

bp = Blueprint('bookmarks', __name__, url_prefix='/')

@bp.get('/bookmarks')
def bookmarks():
    topic = request.args.get('topic', None)
    return [b.to_json() for b in core.get_bookmarks(topic=topic)]

@bp.post('/bookmarks')
def bookmarks_post():
    data = request.json
    topic = core.get_topic_with_name(data['topic'])
    if not topic:
        core.add_topic(data['topic'])
    core.add_bookmark(data['name'], data['topic'], data['link'], data['description'])
    return ''

@bp.delete('/bookmarks/<id>')
def bookmarks_delete(id):
    core.delete_bookmark(id)
    return ''

@bp.patch('/bookmarks/<id>')
def bookmarks_patch(id):
    data = request.json
    update_mask = request.args.get('update_mask', None)
    core.patch_bookmark(id,
                        name=data.get('name', None),
                        link=data.get('link', None),
                        topic_name=data.get('topic', None),
                        description=data.get('description', None),
                        update_mask=update_mask)
    return ''

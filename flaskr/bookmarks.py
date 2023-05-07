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

@bp.get('/bookmarks/<id>')
def bookmark_id(id):
    return core.get_bookmark_with_id(id).to_json()

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

@bp.get('/bookmarks/<id>/tags')
def bookmark_tags(id):
    return [t.to_json() for t in core.get_tags_for_bookmark(id)]

@bp.post('/bookmarks/<id>/tags')
def bookmark_tags_post(id):
    data = request.json
    tag_bookmark_id = data['tag_bookmark_id']
    if not tag_bookmark_id:
        abort(400)
    core.tag_bookmark(id, tag_bookmark_id)
    return ''

@bp.get('/bookmarks/<id>/resources')
def bookmark_resources(id):
    topic = request.args.get('topic', None)
    return [b.to_json() for b in core.get_tagged_with_id(id, topic=topic)]

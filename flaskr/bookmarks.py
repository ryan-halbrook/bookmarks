from flask import Blueprint, request, Response, abort
import flaskr.core.bookmark as bookmark
import flaskr.core.topic as topic

bp = Blueprint('bookmarks', __name__, url_prefix='/')


@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@bp.post('/bookmarks')
def bookmarks_post():
    data = request.json
    bookmark_topic = topic.fetch_single(name=data['topic'])
    if not bookmark_topic:
        topic.create(data['topic'])
        bookmark_topic = topic.fetch_single(name=data['topic'])
    bookmark.create(data['name'],
                    bookmark_topic.id,
                    data['link'],
                    data['description'])
    return ''


@bp.get('/bookmarks/<id>')
def bookmarks_get(id):
    return bookmark.fetch_single(id).to_json()


@bp.get('/bookmarks')
def bookmarks_get_collection():
    topic = request.args.get('topic', None)
    return [b.to_json() for b in bookmark.fetch(topic_name=topic)]


@bp.patch('/bookmarks/<id>')
def bookmarks_patch(id):
    data = request.json
    update_mask = request.args.get('update_mask', 'name,link,topic,description')
    update_fields = update_mask.split(',')
    name = data.get('name', None) if 'name' in update_fields else None
    link = data.get('link', None) if 'link' in update_fields else None
    topic = data.get('topic', None) if 'topic' in update_fields else None
    description = data.get('description', None) if 'description' in update_fields else None
   
    topic_id = None
    if topic:
        topic_id = topic.fetch_single(name=topic).id
        if not bookmark_topic:
            topic.create(topic)
            topic_id = topic.fetch_single(name=topic).id
    bookmark.update(id, name=name, link=link, topic_id=topic_id,
                    description=description)
    return ''


@bp.delete('/bookmarks/<id>')
def bookmarks_delete(id):
    bookmark.delete(id)
    return ''

import flaskr.db as db
from flask import Blueprint, request
import flaskr.core as core

bp = Blueprint('tags', __name__, url_prefix='/')

@bp.route('/tags')
def tags():
    return [t.to_json() for t in core.get_tags()]

@bp.route('/tag/<tag_name>')
def tag(tag_name):
    tag_topic = tag_name.split(':')[0]
    tag_name = tag_name.split(':')[1]
    topic = request.args.get('topic', None)
    return core.get_tagged_with(tag_topic, tag_name, topic=topic)
from flask import Blueprint, request, Response, abort
import flaskr.core.tag as tag

bp = Blueprint('bookmarks', __name__, url_prefix='/bookmarks')


@bp.get('/<id>/resources')
def bookmarks_resources(id):
    topic = request.args.get('topic', None)
    return [b.to_json() for b in tag.fetch_resources(id, topic_name=topic)]


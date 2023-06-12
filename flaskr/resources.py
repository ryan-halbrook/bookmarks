from flask import Blueprint, request, Response, abort
import flaskr.core.tag as tag

bp = Blueprint('bookmarks', __name__, url_prefix='/bookmarks')


@bp.get('/<id>/resources')
def bookmarks_resources(id):
    type_name = request.args.get('type', None)
    return [b.to_json() for b in tag.fetch_resources(id, type_name=type_name)]


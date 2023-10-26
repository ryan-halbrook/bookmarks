from flask import Blueprint, request, abort, g
import bookmarks.core.collection as collection
from bookmarks.auth import login_required

bp = Blueprint('collections', __name__, url_prefix='/')


@bp.get('/collections')
@login_required
def collections_get():
    return [c.to_json() for c in collection.fetch(g.user.id)]


@bp.post('/collections')
@login_required
def collections_post():
    new_collection_name = request.json.get('name')
    if not new_collection_name:
        abort(400)
    return collection.create(g.user.id, new_collection_name).to_json()

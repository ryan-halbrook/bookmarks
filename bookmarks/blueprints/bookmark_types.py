from flask import Blueprint, request, abort, g
import bookmarks.core.bookmark_type as bookmark_type
import bookmarks.core.collection as collection
from bookmarks.auth import login_required

bp = Blueprint('types', __name__, url_prefix='/')


@bp.get('/collections/<id>/types')
@login_required
def types_get(id):
    if collection.collection_user_id(id) != g.user.id:
        abort(404)

    return [t.to_json() for t in bookmark_type.fetch(collection_id=id)]


@bp.patch('/types/<id>')
@login_required
def types_update(id):
    data = request.json
    name = data.get('name', None)
    if not name:
        abort(400)
    btype = bookmark_type.fetch_single(id)
    if not btype:
        abort(404)
    if collection.collection_user_id(btype.collection_id) != g.user.id:
        abort(404)

    bookmark_type.update(id, name=name)
    return id


@bp.delete('/types/<id>')
@login_required
def types_delete(id):
    btype = bookmark_type.fetch_single(id)
    if not btype:
        abort(404)
    if collection.collection_user_id(btype.collection_id) != g.user.id:
        abort(404)

    bookmark_type.delete(id)
    return id

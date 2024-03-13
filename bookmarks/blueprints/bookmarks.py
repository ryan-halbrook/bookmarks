from flask import Blueprint, request, abort, g
import bookmarks.core.bookmark as bookmark
import bookmarks.core.bookmark_type as bookmark_type
import bookmarks.core.collection as collection
from bookmarks.auth import login_required


bp = Blueprint('bookmarks', __name__, url_prefix='/')


def fetch_or_create_type(cid, name):
    b_type = bookmark_type.fetch_single(collection_id=cid, name=name)
    if not b_type:
        bookmark_type.create(name, collection_id=cid)
        b_type = bookmark_type.fetch_single(collection_id=cid, name=name)
    return b_type


@bp.post('/collections/<cid>/bookmarks')
@login_required
def bookmarks_post(cid):
    try:
        cid = int(cid)
    except ValueError:
        abort(400)
    if collection.collection_user_id(cid) != g.user.id:
        abort(404)

    data = request.json
    return bookmark.create(fetch_or_create_type(cid, data['type']),
                           data['name'],
                           data['link'],
                           data['description'],
                           data.get('note'),
                           data.get('noteismarkdown')).to_json()


@bp.get('/collections/<cid>/bookmarks/<bid>')
@login_required
def bookmarks_get(cid, bid):
    try:
        cid = int(cid)
        bid = int(bid)
    except ValueError:
        abort(400)
    if collection.collection_user_id(cid) != g.user.id:
        abort(404)
    return bookmark.fetch_single(id=bid, collection_id=cid).to_json()


@bp.get('/collections/<cid>/bookmarks')
@login_required
def bookmarks_get_collection(cid):
    try:
        cid = int(cid)
    except ValueError:
        abort(400)
    if collection.collection_user_id(cid) != g.user.id:
        abort(404)
    type_name = request.args.get('type', None)

    match_type = request.args.get('match', None)
    query = request.args.get('query', None)

    if match_type and query:
        result = bookmark.search(cid, match_type, query)
    else:
        result = bookmark.fetch(user_id=g.user.id, collection_id=cid,
                                type_name=type_name)

    return [b.to_json() for b in result]


@bp.patch('/collections/<cid>/bookmarks/<bid>')
@login_required
def bookmarks_patch(cid, bid):
    try:
        cid = int(cid)
        bid = int(bid)
    except ValueError:
        abort(400)
    if collection.collection_user_id(cid) != g.user.id:
        abort(404)

    data = request.json
    if not data:
        abort(400)

    type_id = None
    if type_name := data.get('type'):
        type_id = fetch_or_create_type(cid, type_name).id

    bookmark.update(
        bid,
        name=data.get('name'),
        link=data.get('link'),
        type_id=type_id,
        description=data.get('description'),
        note=data.get('note'),
        note_is_markdown=data.get('note_is_markdown'))

    return ''


@bp.delete('/collections/<cid>/bookmarks/<bid>')
@login_required
def bookmarks_delete(cid, bid):
    try:
        cid = int(cid)
        bid = int(bid)
    except ValueError:
        abort(400)
    if bookmark.bookmark_user_id(bid) != g.user.id:
        abort(404)
    bookmark.delete(bid)
    return ''

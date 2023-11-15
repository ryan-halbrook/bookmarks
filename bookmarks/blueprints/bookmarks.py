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
    return b_type.id if b_type else None


@bp.post('/collections/<cid>/bookmarks')
@login_required
def bookmarks_post(cid):
    if collection.collection_user_id(cid) != g.user.id:
        abort(404)

    data = request.json
    type_name = data['type']
    type_id = fetch_or_create_type(cid, type_name)
    bookmark.create(cid,
                    data['name'],
                    type_id,
                    data['link'],
                    data['description'],
                    data.get('note'),
                    data.get('noteismarkdown'))
    return data


@bp.get('/collections/<cid>/bookmarks/<bid>')
@login_required
def bookmarks_get(cid, bid):
    if collection.collection_user_id(cid) != g.user.id:
        abort(404)
    return bookmark.fetch_single(id=bid, collection_id=cid).to_json()


@bp.get('/collections/<cid>/bookmarks')
@login_required
def bookmarks_get_collection(cid):
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
    if collection.collection_user_id(cid) != g.user.id:
        abort(404)

    if mask := request.args.get('update_mask'):
        mask_fields = mask.split(',')
    else:
        mask_fields = None

    def check_mask(field) -> bool:
        return (not mask_fields) or (field in mask_fields)

    def new_key_value(key) -> (str, any):
        if key == 'type_id' and check_mask('type'):
            if new_type_name := request.json.get('type', None):
                return ('type_id', fetch_or_create_type(cid, new_type_name))
        elif check_mask(key):
            return (key, request.json.get(key, None))

    keys = [
            'name',
            'link',
            'type_id',
            'description',
            'note',
            'note_is_markdown',
            ]

    updates = dict(filter(lambda x: x, [new_key_value(k) for k in keys]))
    bookmark.update(bid, **updates)
    return ''


@bp.delete('/collections/<cid>/bookmarks/<bid>')
@login_required
def bookmarks_delete(cid, bid):
    if bookmark.bookmark_user_id(bid) != g.user.id:
        abort(404)
    bookmark.delete(bid)
    return ''

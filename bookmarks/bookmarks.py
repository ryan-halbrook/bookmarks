from flask import Blueprint, request, abort
import bookmarks.core.bookmark as bookmark
import bookmarks.core.bookmark_type as bookmark_type
import bookmarks.core.user as user
import bookmarks.core.collection as collection

bp = Blueprint('bookmarks', __name__, url_prefix='/')


@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,DELETE,PATCH'
    return response


def get_authenticated_user(authorization):
    if not authorization:
        print('no auth')
        abort(401)
    print(authorization)
    authenticated_user = user.get_authenticated_user(
        authorization.split(' ')[1])
    if not authenticated_user:
        abort(500)
    return authenticated_user


def abort_if_unauthorized(user_id, collection_id):
    coll = collection.fetch_single(collection_id)
    if not coll:
        abort(404)
    if coll.user_id != user_id:
        abort(401)


def fetch_or_create_type(cid, name):
    b_type = bookmark_type.fetch_single(collection_id=cid, name=name)
    if not b_type:
        bookmark_type.create(name, collection_id=cid)
        b_type = bookmark_type.fetch_single(collection_id=cid, name=name)
    return b_type.id if b_type else None


@bp.post('/collections/<cid>/bookmarks')
def bookmarks_post(cid):
    user = get_authenticated_user(request.headers['Authorization'])
    abort_if_unauthorized(user.id, cid)

    data = request.json
    type_name = data['type']
    type_id = fetch_or_create_type(cid, type_name)
    bookmark.create(cid,
                    data['name'],
                    type_id,
                    data['link'],
                    data['description'])
    return data


@bp.get('/collections/<cid>/bookmarks/<bid>')
def bookmarks_get(cid, bid):
    user = get_authenticated_user(request.headers['Authorization'])
    abort_if_unauthorized(user.id, cid)
    return bookmark.fetch_single(id=bid, collection_id=cid).to_json()


@bp.get('/collections/<cid>/bookmarks')
def bookmarks_get_collection(cid):
    user = get_authenticated_user(request.headers['Authorization'])
    abort_if_unauthorized(user.id, cid)
    type_name = request.args.get('type', None)

    result = bookmark.fetch(user_id=user.id, collection_id=cid, type_name=type_name)
    return [b.to_json() for b in result]


@bp.patch('/collections/<cid>/bookmarks/<bid>')
def bookmarks_patch(cid, bid):
    user = get_authenticated_user(request.headers['Authorization'])
    abort_if_unauthorized(user.id, cid)

    data = request.json
    update_mask = request.args.get('update_mask', 'name,link,type,description')
    update_fields = update_mask.split(',')
    name = data.get('name', None) if 'name' in update_fields else None
    link = data.get('link', None) if 'link' in update_fields else None
    type_name = data.get('type', None) if 'type' in update_fields else None
    description = data.get(
        'description', None) if 'description' in update_fields else None

    new_type_id = None
    if type_name:
        new_type_id = fetch_or_create_type(cid, type_name)

    bookmark.update(bid, name=name, link=link, type_id=new_type_id,
                    description=description)
    return ''


@bp.delete('/collections/<cid>/bookmarks/<bid>')
def bookmarks_delete(cid, bid):
    user = get_authenticated_user(request.headers['Authorization'])
    abort_if_unauthorized(user.id, cid)
    bookmark.delete(bid, collection_id=cid)
    return ''

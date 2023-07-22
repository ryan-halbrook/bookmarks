from flask import Blueprint, request, Response
import bookmarks.core.bookmark as bookmark
import bookmarks.core.bookmark_type as bookmark_type

bp = Blueprint('bookmarks', __name__, url_prefix='/')


@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,DELETE,PATCH'
    return response


@bp.post('/collections/<cid>/bookmarks')
def bookmarks_post(cid):
    data = request.json
    type_name = data['type']
    btype = bookmark_type.fetch_single(name=type_name)
    if not btype:
        bookmark_type.create(data['type'])
        btype = bookmark_type.fetch_single(name=type_name)
    bookmark.create(cid,
                    data['name'],
                    btype.id,
                    data['link'],
                    data['description'])
    return data


@bp.get('/collections/<cid>/bookmarks/<bid>')
def bookmarks_get(cid, bid):
    return bookmark.fetch_single(bid, collection_id=cid).to_json()


@bp.get('/collections/<cid>/bookmarks')
def bookmarks_get_collection(cid):
    type_name = request.args.get('type', None)
    return [b.to_json() for b in bookmark.fetch(collection_id=cid, type_name=type_name)]


@bp.patch('/collections/<cid>/bookmarks/<bid>')
def bookmarks_patch(cid, bid):
    data = request.json
    update_mask = request.args.get('update_mask', 'name,link,type,description')
    update_fields = update_mask.split(',')
    name = data.get('name', None) if 'name' in update_fields else None
    link = data.get('link', None) if 'link' in update_fields else None
    type_name = data.get('type', None) if 'type' in update_fields else None
    description = data.get('description', None) if 'description' in update_fields else None
   
    btype = None
    if type_name:
        btype = bookmark_type.fetch_single(collection_id=cid, name=type_name)
        if not btype:
            bookmark_type.create(type_name)
            btype = bookmark_type.fetch_single(collection_id=cid, name=type_name)
    type_id = btype.id if btype else None

    bookmark.update(bid, name=name, link=link, type_id=type_id,
                    description=description)
    return ''


@bp.delete('/collections/<cid>/bookmarks/<bid>')
def bookmarks_delete(cid, bid):
    bookmark.delete(bid, collection_id=cid)
    return ''

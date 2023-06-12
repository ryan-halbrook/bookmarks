from flask import Blueprint, request, Response, abort
import flaskr.core.bookmark as bookmark
import flaskr.core.bookmark_type as bookmark_type

bp = Blueprint('bookmarks', __name__, url_prefix='/')


@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,DELETE,PATCH'
    return response


@bp.post('/bookmarks')
def bookmarks_post():
    data = request.json
    type_name = data['type']
    btype = bookmark_type.fetch_single(name=type_name)
    if not btype:
        bookmark_type.create(data['type'])
        btype = bookmark_type.fetch_single(name=type_name)
    bookmark.create(data['name'],
                    btype.id,
                    data['link'],
                    data['description'])
    return data


@bp.get('/bookmarks/<id>')
def bookmarks_get(id):
    return bookmark.fetch_single(id).to_json()


@bp.get('/bookmarks')
def bookmarks_get_collection():
    type_name = request.args.get('type', None)
    return [b.to_json() for b in bookmark.fetch(type_name=type_name)]


@bp.patch('/bookmarks/<id>')
def bookmarks_patch(id):
    data = request.json
    update_mask = request.args.get('update_mask', 'name,link,type,description')
    update_fields = update_mask.split(',')
    name = data.get('name', None) if 'name' in update_fields else None
    link = data.get('link', None) if 'link' in update_fields else None
    type_name = data.get('type', None) if 'type' in update_fields else None
    description = data.get('description', None) if 'description' in update_fields else None
   
    type_id = None
    if type_name:
        type_id = bookmark_type.fetch_single(name=type_name).id
        if not type_id:
            bookmark_type.create(type_name)
            type_id = bookmark_type.fetch_single(name=type_name).id
    bookmark.update(id, name=name, link=link, type_id=type_id,
                    description=description)
    return ''


@bp.delete('/bookmarks/<id>')
def bookmarks_delete(id):
    bookmark.delete(id)
    return ''

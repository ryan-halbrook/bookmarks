from flask import Blueprint, request, Response, abort
import bookmarks.core.collection as collection

bp = Blueprint('collections', __name__, url_prefix='/')


@bp.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'X-PINGOTHER, Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS,DELETE,PATCH'
    return response


@bp.get('/collections')
def collections_get():
    return [c.to_json() for c in collection.fetch()]

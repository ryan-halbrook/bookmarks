from flask import request, abort, g
from flask.views import MethodView
import bookmarks.model.bookmark_type as bookmark_type
import bookmarks.model.collection as collection


class TypeCollectionAPI(MethodView):
    init_every_request = False

    def get(self, id):
        try:
            id = int(id)
        except ValueError:
            abort(400)
        if collection.collection_user_id(id) != g.user.id:
            abort(404)

        return [t.to_json() for t in bookmark_type.fetch(collection_id=id)]


class TypeAPI(MethodView):
    init_every_request = False

    def patch(self, id):
        try:
            id = int(id)
        except ValueError:
            abort(400)

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
        return 'OK'

    def delete(self, id):
        try:
            id = int(id)
        except ValueError:
            abort(400)

        btype = bookmark_type.fetch_single(id)
        if not btype:
            abort(404)
        if collection.collection_user_id(btype.collection_id) != g.user.id:
            abort(404)

        bookmark_type.delete(id)
        return 'OK'

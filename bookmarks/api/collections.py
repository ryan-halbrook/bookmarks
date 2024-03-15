from flask import request, abort, g
from flask.views import MethodView
import bookmarks.model.collection as collection


class CollectionAPI(MethodView):
    init_every_request = False

    def get(self):
        return [c.to_json() for c in collection.fetch(g.user.id)]

    def post(self):
        new_collection_name = request.json.get('name')
        if not new_collection_name:
            abort(400)
        return collection.create(g.user.id, new_collection_name).to_json()

from flask import request, abort, g
from flask.views import MethodView
import bookmarks.model.tag as tag
import bookmarks.model.bookmark as bookmark
import logging

logger = logging.getLogger(__name__)


class TagCollectionAPI(MethodView):
    init_every_request = False

    def post(self, id):
        try:
            id = int(id)
        except ValueError:
            logger.error('Bookmark id must be a valid integer.')
            abort(400)

        data = request.json
        if bookmark.bookmark_user_id(id) != g.user.id:
            abort(404)
        tag_bookmark_id = data.get('tag_bookmark_id', None)
        if not tag_bookmark_id:
            logger.error('tag_bookmark_id not found in request.')
            abort(400)
        try:
            tag.create(id, tag_bookmark_id)
            logger.error('Create tag failed.')
        except Exception:
            logger.error('Create tag failed.')
            abort(400)
        return ''

    def get(self, id):
        try:
            id = int(id)
        except ValueError:
            abort(400)

        if bookmark.bookmark_user_id(id) != g.user.id:
            abort(404)
        return [t.to_json() for t in tag.fetch_tags(id)]


class TagAPI(MethodView):
    init_every_request = False

    def delete(self, id, tag_id):
        try:
            id = int(id)
            tag_id = int(tag_id)
        except ValueError:
            abort(400)

        if bookmark.bookmark_user_id(id) != g.user.id:
            abort(404)
        tag.delete(tag_id)
        return []

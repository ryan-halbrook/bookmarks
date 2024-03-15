import os
from flask import Flask
from bookmarks.auth import login_required
from bookmarks.api.bookmarks import BookmarkCollectionAPI, BookmarkAPI
from bookmarks.api.collections import CollectionAPI
from bookmarks.api.bookmark_types import TypeCollectionAPI, TypeAPI
from bookmarks.api.users import UserAPI, UserLoginAPI, NewUserAPI
from bookmarks.api.tags import TagCollectionAPI, TagAPI


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if 'DB_URI' in os.environ:
        db_uri = os.environ['DB_URI']
    else:
        db_user = os.environ.get('DB_USER', 'postgres')
        db_password = os.environ.get('DB_PASSWORD', 'postgres')
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '5432')
        db_database = os.environ.get('DB_DATABASE', 'postgres')
        db_uri = 'postgresql://%s:%s@%s:%s/%s' % \
            (db_user, db_password, db_host, db_port, db_database)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DB_URI=db_uri
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    app.add_url_rule("/users", view_func=NewUserAPI.as_view("user_new"))
    app.add_url_rule(
        "/users", view_func=login_required(UserAPI.as_view("user")))
    app.add_url_rule(
        "/users/login", view_func=UserLoginAPI.as_view("user_login"))
    app.add_url_rule(
        "/collections",
        view_func=login_required(CollectionAPI.as_view("collections")))
    app.add_url_rule(
        "/collections/<int:id>/types",
        view_func=login_required(
            TypeCollectionAPI.as_view("type_collection")))
    app.add_url_rule(
        "/types/<int:id>", view_func=login_required(TypeAPI.as_view("type")))
    app.add_url_rule(
        "/collections/<int:cid>/bookmarks",
        view_func=login_required(
            BookmarkCollectionAPI.as_view("bookmark_collection")))
    app.add_url_rule(
        "/collections/<int:cid>/bookmarks/<int:bid>",
        view_func=login_required(BookmarkAPI.as_view("bookmark")))
    app.add_url_rule(
        "/bookmarks/<int:id>/tags",
        view_func=login_required(TagCollectionAPI.as_view("tag_collection")))
    app.add_url_rule(
        "/bookmarks/<int:id>/tags/<int:tag_id>",
        view_func=login_required(TagAPI.as_view("tag")))

    @app.get('/')
    def health_check():
        return 'OK'

    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = \
            'X-PINGOTHER, Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = \
            'GET,POST,OPTIONS,DELETE,PATCH'
        return response

    return app

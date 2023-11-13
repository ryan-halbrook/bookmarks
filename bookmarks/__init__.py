import os
from flask import Flask


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

    from bookmarks.blueprints import users
    app.register_blueprint(users.bp)

    from bookmarks.blueprints import bookmark_types
    app.register_blueprint(bookmark_types.bp)

    from bookmarks.blueprints import bookmarks
    app.register_blueprint(bookmarks.bp)

    from bookmarks.blueprints import collections
    app.register_blueprint(collections.bp)

    from bookmarks.blueprints import tags
    app.register_blueprint(tags.bp)

    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = \
            'X-PINGOTHER, Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = \
            'GET,POST,OPTIONS,DELETE,PATCH'
        return response

    return app

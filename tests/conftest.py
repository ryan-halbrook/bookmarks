import os
import tempfile

import pytest
from bookmarks import create_app
from bookmarks.db import get_db, init_db
import bookmarks.core.user as user

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf-8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def authenticated_user(app):
    email = 'user@example.com'
    password = '1234'

    with app.app_context():
        user.add_user(email, password)
        auth_user = user.login(email, password)

        # Steal the collections from the user defined in static test sql
        get_db().execute('UPDATE collections SET user_id = ?', (auth_user.id,))
        get_db().commit()

    return auth_user


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

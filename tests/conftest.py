import os
import pytest
from bookmarks import create_app
from bookmarks.db import get_db, get_cursor, init_db
import bookmarks.model.user as user
from testcontainers.postgres import PostgresContainer  # type: ignore


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf-8')


@pytest.fixture
def app(postgres):
    db_uri = ''.join(postgres.get_connection_url().split('+psycopg2'))
    app = create_app(
            {
                'TESTING': True,
                'SECRET_KEY': 'test secret',
                'DB_URI': db_uri
            })

    with app.app_context():
        cur = get_cursor()

        def clean_db():
            cur.execute('DROP SCHEMA public CASCADE')
            cur.execute('CREATE SCHEMA public')

        def insert_test_data():
            cur.execute(_data_sql)

        clean_db()
        init_db()
        insert_test_data()

        get_db().commit()
        cur.close()

    yield app


@pytest.fixture(scope='session')
def postgres(request):
    postgres = PostgresContainer('postgres:16.1', user='test')
    postgres.start()
    yield postgres
    postgres.stop()


class AuthenticatedUser:
    def __init__(self, user, user_token):
        self.user = user
        self.user_token = user_token


@pytest.fixture
def authenticated_user(app) -> AuthenticatedUser:
    email = 'user@example.com'
    password = '1234'

    with app.app_context():
        new_user = user.add_user(email, password)
        user_token = user.login(email, password)

        # Steal collections from the user defined in static test sql
        try:
            cur = get_cursor()
            cur.execute('UPDATE collections SET user_id = %s', (new_user.id,))
            get_db().commit()
        finally:
            cur.close()

    return AuthenticatedUser(new_user, user_token)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

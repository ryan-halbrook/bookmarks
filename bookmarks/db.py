import psycopg2
import psycopg2.extras
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            current_app.config['DB_URI'],
            cursor_factory=psycopg2.extras.DictCursor
        )

    return g.db


def get_cursor():
    return get_db().cursor()


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    with current_app.open_resource('schema.sql') as f:
        cur = get_cursor()
        cur.execute(f.read().decode('utf8'))
        get_db().commit()
        cur.close()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

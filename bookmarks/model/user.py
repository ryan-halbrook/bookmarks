import bookmarks.db as db
from bookmarks.types import User, UserToken
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
import jwt
import psycopg2.errors


class EmailTaken(Exception):
    pass


class UserNotFound(Exception):
    pass


class InvalidCredentials(Exception):
    pass


def add_user(email: str, password: str) -> User:
    try:
        cur = db.get_cursor()
        cur.execute('INSERT INTO users (username, password) '
                    'VALUES (%s, %s) RETURNING *',
                    (email, generate_password_hash(password),))
        result = cur.fetchone()
        db.get_db().commit()
    except psycopg2.errors.UniqueViolation:
        raise EmailTaken()
    finally:
        cur.close()
    return User(result['id'], result['username'])


def login(email: str, password: str) -> UserToken:
    cur = db.get_cursor()
    cur.execute(
        'SELECT id, password FROM users WHERE username = %s',
        (email,))
    result = cur.fetchone()
    cur.close()

    if not (result and check_password_hash(result['password'], password)):
        raise InvalidCredentials()

    return UserToken(jwt.encode(
        {'user': email},
        current_app.config['SECRET_KEY'],
        algorithm='HS256'))


def get_user(email: str) -> User:
    cur = db.get_cursor()
    cur.execute(
        'SELECT id, username FROM users WHERE username = %s',
        (email,))
    result = cur.fetchone()
    cur.close()
    if not result:
        raise UserNotFound()
    return User(result['id'], result['username'])


def update_user(user_id: str, email: str, password: str) -> User:
    try:
        cur = db.get_cursor()
        cur.execute(
            'UPDATE users SET username = %s, password = %s '
            'WHERE id = %s RETURNING *',
            (email, generate_password_hash(password), user_id,))
        result = cur.fetchone()
        db.get_db().commit()
    except psycopg2.errors.UniqueViolation:
        raise EmailTaken()
    finally:
        cur.close()

    if not result:
        raise UserNotFound()
    return User(result['id'], result['username'])

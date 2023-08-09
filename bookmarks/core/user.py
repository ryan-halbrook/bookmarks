import bookmarks.db as db
from types import User, AuthenticatedUser
from werkzeug.security import generate_password_hash
import jwt
import sqlite3


def add_user(email: str, password: str) -> User | None:
    try:
        db.get_db().execute('INSERT INTO users (username, password) VALUES (?, ?)',
                            email, generate_password_hash(password))
        user_id = db.get_db().cursor().lastrowid
    except sqlite3.Error:
        return None
    return User(user_id, email)


def get_jwt_token(email: str, password: str) -> AuthenticatedUser | None:
    result = db.get_db().execute(
        'SELECT (id, username, password) FROM users WHERE username = ?', email).fetchone()
    if result['password'] != generate_password_hash(password):
        return None
    token = jwt.encode(
        {'user': result['username']}, 'secret', algorithm='HS256')
    return AuthenticatedUser(result['id'], result['username'], token)


def auth_jwt_token(email: str, token: str) -> bool:
    decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
    return email == decoded_token['user']


def get_user(email: str) -> User | None:
    result = db.get_db.execute(
        'SELECT (id, username) FROM users WHERE username = ?',
        (email)).fetchone()
    if not result:
        return None
    return User(result['id', result['username']])


def update_user(token: str, email: str, password: str) -> User | None:
    if not auth_jwt_token(email, token):
        raise
    user = get_user(email)
    if not user:
        raise
    try:
        db.get_db().execute(
            'UPDATE users SET (username, password) VALUES (?, ?) WHERE id = ?',
            email, password, user.user_id)
    except sqlite3.Error:
        return None
    return User(db.get_db().cursor().lastrowid, email)
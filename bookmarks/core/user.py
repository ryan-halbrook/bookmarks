import bookmarks.db as db
from bookmarks.types import User, AuthenticatedUser
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
import jwt
import sqlite3


def add_user(email: str, password: str):
    try:
        cur = db.get_db().cursor()
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                    (email, generate_password_hash(password),))
        user_id = cur.lastrowid
        db.get_db().commit()
    except sqlite3.Error:
        return None
    return User(user_id, email)


def login(email: str, password: str):
    result = db.get_db().execute(
        'SELECT id, password FROM users WHERE username = ?', (email,)).fetchone()
    if not (result and check_password_hash(result['password'], password)):
        return None
    token = jwt.encode(
        {'user': email}, current_app.config['SECRET_KEY'], algorithm='HS256')
    return AuthenticatedUser(result['id'], email, token)


def auth_jwt_token(token: str):
    decoded_token = jwt.decode(
        token, current_app.config['SECRET_KEY'],
        algorithms=['HS256'])
    return decoded_token['user']


def get_user(email: str):
    result = db.get_db().execute(
        'SELECT id, username FROM users WHERE username = ?',
        (email,)).fetchone()
    if not result:
        return None
    return User(result['id'], result['username'])


def update_user(token: str, email: str, password: str):
    current_email = auth_jwt_token(token)
    if not current_email:
        print("token invalid")
        raise
    user = get_user(current_email)
    if not user:
        print("user not found")
        raise
    try:
        cur = db.get_db().cursor()
        cur.execute(
            'UPDATE users SET username = ?, password = ? WHERE id = ?',
            (email, generate_password_hash(password), user.id,))
        db.get_db().commit()
    except sqlite3.Error as e:
        print(e)
        return None

    return get_user(email)


def get_authenticated_user(authorization):
    email = auth_jwt_token(authorization)
    if not email:
        return None
    return get_user(email)

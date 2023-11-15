from datetime import datetime
import jwt
import jwt.exceptions
from flask import current_app


class NameInUse(BaseException):
    pass


class User:
    def __init__(self, id: int, email: str):
        self.id = id
        self.email = email

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email
        }


class InvalidToken(BaseException):
    pass


class UserToken:
    def __init__(self, token: str):
        self.token = token
        self._decoded_token = None

    def to_json(self):
        return {
            'token': self.token
        }

    def decoded_token(self):
        if not self._decoded_token:
            self._decoded_token = jwt.decode(
                self.token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])

        return self._decoded_token

    def username(self):
        return self.decoded_token()['user']


class Collection:
    def __init__(self, id: int, created: datetime, name: str, user_id: int):
        self.id = id
        self.created = created
        self.name = name
        self.user_id = user_id

    def to_json(self):
        return {
            'id': self.id,
            'created': self.created,
            'name': self.name if self.name else 'UNRESOLVED',
            'user_id': self.user_id,
        }


class Type:
    def __init__(self, id: int, name: str, collection_id):
        self.id = id
        self.name = name
        self.collection_id = collection_id

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name if self.name else 'UNRESOLVED',
            'collection_id': self.collection_id,
        }


class Bookmark:
    def __init__(self, id: int, created: datetime, name: str,
                 bookmark_type: Type, link: str, description: str,
                 note: str = None, note_is_markdown: bool = False):
        self.id = id
        self.created = created
        self.name = name
        self.bookmark_type = bookmark_type
        self.link = link
        self.description = description
        self.note = note
        self.note_is_markdown = note_is_markdown

    def to_json(self):
        return {
            'id': self.id,
            'created': self.created,
            'name': self.name,
            'type': self.bookmark_type.to_json(),
            'link': self.link,
            'description': self.description,
            'note': self.note,
            'note_is_markdown': self.note_is_markdown
        }


class Tag:
    def __init__(self, id: int, bookmark: Bookmark):
        self.id = id
        self.bookmark = bookmark

    def to_json(self):
        return {
            'tag_id': self.id,
            'bookmark': self.bookmark.to_json(),
        }

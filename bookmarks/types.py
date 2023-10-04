from datetime import datetime

class User:
    def __init__(self, id: int, email: str):
        self.id = id
        self.email = email

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email
        }


class AuthenticatedUser:
    def __init__(self, id: int, email: str, token: str):
        self.id = id
        self.email = email
        self.token = token

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'token': self.token
        }


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
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name if self.name else 'UNRESOLVED',
        }


class Bookmark:
    def __init__(self, id: int, created: datetime, name: str,
                 bookmark_type: Type, link: str, description: str):
        self.id = id
        self.created = created
        self.name = name
        self.bookmark_type = bookmark_type
        self.link = link
        self.description = description

    def to_json(self):
        return {
            'id': self.id,
            'created': self.created,
            'name': self.name,
            'type': self.bookmark_type.to_json(),
            'link': self.link,
            'description': self.description,
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

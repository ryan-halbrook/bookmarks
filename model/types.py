from datetime import datetime


class User:
    def __init__(self, id: int, username: str, password: str):
        self.id = id
        self.username = username
        self.password = password


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
            'user-id': self.user_id,
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
    def __init__(self, id: int, created: datetime, bookmark: Bookmark,
                 tag_bookmark: Bookmark):
        self.id = id
        self.created = created
        self.bookmark = bookmark
        self.tag_bookmark = tag_bookmark
    
    def to_json(self):
        return {
            'id': self.id,
            'created': self.created,
            'bookmark': self.bookmark.to_json(),
            'tag': self.tag_bookmark.to_json(),
        }

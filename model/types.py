
class Topic:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name if self.name else 'UNRESOLVED',
        }

class Bookmark:
    def __init__(self, id: int, name: str, topic: Topic, link: str, description: str):
        self.id = id
        self.name = name
        self.topic = topic
        self.link = link
        self.description = description

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'topic': self.topic.to_json(),
            'link': self.link,
            'description': self.description,
        }

class Tag:
    def __init__(self, id: int, bookmark: Bookmark, tag_bookmark: Bookmark):
        self.id = id
        self.bookmark = bookmark
        self.tag_bookmark = tag_bookmark
    
    def to_json(self):
        return {
            'id': self.id,
            'bookmark': self.bookmark.to_json(),
            'tag': self.tag_bookmark.to_json(),
        }
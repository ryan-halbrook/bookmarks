import flaskr.db as db
from model.types import Bookmark, Topic, Tag

def get_bookmarks(topic=None):
    if topic:
        fetchResult = db.get_db().execute(
            'SELECT b.id as bookmark_id, b.name as bookmark_name,'
            ' b.link as bookmark_link, t.name as topic_name,'
            ' t.id as topic_id, b.description as bookmark_description'
            ' FROM bookmarks as b, topics as t'
            ' WHERE b.topic_id = t.id AND t.name = ?',
            (topic,)
        ).fetchall()
    else:
        fetchResult = db.get_db().execute(
            'SELECT b.id as bookmark_id, b.name as bookmark_name,'
            ' b.link as bookmark_link, t.name as topic_name,'
            ' t.id as topic_id, b.description as bookmark_description'
            ' FROM bookmarks as b, topics as t'
            ' WHERE b.topic_id = t.id'
        ).fetchall()
    bookmarks = []
    for row in fetchResult:
        bookmarks.append(
            Bookmark(
                row['bookmark_id'],
                row['bookmark_name'],
                Topic(
                    row['topic_id'],
                    row['topic_name']
                ),
                row['bookmark_link'],
                row['bookmark_description']
            )
        )
    return bookmarks

def get_bookmark(topic, name):
    fetchResult = db.get_db().execute(
        'SELECT b.id as id, b.name as name, b.link as link,'
        ' b.description as description, t.id as tag_id, t.name as tag_name '
        ' FROM bookmarks as b,'
        ' topics as t WHERE b.topic_id = t.id'
        ' AND t.name = ? AND b.name = ?',
        (topic, name,)
    ).fetchone()
    return Bookmark(
        fetchResult['id'],
        fetchResult['name'],
        Topic(
            fetchResult['tag_id'],
            fetchResult['tag_name'],
        ),
        fetchResult['link'],
        fetchResult['description'],
    )

def get_bookmark_with_id(id):
    fetchResult = db.get_db().execute(
        'SELECT b.id as id, b.name as name, b.link as link,'
        ' b.description as description, t.id as tag_id, t.name as tag_name '
        ' FROM bookmarks as b,'
        ' topics as t WHERE b.topic_id = t.id'
        ' AND b.id = ?',
        (id,)
    ).fetchone()
    return Bookmark(
        fetchResult['id'],
        fetchResult['name'],
        Topic(
            fetchResult['tag_id'],
            fetchResult['tag_name'],
        ),
        fetchResult['link'],
        fetchResult['description'],
    )

def get_tags_for_bookmark(bookmark_id, topic=None):
    if topic:
        fetchResult = db.get_db().execute(
            'SELECT ta.name as topic_name, a.id as bookmark_id,'
            ' a.name as bookmark_name, a.link as bookmark_link,'
            ' ta.id as topic_id'
            ' FROM tags as t, bookmarks as a, topics as ta'
            ' WHERE a.topic_id = ta.id'
            ' AND t.bookmark_id = ? AND t.tag_bookmark_id = a.id'
            ' AND ta.name = ?',
            (bookmark_id, topic,)
        ).fetchall()
    else:
        fetchResult = db.get_db().execute(
            'SELECT ta.name as topic_name, a.id as bookmark_id,'
            ' a.name as bookmark_name, a.link as bookmark_link,'
            ' ta.id as topic_id, a.description as bookmark_description'
            ' FROM tags as t, bookmarks as a, topics as ta'
            ' WHERE a.topic_id = ta.id'
            ' AND t.bookmark_id = ? AND t.tag_bookmark_id = a.id',
            (bookmark_id,)
        ).fetchall()
    bookmarks = []
    for row in fetchResult:
        bookmarks.append(
            Bookmark(
                row['bookmark_id'],
                row['bookmark_name'],
                Topic(
                    row['topic_id'],
                    row['topic_name']
                ),
                row['bookmark_link'],
                row['bookmark_description']
            )
        )
    return bookmarks

def get_tagged_with(tag_topic, tag_name, topic=None):
    bookmark_id = get_bookmark(tag_topic, tag_name).id
    if topic:
        fetchResult = db.get_db().execute(
            'SELECT ta.name as topic_name, a.id as bookmark_id,'
            ' a.name as bookmark_name, a.link as bookmark_link,'
            ' ta.id as topic_id'
            ' FROM tags as t, bookmarks as a, topics as ta'
            ' WHERE a.topic_id = ta.id'
            ' AND t.bookmark_id = a.id AND t.tag_bookmark_id = ?'
            ' AND ta.name = ?',
            (bookmark_id, topic,)
        ).fetchall()
    else:
        fetchResult = db.get_db().execute(
            'SELECT ta.name as topic_name, a.id as bookmark_id,'
            ' a.name as bookmark_name, a.link as bookmark_link,'
            ' ta.id as topic_id, a.description as bookmark_description'
            ' FROM tags as t, bookmarks as a, topics as ta'
            ' WHERE a.topic_id = ta.id'
            ' AND t.bookmark_id = a.id AND t.tag_bookmark_id = ?',
            (bookmark_id,)
        ).fetchall()
    bookmarks = []
    for row in fetchResult:
        bookmarks.append(
            Bookmark(
                row['bookmark_id'],
                row['bookmark_name'],
                Topic(
                    row['topic_id'],
                    row['topic_name']
                ),
                row['bookmark_link'],
                row['bookmark_description']
            )
        )
    return bookmarks

def add_bookmark(name, topic_name, link, description):
    topic = get_topic_with_name(topic_name)
    if not topic:
        print('Could not find topic: ' + topic_name)
        return

    db.get_db().execute(
        'INSERT INTO bookmarks (name, topic_id, link, description)'
        ' VALUES (?, ?, ?, ?)',
        (name, topic.id, link, description)
    )
    db.get_db().commit()

def patch_bookmark(id, name=None, link=None, topic_name=None, description=None, update_mask=None):
    if not any([name, link, topic_name, description]):
        raise
    bookmark = get_bookmark_with_id(id)
    change_topic = topic_name and bookmark.topic.name != topic_name
    topic_id = None
    if topic_name:
        topic = get_topic_with_name(topic_name)
        if topic:
            topic_id = topic.id
        else:
            add_topic(topic_name)
            topic = get_topic_with_name(topic_name)
            topic_id = topic.id
    if not any([name, link, change_topic, description]):
        raise

    update_fields = ['name', 'link', 'description', 'topic']
    if update_mask:
        update_fields = update_mask.split(',')

    sets = {}
    if name and ('name' in update_fields):
        sets['name'] = name
    if link and ('link' in update_fields):
        sets['link'] = link
    if change_topic and ('topic' in update_fields):
        sets['topic_id'] = topic_id
    if description and ('description' in update_fields):
        sets['description'] = description

    set_stmt = ' SET '
    set_values = []
    first = True
    for key, value in sets.items():
        if not first:
            set_stmt += ', '
        set_stmt += key + ' = ?'
        set_values.append(value)
        first = False

    db.get_db().execute(
        'UPDATE bookmarks' + set_stmt + ' WHERE id = ?',
        set_values + [id]
        #(name, link, topic.id, description, id,)
    )
    db.get_db().commit()


def delete_bookmark(id):
    db.get_db().execute(
        'DELETE FROM bookmarks WHERE id = ?',
        (id,)
    )
    db.get_db().commit()

def get_topic_with_id(id):
    fetchResult = db.get_db().execute(
        'SELECT id, name FROM topics WHERE id = ?',
        (id,)
    ).fetchone()
    return Topic(fetchResult['id'], fetchResult['name'])

def get_topic_with_name(name):
    fetchResult = db.get_db().execute(
        'SELECT id, name FROM topics WHERE name = ?',
        (name,)
    ).fetchone()
    if fetchResult:
        return Topic(fetchResult['id'], fetchResult['name'])
    return None

def get_topics():
    fetchResult = db.get_db().execute(
        'SELECT id, name FROM topics'
    ).fetchall()
    return [Topic(f['id'], f['name']) for f in fetchResult]

def get_tags():
    fetchResults = db.get_db().execute(
        'SELECT t.id as tag_id,'
        ' a.name as bookmark_name, a.id as bookmark_id,'
        ' a.link as bookmark_link, a.description as bookmark_description,'
        ' b.name as tag_bookmark_name, b.id as tag_bookmark_id,'
        ' b.link as tag_bookmark_link, b.description as tag_bookmark_description,'
        ' ta.name as bookmark_topic_name, ta.id as bookmark_topic_id,'
        ' tb.name as tag_topic_name, tb.id as tag_topic_id'
        ' FROM tags as t, bookmarks as a, bookmarks as b,'
        ' topics as ta, topics as tb'
        ' WHERE t.bookmark_id = a.id AND t.tag_bookmark_id = b.id'
        ' AND a.topic_id = ta.id AND b.topic_id = tb.id'
    ).fetchall()
    tags = []
    for row in fetchResults:
        bookmark = Bookmark(
            row['bookmark_id'],
            row['bookmark_name'],
            Topic(
                row['bookmark_topic_id'],
                row['bookmark_topic_name']
            ),
            row['bookmark_link'],
            row['bookmark_description']
        )
        tag_bookmark = Bookmark(
            row['tag_bookmark_id'],
            row['tag_bookmark_name'],
            Topic(
                row['tag_topic_id'],
                row['tag_topic_name']
            ),
            row['tag_bookmark_link'],
            row['tag_bookmark_description']
        )
        tags.append(
            Tag(
                row['tag_id'],
                bookmark,
                tag_bookmark
            )
        )
    return tags

def add_topic(name):
    db.get_db().execute(
        'INSERT INTO topics (name) VALUES'
        ' (?)',
        (name,)
    )
    db.get_db().commit()

-- Bookmark database supporting topics and tagging associations.

CREATE TABLE topics (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY,
    topic_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    link TEXT,
    description TEXT,
    UNIQUE (topic_id, name),
    FOREIGN KEY (topic_id) REFERENCES topics (id)
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    bookmark_id INTEGER NOT NULL,
    tag_bookmark_id INTEGER NOT NULL,
    UNIQUE (bookmark_id, tag_bookmark_id),
    FOREIGN KEY (bookmark_id) REFERENCES bookmarks (id),
    FOREIGN KEY (tag_bookmark_id) REFERENCES bookmarks (id),
    CHECK (bookmark_id != tag_bookmark_id)
);

--Join bookmarks x tags
--bookmark.id | bookmark.topic | bookmark.name | .. | tag.id | tag.bookmark_id | tag.tag_bookmark_id
--group by bookmark.topic
--WHERE bookmark.id == tag.bookmark.id AND tag.tag_bookmark_id == TAG_BOOKMARK_ID

-- SELECT b.name, t.tag_bookmark_id, b.topic_id FROM tags as t, bookmarks as b WHERE t.bookmark_id==b.id AND t.tag_bookmark_id==1 AND b.topic_id==2;

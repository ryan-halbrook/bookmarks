-- Bookmark database supporting types and tagging associations.

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE collections (
    id INTEGER PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE types (
    id INTEGER PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    collection_id INTEGER NOT NULL,
    FOREIGN KEY (collection_id) REFERENCES collections (id)
);

CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    type_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    link TEXT,
    description TEXT,
    UNIQUE (type_id, name),
    FOREIGN KEY (type_id) REFERENCES types (id)
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    bookmark_id INTEGER NOT NULL,
    tag_bookmark_id INTEGER NOT NULL,
    UNIQUE (bookmark_id, tag_bookmark_id),
    FOREIGN KEY (bookmark_id) REFERENCES bookmarks (id),
    FOREIGN KEY (tag_bookmark_id) REFERENCES bookmarks (id),
    CHECK (bookmark_id != tag_bookmark_id)
);

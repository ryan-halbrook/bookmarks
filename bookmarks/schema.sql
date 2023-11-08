-- Bookmark database supporting types and tagging associations.

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE collections (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
            REFERENCES users (id)
            ON DELETE CASCADE
);

CREATE TABLE types (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    collection_id INTEGER NOT NULL,
    CONSTRAINT fk_collection
        FOREIGN KEY (collection_id)
            REFERENCES collections (id)
            ON DELETE CASCADE
);

CREATE TABLE bookmarks (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    type_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    link TEXT,
    description TEXT,
    note TEXT,
    note_is_markdown BOOLEAN DEFAULT FALSE,
    UNIQUE (type_id, name),
    CONSTRAINT fk_type
        FOREIGN KEY (type_id)
            REFERENCES types (id)
            ON DELETE CASCADE
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    bookmark_id INTEGER NOT NULL,
    tag_bookmark_id INTEGER NOT NULL,
    UNIQUE (bookmark_id, tag_bookmark_id),
    CONSTRAINT fk_bookmark
        FOREIGN KEY (bookmark_id)
            REFERENCES bookmarks (id)
            ON DELETE CASCADE,
    CONSTRAINT fk_tag_bookmark
        FOREIGN KEY (tag_bookmark_id)
            REFERENCES bookmarks (id)
            ON DELETE CASCADE,
    CHECK (bookmark_id != tag_bookmark_id)
);

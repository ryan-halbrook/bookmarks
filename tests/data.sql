INSERT INTO users (id, created, username, password)
VALUES
  (1, '2023-01-01 00:00:00', 'example_user', 'password1234');

INSERT INTO collections (id, created, name, user_id)
VALUES
  (1, '2023-01-01 00:00:00', 'test collection', 1);

INSERT INTO collections (id, created, name, user_id)
VALUES
  (2, '2023-01-01 00:00:00', 'another collection', 1);

INSERT INTO types (id, created, name, collection_id)
VALUES
  (10, '2023-01-01 00:00:00', 'test type', 1);

-- bookmarks
INSERT INTO bookmarks (id, created, type_id, name, link, description)
VALUES
  (20, '2023-01-01 00:00:00', 10, 'test bookmark', 'http://example.com', 'Test Bookmark');

INSERT INTO bookmarks (id, created, type_id, name, link, description)
VALUES
  (30, '2023-01-01 00:00:00', 10, 'another test bookmark', 'http://myexample.com', 'Another test bookmark');

INSERT INTO bookmarks (id, created, type_id, name, link, description)
VALUES
  (32, '2023-01-01 00:00:00', 10, 'a third bookmark', 'http://myexample.com', 'third bookmark');

-- tags
INSERT INTO tags(id, created, bookmark_id, tag_bookmark_id)
VALUES
  (40, '2023-01-01 00:00:00', 20, 30);

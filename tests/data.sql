INSERT INTO users (created, username, password)
VALUES
  ('2023-01-01 00:00:00', 'example_user', 'password1234');

INSERT INTO collections (created, name, user_id)
VALUES
  ('2023-01-01 00:00:00', 'test collection', 1);

INSERT INTO collections (created, name, user_id)
VALUES
  ('2023-01-01 00:00:00', 'another collection', 1);

INSERT INTO types (created, name, collection_id)
VALUES
  ('2023-01-01 00:00:00', 'test type', 1);

INSERT INTO types (created, name, collection_id)
VALUES
  ('2023-01-01 00:00:00', 'another type', 1);

-- bookmarks
INSERT INTO bookmarks (created, type_id, name, link, description)
VALUES
  ('2023-01-01 00:00:00', 1, 'test bookmark', 'http://example.com', 'Test Bookmark');

INSERT INTO bookmarks (created, type_id, name, link, description)
VALUES
  ('2023-01-01 00:00:00', 1, 'another test bookmark', 'http://myexample.com', 'Another test bookmark');

INSERT INTO bookmarks (created, type_id, name, link, description)
VALUES
  ('2023-01-01 00:00:00', 1, 'a third bookmark', 'http://myexample.com', 'another bookmark');

-- tags
INSERT INTO tags(created, bookmark_id, tag_bookmark_id)
VALUES
  ('2023-01-01 00:00:00', 1, 2);

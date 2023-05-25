INSERT INTO topics (id, name)
VALUES
  (10, 'test topic');

INSERT INTO bookmarks (id, topic_id, name, link, description)
VALUES
  (20, 10, 'test bookmark', 'http://example.com', 'Test Bookmark');
INSERT INTO bookmarks (id, topic_id, name, link, description)
VALUES
  (30, 10, 'another test bookmark', 'http://myexample.com', 'Another test bookmark');
INSERT INTO bookmarks (id, topic_id, name, link, description)
VALUES
  (32, 10, 'a third bookmark', 'http://myexample.com', 'third bookmark');

INSERT INTO tags(id, bookmark_id, tag_bookmark_id)
VALUES
  (40, 20, 30);

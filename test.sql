INSERT INTO topics (id, name) VALUES (1, "languages");
INSERT INTO topics (id, name) VALUES (2, "blogs");
INSERT INTO topics (id, name) VALUES (3, "frameworks");

INSERT INTO bookmarks (id, topic_id, name, link, description) VALUES (1, 1, "Python", "python.org", "");
INSERT INTO bookmarks (id, topic_id, name, link, description) VALUES (2, 2, "Boot.dev", "blogs.boot.dev", "");
INSERT INTO bookmarks (id, topic_id, name, link, description) VALUES (3, 2, "Python blog", "blogs.python.org", "");
INSERT INTO bookmarks (id, topic_id, name, link, description) VALUES (4, 3, "Flask", "flask.example.com", "");
INSERT INTO bookmarks (id, topic_id, name, link, description) VALUES (5, 1, "C++", "cpp.org", "");
INSERT INTO bookmarks (id, topic_id, name, link, description) VALUES (6, 2, "C++ Blog", "cpp-blog.org", "");

INSERT INTO tags (id, bookmark_id, tag_bookmark_id) VALUES (1, 2, 1);
INSERT INTO tags (id, bookmark_id, tag_bookmark_id) VALUES (2, 3, 1);
INSERT INTO tags (id, bookmark_id, tag_bookmark_id) VALUES (3, 4, 1);
INSERT INTO tags (id, bookmark_id, tag_bookmark_id) VALUES (4, 6, 5);

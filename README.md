# Bookmarks Backend
[![Test](https://github.com/ryan-halbrook/bookmarks/actions/workflows/lint-test.yaml/badge.svg)](https://github.com/ryan-halbrook/bookmarks/actions/workflows/lint-test.yaml)

Bookmarks is an HTTP-based bookmarking service.

## API
http://bookmarks-api.s3-website-us-west-1.amazonaws.com

## Features

### Bookmarks
Every bookmark has a name, type, and link. Bookmarks may also have a description and note.

### Typing
Every bookmark has a 'type'. Type is a string tag, for example 'blog' or 'article'. Types can be used to find and organize related bookmarks.

### Tagging
Bookmarks can be tagged with other bookmarks. Tagging is bidirectional: tagging bookmark A with B will effectively also tag bookmark B with A.

### Collections
Types and their bookmarks belong to a collection. For example, collections can be used to create a collection for programming and another collection for fitness.

## Implementation

Bookmarks is written in Python with the Flask web framework.

Bookmarks uses PostgreSQL as its data store.

## Testing
Run the test suite from the top-level directory:
```
pytest .
```

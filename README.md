# Bookmarks
[![Test](https://github.com/ryan-halbrook/bookmarks/actions/workflows/lint-test.yaml/badge.svg)](https://github.com/ryan-halbrook/bookmarks/actions/workflows/lint-test.yaml)

Bookmarks is a bookmarking service (REST).

## Features

### Bookmarks
Every bookmark has a name, type, description, and link.

### Typing
Every bookmark has a 'type'. Type is a string tag, for example 'blog' or 'article'. It can be used to find related bookmarks by type or organize bookmarks by type.

### Tagging
Bookmarks can be tagged with other bookmarks. Tagging is bidirectional: tagging bookmark A with B will effectively also tag bookmark B with A. The tag has an ID that is the same for both directions. Deleting it will delete the tag in both directions.

### Collections
Types and their bookmarks belong to a collection. Each collection is a separate application level document. For example, collections can be used to create a collection for programming and another collection for fitness.

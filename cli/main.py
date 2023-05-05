import urllib.request as request
import json
import argparse
import sys

from prettytable import PrettyTable, SINGLE_BORDER

def table_create(field_names, collection, row_gen):
    table = PrettyTable()
    table.set_style(SINGLE_BORDER)
    table.align = 'l'
    table.field_names = field_names
    for item in collection:
        table.add_row(row_gen(item))
    return table

def bookmark_list(args):
    url = 'http://127.0.0.1:5000/bookmarks'
    if args.topic:
        url += '?topic=' + args.topic
    req = request.Request(url)
    with request.urlopen(req) as response:
        bookmarks = json.loads(response.read())
        field_names = ['ID', 'Topic', 'Name', 'Link', 'Description']
        def row_gen(b):
            return [b['id'],
                    b['topic']['name'],
                    b['name'],
                    b['link'],
                    b['description']]
        print(table_create(field_names=field_names,
                           collection=bookmarks,
                           row_gen=row_gen))

def bookmark_delete(args):
    req = request.Request('http://127.0.0.1:5000/bookmarks/' + args.id,
                          method='DELETE')
    with request.urlopen(req) as response:
        print(response.status)

def bookmark_add(args):
    name = args.name
    link = args.link
    description = args.description or ''
    topic = args.topic
    if not (name and link and topic):
        print('Specify name, link, and topic')
        return
    data = {"name": name,
            "link": link,
            "description": description,
            "topic": topic}
    req = request.Request('http://127.0.0.1:5000/bookmarks',
                          data=bytes(json.dumps(data), encoding='utf-8'),
                          headers={'Content-Type': 'application/json',
                                   'Accept': 'application/json'},
                          method='POST')
    with request.urlopen(req) as response:
        print(response.status)

def topic_list(args):
    req = request.Request('http://127.0.0.1:5000/topics')
    with request.urlopen(req) as response:
        topics = json.loads(response.read())
        def row_gen(topic):
            return [topic['id'],topic['name']]
        print(table_create(field_names=['ID', 'Name'],
                           collection=topics,
                           row_gen=row_gen))

def tag_list(args):
    req = request.Request('http://127.0.0.1:5000/tags')
    with request.urlopen(req) as response:
        tags = json.loads(response.read())
        field_names = ['Tag ID', 
                       'Bookmark Name (ID)',
                       'Bookmark Topic',
                       'Tag Bookmark Name (ID)',
                       'Tag Bookmark Topic',
                        ]
        def row_gen(tag):
            name = tag['bookmark']['name'] + ' (' + str(tag['bookmark']['id']) + ')'
            tag_name = tag['tag']['name'] + ' (' + str(tag['tag']['id']) + ')'
            return [tag['id'],
                        name,
                        tag['bookmark']['topic']['name'],
                        tag_name,
                        tag['tag']['topic']['name'],
                        ]
        print(table_create(field_names=field_names,
                           collection=tags,
                           row_gen=row_gen))

def register_bookmark_parsers(parser_parent):
    parser_bookmark = parser_parent.add_parser('bookmark')
    parser = parser_bookmark.add_subparsers(required=True)

    ls = parser.add_parser('ls')
    ls.add_argument('--topic', type=str)
    ls.set_defaults(func=bookmark_list)

    add = parser.add_parser('add')
    add.add_argument('--name', type=str)
    add.add_argument('--link', type=str)
    add.add_argument('--description', type=str)
    add.add_argument('--topic', type=str)
    add.set_defaults(func=bookmark_add)

    delete = parser.add_parser('rm')
    delete.add_argument('--id', type=str)
    delete.set_defaults(func=bookmark_delete)

def register_topic_parsers(parser_parent):
    parser_topic = parser_parent.add_parser('topic')
    parser = parser_topic.add_subparsers(required=True)

    ls = parser.add_parser('ls')
    ls.set_defaults(func=topic_list)

def register_tag_parsers(parser_parent):
    parser_tag = parser_parent.add_parser('tag')
    parser = parser_tag.add_subparsers(required=True)

    ls = parser.add_parser('ls')
    ls.set_defaults(func=tag_list)

parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description='Bookmarks Database CLI'
)
subparsers = parser.add_subparsers(required=True)
register_bookmark_parsers(subparsers)
register_topic_parsers(subparsers)
register_tag_parsers(subparsers)

args = parser.parse_args()
args.func(args)

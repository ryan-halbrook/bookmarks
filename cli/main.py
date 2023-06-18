import urllib.request as request
import json
import argparse
import sys

from prettytable import PrettyTable, SINGLE_BORDER

BASE_URL = 'http://127.0.0.1:5000'


def url_create(resource):
    return BASE_URL + resource


def table_create(field_names, collection, row_gen):
    table = PrettyTable()
    table.set_style(SINGLE_BORDER)
    table.align = 'l'
    table.field_names = field_names
    for item in collection:
        table.add_row(row_gen(item))
    return table


def table_create_bookmarks(bookmarks):
    field_names = ['ID', 'Type', 'Name', 'Link', 'Description']

    def row_gen(b):
        return [b['id'],
                b['type']['name'],
                b['name'],
                b['link'],
                b['description']]
    return table_create(field_names=field_names,
                        collection=bookmarks,
                        row_gen=row_gen)


def table_create_tags(tags):
    field_names = ['Tag ID', 'Bookmark ID', 'Type', 'Name', 'Link', 'Description']

    def row_gen(b):
        return [b['tag_id'],
                b['bookmark']['id'],
                b['bookmark']['type']['name'],
                b['bookmark']['name'],
                b['bookmark']['link'],
                b['bookmark']['description']]
    return table_create(field_names=field_names,
                        collection=tags,
                        row_gen=row_gen)


def request_create_json(url, data, method='POST'):
    return request.Request(
            url,
            data=bytes(json.dumps(data), encoding='utf-8'),
            headers={'Content-Type': 'application/json',
                     'Accept': 'application/json'},
                      method=method)


def api_call(resource, data=None, method=None):
    url = url_create(resource)
    if data:
        if not method:
            method = 'POST'
        req = request_create_json(url, data, method=method)
    else:
        if not method:
            method = 'GET'
        req = request.Request(url, method=method)
    return request.urlopen(req)


def api_get(url):
    response = api_call(url)
    return json.loads(response.read())


def api_post(url, data):
    return api_call(url, data=data).status


def api_patch(url, data):
    return api_call(url, data=data, method='PATCH').status


def api_delete(url):
    return api_call(url, data=data, method='DELETE').status


def bookmark_resources(args):
    type = args.type
    types = []
    if type:
        types = [type]
    else:
        types_json = api_get('/types')
        types = [t['name'] for t in types_json]

    for type in types:
        url = '/bookmarks/' + args.id + '/resources'
        url += '?type=' + type
        bookmarks = api_get(url)
        if bookmarks:
            print(type + ':')
            print(table_create_bookmarks(bookmarks))
            print()


def bookmark_list(args):
    url = '/bookmarks'
    if args.type:
        url += '?type=' + args.type
    bookmarks = api_get(url)
    if bookmarks:
        print(table_create_bookmarks(bookmarks))
    else:
        print('No bookmarks found')


def bookmark_show(args):
    bookmark = api_get('/bookmarks/' + str(args.id))
    if not bookmark:
        raise

    print(bookmark['name'] + ', ' + bookmark['link'])
    description = bookmark['description']
    if description and description != '':
        print(bookmark['description'])
    print('ID: ' + str(bookmark['id']))
    print('Topic: ')
    print('  ID: ' + str(bookmark['type']['id']))
    print('  Name: ' + str(bookmark['type']['name']))
    print('Tags:')

    bookmarks = api_get('/bookmarks/' + str(args.id) + '/tags')
    if bookmarks:
        print(table_create_tags(bookmarks))
    else:
        print('No tags')


def bookmark_delete(args):
    print(api_delete('/bookmarks/' + args.id))


def bookmark_add(args):
    name = args.name
    link = args.link
    description = args.description or ''
    type = args.type
    if not (name and link and type):
        print('Specify name, link, and type')
        return
    data = {"name": name,
            "link": link,
            "description": description,
            "type": type}
    print(api_post('/bookmarks', data=data))


def bookmark_update(args):
    id = args.id
    name = args.name
    link = args.link
    description = args.description or ''
    type = args.type
    if not any([name, link, type, description]):
        print('Specify at least one field to update')
        return
    data = {}
    if name:
        data['name'] = name
    if link:
        data['link'] = link
    if type:
        data['type'] = type
    if description:
        data['description'] = description

    print(api_patch('/bookmarks/' + str(id), data=data))


def bookmark_tag(args):
    id = args.id
    tag_id = args.tag
    data = {'bookmark_id': id, 'tag_bookmark_id': tag_id}
    print(api_post('/bookmarks/' + str(id) + '/tags', data=data))


def type_list(args):
    types = api_get('/types')
    def row_gen(type):
        return [type['id'],type['name']]
    print(table_create(field_names=['ID', 'Name'],
                       collection=types,
                       row_gen=row_gen))


def tag_list(args):
    tags = api_get('/tags')
    field_names = ['Tag ID',
                   'Bookmark Name (ID)',
                   'Bookmark Topic',
                   'Tag Bookmark Name (ID)',
                   'Tag Bookmark Topic',
                    ]
    def row_gen(tag):
        bookmark_name = tag['bookmark']['name']
        bookmark_id = str(tag['bookmark']['id'])
        tag_name = tag['tag']['name']
        tag_id = str(tag['tag']['id'])
        return [tag['id'],
                bookmark_name + '(' + bookmark_id + ')',
                tag['bookmark']['type']['name'],
                tag_name + '(' + tag_id + ')',
                tag['tag']['type']['name'],
                ]
    print(table_create(field_names=field_names,
                       collection=tags,
                       row_gen=row_gen))


def register_bookmark_parsers(parser_parent):
    parser_bookmark = parser_parent.add_parser('bookmark')
    parser = parser_bookmark.add_subparsers(required=True)

    ls = parser.add_parser('ls')
    ls.add_argument('--type', type=str)
    ls.set_defaults(func=bookmark_list)

    show = parser.add_parser('sh')
    show.add_argument('id', type=int)
    show.set_defaults(func=bookmark_show)

    add = parser.add_parser('add')
    add.add_argument('--name', type=str)
    add.add_argument('--link', type=str)
    add.add_argument('--description', type=str)
    add.add_argument('--type', type=str)
    add.set_defaults(func=bookmark_add)

    delete = parser.add_parser('rm')
    delete.add_argument('--id', type=str)
    delete.set_defaults(func=bookmark_delete)

    update = parser.add_parser('update')
    update.add_argument('id', type=int)
    update.add_argument('--name', type=str)
    update.add_argument('--link', type=str)
    update.add_argument('--description', type=str)
    update.add_argument('--type', type=str)
    update.set_defaults(func=bookmark_update)

    tag = parser.add_parser('tag')
    tag.add_argument('id', type=int)
    tag.add_argument('tag', type=int)
    tag.set_defaults(func=bookmark_tag)

    resources = parser.add_parser('resources')
    resources.add_argument('id', type=str)
    resources.add_argument('--type', type=str)
    resources.set_defaults(func=bookmark_resources)


def register_type_parsers(parser_parent):
    parser_type = parser_parent.add_parser('type')
    parser = parser_type.add_subparsers(required=True)

    ls = parser.add_parser('ls')
    ls.set_defaults(func=type_list)


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
register_type_parsers(subparsers)
register_tag_parsers(subparsers)

args = parser.parse_args()
args.func(args)

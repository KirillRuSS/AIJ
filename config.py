import json

__json = json.load(open('config.json', 'r'))

DIR = __json.get('dir')

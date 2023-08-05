import json
from collections import namedtuple


def parse_url(url, path):
    if path.startswith("/"):
        path = path[:1]

    if not path.endswith("/"):
        url = url + "/"

    return url + path


def from_json_to_object(data):
    return json.loads(data, object_hook=lambda target: namedtuple('X', target.keys(), rename=True)(*target.values()))

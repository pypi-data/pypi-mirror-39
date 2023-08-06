import json


def pretty_json(data: json, indent=4, sort_keys=True, separators=(",", ": ")) -> json:
    return json.dumps(json.loads(data), indent=indent, sort_keys=sort_keys, separators=separators)

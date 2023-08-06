import json


def pretty_json(json: json, indent=4, sort_keys=True, separators=(",", ": ")) -> json:
    return json.dumps(json.loads(json), indent=indent, sort_keys=sort_keys, separators=separators)

def pretty_json_decode(json: json, indent=4, sort_keys=True, separators=(",", ": ")) -> json:
    return json.dumps(json.loads(json.decode('utf8')), indent=indent, sort_keys=sort_keys, separators=separators)
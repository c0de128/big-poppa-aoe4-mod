"""Print selected keys (with paths) from Essence rgd-decode JSON files. Usage: python -I rgd_values.py <keys,comma> <file.json>..."""
import json, sys
keys = set(sys.argv[1].split(','))
def walk(node, path, out):
    if isinstance(node, dict) and 'key' in node and 'value' in node:
        p = f'{path}/{node["key"]}'
        if isinstance(node['value'], (list, dict)): walk(node['value'], p, out)
        elif node['key'] in keys: out.append((p, node['value']))
    elif isinstance(node, dict):
        for k, v in node.items(): walk(v, path if k == 'data' else f'{path}/{k}', out)
    elif isinstance(node, list):
        for i, v in enumerate(node): walk(v, path, out)
for f in sys.argv[2:]:
    out = []; walk(json.load(open(f, encoding='utf-8-sig')), '', out); print(f'== {f}')
    for p, v in out: print(f'   {p} = {v}')

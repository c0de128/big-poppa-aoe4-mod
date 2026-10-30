"""List spawn_item (squad, number_to_spawn) pairs from Essence rgd-decode JSON. Usage: python -I rgd_spawns.py <file.json>..."""
import json, sys
def items(node, variant, out):
    if isinstance(node, dict) and node.get('key') == 'spawn_item' and isinstance(node.get('value'), list):
        kv = {c.get('key'): c.get('value') for c in node['value'] if isinstance(c, dict)}
        sq = kv.get('squad'); sq = sq.get('value', sq) if isinstance(sq, dict) else sq
        out.append((variant, str(sq).split(chr(92))[-1], kv.get('number_to_spawn')))
        return
    if isinstance(node, dict):
        for k, v in node.items(): items(v, node['key'] if node.get('key') in ('default','xp3','campaign','cordoba','hre_brawl') else variant, out)
    elif isinstance(node, list):
        for v in node: items(v, variant, out)
for f in sys.argv[1:]:
    out = []; items(json.load(open(f, encoding='utf-8-sig')), '?', out)
    print('==', f.split('/')[-1]); [print(f'   {v:8} {s:45} {n}') for v, s, n in out]

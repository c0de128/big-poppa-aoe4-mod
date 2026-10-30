"""Report where Big Poppa's edits sit (variant + enclosing group path) vs May base. Read-only."""
import re, sys, pathlib, collections
OPEN = re.compile(r'^\s*<(\w+)\b([^>]*?)(?<!/)>\s*$')
CLOSE = re.compile(r'^\s*</(\w+)>\s*$')
NAME = re.compile(r'\bname="([^"]*)"')
VAL = re.compile(r'<(\w+) name="([^"]*)" value="([^"]*)"')
def walk(lines):
    stack = []; out = []
    for ln in lines:
        m = OPEN.match(ln)
        if m and not ln.strip().startswith('<?'):
            n = NAME.search(m.group(2)); stack.append((m.group(1), n.group(1) if n else '')); out.append(None); continue
        if CLOSE.match(ln):
            if stack: stack.pop()
            out.append(None); continue
        v = VAL.search(ln)
        if v:
            var = next((nm for t, nm in stack if t == 'variant'), 'default')
            out.append((var, '/'.join(nm for t, nm in stack if t not in ('instance','variant') and nm), v.group(2), v.group(3), ln.strip()))
        else: out.append(None)
    return out
base_root, mod_root = map(pathlib.Path, sys.argv[1:3])
KEYS = {'max_personnel_cap','popcap','food','wood','stone','gold','militia_hre','initial_amount','number_to_spawn','max_vehicle_cap'}
stats = collections.Counter()
for mf in sorted(mod_root.rglob('*.xml')):
    rel = mf.relative_to(mod_root); bf = base_root / rel
    b = [x for x in walk(bf.read_text(encoding='utf-8-sig').splitlines()) if x and x[2] in KEYS]
    m = [x for x in walk(mf.read_text(encoding='utf-8-sig').splitlines()) if x and x[2] in KEYS]
    top = rel.parts[0] + ('/'+rel.parts[1] if rel.parts[0]=='ebps' else '')
    bc = collections.Counter((v,p,k,val) for v,p,k,val,_ in b); mc = collections.Counter((v,p,k,val) for v,p,k,val,_ in m)
    for key in set(bc)|set(mc):
        d = mc[key]-bc[key]
        if d: stats[(top, key[0], re.sub(r'/spawn_item$','/spawn_item',key[1])[-70:], key[2], key[3], 'ADD' if d>0 else 'DEL')] += abs(d)
    # unchanged-but-relevant (to learn exclusions)
    for key in set(bc)&set(mc):
        if key[2] in ('max_personnel_cap','initial_amount') : stats[(top,key[0],key[1][-70:],key[2],key[3],'kept')] += min(bc[key],mc[key])
for k, c in sorted(stats.items()): print(c, *k, sep=' | ')

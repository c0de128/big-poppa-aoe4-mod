"""Apply Big Poppa's edits to a vanilla AoE4 source-XML instance file.

Rules were derived from the May 2026 Big Poppa build vs its May base (tools/bp_analyze.py):
  army   : default variant  race_population_cap_table/max_personnel_cap -> 1000
           any variant      resource_max_cap/{food,wood,stone,gold,militia_hre} 100000 -> 200000
  nodes  : default variant  initial_amount -> 50000
  TCs    : default + xp3    villager spawn_item number_to_spawn -> 2 (patched, or injected after the squad line)
Extra rules (Kev, 2026-10-30) are passed in per file: see EXTRA below.

Usage:
  python -I bp_transform.py <base_instances_dir> <out_dir> <rel_path> [<rel_path> ...]
Line endings and BOM of the base file are preserved; only target lines change.
"""
import re
import sys
import pathlib

OPEN = re.compile(r'^\s*<(\w+)\b([^>]*?)(?<!/)>\s*$')
CLOSE = re.compile(r'^\s*</(\w+)>\s*$')
NAME = re.compile(r'\bname="([^"]*)"')
VALUE = re.compile(r'(\bvalue=")([^"]*)(")')

STORAGE = {'food', 'wood', 'stone', 'gold', 'militia_hre'}

# Kev's decisions for the new civs (army default variant only).
EXTRA = {
    'army/standard_mode/normal_vikings.xml': {
        'army_bag/resource_max_cap/popcap': '1000',
        'army_bag/race_population_cap_table/max_vehicle_cap': '1000',
    },
    'army/standard_mode/normal_scots.xml': {
        'army_bag/resource_max_cap/popcap': '1000',
    },
}


# Quirks in the May build, reproduced as-is (Kev: "re-apply ONLY Big Poppa's existing edits").
#   villager_free_* (Zhu Xi, Japanese free-villager spawns) were left at 1.
#   Golden Horde: villagers already 2 in vanilla; Big Poppa set the SCOUT to 2 (Kev 2026-10-30: keep).
# The May build doubled Tughlaq worker elephants instead of villagers; Kev 2026-10-30 fixed that:
# Tughlaq now follows the normal villager rule and elephants stay at the 17.0 default.
SKIP_SQUADS = ('villager_free',)
QUIRKS = {
    'ebps/races/mongol_ha_gol/buildings/building_town_center_mon_ha_gol.xml': {'double': ('unit_scout_1_mon_ha_gol',)},
    'ebps/races/mongol_ha_gol/buildings/building_town_center_capital_mon_ha_gol.xml': {'double': ('unit_scout_1_mon_ha_gol',)},
}


def wants_double(rel, squad):
    quirk = QUIRKS.get(rel, {})
    if any(s in squad for s in quirk.get('double', ())):
        return True
    if quirk.get('no_villager') or any(s in squad for s in SKIP_SQUADS):
        return False
    return 'villager' in squad


def kind_of(rel):
    if rel.startswith('army/standard_mode/normal_'):
        return 'army'
    if rel.startswith('ebps/races/') and '/buildings/' in rel and 'building_town_center' in rel:
        return 'tc'
    if rel.startswith(('ebps/gameplay/resources/', 'ebps/gaia/animals/', 'ebps/environment/non_tree_resources/')):
        return 'node'
    raise ValueError(f'no Big Poppa rule for {rel}')


def set_value(line, new):
    return VALUE.sub(lambda m: m.group(1) + new + m.group(3), line, count=1)


def transform(rel, text):
    kind = kind_of(rel)
    extra = EXTRA.get(rel, {})
    lines = text.splitlines(keepends=True)
    out = []
    stack = []          # (tag, name)
    spawn = None        # open spawn_item: {'squad': idx in out, 'nts': idx in out, 'variant': str}
    changes = []

    def variant():
        return next((n for t, n in stack if t == 'variant'), 'default')

    def path():
        return '/'.join(n for t, n in stack if t not in ('instance', 'variant') and n)

    for ln in lines:
        body = ln.rstrip('\r\n')
        m_open = OPEN.match(body)
        if m_open and not body.lstrip().startswith('<?'):
            n = NAME.search(m_open.group(2))
            stack.append((m_open.group(1), n.group(1) if n else ''))
            if kind == 'tc' and stack[-1] == ('group', 'spawn_item'):
                spawn = {'squad': None, 'nts': None, 'variant': variant(), 'villager': False}
            out.append(ln)
            continue
        if CLOSE.match(body):
            closing = stack.pop() if stack else None
            if kind == 'tc' and closing == ('group', 'spawn_item') and spawn is not None:
                if spawn['villager'] and spawn['variant'] in ('default', 'xp3'):
                    if spawn['nts'] is not None:
                        old = out[spawn['nts']]
                        if VALUE.search(old).group(2) != '2':
                            out[spawn['nts']] = set_value(old, '2')
                            changes.append(f'{spawn["variant"]}: number_to_spawn -> 2')
                    else:
                        sq = out[spawn['squad']]
                        indent = re.match(r'^\s*', sq).group(0)
                        eol = sq[len(sq.rstrip('\r\n')):] or '\n'
                        out.insert(spawn['squad'] + 1,
                                   f'{indent}<int name="number_to_spawn" value="2" overrideParent="True" />{eol}')
                        changes.append(f'{spawn["variant"]}: number_to_spawn injected = 2')
                spawn = None
            out.append(ln)
            continue

        n = NAME.search(body)
        v = VALUE.search(body)
        if n and v:
            key, val, var, p = n.group(1), v.group(2), variant(), path()
            full = f'{p}/{key}'
            new = None
            if kind == 'army':
                if var == 'default' and full == 'army_bag/race_population_cap_table/max_personnel_cap':
                    new = '1000'
                elif p == 'army_bag/resource_max_cap' and key in STORAGE and val == '100000':
                    new = '200000'
                elif var == 'default' and full in extra:
                    new = extra[full]
            elif kind == 'node':
                if var == 'default' and key == 'initial_amount':
                    new = '50000'
            elif kind == 'tc' and spawn is not None and stack and stack[-1] == ('group', 'spawn_item'):
                if key == 'squad':
                    spawn['squad'] = len(out)
                    spawn['villager'] = wants_double(rel, val)
                elif key == 'number_to_spawn':
                    spawn['nts'] = len(out)
            if new is not None and new != val:
                ln = set_value(ln, new)
                changes.append(f'{var}: {full} {val} -> {new}')
        out.append(ln)

    if stack:
        raise ValueError(f'{rel}: unbalanced tags, left open: {stack}')
    return ''.join(out), changes


def main():
    base, dest = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    for rel in sys.argv[3:]:
        raw = (base / rel).read_bytes()
        bom = raw.startswith(b'\xef\xbb\xbf')
        text = raw.decode('utf-8-sig')
        new, changes = transform(rel, text)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((b'\xef\xbb\xbf' if bom else b'') + new.encode('utf-8'))
        print(f'{rel}\t{len(changes)}\t' + '; '.join(changes))


if __name__ == '__main__':
    main()

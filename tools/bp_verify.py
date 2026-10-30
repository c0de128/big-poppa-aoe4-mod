"""Independent check: every Big Poppa override file vs its vanilla base. Writes a markdown report.

Allowed differences (anything else is flagged UNEXPECTED):
  max_personnel_cap -> 1000
  resource storage (food/wood/stone/gold/militia_hre) 100000 -> 200000
  popcap -> 1000 (normal_vikings / normal_scots only)
  max_vehicle_cap -> 1000 (normal_vikings only)
  initial_amount -> 50000
  number_to_spawn 1 -> 2, or an injected number_to_spawn=2 line (squad shown in the report)
Line endings, BOM and the trailing newline are ignored (reported as formatting only).

Usage: python -I bp_verify.py <mod_instances_dir> <base_instances_dir> <report.md>
"""
import difflib
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

NAME_VAL = re.compile(r'<(\w+) name="([^"]*)" value="([^"]*)"')
SQUAD = re.compile(r'name="squad" value="([^"]*)"')
STORAGE = {'food', 'wood', 'stone', 'gold', 'militia_hre'}


def lines_of(path):
    text = path.read_bytes().decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    return text.rstrip('\n').split('\n')


def squad_near(lines, idx):
    for j in range(idx, max(idx - 15, -1), -1):
        m = SQUAD.search(lines[j])
        if m:
            return m.group(1).split('\\')[-1]
    return '?'


def allowed(rel, old, new):
    """Return a label if the old->new line change is an intended edit, else None."""
    mn = NAME_VAL.search(new)
    if not mn:
        return None
    _, key, nv = mn.groups()
    ov = None
    if old is not None:
        mo = NAME_VAL.search(old)
        if not mo or mo.group(2) != key:
            return None
        ov = mo.group(3)
        # nothing but the value may change
        if old.replace(f'value="{ov}"', '') != new.replace(f'value="{nv}"', ''):
            return None
    if key == 'max_personnel_cap' and nv == '1000':
        return 'pop cap'
    if key in STORAGE and ov == '100000' and nv == '200000':
        return 'stockpile limit'
    if key == 'popcap' and nv == '1000' and rel.endswith(('normal_vikings.xml', 'normal_scots.xml')):
        return 'pop cap (2nd value, new civs)'
    if key == 'max_vehicle_cap' and nv == '1000' and rel.endswith('normal_vikings.xml'):
        return 'Viking villager limit'
    if key == 'initial_amount' and nv == '50000':
        return 'pile 50,000'
    if key == 'number_to_spawn' and nv == '2' and (ov in ('1', None)):
        return 'injected 2 per train' if old is None else '2 per train'
    return None


def main():
    mod, base, report = map(pathlib.Path, sys.argv[1:4])
    files = sorted(p.relative_to(mod).as_posix() for p in mod.rglob('*.xml'))
    rows, unexpected, spawn_rows, fmt_only, bad_xml = [], [], [], 0, []
    for rel in files:
        try:
            ET.parse(mod / rel)
        except ET.ParseError as e:
            bad_xml.append(f'{rel}: {e}')
        a, b = lines_of(base / rel), lines_of(mod / rel)
        counts = {}
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                continue
            olds, news = a[i1:i2], b[j1:j2]
            pairs = list(zip(olds, news)) if tag == 'replace' and len(olds) == len(news) else None
            if pairs is None and tag == 'insert':
                pairs = [(None, n) for n in news]
            if pairs is None:
                unexpected.append(f'{rel}: {tag} base[{i1}:{i2}] mod[{j1}:{j2}]')
                continue
            for k, (o, n) in enumerate(pairs):
                label = allowed(rel, o, n)
                if label is None:
                    unexpected.append(f'{rel}: `{(o or "").strip()}` -> `{n.strip()}`')
                    continue
                counts[label] = counts.get(label, 0) + 1
                if 'per train' in label:
                    spawn_rows.append((rel, squad_near(b, j1 + k), label))
        if not counts:
            fmt_only += 1
        rows.append((rel, counts))

    out = ['# Final check: Big Poppa overrides vs 17.0 vanilla', '',
           f'- Files checked: **{len(files)}**',
           f'- Files identical to 17.0 apart from line endings: {fmt_only}',
           f'- Well-formed XML: {len(files) - len(bad_xml)} / {len(files)}',
           f'- **Unexpected differences: {len(unexpected)}**', '']
    if bad_xml:
        out += ['## ❌ XML parse errors', ''] + [f'- {x}' for x in bad_xml] + ['']
    out += ['## Unexpected differences', '']
    out += [f'- ❌ {u}' for u in unexpected] if unexpected else ['None.']
    out += ['', '## Spawn changes (which squad each "2 per train" applies to)', '',
            '| File | Squad | Change |', '|---|---|---|']
    out += [f'| `{r}` | `{s}` | {l} |' for r, s, l in spawn_rows]
    out += ['', '## Per-file summary', '', '| File | Intended edits |', '|---|---|']
    for rel, counts in rows:
        out.append(f'| `{rel}` | ' + (', '.join(f'{k} ×{v}' for k, v in sorted(counts.items())) or '— (no value changes)') + ' |')
    report.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'files={len(files)} unexpected={len(unexpected)} bad_xml={len(bad_xml)} no_value_changes={fmt_only}')


if __name__ == '__main__':
    main()

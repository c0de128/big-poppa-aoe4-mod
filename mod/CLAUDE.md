# CLAUDE.md — BigPoppa AoE4 mod

Operational notes for Claude. Read before touching this mod.

## What this is

Age of Empires IV "Tuning Pack" mod. Buffs economy and pop cap across all 25 skirmish/MP civilizations (Vikings and Scots added for update 17.0, 2026-10-30). Tested with the AoE4 Content Editor (`EssenceEditor.exe`) on Windows.

Mod ID: `1bfbb3a8-719b-448e-8469-f58c7363bc36`. Type: Extension.

## Build pipeline — DO NOT try to build from CLI

The AoE4 **Content Editor** is what registers local mods with the game. Workflow:

1. User closes the AoE4 game AND the editor.
2. User opens `BigPoppa.aoe4mod` in the editor (`EssenceEditor.exe`).
3. User clicks **Build** in the editor UI. This:
   - Reads `assets/attrib/BigPoppa.xml` (manifest, single `<mod>` tag, no children).
   - Recursively scans `assets/attrib/instances/**/*.xml` for instance overrides.
   - Burns each instance source XML to RGD using the parent-template merge.
   - Packs into `archives/BigPoppa.sga`.
   - Copies the SGA to `%USERPROFILE%\Documents\My Games\Age of Empires IV\mods\extension\local\BigPoppa\BigPoppa.sga`.
   - Registers the mod so it appears in-game as "Local" (orange wrench).
4. User launches AoE4, picks the mod under Tuning Pack, tests.

**Do not attempt to invoke the build via CLI.** There is no headless build path. Edit source XML, then ask the user to rebuild.

## Source XML format (hard-won knowledge)

Format is the **AoE4 editor's source XML**, NOT the RGD-decoded `<Root><RGDNode>` format. Confirmed by decompiling `Essence.Editor.Attributes.dll` (`AttributeReader.LoadInstance`).

### Manifest (`assets/attrib/BigPoppa.xml`)
```xml
<mod guid="1bfbb3a8719b448e8469f58c7363bc36" locdb_path="..\locdb\BigPoppa.locdb" override_instances="True">
</mod>
```
- `override_instances="True"` means compiled RGDs replace base game files at matching paths.
- The mod tag has NO children. All overrides live in `instances/`.

### Instance override (`assets/attrib/instances/<template>/<rel_path>.xml`)
```xml
<instance version="6" description="" template="army">
  <group name="army_bag">
    <float name="max_personnel_cap" value="1000" />
  </group>
</instance>
```
- `template="..."` MUST match the first path segment under `instances/`. E.g. file at `instances/army/standard_mode/normal_english.xml` → `template="army"`.
- `version` is `6` if the file has multiple variants, `4` if only default. Editor enforces this on save; we set it correctly on hand-written files by copying from base reference.
- **Do NOT add `override_type` attribute.** Default is `Override` semantics (full replacement). `override_type="merge"` produces sparse RGDs the game engine ignores — proven to fail in early testing.
- Variant blocks: `<variant name="campaign">...</variant>`, `<variant name="xp3">...</variant>`, etc. Default variant is inlined (no wrapper) because `attributes.xml` has `inline_default_variant="True"`.

### Element types
`<int>`, `<float>`, `<bool>`, `<string>`, `<enum>`, `<group>`, `<list>`, `<enum_table>`, `<colour>`, `<file>`, `<locstring>`, `<state_tree_node>`, `<uniqueid>`, `<template_reference>`, `<instance_reference>`. All take `name="..."` attribute. Value types also take `value="..."`. `overrideParent="True"` forces a value to override the parent's; otherwise the editor's merge inherits.

## "Merging" vs "replacing" civs — THE PHASE 4 TRAP

Civ TC source XMLs come in two flavors:

- **Replacing civs** — `<list name="spawn_items" overrideParent="True">` with FULL content including explicit `<int name="number_to_spawn" value="N" />`. To change behavior: patch the value in source. Examples: HRE, Jin Dynasty, Chinese, Malian, Japanese, Mongol regular+capital, Mongol HA, Sultanate Tughlaq.
- **Merging civs** — `<list name="spawn_items">` (no `overrideParent`) with sparse content (just squad refs). They **inherit** `number_to_spawn` from `core/building_town_center` at burn time. To change behavior: **INJECT** an explicit `<int name="number_to_spawn" value="2" overrideParent="True" />` line right after the villager squad ref. Examples: English, Abbasid, Byzantine, French, Lancaster, Ottoman, Rus, Sultanate, Templar.

**Critical**: Overriding only `core/building_town_center` does NOT propagate to merging civs at burn time. Tested and failed in-game. Per-civ explicit injection is required. The base game's working "1000pop,MoreResources,FasterVillages" mod uses this same approach.

## File inventory (115 instance files)

| Phase | Path | Count | What |
|---|---|---|---|
| 2a/2b | `instances/army/standard_mode/normal_<civ>.xml` | 25 | Pop cap (`max_personnel_cap=1000` and `resource_max_cap/popcap=1000`, both on every civ) + storage caps (`food/wood/stone/gold/militia_hre=200000`) in `army_bag`. Vikings also `max_vehicle_cap=1000` |
| 3 | `instances/ebps/gameplay/resources/gold/` | 3 | Gold piles → `initial_amount=50000` |
| 3 | `instances/ebps/gameplay/resources/stone/` | 3 | Stone piles → 50000 |
| 3 | `instances/ebps/gameplay/resources/food/` | 14 | Berries (8) + fish (6) → 50000. The 3 `_emi` fish have no own `initial_amount` and stay at base (1000 / 600 / 600 in the compiled mod) |
| 3 | `instances/ebps/gaia/animals/` | 8 | Live boar/deer/reindeer + 4 sheep colors → 50000. Live enchanted_stag has no own `initial_amount` and stays at 350 (its corpse is 50000) |
| 3 | `instances/ebps/environment/non_tree_resources/` | 8 | Animal corpses → 50000 |
| 4 | `instances/ebps/races/core/buildings/` | 1 | Core TC override (defensive, not load-bearing) |
| 4 | `instances/ebps/races/<civ>/buildings/building_town_center*.xml` | 53 | Per-civ TC overrides — villager `number_to_spawn=2` in default+xp3 variants |

### 17.0 update (2026-10-30)
- Added Vikings (`_vik`, replacing-style TCs) and Scots (`_sco`, merging-style TCs): 2 army files + 4 TC files.
- 36 override files that had gone stale were refreshed from 17.0 reference data, re-applying only Big Poppa's edits.
- Full record: `docs/FINDINGS.md` at the repo root.

### Phase 4 special cases
- **Jin Dynasty** has a 4th spawn_item: `unit_mounted_villager_1_jin`. Also patched to 2.
- **Golden Horde** villagers are already 2 in the base game; Big Poppa also sets the scout (`unit_scout_1_mon_ha_gol`) to 2. Kept on purpose.
- **Tughlaq** TCs train 2 villagers; worker elephants stay at the base game value (1).
- **`villager_free_*`** spawns (free-villager events) stay at 1.
- **Mongol** has 5 TC files: `mon`, `capital_mon`, `moving_mon`, `capital_moving_mon`, `dummy_start`. Only `mon` and `capital_mon` train villagers; the moving/dummy files have no villager spawn_items and are verbatim copies (kept for defensive parity with the working reference mod).
- **xp3 variant villager** is patched on every TC where the variant exists explicitly in source; elsewhere the xp3 villager count comes from inheritance. Army files have no xp3 block, so the default pop cap edit is expected to cover Empire Wars. Neither is tested in game.
- **Campaign variant** intentionally NOT patched in any phase — campaign games stay at base game values.
- **Cordoba variant** (event mode) NOT patched.

## What we deliberately did NOT do
- No villager unit file changes. Working reference mod also doubles `gather_rate` (0.75→1.5) and `resource_carry_capacity` (10→20) on every villager — we did not include this. If user asks for "faster villagers" later, this is the path.
- No tree/wood overrides. User explicitly scoped this out of Phase 3.
- No farm overrides.
- No civ-specific Byzantine `merc_byz` storage cap raise (it stayed at 100000).
- No Japanese `action`/`command` storage cap changes (those use 100000 as a marker for Japanese-specific mechanics, not as a literal resource cap).

## Tooling

### AOEMods.Essence (essential for investigation)
Pre-built CLI at `%USERPROFILE%/aoe4work/Essence/AOEMods.Essence.CLI.exe`. Source repo cloned at `%USERPROFILE%/aoe4work/AOEMods.Essence/`.

Useful commands:
```
.../AOEMods.Essence.CLI.exe sga-unpack <input.sga> <output_dir>
.../AOEMods.Essence.CLI.exe rgd-decode <input.rgd> <output.xml>
.../AOEMods.Essence.CLI.exe rgd-encode <input.xml> <output.rgd>
```
The decompiled editor DLLs live at `%USERPROFILE%/aoe4work/decomp_attribs/` (via `ilspycmd`). Useful when you need to know what the editor actually does.

### Reference data (already extracted)
- `%USERPROFILE%/aoe4work/cardinal_refattribs/` — base game SOURCE XML (from `cardinal/archives/ReferenceAttributes.sga`). The canonical reference for any instance file's structure.
- `%USERPROFILE%/aoe4work/base_attrib/` — base game COMPILED RGDs (from `cardinal/archives/Attrib.sga`). Use for diff against working mods to identify what changed.
- `%USERPROFILE%/aoe4work/ref_unpacked/` — the working "1000pop,MoreResources,FasterVillages" reference mod's compiled RGDs. Empirical ground truth for what works.

### Editor DLLs
`C:/Program Files (x86)/Steam/steamapps/common/Age of Empires IV/Essence.Editor.*.dll`. Decompile with `ilspycmd` when uncertain about editor behavior.

## Workflow for adding overrides

1. **Find the base reference file** in `cardinal_refattribs/instances/...`. If absent, the field is inherited — find it in the parent template (often `core/...`).
2. **Identify the attribute name precisely.** Don't guess. Decode the working mod's RGD and diff against base RGD to verify the EXACT attribute being changed.
3. **Decide merging vs replacing.** If the civ source XML lacks the field, you either need to (a) inject the explicit line with `overrideParent="True"`, or (b) override the parent template. Per-civ explicit is more reliable.
4. **Copy full base source XML for the file** (matches the working reference mod's pattern of providing full content; sparse-delta files compile to sparse RGDs that the engine doesn't merge correctly).
5. **Change only the target value(s).** Default variant only unless explicitly scoping to other variants. Leave campaign/cordoba alone unless requested.
6. **Verify after edit**: `grep -n "<attr>" <file>` to confirm value AND check no other occurrences accidentally changed.
7. **Ask user to rebuild and test in-game.** Don't claim success until they confirm.

## Common pitfalls
- Bash loops over paths-with-spaces silently fail. Use `find ... -print0 | while IFS= read -r -d '' f`, or use PowerShell.
- `sed` `0,/addr/{}` syntax needs `/` as the address separator. Custom separators inside don't always work. PowerShell + .NET regex is more reliable for multi-file XML edits.
- Awk regex doesn't support `\` literal backslash sanely on Windows paths inside square brackets. Use PowerShell for path-content matching.
- The editor's burn is **per-instance** — it does NOT propagate parent template changes to instances that don't have a source override in the mod. Putting a single core override isn't enough; you need source files for every civ TC.
- Don't put overrides inside `<mod>` in `BigPoppa.xml`. They go in separate files under `instances/`.

## Files to never touch
- `BigPoppa.aoe4mod` — editor project file
- `assets/_default.burnproj` — burn pipeline config
- `assets/mod.rdo` — mod display metadata
- `assets/mod.png` — mod icon
- `cache/`, `archives/` — editor output, regenerated on Build
- `.aoe4/` — editor session/state

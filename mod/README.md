# BIG POPPA

Age of Empires IV Tuning Pack mod. Skirmish/MP buffs across all 25 civilizations, including Vikings and Scots (update 17.0, Raiders of the North).

## What it changes

| Change | Value | Scope |
|---|---|---|
| Population cap (`max_personnel_cap`) | 200 → **1000** | All 25 civs, standard skirmish/MP |
| Population cap (`resource_max_cap/popcap`) | 200 → **1000** | All 25 civs (both pop values match on every civ since 2026-10-30) |
| Viking villager limit (`max_vehicle_cap`) | 200 → **1000** | Vikings only (Viking villagers use their own pop pool) |
| Food/wood/stone/gold storage cap | 100,000 → **200,000** | All 25 civs |
| HRE militia (`militia_hre`) storage cap | 100,000 → **200,000** | All 25 civs |
| Gold piles (deposit + small + tiny) | varies → **50,000** | All 3 sizes |
| Stone piles (deposit + small + ruins) | varies → **50,000** | All 3 sizes |
| Berry bushes + prickly pear (all variants) | varies → **50,000 food** | 8 variants |
| Fish (deep water, river, shore) | varies → **50,000 food** | 3 standard variants (see exceptions) |
| Live huntable/herdable animals | varies → **50,000 food** | Boar, deer, reindeer, sheep (4 colors) (see exceptions) |
| Animal corpses (post-kill harvest) | varies → **50,000 food** | Boar, deer, enchanted stag, reindeer, sheep (4 colors) |
| Villagers per TC train cycle | 1 → **2** | All 25 civs, default variant (plus xp3/Empire Wars where the TC file declares it) |
| Jin Dynasty mounted villager per train | 1 → **2** | Jin TCs, default variant |
| Golden Horde scout per train | 1 → **2** | Golden Horde TCs, default variant (kept from the May build on purpose) |

### Known exceptions (not 50,000)

These four files have no pile size of their own, so they keep the base game amount. Checked in the compiled mod:

| File | Pile size in the built mod |
|---|---|
| `resource_food_deep_water_fish_emi` | 1,000 |
| `resource_food_river_fish_emi` | 600 (Empire Wars: 500) |
| `resource_food_shore_fish_emi` | 600 (Empire Wars: 500) |
| `gaia_huntable_enchanted_stag` (live) | 350 (its corpse is 50,000) |

## What it does NOT change

- Trees / wood gathering (intentional — keeps wood scarcity)
- Farms (intentional)
- Villager gather speed and carry capacity (left at base values)
- House population (+10) and starting resources
- Campaign variant data (campaign games behave normally)
- Cordoba event mode variant
- Scout `number_to_spawn` (still 1 per train, except Golden Horde)
- HRE prelate `number_to_spawn` (still 1 per train)
- Tughlaq worker elephants (still 1 per train)
- Civ-specific resources: Byzantine `merc_byz` mercenary cap, Japanese `action`/`command` markers, Mongol Ovoo, Rus Hunting Cabin, Aachen Chapel relic income, Sultanate free-villager-from-tech, Malian cattle, Scots Highland Cattle cap (21), Scots fish ponds, Viking Longhouse farmsteads, Japanese shrines, Mongol moving TC behavior

## Civilizations covered (25)

abbasid, abbasid_ha_01 (House of Saladin), byzantine, byzantine_ha_mac (Macedonian Dynasty), chinese, chinese_ha_01 (Zhu Xi's Legacy), english, french, french_ha_01 (Jeanne d'Arc), hre, hre_ha_01 (Order of the Dragon), japanese, japanese_ha_sen (Sengoku Daimyo), jin_dynasty, lancaster, malian, mongol, mongol_ha_gol (Golden Horde), ottoman, rus, scots, sultanate (Delhi), sultanate_ha_tug (Tughlaq Dynasty), templar, vikings

## Game modes covered

- **Standard skirmish/MP**: full coverage. Tested in game on 2026-10-30.
- **Empire Wars (xp3 variant)**: the army files have no separate xp3 block, so the pop cap edit is expected to apply. Villager 2-per-train is patched in TCs that declare an xp3 block. Not tested in game.
- **Nomad**: covered via standard TC overrides. Players build a regular TC, so our overrides apply. Not tested in game.
- **Campaign**: NOT covered — campaign games run with base values intact
- **Cordoba event mode**: NOT covered

## Repository layout

```
BigPoppa/
├── BigPoppa.aoe4mod              # Editor project file
├── README.md                     # This file
├── CLAUDE.md                     # Operational notes for AI collaboration
├── assets/                       # Source files (edit these)
│   ├── _default.burnproj         # Build pipeline config (do not edit)
│   ├── mod.png                   # Mod icon
│   ├── mod.rdo                   # Mod display metadata
│   ├── attrib/
│   │   ├── BigPoppa.xml          # Mod manifest (override_instances=True)
│   │   └── instances/            # All override source XML (115 files)
│   │       ├── army/standard_mode/      # 25 army files (pop cap, storage caps)
│   │       └── ebps/
│   │           ├── gameplay/resources/  # gold (3), stone (3), food (14)
│   │           ├── gaia/animals/        # 8 live animals
│   │           ├── environment/non_tree_resources/  # 8 corpses
│   │           └── races/
│   │               ├── core/buildings/  # 1 core TC defensive override
│   │               └── <civ>/buildings/ # 53 per-civ TC overrides
│   └── locdb/                    # Localization strings
├── archives/                     # Build output: BigPoppa.sga (regenerated, not in git)
├── cache/                        # Build intermediate cache (regenerated, not in git)
└── .aoe4/                        # Editor session state (not in git)
```

## How to build

1. Close AoE4 and the AoE4 Content Editor if either is running.
2. Open `BigPoppa.aoe4mod` in the AoE4 Content Editor (`EssenceEditor.exe` from the editor install).
3. Click **Build** in the editor.
4. Editor produces `archives/BigPoppa.sga` and copies it to the local mods directory at `mods/extension/local/BigPoppa/BigPoppa.sga`.
5. Launch AoE4. The mod appears as "Local — BIG POPPA" with an orange wrench icon.
6. Activate it as a Tuning Pack in the lobby.

## How the override mechanism works (high level)

The mod declares `override_instances="True"` in `BigPoppa.xml`. At build time, the editor:

1. Reads `BigPoppa.xml` (manifest).
2. Recursively scans `assets/attrib/instances/**/*.xml`.
3. For each source XML, merges with its parent template (looked up via `parent_pbg` instance reference) and produces a compiled RGD.
4. Packs all RGDs into `BigPoppa.sga` at paths matching the base game's instance paths (e.g. `attrib/army/standard_mode/normal_english.rgd`).

At runtime, AoE4 with `override_instances=True` uses our RGDs as full replacements for the corresponding base game files. Since our compiled RGDs are full instance trees (not deltas), every field is authoritative.

For deeper notes on the format, "merging" vs "replacing" civ TC patterns, and tooling, see `CLAUDE.md`.

## Reference

- AoE4 Content Editor: bundled with Age of Empires IV (free download from Steam: "Age of Empires IV Content Editor")
- AOEMods.Essence (community tool for SGA/RGD inspection): https://github.com/aoemods/AOEMods.Essence
- Reference working mod for empirical patterns: "1000pop,MoreResources,FasterVillages" (Steam Workshop)

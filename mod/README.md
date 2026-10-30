# BIG POPPA

Age of Empires IV Tuning Pack mod. Skirmish/MP buffs across all 23 civilizations.

## What it changes

| Change | Value | Scope |
|---|---|---|
| Population cap | 200 → **1000** | All 23 civs, standard skirmish/MP |
| Food/wood/stone/gold storage cap | 100,000 → **200,000** | All 23 civs |
| HRE militia (`militia_hre`) storage cap | 100,000 → **200,000** | All 23 civs |
| Gold piles (deposit + small + tiny) | varies → **50,000** | All 3 sizes |
| Stone piles (deposit + small + ruins) | varies → **50,000** | All 3 sizes |
| Berry bushes + prickly pear (all variants) | varies → **50,000 food** | 8 variants |
| Fish (deep water, river, shore + _emi variants) | varies → **50,000 food** | 6 variants |
| Live huntable/herdable animals | varies → **50,000 food** | Boar, deer, reindeer, enchanted stag, sheep (4 colors) |
| Animal corpses (post-kill harvest) | varies → **50,000 food** | Matches the animal types above |
| Villagers per TC train cycle | 1 → **2** | All 23 civs, default + Empire Wars (xp3) modes |
| Jin Dynasty mounted villager per train | 1 → **2** | Both Jin TCs, default variant |

## What it does NOT change

- Trees / wood gathering (intentional — keeps wood scarcity)
- Farms (intentional)
- Villager gather speed and carry capacity (left at base values)
- Campaign variant data (campaign games behave normally)
- Cordoba event mode variant
- Scout `number_to_spawn` (still 1 per train)
- HRE prelate `number_to_spawn` (still 1 per train)
- Civ-specific resources you'd expect to be untouched: Byzantine `merc_byz` mercenary cap, Japanese `action`/`command` markers, Mongol Ovoo, Rus Hunting Cabin, Aachen Chapel relic income, Sultanate free-villager-from-tech, Malian cattle, Japanese shrines, Mongol moving TC behavior

## Civilizations covered (23)

abbasid, abbasid_ha_01 (House of Saladin), byzantine, byzantine_ha_mac (Macedonian Dynasty), chinese, chinese_ha_01 (Zhu Xi's Legacy), english, french, french_ha_01 (Jeanne d'Arc), hre, hre_ha_01 (Order of the Dragon), japanese, japanese_ha_sen (Sengoku Daimyo), jin_dynasty, lancaster, malian, mongol, mongol_ha_gol (Golden Horde), ottoman, rus, sultanate (Delhi), sultanate_ha_tug (Tughlaq Dynasty), templar

## Game modes covered

- **Standard skirmish/MP**: full coverage
- **Empire Wars (xp3 variant)**: pop cap covered via army XML files (default variant in our source = default game mode); villager 2-per-train covered via core TC override + xp3 injection in TCs that explicitly declare the variant
- **Nomad**: covered via standard TC overrides — players build a regular TC, our overrides apply automatically
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
│   │   └── instances/            # All override source XML (109 files)
│   │       ├── army/standard_mode/      # 23 army files (pop cap, storage caps)
│   │       └── ebps/
│   │           ├── gameplay/resources/  # gold (3), stone (3), food (14)
│   │           ├── gaia/animals/        # 8 live animals
│   │           ├── environment/non_tree_resources/  # 8 corpses
│   │           └── races/
│   │               ├── core/buildings/  # 1 core TC defensive override
│   │               └── <civ>/buildings/ # 49 per-civ TC overrides
│   └── locdb/                    # Localization strings
├── archives/                     # Build output: BigPoppa.sga (regenerated)
├── cache/                        # Build intermediate cache (regenerated)
└── .aoe4/                        # Editor session state
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

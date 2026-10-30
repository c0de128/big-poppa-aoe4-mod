# AoE4 Modding Primer (for Claude Code)

Read this before Phase 1. Items marked **VERIFY** are from community sources — confirm against real files.

> **Verified on Kev's PC (2026-10-30):**
> - Documents is redirected to `%USERPROFILE%\OneDrive - <Company>\Documents`.
> - Subscribed mods live in `mods\extension\subscriptions\<listing id>\` (not `subscribed`). Local builds live in `mods\extension\local\<mod>\`.
> - Content Editor projects are plain XML in `mods\<ModName>\`. Overrides are under `assets\attrib\instances\` and are **full copies** of the base file, not deltas.
> - Pop cap uses **two** fields per civ: `army_bag/race_population_cap_table/max_personnel_cap` and `army_bag/resource_max_cap/popcap`. Some civs also have a separate `max_vehicle_cap` (e.g. Viking villagers).
> - Starting resources are not changed by Big Poppa.
> - Republishing the same project from the Mod Publisher updates the existing listing and keeps its rating.
> - AOEMods.Essence 0.7.0 reads only the **first** table of contents of a mod `.sga`. Use `tools/sga_dump_all.py` to see every file, including the description and cover.

## 1. How AoE4 mods are made and shipped

- Mods are built in Relic's official **Content Editor** (`EssenceEditor.exe`, installed with the game / "AoE4 Content Editor" tool). It's a **GUI** — Claude Code can't click through it. Kev does those steps (see `HUMAN_STEPS.md`).
- Four mod types: **Crafted Map, Generated Map, Tuning Pack, Game Mode**.
  - **Tuning Pack** = changes to game data ("attributes"): costs, stats, pop cap, etc. Edited in the **Attribute Editor** inside the Content Editor.
  - **Game Mode** = Lua-like **SCAR** scripts that run during a match (e.g. set starting resources, set pop cap at game start).
- Mods are distributed through the **in-game mod browser / ageofempires.com/mods**, **not Steam Workshop**. Updating means republishing from the Content Editor with the same account that published it.

## 2. Where files live (Windows) — VERIFY on Kev's PC

| What | Likely location |
|---|---|
| Installed mods (local + subscribed) | `Documents\My Games\Age of Empires IV\mods\extension\local` and `...\mods\extension\subscribed` (check sibling folders under `mods\` too) |
| Content Editor projects (editable source) | Default "Location" on mod creation is the **Documents** folder — search `Documents` (and OneDrive Documents) for a folder named like `Big Poppa` / `BigPoppa` / `big_poppa` |
| Game data archives | Steam install, e.g. `...\steamapps\common\Age of Empires IV\cardinal\archives\Attrib.sga` |

`Documents` is often redirected to `OneDrive\Documents`. Check both.

## 3. File formats & tools

- **`.sga`** = Relic archive (like a zip). Compiled mods ship as `.sga` + metadata.
- **`.rgd`** = compiled attribute data inside the archive.
- **AOEMods.Essence** (open source, github.com/aoemods/AOEMods.Essence) — has a CLI that can:
  - `sga-unpack <input.sga> <output-folder>` — unpack an archive
  - `rgd-decode <input> <output> -b -f json` — decode `.rgd` files to readable JSON (`-b` = whole folder)
  - Needs the .NET runtime. Example usage (from AoE4 World's data pipeline):
    ```
    dotnet AOEMods.Essence.CLI.dll sga-unpack ./Attrib.sga ./attrib-raw
    dotnet AOEMods.Essence.CLI.dll rgd-decode ./attrib-raw ./attrib-json -b -f json
    ```
- Decoded JSON is for **reading and diffing**. Don't plan on hand-editing and repacking a `.sga` for publishing — the supported path is rebuilding in the Content Editor.

## 4. Population cap — where it lives

**Tuning Pack route (data):**
`Attributes → army → <each civ's army bag> → race_population_cap_table → max_personnel_cap`
- Each civ has its **own** army bag. That's why the new civs didn't inherit Big Poppa's changes: they have new army bags the old mod never touched.
- Note: some civs use "vehicle" pop for special things (community note: Mongol sheep, Byzantine/Roman prelate). Check whether the cap table has more than one cap type per civ.

**Game Mode route (script):**
```lua
Player_SetMaxCapPopulation(player.id, CT_Personnel, 1000)   -- raises the ceiling
Player_SetMaxPopulation(player.id, CT_Personnel, value)     -- current cap
```
A script applies to all players regardless of civ — useful if the data route needs per-civ entries we can't add.

## 5. Starting resources — where it likely lives

- Script: `Player_SetResource(player.id, RT_Food|RT_Wood|RT_Gold|RT_Stone, amount)` in a game mode.
- Data: look in the civ/race or army bag attributes for starting-resource fields. **VERIFY by diffing** Big Poppa vs vanilla — whatever differs is what the mod changed.

## 6. Gotchas

- Tuning packs can load silently and **not apply** if they're stale/incompatible. Always test in a real skirmish and read the pop counter.
- New civs' internal names are **not** guaranteed to be `vikings` / `scots`. Find them in the decoded vanilla data.
- Variant civs (e.g. Order of the Dragon, Zhu Xi's Legacy, Jeanne d'Arc, Ayyubids) have their own entries too — make sure ALL civs in the current game are covered, not just the two new ones.

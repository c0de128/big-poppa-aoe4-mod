# Project Brief — Big Poppa update

> **Status (2026-10-30): done.** All 25 civs are covered and the pop cap is 1000 on both values. The update is published on #503437, but the latest republish still needs confirming (see `HUMAN_STEPS.md`). A second mod, **BIG POPPA 500** (500 pop), was added and published as #562254. Full record: `FINDINGS.md`.

## The situation (plain English)

- Kev made an AoE4 mod called **Big Poppa**. It's published and currently installed (subscribed) in his game on Steam.
- On **Oct 29, 2026** the *Raiders of the North* expansion (game update 17.0) added two new civs: **Vikings** and **Scots**.
- Big Poppa was built before those civs existed, so they don't get the mod's changes. They play like normal.
- Kev **lost the original project files** (the editable source). All we have for sure is the compiled mod the game downloaded. *(Later found in Phase 1: the project was intact in OneDrive Documents.)*

## The goal

1. **Every civ Big Poppa is missing** (Vikings, Scots, and any other civ added since it was built) gets **the same treatment** every other civ gets in Big Poppa.
2. **Population cap = 1000** for every civ (old and new).
3. Publish the updated mod under Kev's existing mod listing.

## What Big Poppa does (Kev's notes — confirm in the Phase 3 diff)

- **2 villagers per train.** Check every civ's villager-producing building(s), especially Vikings' and Scots' (they may train villagers from different/new buildings).
- **50,000 resources in every non-tree resource node** (gold, stone, berries, fish, huntable/herdable animals + corpses). ✅ **Kev decided (2026-10-30): keep 50,000** to match existing civs. (An earlier note said 100,000; the mod has always used 50,000.) There are no new non-tree node types in 17.0, only new pine trees.
- **Stockpile limit 200,000** (food/wood/stone/gold, up from 100,000). This was already in the mod and is applied to the new civs too.

## Kev's decisions (2026-10-30)

1. Resource piles: **keep 50,000**.
2. **Viking villager limit** (`max_vehicle_cap`, Vikings only): **200 → 1000**.
3. Scots Highland Cattle cap (21), Scots fish ponds, Viking Longhouse farmsteads: **leave as-is**.
4. **Refresh the 36 out-of-date override files** from 17.0 data, re-applying **only** Big Poppa's existing edits.
5. New civ army files: pop cap 1000 on **both** cap values (`max_personnel_cap` and `resource_max_cap/popcap`).
6. Golden Horde keeps **2 scouts per train** (an original Big Poppa quirk).
7. Tughlaq: TCs train **2 villagers**, and worker elephants go back to **1** (this fixes the May quirk).
8. Description says **25 civs**, plus new cover art.
9. **Both pop values equal on every civ.** The 23 original civs' `resource_max_cap/popcap` changed 200 → 1000 (this replaces the "leave at 200" rule).
10. **Second mod BIG POPPA 500:** identical to Big Poppa but 500 everywhere Big Poppa has 1000. It has its own ID, name, description and cover.
- **Houses stay +10 pop** (unchanged, same as original). Players build lots of houses.
- **Starting resources stay default** unless the diff shows Big Poppa changed them.

## Open questions (answer from evidence, then confirm with Kev)

*All answered (see `FINDINGS.md` Phase 1/3):*
- It changes pop cap, storage, piles and villagers per train, but not starting resources or gather rates.
- It's a Tuning Pack.
- Pop was already 1000 (`max_personnel_cap`).
- The source project was found.

- **What exactly does Big Poppa change?** "Same resources" most likely means starting resources and/or gather rates, but we confirm by decoding the mod and diffing it against the vanilla game. Write the full list of changes in `FINDINGS.md`.
- **What type of mod is it?** Tuning Pack (data/attribute changes) or Game Mode (script/SCAR changes) — or both. This decides how we rebuild it.
- **Is the original pop cap already 1000?** If it was something else, flag it before changing.
- **Can we find the original source project?** Check the default Content Editor locations first (see PLAN Phase 1). If found, life is much easier.

## Out of scope (unless Kev says otherwise)

- Balance changes to unique units or new-civ mechanics (Sagas, Longhouse, Mustering Hall, etc.).
- New features of any kind.

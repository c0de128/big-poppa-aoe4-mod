# FINDINGS (Claude Code updates this after each phase)

## Phase 1 — Find the mod (done 2026-10-30, read-only)

### Plain English
- **The "lost" project isn't lost.** The full editable Big Poppa project is still on the PC, in the Documents folder that is now redirected into OneDrive.
- It's a **Tuning Pack** built from plain-text XML files. It covers **23 civs**. The only civs missing are **Vikings** and **Scots** (25 civs exist now).
- The project file has a **mod ID**, and the game lists the published mod as subscription **503437**. Because we have the original project, republishing from it should update the same listing. That's the officially documented path, but it hasn't been tested yet.
- A copy is saved in `work/original_mod/`. Nothing in the original folders was changed.

### Where everything is
| What | Path |
|---|---|
| Documents (redirected) | `%USERPROFILE%\OneDrive - <Company>\Documents` (plain `Documents` and `OneDrive\Documents` have no AoE4 folder) |
| **Source project** | `...\Documents\My Games\Age of Empires IV\mods\BigPoppa\BigPoppa.aoe4mod` (+ `assets\attrib\instances\` = 109 override XMLs) |
| Local build | `...\mods\extension\local\BigPoppa\BigPoppa.sga` (+ `BigPoppa.jpg` thumbnail) |
| Subscribed copy | `...\mods\extension\subscriptions\503437\BigPoppa.sga` |
| Other subscription | `...\mods\extension\subscriptions\457307\`: empty folder, not Big Poppa |
| Load order | `...\Age of Empires IV\mods_meta_data.lua` → `BigPoppa` (priority 1), `503437` (priority 2), both enabled |
| Game install | `C:\Program Files (x86)\Steam\steamapps\common\Age of Empires IV` (Steam library only on C:) |
| Vanilla data | `...\cardinal\archives\Attrib.sga` (110 MB) **and** `ReferenceAttributes.sga` (30 MB, vanilla *source* XML). Both are dated 2026-10-30, i.e. update 17.0 |
| Earlier work folder (May 2026) | `%USERPROFILE%\aoe4work\`. Holds AOEMods.Essence (prebuilt CLI, same 0.7.0 zip size), extracted 16.x reference data, decompiled editor DLLs, and the "1000pop,MoreResources,FasterVillages" reference mod |
| Docs zip | `%USERPROFILE%\Downloads\big-poppa-docs(.zip)`: just this project's docs, not mod files |

The three `.sga` copies (project `archives\`, local, subscribed) are **identical** (SHA-256 `b539c4b1…`, 2,673,150 bytes, built 2026-05-15 08:34). The published mod is exactly the local build.

### Copied to `work/original_mod/` (verified: 124 files, 9,980,131 bytes, hashes match)
- `source_project/`: the whole `mods\BigPoppa` project folder
- `compiled_local/`: `BigPoppa.sga` + `BigPoppa.jpg`
- `compiled_subscribed_503437/`: `BigPoppa.sga`
- `mods_meta_data.lua`

### Mod identity (for "update the same listing")
- `BigPoppa.aoe4mod`: `<ID>1bfbb3a8-719b-448e-8469-f58c7363bc36</ID>`, `<Type>Extension</Type>`
- `assets\attrib\BigPoppa.xml`: `<mod guid="1bfbb3a8719b448e8469f58c7363bc36" … override_instances="True">`
- `assets\mod.rdo`: `DataObject Name="BigPoppa" Type="Mod" Id="1646313236515342441"`
- Published/subscription ID: **503437**
- ❓ Which of these the publisher uses to match the listing is not documented. Since we have the original project (same ID), the official "rebuild + Publish overwrites Published" path applies. Confirm in the Mod Publisher that it shows Big Poppa as already published before clicking.
- ⚠️ `ProjectSettings.xml` remembers the old path `%USERPROFILE%\Documents\...`. The folder has since moved into OneDrive (folders dated 2026-10-21, files still dated May). The editor should still open the `.aoe4mod` from its new location, but that's untested.

### What the mod does (from its own README/description + quick value check)
The project includes `README.md` and `CLAUDE.md` written during the May 2026 build. They document every change. A quick count of values in the copied XML matches them:
- **Pop cap 1000**: `army/standard_mode/normal_<civ>.xml` → `army_bag/max_personnel_cap = 1000` (23 files). Storage caps food/wood/stone/gold/militia_hre 100k → **200k**.
- **2 villagers per train**: per-civ Town Center files `ebps/races/<civ>/buildings/building_town_center*.xml` → `number_to_spawn = 2` (49 files + 1 core). Jin's mounted villager is doubled too.
- **Resource nodes = 50,000** (gold ×3, stone ×3, berries/prickly pear ×8, fish ×6, live animals ×8, corpses ×8).
- Not changed: trees, farms, gather rates, carry capacity, starting resources, campaign/Cordoba variants.
- ⚠️ `resource_max_cap/popcap` was left at **200** (31 occurrences). Research suggested setting it equal to the cap. The mod evidently worked without it. Check in Phase 3.

### ⚠️ Discrepancies with Kev's notes (need Kev's answer)
1. **Resource nodes: 50,000 in the mod, not 100,000.** The mod's in-game description also says "50,000 each". The only 100,000 in the mod is the old *storage* cap (raised to 200,000). Keep 50,000 for Vikings/Scots nodes (consistent), or change everything to 100,000 (a new change)?
2. **"Lost project files"**: they exist (above). If Kev has a different, newer copy somewhere, say so.

### Phase 1 implications for later phases
- **Phase 2 is mostly done already**: .NET 6.0.36 is installed and the Essence CLI exists in `aoe4work`. Plan: copy (not move) it into `tools/`, then run a quick test.
- **Phase 3 gets simpler**: no need to reverse-engineer the mod. The source XML *is* the spec. Phase 3 becomes three things:
  1. Find the Vikings/Scots army + Town Center files in 17.0 `ReferenceAttributes.sga`, including whatever buildings train their villagers.
  2. Find any new 17.0 resource node types.
  3. Check whether 17.0 changed the base versions of the 107 files we override. Our files are *full copies* of May-era base data, so stale copies could undo 17.0 balance changes or break things.
- **Phase 3.5 question is already answered**: the editor's source files are readable XML, and the May build was done by writing them directly. That worked and was published. Kev still needs to click **Build** and **Publish** in the editor; there's no command-line build.

## Phase 2 — Tools
_not started_

## Phase 3 — New civs, new nodes, stale copies (done 2026-10-30, report only, nothing fixed)

### Plain English
- **Backup made**: `work/backup_bigpoppa_2026-10-30/` (124 files, every SHA-256 hash matches the original).
- **Vikings and Scots each need 3 files**: 1 army file (pop cap and storage) and 2 Town Centers (2 villagers per train). Only Town Centers train villagers. The Viking Longhouse doesn't.
- **No new non-tree resource nodes in 17.0.** The only new nodes are 9 pine trees, and Big Poppa leaves trees alone on purpose. Nothing to add there.
- **Watch out:** Viking **villagers use a separate population pool** ("vehicle" pop, capped at 200). Even at 1000 total pop, Vikings may be stuck at 200 villagers unless we raise that too. Needs Kev's call.
- **36 of Big Poppa's 109 files are out of date.** The 17.0 update (and patches since May) changed them, and our old copies would undo those changes. Most are small. A few matter for gameplay (list below).

### How this was checked
- Tool: `tools/Essence/` (AOEMods.Essence CLI **0.7.0**, copied from `%USERPROFILE%\aoe4work\Essence`). Runs on the installed .NET 6.0.36.
- 17.0 vanilla *source* XML: unpacked `ReferenceAttributes.sga` (dated 2026-10-30) → `work/vanilla_ref_17/` (31,043 files in 48 s).
  - It's the same XML format Big Poppa's project uses, so no RGD decoding was needed.
- May vanilla (the base Big Poppa was built on): `%USERPROFILE%\aoe4work\cardinal_refattribs\` (28,130 files, extracted 2026-05-14). 17.0 added 2,989 files and removed 78.
- **Stale check**: for each of the 109 override files, compare May base vs 17.0 base. Big Poppa's own edits are not part of this comparison, so any difference is a change made by the game.
- Line order and `List.ItemID` attributes were ignored, because Relic reshuffles them. Raw diffs looked huge (core TC 12,924 lines) but are mostly reordering.
- Outputs:
  - `work/diff/stale_summary.tsv` (raw)
  - `work/diff/stale_detail.txt` (real changes per file)
  - `work/diff/stale/*.diff`

### 1. Vikings & Scots files (17.0)
| Purpose | Vikings | Scots |
|---|---|---|
| Army (pop cap, storage) | `army/standard_mode/normal_vikings.xml` | `army/standard_mode/normal_scots.xml` |
| Town Center | `ebps/races/vikings/buildings/building_town_center_vik.xml` | `ebps/races/scots/buildings/building_town_center_sco.xml` |
| Capital TC | `ebps/races/vikings/buildings/building_town_center_capital_vik.xml` | `ebps/races/scots/buildings/building_town_center_capital_sco.xml` |
| Villager squad | `sbps\races\vikings\unit_villager_1_vik` | `sbps\races\scots\unit_villager_1_sco` |
| TC style (see the old `CLAUDE.md` "merging vs replacing") | **Replacing**: explicit `number_to_spawn=1`, so patch it to 2 | **Merging**: no `number_to_spawn`, so inject `number_to_spawn=2 overrideParent="True"` |

Only the 4 TC files train villagers. I searched every Vikings/Scots building for villager squads.

**Army values (vanilla 17.0)**
| | Vikings | Scots | English (for comparison) |
|---|---|---|---|
| `max_personnel_cap` | 200 | 200 | 200 (Big Poppa: 1000) |
| `max_vehicle_cap` | **200** | **21** | 0 |
| `resource_max_cap/popcap` | 200 | 200 | 200 (Big Poppa left it at 200) |
| storage food/wood/stone/gold/militia_hre | 100,000 | 100,000 | 100,000 (Big Poppa: 200,000) |
| starting food/wood/gold/stone | 0/200/100/0 | 200/200/100/0 | 200/200/100/0 (unchanged) |

- ⚠️ **Viking villagers use 1 `vehicle_pop`** (`unit_villager_1_vik.xml`), so `max_vehicle_cap=200` probably limits Viking villager count. ❓ It's unclear whether they also cost personnel pop. Phase 3.5 smoke test can show it.
- ⚠️ **Scots `max_vehicle_cap=21`** limits **Highland Cattle** (`gaia_highland_cattle_sco`, 1 vehicle pop, 0 personnel pop), a Scots-only herdable food unit made from a building.

**Civ-specific food sources (not neutral nodes)**
- Scots Highland Cattle; Scots fish ponds `building_resource_fish_pond(_upgraded)_sco` (10,000 food); Vikings Longhouse farmsteads (cabbage/turnip).
- These are civ mechanics, like Malian cattle and farms, which Big Poppa deliberately left alone. They don't count as "nodes". Kev decides.

### 2. New 17.0 resource node types
- Neutral nodes with `initial_amount`: May 68 → 17.0 73. The 5 new ones are 3 "rogue" mode items (`rogue_endless_oak` 50,000, `prized_ndama(_corpse)_rogue` 2,000) and 2 Scots fish ponds (above).
- New files under `ebps/gameplay/resources`: 9, **all pine trees** (`pine_thin_*`, `scots_pine_*`, likely for the Scottish Heathland / Tundra biomes). There are no new gold, stone, berry, fish or animal nodes, and nothing new under `ebps/gaia` or `environment/non_tree_resources`.
- ✅ **Big Poppa already covers every non-tree node type in 17.0.**

### 3. Stale copies: 36 of 109 files changed by the game since May (73 unchanged)
| Risk | Files | What 17.0 changed (our copy would undo it) |
|---|---|---|
| 🔴 Gameplay / new-civ interaction | 7 berry bush + prickly pear files | New `interaction_type` entries **`resource_gather_cattle_sco` / `resource_worked_cattle_sco`**, so Scots Highland Cattle can graze berries. Also gather-slot changes (`prefer_number` 5→1, `max_number`). Our stale copies would probably **break the Scots cattle mechanic** on berries. |
| 🔴 Balance / civ abilities | Abbasid TC + capital TC | Golden Age bonus abilities 1–3 **replaced by `city_planning_buff_abb`**. Our copy keeps the old ones. |
| 🟠 Balance | core TC, HRE OotD TC, Chinese TCs | TC build time 150→165 (core), 120→132 (OotD), Chinese 75/82.5, plus new production-count fields |
| 🟠 Balance | Mongol TC + capital | Stone cost 62.5→60 |
| 🟠 Balance | Mongol moving capital TC | Pack speed 3→3.6 |
| 🟠 Wrong unit | Jeanne d'Arc TCs (both) | Scout changed from French scout to `unit_scout_1_fre_ha_01` |
| 🟡 Civ trait numbers | 8 army files (abbasid, byzantine, hre, hre_ha_01, jin, mongol, rus, templar) | `int_value` changes in civ trait/bonus tables (e.g. Rus 5→20, Jin 90→75, Mongol 130/160→140/170); Abbasid/HRE gained new trait entries |
| 🟡 Minor | river fish; TCs for Ayyubids, Macedonian, Lancaster, Golden Horde, Templar, Tughlaq, Jin | New `unit_type=scar_town_center` tag (scripts use it to find TCs), pathing tags, Jin file now version 6 with variants |

**Conclusion:** the stale copies would quietly undo several 17.0 changes. The berry/cattle one probably affects Scots directly. Rebuilding those 36 files from the **17.0 base + Big Poppa's same edits** looks like the right fix. That's a Phase 4 decision; nothing has been changed.

### Open questions for Kev (before Phase 4)
1. **Resource nodes**: your reply had the choice template unfilled. A = keep 50,000, or B = raise all to 100,000?
2. **Viking villagers' separate 200 pool** (`max_vehicle_cap`): raise it with the pop cap so Vikings can have more than 200 villagers?
3. **Scots Highland Cattle cap of 21** and Scots/Viking civ-specific food (cattle, fish ponds, farmsteads): leave as-is, like Malian cattle?
4. **Refresh the 36 stale files** from 17.0 data (keeping Big Poppa's edits)?

## Phase 4/5 — Files updated in the project (done 2026-10-30, NOT built or published)

### Plain English
- The Big Poppa project now has **115** override files: the 109 old ones (36 refreshed to 17.0) plus 6 new ones for Vikings and Scots.
- A separate checker compared **every** file with the 17.0 game files and found **zero unexpected differences**. All 115 are valid XML.
- Nothing was built or published. Kev does that in the Content Editor.

### What changed in `...\mods\BigPoppa\assets\attrib\instances\`
- **36 refreshed**: the Phase 3 stale list, rebuilt from 17.0 `ReferenceAttributes.sga` with Big Poppa's same edits. They now include 17.0's own changes (cattle-on-berries, Abbasid TC ability swap, build times, etc.).
- **6 new**:
  - `army/standard_mode/normal_vikings.xml`: `max_personnel_cap` 1000, `resource_max_cap/popcap` 1000, **`max_vehicle_cap` 1000 (Viking villager limit)**, storage 200,000
  - `army/standard_mode/normal_scots.xml`: `max_personnel_cap` 1000, `resource_max_cap/popcap` 1000, storage 200,000
  - `ebps/races/vikings/buildings/building_town_center(_capital)_vik.xml`: villager `number_to_spawn` 1→2
  - `ebps/races/scots/buildings/building_town_center(_capital)_sco.xml`: injected villager `number_to_spawn=2 overrideParent="True"` ("merging" TC style)
- **73 untouched**: their 17.0 base is identical to May.
- Not touched: `BigPoppa.aoe4mod`, `BigPoppa.xml`, `mod.rdo`, locdb, `archives\`, `cache\`.
  - ⚠️ The in-game **description still says "all 23 current civs including Jin Dynasty"**. Updating it (locdb text) is optional and Kev's call.

### How it was done (reproducible)
- `tools/bp_transform.py`: Big Poppa's edit rules, derived from the May build vs its May base (`tools/bp_analyze.py`).
  - **Proven**: applied to May base, it reproduces all **109** May Big Poppa files exactly (line endings/final newline aside).
  - Applied to 17.0, it gives 73 identical / 36 changed (= the Phase 3 list exactly) / 6 new.
  - Staged in `work/staging_17/`, copied into the project, and all 42 verified byte-for-byte.
- `tools/bp_verify.py`: an independent line diff of every project file vs 17.0 base. It only allows the intended edits. Report: `work/diff/final_check.md`.
- `tools/sga_count.py`: counts files across all archive TOCs (Essence only reads the first).
  - 17.0 `ReferenceAttributes.sga` has 1 TOC / 31,043 files, and Essence extracted 31,043, so it's complete.
  - The old `BigPoppa.sga` is v11 with 3 TOCs, so it isn't unpacked with Essence.
  - The new build's attrib TOC should hold **116** files.
- Rollback: `work/backup_bigpoppa_2026-10-30/` (verified copy of the whole project before any change).

### ⚠️ Flags (details in `work/diff/final_check.md`)
1. **Original-build quirks, reproduced exactly as instructed**:
   - **Golden Horde scouts ×2** (vanilla GH villagers are already ×2).
   - **Tughlaq worker elephants ×2, Tughlaq villagers NOT doubled.**
   - Big Poppa's README says scouts stay 1, so these look like May bugs. Kev's call whether to fix.
2. `_emi` fish variants + live enchanted stag have no own `initial_amount`, so their piles may not be 50,000 (unchanged since May).
3. New civs have `resource_max_cap/popcap` = 1000; the old 23 civs keep 200 there (and work). Watch for any difference in testing.
4. `ProjectSettings.xml` still points at the pre-OneDrive path. If the editor complains, open `BigPoppa.aoe4mod` via File → Open.

## Phase 6a — Build verification (2026-10-30, Kev built in the Content Editor; not yet published or tested)

- Editor log: "115 instances loaded / validated", "Writing [115] instance RGD files (Full Burn)", no errors.
- New `BigPoppa.sga` (2,792,064 bytes, 09:48) is in both `mods\BigPoppa\archives\` and `mods\extension\local\BigPoppa\` (identical hashes). The subscribed copy (503437) is still the old May build, as expected until Kev publishes.
- File count (`tools/sga_count.py`): v11, 3 TOCs. **attrib = 116** (115 overrides + `BigPoppa.xml`, exactly as predicted), info = 2, locale = 1.
- Essence unpacked and decoded all 116 attrib files → `work/new_build/decoded/`. Compiled values (`tools/rgd_values.py`):
  - Vikings: `max_personnel_cap` 1000, `popcap` 1000, `max_vehicle_cap` 1000, storage 200,000; TC first spawn item (villager) = 2, scout/völva = 1
  - Scots: `max_personnel_cap` 1000, `popcap` 1000, `max_vehicle_cap` 21 (unchanged, as decided), storage 200,000; both TCs: villager = 2, scout = 1
  - Spot-checks: the berry bush has 50,000 plus the 17.0 cattle interaction. The Abbasid TC has the 17.0 `city_planning_buff_abb`; its remaining `golden_age_bonus_*` references are also in 17.0 vanilla.

## Phase 6b — Rebuild after quirk decisions (2026-10-30 10:13; not published or tested)

- Editor log: 115 instances loaded/validated/written, no errors.
- New `BigPoppa.sga`: 2,792,069 bytes. The project `archives\` and `extension\local\` copies are identical. 3 TOCs, **attrib = 116** (as expected).
- Decoded all 116 → `work/new_build_2/decoded/`. Spawn counts (`tools/rgd_spawns.py`):
  - **Tughlaq** TC + capital: villager **2**, scout 1, worker elephant **1** ✅ (fixed)
  - Golden Horde: villager 2 (vanilla), scout **2** (kept, per Kev)
  - Vikings: villager 2, scout 1, völva 1. Scots: villager 2, scout 1. English (sanity check): default 2, xp3 2, campaign 1.
- Vikings/Scots army values unchanged from 6a: pop cap 1000 ×2, Viking villager limit 1000, Scots cattle cap 21.
- ⚠️ This build still has the **old description** ("23 civs"). The new text has not been saved yet (awaiting Kev's OK).

## Phase 6c — Rebuild with new description (2026-10-30 10:23; not published or tested)

- Editor log: 115 instances written, "[2] burnt and [2] cached" (the description was rebuilt), no errors.
- New `BigPoppa.sga`: 2,792,089 bytes. The project `archives\` and `extension\local\` copies are identical (SHA-256 `e2a4943f…`). 3 TOCs: **attrib 116**, info 2, locale 1.
- All 119 files extracted from **every** TOC with `tools/sga_dump_all.py` (Essence only reads the first TOC). Compared with the 6b build: **the only changed file is `locale/en/en.ucs`**. All 116 attrib files and both info files are byte-identical.
- Description in the build now ends: "Works with all 25 current civs, including Vikings and Scots (Raiders of the North)." The mod name is unchanged (its em dash is U+2014, same as the May build).
- This is the build to test, then publish.

## Phase 6d — In-game test (2026-10-30)
- Kev tested the 10:23 build (Local tuning pack) in game: **"THE MOD WORKS GREAT!"**
- Not yet published. Next step is Kev's: publish from **Mods → My Mods → Mod Publisher** as an update to listing 503437.

## Phase 6e — New cover art + rebuild (2026-10-30 12:06; not published)
- Kev supplied new cover art (25 civs, "Updated 10/30/26"). Converted to PNG → `assets\mod.png`; the .jpg copied to `mods\extension\local\BigPoppa\BigPoppa.jpg`. Old files backed up in `work/backup_pre_coverart/`.
- New `BigPoppa.sga` (2,643,053 bytes, 12:06) is identical in the project and local folders. 116 attrib + 2 info + 1 locale files, all extracted OK.
- Against the tested 10:23 build, the **only** changed file is `info/mod.rrtex` (the cover image). All 116 data files and the description are byte-for-byte the same.

## Phase 7 — Published (2026-10-30)
- Kev published from the Mod Publisher. It updated the **existing listing 503437** in place (same listing, rating 4.5/5 from 16 kept). It shows the new cover art, the 25-civ description and update date 10/30/2026.
- The new download in `mods\extension\subscriptions\503437\` (`ed0a9651...sga`, 2,643,053 bytes) is **byte-identical** to the 12:06 build (SHA-256 `bc0c1deab273c83f...`).
- The local "Update Mod" panel crops the square cover art to a wide strip; the published listing shows it in full.
- Public repo: https://github.com/c0de128/big-poppa-aoe4-mod

## Phase 8: BIG POPPA 500 (second mod, 2026-10-30; not built or published)
- Kev made a new tuning pack in the Content Editor: `mods\BIG POPPA 500\`, mod ID `44d9ed12-23d8-4545-b9bf-501dc39221bf` (BigPoppa is `1bfbb3a8-...`, listing 503437).
- Kev's own project files were kept as-is: ID, manifest, `_default.burnproj`, `mod.rdo`, 1920x1080 `mod.png`, and the name/description he typed into `BIG POPPA 500_en.csv`. The CSV matches his requested text word for word.
- The empty project was backed up to `work/backup_bp500_empty/` before changes.
- Copied BigPoppa's 115 `assets\attrib\instances` files, with no metadata. Then, in the default variant only, every pop value of 1000 became 500:
  - `max_personnel_cap`: 25 civs
  - `resource_max_cap/popcap`: Vikings and Scots only (the other 23 civs stay at 200, the same as BigPoppa)
  - Vikings `max_vehicle_cap`: 1
- Diff against BigPoppa: 25 files differ, by exactly 28 lines, all of them pop 1000 to 500. The other 90 files are identical, and no file exists on only one side.
- BigPoppa's 115 data files were hash-checked before and after: unchanged.

## Phase 9: Both pop values match on every civ (2026-10-30; neither mod built or published)
- **Kev's decision:** `max_personnel_cap` and `resource_max_cap/popcap` must be equal on all 25 civs. This replaces the Phase 8 rule of changing only values that were 1000.
- **Backups:** both projects' `assets\` folders, plus BigPoppa hashes, are in `work/backup_pre_popcap1000/`.
- **BigPoppa:** `resource_max_cap/popcap` 200 → **1000** in the default variant for the 23 civs that were still at 200.
  - Diff of all of `assets\` against the backup: 23 files, exactly 23 lines, all `popcap 200 → 1000`. Nothing else changed.
- **BIG POPPA 500:** the same field 200 → **500** for those 23 civs.
  - Diff of the data files against the new BigPoppa: 25 files differ by exactly 51 lines. Those are `max_personnel_cap` 1000 → 500 (25), `popcap` 1000 → 500 (25) and Vikings `max_vehicle_cap` 1000 → 500 (1).
  - No file exists on only one side.
  - The name and description in `BIG POPPA 500_en.csv` match Kev's text exactly.
- **Result:** in the default variant, BigPoppa is 1000/1000 and BIG POPPA 500 is 500/500 on all 25 civs.
  - Campaign variants were left at 200 in both mods, as before.
  - Other civs' `max_vehicle_cap` values are unchanged (HRE 200, Scots 21, Mongol 30, ...).
- ⚠️ The public GitHub repo still describes the old 200 value for the 23 civs (`mod/README.md`), and its XMLs are the pre-change copies.

## Phase 9b: Both mods built and verified (2026-10-30; not published)
- **BigPoppa** `BigPoppa.sga` (2,643,038 bytes, 12:34, SHA-256 `9402119f8ef84ac6...`): the project and local copies are identical.
  - 116 attrib + 2 info + 1 locale files, all extracted OK.
  - Against the published 12:06 build, only 23 army files differ.
  - Decoded: all 25 civs are `max_personnel_cap` 1000 / `resource_max_cap/popcap` 1000. Vikings `max_vehicle_cap` is 1000.
- **BIG POPPA 500** `BIG_POPPA_500.sga` (3,447,650 bytes, 12:38, SHA-256 `6605c51d2d3ae502...`): the project and local copies are identical.
  - 116 attrib + 2 info + 1 locale files, all extracted OK.
  - Against the new BigPoppa build, the differences are 25 army files, `mod.bin`, `mod.rrtex` (cover), `en.ucs` (name and description), and the mod manifest RGD (named after each mod). The other 90 data files are identical.
  - Decoded: all 25 civs are 500/500. Vikings `max_vehicle_cap` is 500.
  - The name and description match Kev's text (with a real U+2014 dash).

## Phase 9c: BIG POPPA 500 tested + cover art (2026-10-30; not published)
- Kev tested the 12:38 BIG POPPA 500 build in game: "worked perfectly".
- New cover art (1024x1024 JPG from Kev) converted to PNG → `mods\BIG POPPA 500\assets\mod.png`. The old 1920x1080 image is backed up in `work/backup_bp500_coverart/`. The BigPoppa cover was checked: untouched.
- ⚠️ The "UPDATED 10/30/26" ribbon covers the last "0" of "500" in the title.
- A rebuild is needed to pack the new cover.

## Phase 9d: BIG POPPA 500 rebuilt with cover art (2026-10-30 13:11; not published)
- `BIG_POPPA_500.sga` (2,832,996 bytes, SHA-256 `c02e00bd4c8aa359...`): the project and local copies are identical.
  - 116 attrib + 2 info + 1 locale files, all extracted OK.
  - Against the tested 12:38 build, the only changed file is `info/mod.rrtex` (the cover). Pop values, data and description are byte-for-byte the same.
- The BigPoppa build is unchanged (`9402119f8ef84ac6...`).

## Phase 10: Both published; GitHub updated (2026-10-30)
- **BIG POPPA 500** is published as a new listing, **#562254**. The download in `subscriptions\562254\BIG_POPPA_500.sga` is byte-identical to the verified 13:11 build (`c02e00bd...`).
- **BIG POPPA** (#503437): Kev reports it was published. At the time of checking, the subscribed copy on this PC was still the 12:06 version (`bc0c1deab...`), not the 12:34 build (`9402119f...`). Re-check after the game syncs.
- **GitHub** (commit `9098ed6`):
  - `mod/` was synced with the live BigPoppa project (23 army files: popcap 1000).
  - Added `mod-500/` with the BIG POPPA 500 project, assets only.
  - Updated the READMEs and notes, and refreshed `docs/` (with personal paths replaced by placeholders).
  - Personal info scan: 0 hits.

## Decisions log
| Date | Decision | Why |
|---|---|---|
| 2026-10-30 | Houses stay +10 pop; no house-pop script | Same as original Big Poppa (Kev) |
| 2026-10-30 | Starting resources stay default unless diff shows otherwise | Kev. Phase 1: the mod does not change them |
| 2026-10-30 | Scope = every civ Big Poppa misses | Kev. Phase 1: that's Vikings + Scots |
| 2026-10-30 | Resource piles stay **50,000** | Kev: match existing civs |
| 2026-10-30 | Viking villager limit (`max_vehicle_cap`) 200 → **1000** | Kev: Viking villagers use a separate pop pool |
| 2026-10-30 | Scots Highland Cattle cap, fish ponds, Longhouse farmsteads **unchanged** | Kev: civ mechanics, like Malian cattle |
| 2026-10-30 | Refresh 36 stale files from 17.0, re-applying **only** Big Poppa's existing edits | Kev: avoid undoing 17.0 changes |
| 2026-10-30 | New army files: 1000 on both cap values | Kev |
| 2026-10-30 | Original quirks (GH scouts ×2, Tughlaq elephants ×2 / villagers ×1) reproduced, not fixed | "ONLY existing edits"; flagged for Kev |
| 2026-10-30 | Golden Horde 2 scouts per train: **keep** | Kev |
| 2026-10-30 | Tughlaq: TCs train **2 villagers**; worker elephants back to 17.0 default (1) | Kev. Done in both Tughlaq TCs; final check re-run, 0 unexpected (old files in `work/backup_pre_tughlaq_fix/`) |
| 2026-10-30 | Mod description: say 25 civs incl. Vikings + Scots | Kev approved the shown text. Saved in `assets\locdb\BigPoppa_en.csv` (string 2, last sentence only; backup in `work/backup_pre_description/`) |
| 2026-10-30 | Build 10:23 passed Kev's in-game test | Kev: "THE MOD WORKS GREAT!" |
| 2026-10-30 | Published as an update to listing 503437 | Kev. Download verified identical to the tested build plus the new cover art |
| 2026-10-30 | BIG POPPA 500: mirror BigPoppa with 500 in place of 1000 (only values that were 1000) | Kev |
| 2026-10-30 | Both pop values equal on all 25 civs: BigPoppa 1000/1000, BIG POPPA 500 500/500 | Kev (replaces the Phase 8 rule of changing only values that were 1000) |

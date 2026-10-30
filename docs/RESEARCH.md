# RESEARCH — Phase 0 (research only, 2026-10-30)

No files outside this project folder were touched. Nothing was downloaded or run.

**Legend**
- ✅ **CONFIRMED**: seen in an official doc, in source code, or in a data file (URL given).
- 🟡 **COMMUNITY**: stated by forum or wiki users, and at least one person reports it working. Not official.
- ❓ **UNVERIFIED**: inference, a single anecdote, or not found anywhere. Must be checked against real files or a test.

**Access notes:**
- support.ageofempires.com blocks normal fetches (403 / Cloudflare). I read it through its Zendesk JSON API and Wayback snapshots.
- wiki.aoemods.com is **offline** (closed for inactivity). I read it through Wayback.
- The aoemods/attrib data dump is from 2022, so its *field names* are only a strong hint until we decode the current `Attrib.sga`.

---

## 1. Plain-English picture

- **How the mod works:** Big Poppa is (most likely) a **Tuning Pack**: copies of game data files with different numbers. The game only swaps in a modded file when its name matches a real game file exactly.
- **Why the new civs miss out:** every civ has **its own** "army" data file holding its pop cap and starting resources. Vikings and Scots got brand-new files that Big Poppa never copied. The devs said exactly this happened before with Ottomans and Malians. The official fix is to *repeat the changes for the new civs and republish*.
- **Reading the mod:** we can open both the mod and the game's data with a free tool (AOEMods.Essence) and compare them. That tells us exactly what Big Poppa changes.
- **The biggest unknown is updating your *existing* listing.** The official way to update is to republish the *same* local mod. Nobody documents whether a rebuilt-from-scratch project can update the old listing.

---

## 2. Confirmed vs unverified

### Mod mechanics
| Fact | Status | Source |
|---|---|---|
| Tuning pack overrides only files with **the same file name** as the core file ("only overwrites units… that share a file name") | ✅ | [Cloning an Asset](https://support.ageofempires.com/hc/en-us/articles/4414795815572-1-Cloning-an-Asset) |
| New civs do **not** inherit a tuning pack's per-civ clones. Fix: replicate the changes for each new civ and re-publish | ✅ | [Ottoman and Malian Mod Update Guide](https://support.ageofempires.com/hc/en-us/articles/10265086303892-Ottoman-and-Malian-Mod-Update-Guide) |
| Attribute Editor categories: **Army** = "Starting resources, units, and buildings"; **EBPS** = includes gather rate; **Statemodel_schema** = player/civ values | ✅ | [Attribute Editor Guide](https://support.ageofempires.com/hc/en-us/articles/7363714186516-Attribute-Editor-Guide) |
| Files under `statemodel_schema` **cannot be cloned** (so house pop can't be changed in a tuning pack) | 🟡 | [forum: increase house capacity](https://forums.ageofempires.com/t/tuning-mod-increase-houses-capacity/267050), [wiki Population_Cap (archived)](http://web.archive.org/web/20230923085733/https://wiki.aoemods.com/wiki/Population_Cap) |
| The official "Propagating Unit Stats" guide is **outdated**: "Inherit from Parent" / "Clone Override Parent Settings" are reportedly gone, and Core edits don't flow to per-civ copies | 🟡 (forum, Oct 2026) | [forum: Guide outdated](https://forums.ageofempires.com/t/guide-outdated/290556) |
| Official support won't help with Content Editor problems ("technical limitations") | 🟡 | same thread |
| Some users say pop-cap fields turned purple or wouldn't accept edits after patches | ❓ anecdotes (2022–2025) | [forum: change population limit](https://forums.ageofempires.com/t/how-to-change-the-population-limit-from-aoe4-content-editor-essenceeditor-exe/205739) |

### Civ internal names (all 25)
✅ From aoe4world's current config (pushed 2026-10-28), [civs.ts](https://github.com/aoe4world/data/blob/main/src/lib/config/civs.ts). I checked it directly.

| Civ | attribName | Civ | attribName |
|---|---|---|---|
| Abbasid | `abbasid` | Malians | `malian` |
| Ayyubids | `abbasid_ha_01` | Mongols | `mongol` |
| Byzantines | `byzantine` | Order of the Dragon | `hre_ha_01` |
| Chinese | `chinese` | Ottomans | `ottoman` |
| Delhi | `sultanate` | Rus | `rus` |
| English | `english` | **Scots** | **`scots`** (suffix `_sco`) |
| French | `french` | Sengoku | `japanese_ha_sen` |
| Golden Horde | `mongol_ha_gol` | Tughlaq | `sultanate_ha_tug` |
| HRE | `hre` | **Vikings** | **`vikings`** (suffix `_vik`) |
| House of Lancaster | `lancaster` | Zhu Xi's Legacy | `chinese_ha_01` |
| Japanese | `japanese` | Jeanne d'Arc | `french_ha_01` |
| Jin Dynasty | `jin_dynasty` | Knights Templar | `templar` |
| Macedonian | `byzantine_ha_mac` | | |

❓ Per CLAUDE.md ("don't guess"), these are third-party evidence. **Phase 3 must confirm them in the decoded vanilla `army/` folder.** Big Poppa probably also misses other newer civs, such as Golden Horde, Macedonian, Sengoku, Tughlaq and Jin, depending on when it was last published. The diff will tell us.

---

## 3. Where things live

### Pop cap
**Tuning pack (data)**: file `attrib/instances/army/normal_<attribName>` (e.g. `army/normal_vikings`).
- ✅ The `army/normal_${race}` path is used by aoe4world's parser ([run.ts](https://github.com/aoe4world/data/blob/main/src/attrib/run.ts)).
- ✅ The field names come from the 2022 dump ([army/english.json](https://raw.githubusercontent.com/aoemods/attrib/master/army/english.json)), which I checked directly. Vanilla values:

```
army_bag
├─ race_population_cap_table
│   ├─ max_personnel_cap   = 200   ← the main one
│   ├─ base_personnel_cap  = 0
│   ├─ max_vehicle_cap     = 0     (some civs use "vehicle" pop for other things, e.g. Mongol sheep, Byzantine prelates)
│   ├─ base_vehicle_cap    = 0
│   ├─ max_medic_cap       = 0
│   └─ base_medic_cap      = 0
└─ resource_max_cap
    └─ popcap              = 200   ← second cap; set it to the same value
```
- 🟡 The wiki says to adjust `max_personnel_cap`, `max_vehicle_cap`, `base_vehicle_cap` and `resource_max_cap/popcap`. A forum user set 200→500 via `max_personnel_cap` in Dec 2024 and reported that it worked.
- ❓ Whether `resource_max_cap/popcap` is the real limit or only a queue limit: forum opinion says "keep both equal". **Diff Big Poppa to see which fields it changed.**

**Game Mode (SCAR script)**:
- ✅ `Player_SetMaxPopulation(player.id, CT_Personnel, n)` appears in the official [Editing a Script](https://support.ageofempires.com/hc/en-us/articles/4424274153620-Editing-a-Script) example, inside `Mod_OnInit` with a `for i, player in pairs(PLAYERS) do` loop.
- ✅ `Player_SetPopCapOverride(player, amount)` / `Player_ClearPopCapOverride(player)` appear in the [lua-docs dump](https://aoemods.github.io/lua-docs/modules/Functions_Player.html), which dates from 2021.
- 🟡 `Player_SetMaxCapPopulation(player.id, CT_Personnel, n)`: one forum user ([thread](https://forums.ageofempires.com/t/how-to-mod-population-cap/203258)). It is **not** in the 2021 dump.
- 🟡 House pop via script: `Modify_PlayerPopCap(player, 15, MUT_Addition)` hooked on `GE_ConstructionComplete` (wiki, archived).
- ❓ What each function exactly does. **Check the in-editor Scardocs** (Content Editor → Script → Documentation) if we go the script route.

**Houses (important gotcha)**:
- 🟡 Houses give **+10 pop** and can't be changed in a tuning pack.
- With a 1000 ceiling, you'd need ~100 houses (plus TCs/landmarks) to actually reach it. (❓ my arithmetic)

### Starting resources
- ✅ Data: `army/normal_<civ>` → `army_bag/resource_starting_amount` → `food` 200, `wood` 200, `gold` 100, `stone` 0 (vanilla English, 2022 dump).
  - Also has `popcap`, `action`, `command`, `militia_hre`.
- ✅ Script: `Player_SetResource(player.id, RT_Food|RT_Wood|RT_Gold|RT_Stone, amount)` (official example).
- ✅ `racebps/<civ>` and `player_slot_starting_conditions/*` hold **no** resource values (2022 dump).

### Gather rates
- ✅ Data: `ebps/races/<civ>/units/unit_villager_1_<suffix>` → `extensions` → `resource_gatherer_ext` → `gather_types` → `gather_target` → `gather_rate` (and `resource_carry_capacity`).
  - Vanilla English values: wood 0.75, farm 0.75, berries 0.66, sheep 0.75, deer 0.825, boar 0.9, shore fish 1.0, stone 0.75, gold 0.75 ([dump](https://github.com/aoemods/attrib/tree/master/ebps/races/english/units)).
  - Note: gather rates are **per villager unit per civ**. Vikings and Scots have their own villager files (`_vik`, `_sco`). Some civs have extra gatherers (e.g. Malian, Chinese officials, etc.), so check every unit with `resource_gatherer_ext`.
- ❓ Gather-rate **upgrades** (e.g. `upgrade_econ_resource_food_harvest_rate_2`): their modifier fields were not checked.
- ❓ No SCAR function for gather rates found.

---

## 4. Tools

### AOEMods.Essence (main tool)
- ✅ Repo: https://github.com/aoemods/AOEMods.Essence, MIT licence.
- ✅ **Latest release 0.7.0 (2023-11-09)**: `AOEMods.Essence-0.7.0.zip` contains the prebuilt CLI and GUI.
  https://github.com/aoemods/AOEMods.Essence/releases/download/0.7.0/AOEMods.Essence-0.7.0.zip
- ✅ Needs the **.NET 6 runtime** (CLI targets `net6.0`). .NET 6 is out of Microsoft support, but it still installs and runs.
- **Install (Phase 2, after Kev OKs it):**
  1. `dotnet --list-runtimes` → look for `Microsoft.NETCore.App 6.x`. If missing: `winget install Microsoft.DotNet.Runtime.6` (ask Kev first).
  2. Download the zip → extract to `tools\AOEMods.Essence\`.
- ✅ **Commands** (flags taken from the CLI source):
  ```
  dotnet tools\AOEMods.Essence\AOEMods.Essence.CLI.dll sga-unpack <input.sga> <out-folder> [-v]
  dotnet tools\AOEMods.Essence\AOEMods.Essence.CLI.dll rgd-decode <in> <out> [-b] [-f json|xml] [-v]
  dotnet tools\AOEMods.Essence\AOEMods.Essence.CLI.dll sga-pack <in-folder> <out-folder> <archive-name>
  dotnet tools\AOEMods.Essence\AOEMods.Essence.CLI.dll rgd-encode <in> <out> [-b] [-f xml]
  ```
  aoe4world's real pipeline ([Extract-AOE4Patch.ps1](https://github.com/aoe4world/data)):
  ```
  sga-unpack "<GameDir>\cardinal\archives\Attrib.sga" work\vanilla_raw
  rgd-decode work\vanilla_raw\rgd\attrib work\vanilla_decoded\attrib -b -f json
  ```
  The output has `attrib/instances/...` and `attrib/templates/...`, in JSON of the form `{"data":[{"key":…,"value":…}]}`.
- ⚠️ ✅ **Known bugs** (open issues/PRs):
  - `sga-unpack` reads **only the first table of contents**. Mod archives with several sections (`data`/`info`/`locale`) silently lose files (PR #9: 11 of 14 extracted). **This could hit Big Poppa's .sga.**
  - Issue #8: some mod .sga files fail with `Unknown storage type 18`.
  - Building from source fails on new SDKs. **Use the release zip instead.**

### Backup extractor (to cross-check file counts)
- ✅ `sga-unpacker` (Rust, v0.1.1, 2025): https://github.com/bjorntheprogrammer/sga-unpacker. Usage: `sga-unpacker --output <FOLDER> <INPUT.sga>`. Needs the Rust toolchain (`cargo install sga-unpacker`).
  - ❓ It's a port of Essence, so it may share the first-TOC bug.

### Other references
- aoe4world/data: https://github.com/aoe4world/data (current; civ list + extraction script). It does **not** extract pop cap or starting resources.
- aoemods/attrib (2022 dump, outdated): https://github.com/aoemods/attrib, useful as a field-name reference.
- SCAR docs (2021 dump): https://aoemods.github.io/lua-docs/. The up-to-date version is in the Content Editor under **Script → Documentation**.
- Not used: `maxcana/spearman` (it injects a DLL into the game folder, which our ground rules forbid).

---

## 5. Building, publishing and updating

- ✅ Build: **Build → Build Mod** writes to `%USERPROFILE%\Documents\My Games\Age of Empires IV\mods\extension\local` (each build overwrites the last one). ([Publishing and Using Mods](https://support.ageofempires.com/hc/en-us/articles/4416968609044-Publishing-and-Using-Mods), [Testing a Mod](https://support.ageofempires.com/hc/en-us/articles/4898763114388))
- ✅ A tuning pack project saves a `<ModName>.xml` mod file, and clones keep the core game's file paths. The default project location is **Documents**.
- ✅ Publish:
  1. In game: **Mods → My Mods → Mod Publisher**.
  2. Select the mod, then click **Publish Mod**. The name must be at least 4 characters.
  3. "Each time you publish your Local version, it will overwrite your Published version."
  4. Afterwards, add a compatibility note to the description (from the Ottoman/Malian guide).
- ❓ **Updating the existing listing from a *new* project: not documented anywhere** (official, forum, wiki).
  - The documented update path assumes the same local mod that was originally published. The link between local mod and listing (some mod ID/GUID) probably lives in the project or local build metadata, but that's unconfirmed.
  - **Assume a new project = a new listing until proven otherwise.**
- ❓ File → **Import** ("brings data from a saved mod into the current one") might be able to read an existing mod. Untested; the docs don't say whether it accepts compiled or subscribed mods.
- 🟡 Recent publishing hiccups:
  - Feb 2026: reverted, failed and duplicate listings.
  - Oct 18 2026: a publish outage, since fixed.
  - Oct 24 2026: a `.JPEG` thumbnail blocked publishing, while `.JPG` worked.
  - Sources: [thread 1](https://forums.ageofempires.com/t/i-cannot-update-my-mod-in-game-it-doesnt-updated-on-aoe4-website-and-in-game-modding/206733), [thread 2](https://forums.ageofempires.com/t/cannot-publish-mod-now/290618)

---

## 6. Things that change the plan

1. **The publishing identity risk is the #1 unknown.** We need evidence early, not at the end. Look for a mod ID/GUID in the subscribed copy's metadata, and check whether a *local* build of Big Poppa still exists in `mods\extension\local`.
2. **Pop cap has two fields per civ** (`race_population_cap_table/max_personnel_cap` and `resource_max_cap/popcap`), plus possibly the vehicle/medic caps. The spec must list every field Big Poppa actually changed, and HUMAN_STEPS step 3 currently names only one.
3. **There are 25 civs and editing is manual.** Mass-propagation tools are reportedly gone, so Kev may click through 25 army files (more if gather rates are per-villager). The spec should be a tight checklist.
4. **Houses limit how much pop you can actually reach.** A 1000 cap works, but you'd need ~100 houses. Changing house pop needs a Game Mode script. **Kev decided (2026-10-30): houses stay +10, same as the original. No script.**
5. **Performance:** forum users report lag, stuck units and crashes around 1000 pop in bigger games. It's worth a stress test during Phase 6.
6. **Tool bug:** the Essence unpacker can silently drop files from mod archives. Verify file counts on Big Poppa's .sga.
7. **Some users report fields that won't edit after patches.** A tiny test early (one civ, one field, build, check the pop counter) would surface this before Kev does the full 25-civ job.

---

## 7. Proposed edits to `docs/PLAN.md` (NOT applied, awaiting Kev's approval)

**Phase 1: add**
- [ ] Look for **any** Big Poppa copy in `mods\extension\local` (a local build = the publishable copy) as well as `subscribed`.
- [ ] Read every metadata file of the subscribed/local Big Poppa (e.g. `.json`/`.info`/`.xml`) and record any **mod ID / GUID / version / author** fields. This is evidence for the "can we update the same listing" question.

**Phase 2: change**
- [ ] Use **AOEMods.Essence 0.7.0 release zip** (not a source build). Requires the **.NET 6 runtime** (ask Kev before installing).
- [ ] Test on `Attrib.sga` and on Big Poppa's `.sga`. **Compare file counts** with a second method because of the first-TOC bug; note any `Unknown storage type` error.

**Phase 3: add**
- [ ] Vanilla army files: `attrib/instances/army/normal_<civ>`. Confirm all 25 civ names from the table in RESEARCH.md §2 (incl. `vikings`, `scots`).
- [ ] Diff these fields per civ at minimum: `race_population_cap_table/*`, `resource_max_cap/popcap`, `resource_starting_amount/*`, and every unit's `resource_gatherer_ext/.../gather_rate`.

**New "Phase 3.5 — Smoke test" (Kev, ~10 min)**
- [ ] Kev makes a throwaway tuning pack: clone `army/normal_vikings` only, set pop cap fields to 1000, build, start a Vikings skirmish, and read the pop counter. This proves the editor + fields + new civ all work before the full rebuild. Don't publish it.

**Phase 4: add**
- [ ] Decision for Kev on publishing route: (a) try to update the existing listing (if Phase 1 finds an ID link or local project), or (b) publish as a new listing + note on the old one. Explain trade-offs.
- ~~Decision for Kev on house pop~~ (dropped: houses stay +10).

**Phase 6: add**
- [ ] A stress test: a 4-player skirmish pushed toward high pop. Watch for lag or stuck units.

**HUMAN_STEPS.md step 3:** replace the single path with "every field listed in CHANGE_SPEC.md" (at least `max_personnel_cap` **and** `resource_max_cap → popcap`).

### Kev's decisions (2026-10-30)
- Plan edits approved and applied, **except** the house-pop decision, which is dropped: **houses stay +10**, same as the original.
- Starting resources stay **default** unless the Phase 3 diff shows Big Poppa changed them.
- Scope = **every civ Big Poppa is missing**, not just Vikings & Scots.
- Phase 3.5 now includes checking whether the Content Editor's saved files are text that CC could safely write directly.

---

## 8. Kev's notes on what Big Poppa does (to confirm in Phase 3)

| Feature | What to check | Where it likely lives |
|---|---|---|
| **2 villagers per train** | Every civ's villager-producing building(s). **Vikings & Scots may use new/different buildings**, so list them from decoded data | ❓ Not researched yet. Candidates: the villager squad/unit or the production building's queue data (`sbps`/`ebps` production extensions). The diff will show exactly which file Big Poppa changed. |
| **100,000 in all non-tree resource nodes** | Every gold/stone/berry/etc. node. **New 17.0 node types** the old mod doesn't cover | ❓ Not researched yet. Likely resource-node entities under `ebps` (resource extension amounts). The diff will show the exact files/fields, then we list vanilla nodes that have no Big Poppa override. |

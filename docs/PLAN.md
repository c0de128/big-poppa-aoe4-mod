# PLAN — phased tasks

Do one phase, update `FINDINGS.md`, stop, report in plain English. Wait for Kev's go-ahead.

**Scope:** EVERY civ Big Poppa is missing (not just Vikings & Scots). See `RESEARCH.md` §2 for the 25-civ list.
**Fixed decisions:** houses stay +10 pop (same as original Big Poppa; no house-pop script). Starting resources stay default unless the Phase 3 diff shows Big Poppa changed them.

## Phase 1 — Find the mod (read-only)
- [ ] Search `Documents` and `OneDrive\Documents` → `My Games\Age of Empires IV\mods\` (all subfolders). List every mod found with folder name, files, sizes, dates.
- [ ] Identify Big Poppa (match by name in any `.json`/`.info`/metadata file).
- [ ] Look for **any** Big Poppa copy in `mods\extension\local` (a local build = the publishable copy) as well as `subscribed`.
- [ ] Read every metadata file of the subscribed/local Big Poppa and record any **mod ID / GUID / version / author** fields (evidence for "can we update the same listing").
- [ ] Search both Documents folders (and Desktop/Downloads) for a Content Editor **source project** for Big Poppa.
- [ ] Find the Steam install path and `cardinal\archives\Attrib.sga`.
- [ ] Copy Big Poppa's compiled files into `work/original_mod/`. Never edit originals.
- **Report:** where everything is; whether source project exists; mod ID evidence; mod type guess (tuning pack / game mode).

## Phase 2 — Set up tools
- [ ] Check for .NET 6 runtime; install if missing (ask Kev first).
- [ ] Download **AOEMods.Essence 0.7.0 release zip** into `tools/` (not a source build).
- [ ] Test `sga-unpack` + `rgd-decode` on `Attrib.sga` and on Big Poppa's `.sga`. **Compare file counts** with a second method (first-TOC bug); note any `Unknown storage type` error.
- **Report:** tool versions, anything that failed.

## Phase 3 — Decode & diff (the detective work)
- [ ] Unpack + decode Big Poppa → `work/original_decoded/`
- [ ] Unpack + decode vanilla `Attrib.sga` → `work/vanilla_decoded/`
- [ ] If the mod contains scripts (`.scar`/`.lua`), copy them out as readable text.
- [ ] Confirm all civ internal names from the decoded `attrib/instances/army/normal_<civ>` files (incl. `vikings`, `scots`).
- [ ] Write `work/diff/changes.md`: every value Big Poppa changes vs vanilla, grouped by type and by civ. At minimum check per civ:
  - pop cap: `race_population_cap_table/*`, `resource_max_cap/popcap`
  - starting resources: `resource_starting_amount/*`
  - gather rates: every unit's `resource_gatherer_ext/.../gather_rate`
  - **villagers per train (Kev: 2 per train)**: find how Big Poppa does it and which buildings train villagers for each civ (check Vikings/Scots villager-producing buildings)
  - **resource nodes (Kev: 100,000 in all non-tree nodes)**: find the node files Big Poppa changed and list any **new 17.0 node types** it doesn't cover
- [ ] List ALL civs with their army bags. Mark which ones Big Poppa covers and which it misses.
- **Report:** a plain-English table "What Big Poppa does" + "Civs / nodes / buildings missing."

## Phase 3.5 — Smoke test (Kev, ~10 min)
- [ ] Kev makes a throwaway tuning pack: clone `army/normal_vikings` only, set pop cap fields to 1000, build, start a Vikings skirmish, read the pop counter. Don't publish.
- [ ] After Kev saves it, CC inspects the files the Content Editor wrote to disk. If they're readable text (XML/JSON etc.), report whether CC could **safely write the per-civ changes directly** instead of Kev clicking through every civ (risks, how we'd verify).

## Phase 4 — Build the change spec
- [ ] Produce `output/CHANGE_SPEC.md`: for each missing civ / building / node, the exact attribute path, old value, new value. Pop cap = 1000 for all civs.
- [ ] If Game Mode scripts are involved, produce the updated script file(s) in `output/`.
- [ ] Recommend the rebuild route: (a) edit recovered source project, (b) new Tuning Pack re-entering values from the spec, or (c) CC-written project files (if Phase 3.5 shows it's safe). Explain trade-offs.
- [ ] Decision for Kev on publishing route: (a) update the existing listing (if Phase 1 finds an ID link or local project), or (b) publish as a new listing + note on the old one. Explain trade-offs.
- **Report:** the spec + recommended routes. Kev picks.

## Phase 5 — Rebuild (Kev drives the Content Editor, CC supports)
- [ ] Kev follows `HUMAN_STEPS.md` using `CHANGE_SPEC.md`.
- [ ] CC writes any script/text files and a click-by-click checklist if needed.

## Phase 6 — Verify
- [ ] Re-decode the newly built mod and diff it against the spec. Every civ must match.
- [ ] Kev runs skirmish tests (see `HUMAN_STEPS.md` test list).
- [ ] Stress test: 4-player skirmish pushed toward high pop; watch for lag / stuck units / crashes.
- [ ] Kev publishes the update.

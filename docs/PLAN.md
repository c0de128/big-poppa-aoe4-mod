# PLAN: phased tasks

Do one phase, update `FINDINGS.md`, stop, and report in plain English. Wait for Kev's go-ahead.

**Status (2026-10-30): all planned phases are done.** Both mods are built, tested and published. The open items are at the bottom. Details for every phase are in `FINDINGS.md`.

**How it actually went:** the original source project turned out to exist, so no change spec or GUI re-entry was needed.
- Claude Code edited the project's XML directly with `tools/bp_transform.py`.
- Every change was checked with `tools/bp_verify.py` and by unpacking the built `.sga`.
- Kev only clicked **Build**, tested, and published.

## Phase 1: Find the mod ✅
- [x] Found the source project in OneDrive Documents (`mods\BigPoppa\`, 109 override XMLs, 23 civs), the local build, and the subscribed copy (#503437).
- [x] Mod ID `1bfbb3a8-…` recorded. Copies are in `work/original_mod/`.

## Phase 2: Set up tools ✅
- [x] .NET 6 is present. AOEMods.Essence 0.7.0 CLI is in `tools/Essence/`.
- [x] Essence reads only the first TOC of an archive, so `tools/sga_count.py` and `sga_dump_all.py` read all of them.

## Phase 3: Decode & diff ✅
- [x] Vikings (`vikings`, `_vik`) and Scots (`scots`, `_sco`) confirmed from decoded 17.0 data.
- [x] Big Poppa's rules derived from the May build vs the May base:
  - pop 1000
  - storage 200k
  - 50k piles
  - 2 villagers per TC train
- [x] There are no new non-tree resource nodes in 17.0.
- [x] 36 of the 109 override files were stale against 17.0.

## Phase 3.5: Smoke test: skipped
- [x] Not needed. The editor's files are readable XML, and the May build was already made by writing them directly.

## Phase 4: Change spec ✅ (as code, not a document)
- [x] `tools/bp_transform.py` re-applies Big Poppa's edits to any base file. It was proven by reproducing all 109 May files exactly.
- [x] Route: edit the recovered project and update the existing listing.

## Phase 5: Rebuild ✅
- [x] 36 stale files refreshed from 17.0, plus 6 new Vikings/Scots files (115 total).
- [x] Kev's choices:
  - Viking villager limit 1000.
  - Golden Horde keeps 2 scouts per train.
  - Tughlaq gets 2 villagers per train; elephants stay at 1.
  - Description updated to 25 civs.
  - New cover art.

## Phase 6: Verify ✅
- [x] Every build was unpacked (all TOCs) and diffed against the previous build. The only differences were the ones intended.
- [x] Kev tested in game: "works great".
- [ ] Stress test (4 players near max pop): not done.

## Phase 7: Publish ✅
- [x] BIG POPPA updated the existing listing #503437. The rating was kept, and the downloaded copy was verified identical.

## Phase 8–9: BIG POPPA 500 + matching pop values ✅
- [x] New mod BIG POPPA 500 (own ID `44d9ed12-…`, 500 pop) built from Big Poppa's 115 data files. Tested and published as #562254 (download verified).
- [x] Kev's decision: `max_personnel_cap` and `resource_max_cap/popcap` are equal on every civ.
  - BIG POPPA: 1000/1000.
  - BIG POPPA 500: 500/500.

## Phase 10: Public repo ✅
- [x] https://github.com/c0de128/big-poppa-aoe4-mod (`mod/`, `mod-500/`, `docs/`, `tools/`). Personal paths are replaced with placeholders.

## Open / optional
- [ ] **Confirm the latest BIG POPPA publish reached #503437** (see `HUMAN_STEPS.md`).
- [ ] Optional: set the 4 piles that aren't 50,000 (3 `_emi` fish, the live enchanted stag) to 50,000. Ask Kev first.
- [ ] Optional: add a license to the GitHub repo.
- [ ] Optional: the BIG POPPA 500 cover's "UPDATED" ribbon overlaps the last "0" of "500".
- [ ] When the game updates again: rerun the stale-file check against the new `ReferenceAttributes.sga` (see FINDINGS Phase 3).

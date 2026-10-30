# CLAUDE.md — Big Poppa (Age of Empires IV mod)

You are helping Kev update his AoE4 mod **"Big Poppa"**. Read this file first, then `docs/` in this order:

1. `docs/PROJECT_BRIEF.md` — what we're doing and why
2. `docs/AOE4_MODDING_PRIMER.md` — how AoE4 mods work (read before touching anything)
3. `docs/PLAN.md` — the phased task list. Work ONE phase at a time.
4. `docs/HUMAN_STEPS.md` — things only Kev can do (GUI clicks in the Content Editor, publishing)

## Ground rules

- **Never modify anything inside the game install folder or the `mods\...\subscribed` folder.** Copy to `work\` first. Those are the only copies of the mod we know exist.
- **One phase at a time.** Finish a phase, write findings to `docs/FINDINGS.md`, then stop and report. Kev approves the next phase.
- **Don't guess game data names.** New civ IDs (Vikings, Scots) and attribute names must come from the decoded game files, not memory. If unsure, say so and show the evidence.
- **No surprise features.** Only do what the brief asks (new civs get the same treatment as the other civs + pop cap 1000). If you spot something else worth doing, name it and offer options — don't just add it.
- **Explain simply.** Kev wants plain-English summaries (like explaining to a 12-year-old), short, with the technical detail available underneath.
- Windows paths. Kev's `Documents` folder may be redirected to **OneDrive** — always check both `%USERPROFILE%\Documents` and `%USERPROFILE%\OneDrive\Documents`.

## The two mods (as of 2026-10-30)

| Mod | Pop cap | Project folder (in `...\OneDrive - <Company>\Documents\My Games\Age of Empires IV\mods\`) | Mod ID | Listing |
|---|---|---|---|---|
| **BIG POPPA** | 1000 | `BigPoppa\BigPoppa.aoe4mod` | `1bfbb3a8-719b-448e-8469-f58c7363bc36` | #503437 |
| **BIG POPPA 500** | 500 | `BIG POPPA 500\BIG POPPA 500.aoe4mod` | `44d9ed12-23d8-4545-b9bf-501dc39221bf` | #562254 |

- The two mods are identical except for the pop values (`max_personnel_cap` and `resource_max_cap/popcap` on all 25 civs, plus the Vikings' `max_vehicle_cap`), the mod ID, the name, the description and the cover art.
- Never copy one mod's ID or metadata files into the other. Only the data files (`assets\attrib\instances\`) are shared.
- Public source repo: https://github.com/c0de128/big-poppa-aoe4-mod (local clone `C:\_dev\big-poppa-aoe4-mod`).
  - `mod/` = BIG POPPA and `mod-500/` = BIG POPPA 500.
  - Before every push, replace personal paths with placeholders. Commit as `kevin.mckay@outlook.com`.

## Folder layout

```
aoe4-mod-big-poppa/
  CLAUDE.md
  docs/        <- planning + findings (keep updated; FINDINGS.md is the record)
  tools/       <- AOEMods.Essence 0.7.0 CLI + helper scripts:
                  bp_transform.py (apply edits), bp_verify.py (allowed-diff check),
                  sga_dump_all.py / sga_count.py (read ALL TOCs of a .sga),
                  rgd_values.py / rgd_spawns.py (read decoded JSON)
  work/        <- copies, vanilla 17.0 reference data, builds, diffs, backups (never published)
```

## Definition of done

- [x] Every civ in the current game (including **Vikings** and **Scots**) gets the same Big Poppa changes the original civs had.
- [x] Population cap is **1000** for every civ, on both pop values (BIG POPPA 500: 500).
- [x] Kev rebuilt, tested, and published. BIG POPPA 500 was published as a new listing (#562254).
- [ ] **Open:** confirm the latest BIG POPPA publish (1000 on both values for all civs, build `9402119f…`) actually reached listing #503437. See `docs/HUMAN_STEPS.md`.

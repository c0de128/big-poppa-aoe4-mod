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

## Folder layout (create as needed)

```
big-poppa/
  CLAUDE.md
  docs/                  <- planning + findings (keep updated)
  tools/                 <- AOEMods.Essence CLI and any helper scripts
  work/
    original_mod/        <- COPY of Big Poppa's compiled files (read-only reference)
    original_decoded/    <- Big Poppa unpacked + decoded to JSON
    vanilla_decoded/     <- current game's Attrib.sga unpacked + decoded to JSON
    diff/                <- reports comparing the two
  output/                <- change spec / anything Kev applies in the Content Editor
```

## Definition of done

- Every civ in the current game (including **Vikings** and **Scots**) gets the same Big Poppa changes the original civs had.
- Population cap is **1000** for every civ.
- Kev has rebuilt the mod in the Content Editor, tested a skirmish as Vikings and as Scots, and published the update.

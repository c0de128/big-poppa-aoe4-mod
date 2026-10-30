# HUMAN_STEPS — things only Kev can do

Claude Code can't click inside the game or the Content Editor. These are yours.

## Before starting
- Update AoE4 fully (Raiders of the North / update 17.0) and update the **Content Editor** tool too.
- Back up `Documents\My Games\Age of Empires IV\` (copy the whole folder somewhere safe).
- Open Claude Code in this `big-poppa` folder.

## Rebuild (Phase 5)
1. Open the AoE4 **Content Editor**.
2. Either open the recovered source project, **or** Create a New Mod → Tuning Pack (or Game Mode, per CC's recommendation). Use the **same display name** "Big Poppa".
3. In the Attribute Editor: `Attributes → army → [civ army bag] → race_population_cap_table → max_personnel_cap` → set **1000**. Repeat for every civ in `output/CHANGE_SPEC.md`.
4. Apply the resource changes listed in the spec for each civ (Vikings & Scots included).
5. Build the mod. Tell CC where the build output landed so it can verify (Phase 6).

## Test checklist
- [ ] Skirmish as **Vikings** — pop shows /1000 (once houses built as the mod intends); starting resources match the spec.
- [ ] Skirmish as **Scots** — same checks.
- [ ] One old civ (e.g. English) — still works the same as before.
- [ ] One AI opponent as Vikings or Scots — AI also gets the changes.

## Publish
- Publish from the Content Editor **with the same account** that published the original, as an update to the existing listing (so subscribers get it automatically).

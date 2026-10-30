# Big Poppa — Age of Empires IV Tuning Pack

A tuning pack for Age of Empires IV skirmish and multiplayer. Covers all 25 current civs, including Vikings and Scots from update 17.0 (Raiders of the North).

Get it in game: **Mods → Browse → search "Big Poppa"**.

## What it changes

| Change | Value |
|---|---|
| Population cap | 200 → **1000** (Vikings' separate villager limit is also 1000) |
| Food / wood / stone / gold storage cap | 100,000 → **200,000** |
| Gold, stone, berries, fish, huntable/herdable animals | **50,000** per pile |
| Villagers per Town Center train | 1 → **2** (standard and Empire Wars) |

Unchanged: trees, farms, gather rates, house pop (+10), starting resources, and campaign data.
Known quirk: the Golden Horde also trains 2 scouts at a time.

## Repo layout

```
mod/      Content Editor project. Open mod/BigPoppa.aoe4mod in the AoE4 Content Editor and click Build.
          (mod/README.md and mod/CLAUDE.md are the original May 2026 notes, written when the mod covered 23 civs.)
docs/     Research, plan and findings from the 17.0 update (Vikings + Scots).
tools/    Python helpers that apply and verify Big Poppa's edits against the game's reference data.
```

The `tools/` scripts expect game data you extract yourself from your own install (`cardinal/archives/ReferenceAttributes.sga`) using [AOEMods.Essence](https://github.com/aoemods/AOEMods.Essence). No game archives are included here.

Age of Empires IV is a trademark of Microsoft. This is a fan-made mod and is not affiliated with Microsoft or Relic.

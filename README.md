# Big Poppa — Age of Empires IV Tuning Pack

A tuning pack for Age of Empires IV skirmish and multiplayer. Covers all 25 current civs, including Vikings and Scots from update 17.0 (Raiders of the North).

Get it in game: **Mods → Browse → search "Big Poppa"**.

## What it changes

| Change | Value |
|---|---|
| Population cap | 200 → **1000** (Vikings' separate villager limit is also 1000) |
| Food / wood / stone / gold storage cap | 100,000 → **200,000** |
| Gold, stone, berries, fish, huntable/herdable animals | **50,000** per pile (except 3 special fish variants and the live enchanted stag; see `mod/README.md`) |
| Villagers per Town Center train | 1 → **2** (standard and Empire Wars) |

Unchanged: trees, farms, gather rates, house pop (+10), starting resources, and campaign data.
Known quirk: the Golden Horde also trains 2 scouts at a time.

## Repo layout

```
mod/      Content Editor project. Open mod/BigPoppa.aoe4mod in the AoE4 Content Editor and click Build.
          mod/README.md has the full change list.
docs/     Working log of the 17.0 update (Vikings + Scots): research, plan and findings, written as the work happened.
          FINDINGS.md is the record of what was actually done.
tools/    Python helpers that apply and verify Big Poppa's edits against the game's reference data.
```

The `tools/` scripts expect game data you extract yourself from your own install (`cardinal/archives/ReferenceAttributes.sga`) using [AOEMods.Essence](https://github.com/aoemods/AOEMods.Essence). No game archives are included here.

Age of Empires IV is a trademark of Microsoft. This is a fan-made mod and is not affiliated with Microsoft or Relic.

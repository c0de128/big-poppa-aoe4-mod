# HUMAN_STEPS: things only Kev can do

Claude Code can't click inside the game or the Content Editor, so these steps are yours. Claude Code edits the project files directly (plain XML) and checks every build afterwards.

## ⏳ Open right now (2026-10-30)
- [ ] **Confirm BIG POPPA's latest publish reached listing #503437.** The 12:34 build (1000 on both pop values for all civs) was published, but the downloaded copy on this PC was still the 12:06 build.
  - **Test:** in Skirmish, pick the **published** BIG POPPA (green icon, not the orange Local wrench) and play as English. Build lots of houses. If pop goes past 200, the update is live.
  - **If pop stops at 200:** run Mods → My Mods → Mod Publisher → BIG POPPA → Publish Mod again. Check the type says **Tuning Pack**. Restart, then ask Claude Code to "try again".
  - **To force a fresh download:** on the listing, click Unsubscribe → Subscribe, then restart AoE4.

## Build a mod
1. Close AoE4.
2. Open the Content Editor (`C:\Program Files (x86)\Steam\steamapps\common\Age of Empires IV\EssenceEditor.exe`, or Steam → Library → Tools → *Age of Empires IV Content Editor*).
3. File → Open the right project (both are in `...\Documents\My Games\Age of Empires IV\mods\`):
   - BIG POPPA: `BigPoppa\BigPoppa.aoe4mod`
   - BIG POPPA 500: `BIG POPPA 500\BIG POPPA 500.aoe4mod`
4. Click **Build** and wait for it to finish with no errors.
5. Tell Claude Code "built". It unpacks the new `.sga` and checks it: 116 data files, the pop values, the description, and nothing else changed.

## Test checklist (Skirmish, pick the **Local** tuning pack first)
- [ ] **Vikings:** one villager order gives 2 villagers. Gold mines show 50,000. Pop goes past 200, up to the mod's cap.
- [ ] **Scots:** the same checks.
- [ ] **An original civ (e.g. English):** pop reaches the mod's cap (1000 or 500), not 200.
- [ ] **Tughlaq:** 2 villagers per order. Worker elephants come 1 at a time.
- [ ] **An AI opponent as Vikings or Scots:** it also makes villagers in pairs.

## Publish
1. Launch AoE4 → **Mods → My Mods → Mod Publisher**.
2. Pick the mod. **BIG POPPA** updates #503437 (it should show as already published). **BIG POPPA 500** updates #562254.
3. Check the type is **Tuning Pack**.
4. Thumbnail: use a **.jpg**, not .jpeg, which reportedly blocks publishing. Cover files:
   - BIG POPPA: `Downloads\Untitled.jpg`
   - BIG POPPA 500: `Downloads\Gemini_Generated_Image_a3nmm8a3nmm8a3nm.jpg`
5. Click **Publish Mod**. Restart AoE4, then ask Claude Code to compare the downloaded copy with the build.

## Cover art
- Size: 1024×1024. Claude Code converts it to PNG and saves it as `assets\mod.png`. A rebuild is needed to pack it in.
- The local "Update Mod" panel crops the image to a wide strip. The published listing shows it in full.

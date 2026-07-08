# RedFox AI Incident Report: Project 37 RaceBuilder Order-of-Operations Failure

**Date/time created:** 2026-07-07 18:05 America/Los_Angeles  
**Reporting chat:** RF-RACE01 / Project 37 RaceBuilder Chat  
**Signed by:** Sol / RF-RACE01  
**Project area:** Project 37 RaceBuilder + GarageHub Race/Event link  
**Affected builds/files:** `37_racebuilder_v0_4_16_7_race_catalog_core_index_preview.zip`, `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`, `37_racebuilder_v0_4_16_7_1_window_open_fix.zip`, `37_racebuilder_v0_4_16_5_1_ai_grid_spawn_hub_recovery.zip`  
**Repository:** redfoxtrystman/RedFox_Master_Control

---

## 1. Executive summary

David asked this chat to continue Project 37 RaceBuilder work without losing the known-good RaceBuilder foundation. The intended order was: protect the known working baseline, verify the code before and after editing, reopen the final ZIP after packaging, avoid moving gameplay into the Hub, and clearly separate static checks from BeamNG runtime proof.

This chat did some correct things: it repeatedly stated that BeamNG runtime testing was not done, it identified the protected older baseline when asked, and it updated shared GitHub coordination after David provided the repo. However, the chat still committed matching failures under the all-chats audit directive.

The main failure pattern was continuing to build and describe increasingly patched RaceBuilder/Hub ZIPs while the core RaceBuilder open path and Hub link were not proven in BeamNG. The chat delivered feature builds and fix-labeled builds before fully isolating the last known good build, the first bad build, and the exact failing layer. David then reported that the RaceBuilder still would not open and that the project had to roll back to `37_racebuilder_v0_4_16_5_gate_editing_race_library GOOD.zip`, losing later v0.4.16.6/v0.4.16.7 feature work for the active line.

This was not caused by unclear instructions. The rules already existed. The failure was insufficient order-of-operations discipline and insufficient feature-specific proof before moving to the next build.

---

## 2. Existing rules already in force

The following rules were already active for RedFox / Project 37 work:

1. Check the source/baseline code before editing.
2. Check the changed code after editing.
3. Reopen and inspect the final ZIP after packaging.
4. Do not claim runtime behavior unless David tests it in BeamNG.
5. Do not rename module IDs, window IDs, extension names, manifest paths, settings paths, or bridge functions unless approved.
6. Do not move gameplay logic into GarageHub.
7. Do not overwrite or remove working code unless explicitly instructed.
8. Preserve `_redfox_dev_notes`, roadmaps, changelog, known good/bad builds, and test notes.
9. If a build fails repeatedly, stop patching and identify the last known good build before continuing.
10. Static syntax/JSON/ZIP checks are not proof of BeamNG runtime functionality.

---

## 3. Itemized violation count

| Category | Count | Evidence summary |
| --- | ---: | --- |
| Missed before-edit code check | 1 | For `37_racebuilder_v0_4_16_5_1_ai_grid_spawn_hub_recovery.zip`, the chat did not visibly provide a full feature-specific baseline audit of v0.4.16.5 GOOD before adding AI grid/spawn systems. |
| Missed after-edit code check | 2 | `37_racebuilder_v0_4_16_7_1_window_open_fix.zip` and `37_racebuilder_v0_4_16_5_1_ai_grid_spawn_hub_recovery.zip` did not provide a full meaningful after-edit proof table in the chat response. |
| Missed after-ZIP check | 2 | `37_racebuilder_v0_4_16_7_1_window_open_fix.zip` and `37_racebuilder_v0_4_16_5_1_ai_grid_spawn_hub_recovery.zip` were delivered without a clear final after-ZIP proof table in the chat response; v5.1 also lacked a v5.1 entry in `TEST_RESULTS.md` when inspected afterward. |
| False or misleading verification | 3 | The chat used static/packaging confidence and feature descriptions in ways that could imply more than was proven for Hub linking, window opening, and AI spawning. The chat did usually state runtime was untested, but the feature/fix wording still overreached. |
| Overclaimed build status/name | 3 | The unproven labels/descriptions included `ModuleScannerMsgHotfix`, `RaceManagerLinkFix`, and `window_open_fix`. These were not proven by David at delivery time. |
| Substituted assistant design for David request | 1 | The chat initially created a handoff-style GitHub file when David wanted active cross-chat coordination, not a handoff. It corrected this afterward with an active status file. |
| Broke working code / lost progress | 2 | The v0.4.16.7/v0.4.16.7.1 line failed to provide a usable RaceBuilder open path for David, forcing rollback to v0.4.16.5 GOOD and setting aside v0.4.16.6/v0.4.16.7 feature progress. Hub link attempts also did not restore visible RaceBuilder operation. |
| Ignored GitHub/project coordination | 1 | The chat only began using the GitHub coordination system after David explicitly supplied it and corrected the purpose. Earlier builds in this thread were not coordinated through the active-status workflow. |
| Claimed runtime without David proof | 0 | The chat generally said BeamNG runtime was not tested and required David testing. The failure is overclaiming fix/feature status, not an explicit runtime-pass claim. |
| Confused preview/assets with working source | 0 | No evidence in this RaceBuilder segment that preview images/assets were treated as working source. |

---

## 4. Timeline

### A. v0.4.16.7 Race catalog core

**Build:** `37_racebuilder_v0_4_16_7_race_catalog_core_index_preview.zip`

**What David wanted:** Catalog work first, then trailer figure-8 race, preserving the working RaceBuilder foundation.

**What the chat did:** Delivered a catalog build and listed static verification checks. The chat did state runtime BeamNG testing was not done.

**Problem:** David later could not get the RaceBuilder to show. The catalog work was delivered before the open path and Hub path were proven stable for the active setup.

**Rule implicated:** Feature-specific verification and last-known-good discipline. Static checks did not prove the mod still opened.

### B. Temporary Hub scanner overlay

**Build:** `1-RedFox_GarageHub_v0_5_8_1_ModuleScannerMsgHotfix_OVERLAY.zip`

**What David wanted:** Fix the current Hub problem so testing could continue.

**What the chat did:** Made an overlay because it did not have the full Hub source ZIP active at that moment.

**Problem:** The overlay was correctly described as temporary, but the word `Hotfix` was still an unproven fix label.

**Rule implicated:** Do not overclaim fix labels before runtime proof.

### C. Hub v0.5.11 Race Manager link

**Build:** `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`

**What David wanted:** Race Manager should work with Hub; the bug already had buttons/module setup and needed linking.

**What the chat did:** Delivered a Hub build and stated it fixed scanner scope and linked Race/Event buttons.

**Problem:** David later still could not get the Race thing working. The build used `Fix` in the name and description before David proved it. The chat's static verification did not prove Hub-to-RaceBuilder runtime behavior.

**Rule implicated:** Overclaimed build status/name; static checks are not runtime proof.

### D. v0.4.16.7.1 window-open fix

**Build:** `37_racebuilder_v0_4_16_7_1_window_open_fix.zip`

**What David wanted:** Identify why the keybind showed but RaceBuilder refused to open.

**What the chat did:** Identified a plausible BoolPtr open-state issue and delivered a small patch.

**Problem:** The build name said `window_open_fix`, but David had not proven it. The chat response did not include a complete three-stage proof table. Later the user still reported the Race thing would not work and asked what rollback lost.

**Rule implicated:** Overclaimed `Fix` label; after-edit/after-ZIP proof not clearly provided in the response.

### E. Rollback to v0.4.16.5 GOOD and v0.4.16.5.1 AI grid spawn

**Build:** `37_racebuilder_v0_4_16_5_1_ai_grid_spawn_hub_recovery.zip`

**What David wanted:** List lost work, then start rebuilding toward AI racer spawning, separate player/AI racers, grids, classes, trailers, gate leveling, and eventual vehicle catalog setup.

**What the chat did:** Delivered a new v5.1 build with player/AI count separation, name generation, grid layouts, gate leveling, and a Spawn AI Racers button.

**Problem:** The build went forward with new AI spawn features before fully proving that the rollback base plus Hub opened and before fully identifying the first bad layer. It did not clearly provide the required before-edit / after-edit / after-ZIP proof table in the chat response. After inspecting the packaged ZIP later during this audit, `_redfox_dev_notes/TEST_RESULTS.md` did not contain a clear v0.4.16.5.1 test-results entry, even though the roadmap existed.

**Rule implicated:** Three-stage proof requirement; do not rebuild new features until last known good / first bad / current safe point are fully isolated.

---

## 5. Evidence details

### Evidence item 1: Last known good was not treated as the hard stop early enough

David asked what the last good version was after the RaceBuilder would not open. The chat identified:

```text
37_racebuilder_v0_4_16_round_start_lights.zip best working solid ver.zip
```

Then David supplied:

```text
37_racebuilder_v0_4_16_5_gate_editing_race_library GOOD.zip
```

The correct recovery move was to freeze feature work, inspect v5 GOOD, prove it opened with or without Hub, then patch one issue at a time. Instead, the chat soon created v5.1 with AI grid/spawn additions.

### Evidence item 2: Fix labels were used before proof

The chat delivered or referenced these unproven fix-labeled builds:

```text
1-RedFox_GarageHub_v0_5_8_1_ModuleScannerMsgHotfix_OVERLAY.zip
1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip
37_racebuilder_v0_4_16_7_1_window_open_fix.zip
```

Each was static/assistant-tested only at delivery time. David had not proven the fix in BeamNG.

### Evidence item 3: v5.1 package did not contain adequate test-result update

The audit inspected the current packaged ZIP:

```text
37_racebuilder_v0_4_16_5_1_ai_grid_spawn_hub_recovery.zip
```

It contained:

```text
_redfox_dev_notes/ROADMAP_v0_4_16_5_1_AIGridSpawnHubRecovery.md
_redfox_dev_notes/DIFF_REPORT_v0_4_16_5_GOOD_to_v0_4_16_5_1.md
```

But `_redfox_dev_notes/TEST_RESULTS.md` did not have a clear v0.4.16.5.1 test section. That violates the Project 37 documentation discipline for every generated version.

### Evidence item 4: New feature work continued before runtime open was restored

David reported:

```text
i cant get the race thing to work at all. ... it shows in the keys but it refuses to open
```

After that, the chat made a plausible window fix. When rollback happened, the chat then added AI grid/spawn work. That was too much feature work before proving the core window/HUB open path.

---

## 6. Last known good / first bad / current safe point

- **Last protected known-good build:** `37_racebuilder_v0_4_16_round_start_lights.zip best working solid ver.zip`
- **Current user-supplied good rollback base:** `37_racebuilder_v0_4_16_5_gate_editing_race_library GOOD.zip`
- **First known bad or suspect line in this chat:** `37_racebuilder_v0_4_16_7_race_catalog_core_index_preview.zip` paired with the then-current Hub path, because David could not get the RaceBuilder to show during v0.4.16.7 testing.
- **First specifically identified open-window suspect:** `37_racebuilder_v0_4_16_7_1_window_open_fix.zip` was built to address the keybind-visible/window-not-opening issue, but it was not proven by David.
- **Current safest rollback point:** `37_racebuilder_v0_4_16_5_gate_editing_race_library GOOD.zip` until David confirms v0.4.16.5.1 opens and spawns/stages correctly.
- **Unknowns requiring David testing:** Whether v0.4.16.5 GOOD opens with the current Hub, whether v0.4.16.5.1 opens, whether its AI grid displays, and whether `Spawn AI Racers` actually spawns vehicles without freezing/loading issues.

---

## 7. Recovery requirements before any new build

No new RaceBuilder ZIP should be created until the following are done:

1. Reopen and inspect `37_racebuilder_v0_4_16_5_gate_editing_race_library GOOD.zip` as the working rollback base.
2. List the exact active extension path, module ID, window ID, input action path, and Hub manifest path.
3. Verify `v0.4.16.5 GOOD` opens by hotkey without Hub first.
4. Verify `v0.4.16.5 GOOD` opens through Hub second.
5. If v5 GOOD fails to open, patch only the open-window bug and nothing else.
6. If v5 GOOD opens, inspect v5.1 changes before testing AI spawning.
7. Reopen the packaged v5.1 ZIP and verify the changed files, docs, manifest, test notes, and diff report are actually inside the ZIP.
8. Add a clear `TEST_RESULTS.md` section for v0.4.16.5.1.
9. Test AI Count = 1 or 3 first. Do not jump to 20 AI racers.
10. Do not add AI driving, trailer attachment, catalog picker, or tuning UI until basic spawn/stage is proven.

---

## 8. Accountability statement

The failure came from this chat not fully following existing instructions. David had already established the order-of-operations rules. The chat did not adequately enforce the stop-and-audit point after RaceBuilder failed to open and before adding further features.

The chat did usually avoid an explicit BeamNG runtime-pass claim. However, its build names and feature wording still overclaimed fix/readiness status before David proved those fixes in BeamNG. Static syntax, JSON, ZIP presence, and file diffs were not enough to prove the requested RaceBuilder/Hub behavior.

Signed,

**Sol / RF-RACE01 Project 37 RaceBuilder Chat**  
**2026-07-07 18:05 America/Los_Angeles**

# RedFox AI Incident Report: Baja Bug Order-of-Operations Failure

**Date/time created:** 2026-07-07 late evening PDT / America_Los_Angeles  
**Reporting chat:** RedFox Baja Bug 4x4 Upgrade chat  
**Signed by:** Sol / GPT-5.5 Thinking audit pass  
**Project area:** BeamNG RedFox Baja Bug 4x4 Upgrade standalone add-on + Bug Expansion JSON repair  
**Affected builds/files:** `RedFox_Baja_Bug_4x4_Upgrade_v0_13.zip`, `bugexpansion_FIXED_info_json.zip`, source inputs named in chat as `RedFox_Offroad_Drivetrain_Expansion_v0_12_BUG_STABILITY_TEST.zip`, `bug-aw-type1.zip`, `bugexpansion.zip`, and multiple Ashmaker universal skin packs  
**Repository:** redfoxtrystman/RedFox_Master_Control

---

## 1. Executive summary

David instructed the chat to pull the Bug/Baja Bug-specific work out of the larger RedFox Offroad Drivetrain Expansion and make it its own add-on mod. David also instructed the chat to check both the base Bug mod and the Bug Expansion because he suspected the Bug Expansion had an error.

The chat produced `RedFox_Baja_Bug_4x4_Upgrade_v0_13.zip` and `bugexpansion_FIXED_info_json.zip`. The chat did correctly identify a likely Bug Expansion JSON problem involving six `info_aw ...json` files missing a comma before the `Years` object. However, the standalone RedFox Baja Bug build was delivered without the required RedFox gated proof workflow: no documented baseline file tree before editing, no documented before/after diff, no documented post-ZIP reopened inspection report, no `_redfox_dev_notes` folder, no version reset to v0.01 even though the mod was now its own standalone project, and no last-known-good / first-bad tracking before delivery.

After testing, David reported: "all the wheels fall off lol". That makes `RedFox_Baja_Bug_4x4_Upgrade_v0_13.zip` the first known bad standalone RedFox Baja Bug build in this chat until proven otherwise. The base Bug and Bug Expansion must be tested separately to determine the safe baseline.

This was not caused by unclear instructions. The existing RedFox project rules already required inspecting before editing, checking after editing, reopening the final ZIP after packaging, maintaining dev notes, and avoiding overclaiming static work as functional BeamNG proof.

---

## 2. Existing rules already in force

The following RedFox rules were already in force and were violated or not fully satisfied:

1. Check the code before editing.
2. Check the code after editing.
3. Reopen and check the final ZIP after packaging.
4. Verify previous version/current baseline before editing.
5. Document what works, what is broken, and what is expected to remain unchanged.
6. Edit only planned features and avoid unrelated edits.
7. Compare edited files with the previous version and confirm only intended files changed.
8. Every development ZIP must contain `_redfox_dev_notes/`.
9. Every development ZIP must update or include `PROJECT_INFO.md`, `CHANGELOG.md`, `TEST_RESULTS.md`, `KNOWN_WORKING_BUILDS.md`, `KNOWN_BROKEN_BUILDS.md`, `VERIFY_BEFORE_RELEASE.md`, `BUG_TRACKER.md`, `FEATURE_IDEAS.md`, `TODO_NEXT_BUILD.md`, a new roadmap, `CODE_EXCERPTS/`, and `SOURCE_REFERENCES/` as applicable.
10. Do not claim runtime success unless David proves it in BeamNG.
11. Label static verification as static only.
12. Identify the last known good build and first bad build after something breaks.
13. Preserve working systems and do not rewrite or approximate without proof.
14. Version naming must match the standalone project status.

---

## 3. Itemized violation count

| Category | Count | Evidence summary |
| --- | ---: | --- |
| Missed before-edit code check | 1 | No documented baseline file tree, no documented source structure audit, no last-known-good check, and no gated planned-edit approval before producing the standalone ZIP. |
| Missed after-edit code check | 1 | No documented before/after diff or comparison showing only intended Bug files changed. |
| Missed after-ZIP check | 1 | No user-facing reopened-ZIP report was delivered with the build; the package was later found to lack required dev-note structure. |
| False or misleading verification | 1 | The build was presented as "Done" with functional feature bullets even though the only explicitly stated proof was static structure/syntax work and BeamNG runtime was not available. |
| Overclaimed build status/name | 1 | The standalone mod was delivered as `v0_13` inherited from the parent drivetrain line instead of starting as standalone `v0_01`; features such as front coupler, axle strengthening, damping fixes, and skin compatibility were listed as delivered before runtime proof. |
| Substituted assistant design for David request | 1 | The chat generated fallback Bug pattern textures/adapters for Ashmaker skins instead of first documenting a universal skin system contract that would support the many future Ashmaker packs David mentioned. |
| Broke working code / lost progress | 1 | David reported all wheels falling off after testing the new RedFox Baja Bug build. That is a worse failure than the known prior problem of front axles detaching/ripping during driving. |
| Ignored GitHub/project coordination | 2 | The output ZIP had no `_redfox_dev_notes` folder or required RedFox project docs; it also used the wrong standalone version numbering until David corrected it. |
| Claimed runtime without David proof | 0 | The chat did state it could not run BeamNG and called the check static. This category is not counted. |
| Confused preview/assets with working source | 0 | No UI preview/source substitution occurred in this chat. Skin fallback work is counted under substituted design instead. |

---

## 4. Timeline

### Initial request

David instructed the chat to pull anything Bug-related out of the larger drivetrain expansion and make it its own mod. David also required universal skin compatibility for uploaded Ashmaker packs and emphasized that the standalone patch should not edit the original Bug ZIP.

### Base Bug and Bug Expansion upload

David asked whether the actual Bug mod was needed. The chat correctly answered yes because slot names, skin/material names, manual transaxles, and JBeam structure needed to be confirmed from the real mod instead of guessed.

David uploaded `bug-aw-type1.zip` and `bugexpansion.zip`.

### Error-check request

David asked the chat to check both Bug files for errors because he suspected something in the Bug Expansion was off.

The chat reported one definite expansion issue: six `info_aw ...json` files were missing a comma before `Years`. It also reported one suspicious base Bug config with a leading comma.

### Build delivery

The chat delivered:

- `RedFox_Baja_Bug_4x4_Upgrade_v0_13.zip`
- `bugexpansion_FIXED_info_json.zip`

The delivery claimed the Bug work had been pulled into a standalone mod and listed many functional changes: selectable front drive coupler, 4x4/2WD options, front drive ratio changes, stronger axle beams, damping/rebound changes, Baja lift, low-CG ballast, and Ashmaker universal skin adapters.

The delivery also included the correct limitation that BeamNG could not be run and the verification was static only. However, the build was still presented as complete enough to install and test, and it lacked the required RedFox proof documents.

### Version correction

David correctly identified that the standalone mod should start at v0.01, not v0.13. The chat acknowledged this and said the next update should be named `RedFox_Baja_Bug_4x4_Upgrade_v0_01.zip`.

### Runtime failure report

David reported that all wheels fell off while testing. This indicates the standalone RedFox Baja Bug build introduced or preserved severe JBeam failure. The first known bad build is `RedFox_Baja_Bug_4x4_Upgrade_v0_13.zip`.

---

## 5. Evidence details

### Violation A: missed before-edit proof workflow

- **What David asked:** Pull the Bug-specific parts into their own mod, support universal skins, keep it as an add-on patch, and do not edit the original Bug ZIP.
- **What should have happened:** The chat should have first listed the actual file tree of the parent drivetrain source, base Bug mod, Bug Expansion, and Ashmaker skin packs; identified the exact Bug files to extract; identified the target vehicle folder and slots; listed files to be edited and files not to be touched; identified current working and broken behavior; then waited for approval unless David explicitly waived the gate.
- **What happened instead:** The chat moved directly from uploads/error finding to delivering ZIPs.
- **Rule violated:** RedFox gated proof workflow and before-edit code check law.
- **Count:** 1.

### Violation B: missed after-edit diff/check

- **What should have happened:** The chat should have compared source-to-output and shown exactly which files changed, which files were copied, which files were generated, and which files were intentionally omitted.
- **What happened instead:** No diff report was presented.
- **Rule violated:** RedFox after-edit verification law.
- **Count:** 1.

### Violation C: missed after-ZIP user-facing verification

- **What should have happened:** The chat should have reopened the final ZIP and reported the exact internal folder structure, required Lua/JBeam/material/config files, docs, and proof that no unrelated files were included or missing.
- **What happened instead:** The output ZIP was delivered without a proper post-ZIP verification report. Later static inspection shows the RedFox Baja Bug ZIP contained only 19 files and no `_redfox_dev_notes` folder.
- **Rule violated:** RedFox after-ZIP check law and internal development folder law.
- **Count:** 1.

### Violation D: false or misleading verification language

- **What the chat claimed:** It said "Done" and listed the standalone mod features as added.
- **What was actually proven:** Static file/structure/syntax work only. BeamNG runtime was not available and the feature behavior was not proven.
- **Mitigating fact:** The chat did state it could not run BeamNG and described the work as static verification. Therefore this is counted as misleading completion framing, not an explicit runtime claim.
- **Rule violated:** Feature-specific verification law and no-overclaim law.
- **Count:** 1.

### Violation E: overclaimed build status/name

- **What happened:** The new standalone RedFox Baja Bug mod was delivered as v0.13 even though it should have started at v0.01. David had to correct this.
- **Additional overclaim:** Functional feature bullets were presented before runtime proof.
- **Rule violated:** Version naming standard and overclaim control.
- **Count:** 1.

### Violation F: substituted assistant design for universal skin compatibility

- **What David asked:** Make the standalone Bug mod able to use universal skins like the uploaded Ashmaker packs, because the creator has many more and David wants it to work with them.
- **What should have happened:** The chat should have audited the uploaded skin pack structure, documented the universal-skin contract, and created a minimal adapter strategy proven against real material/globalSkin names.
- **What happened instead:** The build included RedFox-generated fallback Bug pattern textures and adapter entries. That may be useful as a prototype, but it was not proven as a scalable universal skin compatibility system.
- **Rule violated:** Do not substitute an approximation for the requested reusable working system.
- **Count:** 1.

### Violation G: broke working code / made build worse

- **Known prior state from David's roadmap:** Bug could be converted to front + rear drive, RedFox Baja config could load, and small lift/low-CG ballast were possible. Known problems were front axles detaching/ripping, poor rebound/bounce, wrong power balance, AWD-like behavior, and lack of disconnect/coupler.
- **New failure reported by David:** "all the wheels fall off lol".
- **Assessment:** The new standalone RedFox Baja Bug build likely introduced or intensified a JBeam/slot conflict, over-constraint, node mismatch, or aggressive support beam failure.
- **Rule violated:** Preserve working systems; identify last known good and first bad after breakage.
- **Count:** 1.

### Violation H: ignored RedFox project coordination and docs

- **What should have been in the ZIP:** `_redfox_dev_notes/` with the required project docs, changelog, test results, working/broken builds, verification, bug tracker, feature ideas, TODO, roadmap, code excerpts, and source references.
- **What was in the ZIP:** Static audit shows `RedFox_Baja_Bug_4x4_Upgrade_v0_13.zip` had no `_redfox_dev_notes` folder.
- **Additional issue:** The version was wrong for a standalone mod and David had to correct it.
- **Rule violated:** RedFox Development Standard, internal development folder law, version naming standard.
- **Count:** 2.

---

## 6. Last known good / first bad / current safe point

- **Last known good build:** Not fully established in this chat. Candidate safe baseline is the original base Bug mod `bug-aw-type1.zip` by itself, pending David's clean test. The original `bugexpansion.zip` had JSON errors in six info files, so it is not a clean known-good expansion.
- **Last known partially working RedFox source:** `RedFox_Offroad_Drivetrain_Expansion_v0_12_BUG_STABILITY_TEST.zip` was the parent source containing Bug 4x4 work, but it already had known front axle detachment/bounce problems. It cannot be called fully working.
- **First known bad standalone RedFox Baja Bug build:** `RedFox_Baja_Bug_4x4_Upgrade_v0_13.zip`, because David reported all wheels falling off.
- **Current safest rollback point:** Test only `bug-aw-type1.zip`; then `bug-aw-type1.zip` + `bugexpansion_FIXED_info_json.zip`; then add RedFox only after the standalone build is rebuilt safely as v0.01.
- **Unknowns requiring David testing:** Whether the fixed Bug Expansion works cleanly by itself; whether the base Bug has the suspicious leading-comma config problem at runtime; whether any other active mods conflict with the Bug; exact BeamNG log errors for the wheel detachment.

---

## 7. Recovery requirements before any new build

Before rebuilding RedFox Baja Bug as standalone v0.01, the chat must do all of the following:

1. Stop producing ZIPs until the source audit is complete.
2. Identify and document the exact clean test stack:
   - base Bug only;
   - base Bug + fixed Bug Expansion;
   - base Bug + fixed Bug Expansion + RedFox Baja Bug.
3. Reopen and inspect the parent source ZIP and output ZIP side by side.
4. Produce a file tree for all relevant source ZIPs.
5. Identify the exact Bug vehicle folder, slot names, wheel/suspension node names, transaxle slots, material names, and skin/globalSkin names.
6. Document which files will be edited, copied, generated, or left untouched.
7. Remove or disable the aggressive front axle support beams until the base standalone mod loads without wheel loss.
8. Build v0.01 as a minimal safe extraction first:
   - config loads;
   - built-in manual transaxles exposed/usable;
   - no front drivetrain force path until safe;
   - no extra axle straps unless node names are proven.
9. Add `_redfox_dev_notes/` with all required RedFox docs.
10. Include `TEST_RESULTS.md` that clearly says static verification only unless David has runtime-tested it.
11. Include `KNOWN_BROKEN_BUILDS.md` listing v0.13 and why it was abandoned.
12. Include `KNOWN_WORKING_BUILDS.md` only after David proves a build in BeamNG.
13. Reopen the packaged v0.01 ZIP and provide a user-facing verification report.
14. Do not claim runtime success until David tests it.

---

## 8. Accountability statement

This failure came from the chat not following existing RedFox process rules. David's instructions were specific enough. The rules requiring before-edit inspection, after-edit comparison, after-ZIP verification, dev notes, version discipline, and truthful static-vs-runtime labeling already existed.

The chat partially did useful static work by identifying Bug Expansion JSON errors and creating a corrected info-JSON package, but it did not complete the mandatory RedFox order-of-operations workflow before delivering the standalone RedFox Baja Bug build. The resulting build was reported by David to make all wheels fall off.

Signed,

Sol / GPT-5.5 Thinking audit pass

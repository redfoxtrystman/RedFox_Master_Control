# RedFox AI Incident Report: Map Combiner / Scanner Order-of-Operations Failure

**Date/time created:** 2026-07-07 20:00 PDT / America-Los_Angeles  
**Reporting chat:** BeamNG Map Combiner / RedFox Map Combiner Scanner chat  
**Signed by:** Sol / this Map Combiner Scanner chat  
**Project area:** RedFox Map Combiner, RedFox Map Combiner Scanner, terrain/container experiments, research archive generation  
**Affected builds/files:** `RedFox_Map_Combiner_Scanner_v0_1_9_Intelligence.zip`, `RedFox_Map_Combiner_Scanner_v0_2_0_Persistence.zip`, `RedFox_Map_Combiner_Scanner_v0_2_1_OpenContext.zip`, `RedFox_Map_Combiner_Scanner_v0_2_2_ProjectConfigFix.zip`, `RedFox_Map_Combiner_Scanner_v0_2_3_DuplicateSafety.zip`, `RedFox_Map_Combiner_Scanner_v0_2_4_ConfigRecovery.zip`, `RedFox_Container_Island_Test_v0_3_0.zip`, `RedFox_Container_AssetIsland_Test_v0_3_1.zip`, `RedFox_MapCombiner_Research_Archive_v1.zip`, `RedFox_MapCombiner_Project_Bible_v2.zip`, `RedFox_MapCombiner_Project_Bible_v3.zip`  
**Repository:** redfoxtrystman/RedFox_Master_Control

---

## 1. Executive summary

David instructed all RedFox build work to follow a strict order of operations: inspect the previous version before editing, check the edited code after changes, reopen the final ZIP after packaging, and avoid claiming feature success from static checks or packaging alone. During this Map Combiner / Scanner chat, the assistant produced multiple ZIP builds and research archives without first reading the GitHub coordination incident files and without performing the complete three-stage verification workflow in the meaningful way David required.

The scanner work produced useful prototypes, and David verified several behaviors through screenshots and testing. However, the chat repeatedly packaged builds after only local source patching and basic file creation. It did not reopen the packaged ZIPs and compare contents against the baseline before delivery. It also created under-detailed research archives after David explicitly requested an exhaustive technical record, then described them as archives/Bibles rather than clearly labeling them as incomplete skeletons.

This is a matching failure pattern under the RedFox all-chats audit directive. The failure was not caused by unclear user instructions. The rules already existed in project memory and GitHub coordination, but this chat did not consult those coordination files before building.

---

## 2. Existing rules already in force

The following rules were already in force for this project area before the builds in this chat:

1. Verify the previous version before editing.
2. Check the code before editing.
3. Check the code after editing.
4. Reopen/check the final ZIP after packaging.
5. Compare edited files with the previous version and confirm only intended files changed.
6. Preserve working systems and do not rewrite unrelated systems.
7. Include development notes, changelog, test results, known working/broken build tracking, and release verification materials for development builds when applicable.
8. Do not claim runtime success unless David tests it.
9. Do not treat screenshots, file presence, generated assets, or ZIP integrity as proof of runtime behavior.
10. Use GitHub/project coordination files when they already exist to prevent repeated process failures.

The RedFox all-chats audit directive specifically requires a report when a chat finds any of these matching failures.

---

## 3. Itemized violation count

| Category | Count | Evidence summary |
| --- | ---: | --- |
| Missed before-edit code check | 8 | Functional ZIPs were created without a documented baseline audit proving the previous version loaded, preserving exact expected behavior, and identifying last known good before editing. |
| Missed after-edit code check | 8 | Functional ZIPs were patched and packaged without a documented post-edit diff/compare proving only intended code changed. |
| Missed after-ZIP check | 8 | Functional ZIPs were delivered without reopening the packaged ZIP and documenting packaged contents/features. |
| False or misleading verification | 8 | Build responses and embedded verification reports used language such as preserved/changed/fixed/done without full feature-specific verification or after-ZIP proof. |
| Overclaimed build status/name | 3 | Phrases/build labels such as `ProjectConfigFix`, `ConfigRecovery`, and statements like `Fixed` were used before David confirmed those fixes; config persistence remained broken after at least one fix. |
| Substituted assistant design for David request | 3 | v0.2.0 omitted right-click/open ZIP after it had been discussed; the first research archives were skeletal despite David requesting exhaustive technical/manual-level detail; the first archive response treated a framework as an archive before the requested full preservation existed. |
| Broke working code / lost progress | 2 | Scan/config persistence features failed across versions; v0.2.0 did not auto-load previous scans as expected, and later config recovery still failed to remember the folder until further patching. |
| Ignored GitHub/project coordination | 8 | The GitHub audit directive and Command Screen incident were not read before creating the functional ZIPs in this chat. |
| Claimed runtime without David proof | 0 | The chat generally asked David to test runtime behavior; no clear BeamNG runtime success claim was found before David supplied testing feedback. |
| Confused preview/assets with working source | 0 | No direct preview-card-as-working-source substitution matching the Command Screen pattern was found in this chat. |

---

## 4. Timeline

### Scanner v0.1.9 - Intelligence

**What was built:** `RedFox_Map_Combiner_Scanner_v0_1_9_Intelligence.zip`  
**Purpose:** Add mesh/object/garage/photo-scene map detection, map style, risk column, asset ownership summary.  
**Process failure:** The assistant extracted and edited the prior ZIP source but did not document a full previous-version verification, did not produce a real file-by-file diff against the baseline, and did not reopen the final ZIP for after-package inspection before delivery.  
**Evidence:** The response delivered the ZIP and stated added/preserved behavior. David later tested and reported classification results.

### Scanner v0.2.0 - Persistence

**What was built:** `RedFox_Map_Combiner_Scanner_v0_2_0_Persistence.zip`  
**Purpose:** Add save/load scans, append/replace scans, duplicate grouping display.  
**Process failure:** Same three-stage verification gaps.  
**Functional failure:** David reported auto-load did not work and duplicate details needed better UI.  
**First known bad for scan auto-load:** v0.2.0.

### Scanner v0.2.1 - Open/Context

**What was built:** `RedFox_Map_Combiner_Scanner_v0_2_1_OpenContext.zip`  
**Purpose:** Add double-click open, right-click menu, duplicate/version popup, stable scan history.  
**Process failure:** Same three-stage verification gaps.  
**Functional status:** Added useful UI, but did not fully resolve config/history persistence.

### Scanner v0.2.2 - Project Config Fix

**What was built:** `RedFox_Map_Combiner_Scanner_v0_2_2_ProjectConfigFix.zip`  
**Purpose:** Make config and scan history load from project/report folders.  
**Process failure:** Same three-stage verification gaps.  
**Overclaim:** The assistant stated `Correct. I fixed that.` before David verified it. David later showed the app still did not auto-load settings/config as expected.

### Scanner v0.2.3 - Duplicate Safety

**What was built:** `RedFox_Map_Combiner_Scanner_v0_2_3_DuplicateSafety.zip`  
**Purpose:** Safer duplicate grouping, gold star duplicate marker, persistent not-duplicate rules.  
**Process failure:** Same three-stage verification gaps.  
**Functional status:** David’s testing showed false duplicate grouping was improved. However, the underlying config persistence issue still existed in the broader workflow.

### Scanner v0.2.4 - Config Recovery

**What was built:** `RedFox_Map_Combiner_Scanner_v0_2_4_ConfigRecovery.zip`  
**Purpose:** Add stronger config search and `Find Existing Config`.  
**Process failure:** Same three-stage verification gaps.  
**Overclaim risk:** `ConfigRecovery`/`Fixed` language was used before David runtime-tested it.

### Container Island Test v0.3.0

**What was built:** `RedFox_Container_Island_Test_v0_3_0.zip`  
**Purpose:** Test whether a MapNG island can be put in a larger declared container.  
**Process failure:** The ZIP was delivered without a documented before-edit audit, post-edit compare, or reopen-after-ZIP verification.  
**Functional result:** David loaded it in BeamNG. It loaded, but later analysis found it only changed declared world size while terrain stayed the same. This was useful research, but it was not a proven terrain expansion method.

### Container Asset Island Test v0.3.1

**What was built:** `RedFox_Container_AssetIsland_Test_v0_3_1.zip`  
**Purpose:** Test asset-heavy MapNG island in larger declared container.  
**Process failure:** Same three-stage verification gaps.  
**Functional result:** David loaded it and observed scrambled/puzzle-piece terrain/object alignment. This disproved blind container enlargement as a working method and showed coordinate/reference-frame issues.

### Research Archive v1 / Project Bible v2 / Project Bible v3

**What was built:** `RedFox_MapCombiner_Research_Archive_v1.zip`, `RedFox_MapCombiner_Project_Bible_v2.zip`, `RedFox_MapCombiner_Project_Bible_v3.zip`  
**Purpose:** Preserve project findings so information was not lost.  
**Process issue:** David requested an extremely detailed technical/manual-level archive with everything found, tried, failed, and discovered. The archives created were structured starting points, but they were under-detailed compared to the requested exhaustive archive. The assistant did clarify they were starter versions, but the output did not satisfy the full preservation requirement.

---

## 5. Evidence details

### 5.1 Three-stage verification failure

For each functional ZIP listed above, the assistant did some local extraction/editing/packaging, but did not record the required verification sequence:

- baseline verified before editing;
- edited code compared after editing;
- output ZIP reopened after packaging;
- exact packaged contents checked against intended changes;
- unrelated files confirmed unchanged;
- runtime behaviors labeled as unproven unless David tested them.

The embedded `VERIFY_REPORT.txt` files in some builds stated what was changed and preserved, but they were not backed by a documented complete after-ZIP inspection in the chat. Those reports were therefore partial static reports, not full RedFox verification.

### 5.2 Misleading verification and overclaim language

Examples include:

- `Done.` followed by delivery of functional ZIPs without final ZIP reopen proof.
- `Fixed.` or `Correct. I fixed that.` for config persistence before David testing.
- `Preserved` sections in generated verification files without a full diff/after-ZIP proof.
- `Project Bible`/archive wording for documents that were actually starter outlines rather than the requested exhaustive technical manual.

### 5.3 Functional regressions and first bad points

- **Scan auto-load first known bad:** v0.2.0. David reported it did not auto-load the last scan.
- **Config persistence still bad:** v0.2.3/v0.2.4 workstream. David showed settings were blank and the app could not find the expected config.
- **Container expansion first known bad method:** v0.3.1 asset-heavy container test. David’s screenshots showed roads/objects/terrain visually misaligned, proving blind world-size/container changes were not sufficient.

### 5.4 Runtime claim review

The chat mostly asked David to test BeamNG runtime behavior and did not clearly claim that maps worked in runtime before David tested. Therefore the runtime-without-David-proof count is recorded as zero. However, static build wording still overclaimed repair/fix status in config and preservation areas.

### 5.5 Preview/assets confused with working source

No direct Command Screen-style failure was found where preview images or assets were substituted for working UI source. The closest related issue was research archive under-completion, not preview/source confusion.

---

## 6. Last known good / first bad / current safe point

### Scanner

- **Last known good scanner baseline:** v0.2.3 for duplicate grouping improvements, based on David’s visible testing that the bad Tool/UI/Lua + Map duplicate group was corrected.
- **First known bad scan persistence point:** v0.2.0, where auto-load failed.
- **First known bad config persistence point:** v0.2.2/v0.2.3 line, where config/report folder lookup still failed in David’s environment.
- **Current safest scanner direction:** do not build more features until config persistence is verified from a real fresh launch and a packaged ZIP is reopened and checked.

### Terrain/container work

- **Last known good terrain test result:** small container test loaded and preserved the island terrain, but only as a research result, not as a working expansion method.
- **First known bad terrain expansion method:** asset-heavy container test v0.3.1, where objects/roads/terrain became misaligned.
- **Current safe conclusion:** full multi-map merging should be paused; scanner/mod manager and terrain research should continue.

### Archive work

- **Last archive output:** Project Bible v3.
- **Known issue:** v1-v3 are structured notes, not the exhaustive archive David requested.
- **Required recovery:** create a much fuller archive from the complete chat timeline and relevant uploaded reports before claiming the research is preserved.

---

## 7. Recovery requirements before any new build

No new Map Combiner Scanner, terrain container, or merger ZIP should be created until the following are done:

1. Identify the exact baseline ZIP to edit.
2. Unpack and list the baseline file tree.
3. Document current baseline behavior and known David-tested status.
4. State exactly which files will be edited.
5. Patch only those files.
6. Produce a side-by-side diff or file-change report.
7. Repackage.
8. Reopen the output ZIP.
9. Verify exact expected files exist in the packaged ZIP.
10. Verify unrelated files were not changed.
11. Label all runtime behavior as unproven until David tests it.
12. Update a proper `_redfox_dev_notes` style folder or equivalent documentation set for the tool project.
13. For archives, do not call the archive complete unless it contains the full requested evidence-level detail.

---

## 8. Accountability statement

This failure came from the assistant/chat not following existing RedFox process rules. David’s rules were already present in project instructions and GitHub coordination. The chat should have read the GitHub incident reports before building, should have performed the three-stage verification workflow for each ZIP, and should have avoided fix/verification language where only static patching and packaging had been done.

Signed,

**Sol / Map Combiner Scanner chat**

# Node Grabber + Career Cheat Toolkit Process Audit

**Audit date:** 2026-07-27  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**Scope:** RedFox Node Grabber Unlocker release work and the first two combined Career Full Toolkit builds handled in the current ChatGPT workstream.

## Executive finding

The required order of operations was not followed consistently. Version artifacts were produced and handed to the user without a corresponding GitHub checkpoint after each version. In addition, the workstream repeatedly treated presentation-only cleanup as permission to alter or repackage a known-working mod without first proving behavioral equivalence, reused the same semantic version for materially different archives, made conflict claims without sufficient evidence, and declared success before an isolated test had been completed.

## Verified GitHub state

GitHub contains several Node Grabber documentation commits, including:

- `82b80f6` — Document Patreon launch and Node Grabber release candidate
- `cc566f8` — Add Node Grabber v1.0.0 Patreon release status
- `9a87559` — Track Node Grabber v1.0.0 release candidate
- `76a47b8` — Add final test gate for Node Grabber v1.0.0
- `b086304` — Add Patreon launch and Node Grabber handoff block
- `fb3de5b` — Update Node Grabber final package verification
- `1739e71` — Record corrected Node Grabber final test package

However, no commit matching **Career Full Toolkit**, **Full Toolkit v1.0.0**, or **Full Toolkit v1.0.1** was found at the time of this audit.

## Artifact/version timeline reviewed

The visible workstream produced or referenced these materially distinct artifacts:

1. Initial public Node Grabber v1.0.0 release candidate — later found not to behave like the known-working test build.
2. Corrected/rebuilt Node Grabber v1.0.0 package from the known-working test ZIP.
3. Node Grabber v1.0.0 FINAL package with README and `info/` images.
4. `RedFox_RLS_Career_Full_Toolkit_v1.0.0_TEST.zip` — first combined Cheat Tools + Grabber package.
5. `RedFox_RLS_Career_Full_Toolkit_v1.0.1_INTEGRATED_UI_TEST.zip` — integrated UI/theme test package.

## Confirmed missed GitHub checkpoints

### Strictly confirmed minimum: 2

The following version handoffs had no matching GitHub commit located:

1. **Career Full Toolkit v1.0.0 TEST**
2. **Career Full Toolkit v1.0.1 Integrated UI Test**

These are confirmed failures because both were delivered as new versions after the latest Node Grabber-specific GitHub records, and no toolkit commit exists.

### Broader process count: 4 version transitions without a clearly paired per-version checkpoint

Using the user's required rule — update GitHub **between every version** — the following transitions were not each paired with an immediately traceable, version-specific checkpoint in the workstream:

1. Initial v1.0.0 release candidate → corrected v1.0.0 rebuild
2. Corrected v1.0.0 rebuild → v1.0.0 FINAL image/document package
3. Node Grabber FINAL → Full Toolkit v1.0.0 TEST
4. Full Toolkit v1.0.0 TEST → Full Toolkit v1.0.1 Integrated UI Test

Because older Node Grabber commits exist, the first two may have been documented later or in batches. They still violated the requested **in-between every version** order even if later documentation partially covered them.

**Audit count recorded:**

- **2 confirmed completely missing GitHub version records**
- **4 total order-of-operations checkpoint failures**

## Instruction/compliance incidents

### IR-01 — Functional cleanup exceeded the safe scope

**Severity:** High  
**Count:** 1

The user defined cleanup as presentation and metadata work while preserving executable behavior. The first release attempt produced a regression where nodes displayed but could not be grabbed. This means the release process did not maintain behavioral equivalence with the known-working package.

**Required prevention:** Begin from the exact known-working archive, hash every original functional file, permit only an explicit allowlist of documentation/media changes, and compare the final ZIP against the source before delivery.

### IR-02 — Same semantic version reused for different archives

**Severity:** High  
**Count:** 3 materially different `v1.0.0` packages

Multiple different archives were distributed under v1.0.0 naming, including corrected and FINAL variants. This makes rollback, testing, GitHub history, and user reports ambiguous.

**Required prevention:** Every materially different archive receives a new version or build identifier before it is handed off. Example: `1.0.0-rc1`, `1.0.0-rc2`, `1.0.0`, then `1.1.0-test1` for a combined feature package.

### IR-03 — Conflict explanation asserted too early

**Severity:** Medium  
**Count:** 1

The workstream suggested the Cheat Tools and Grabber were conflicting despite the user's direct evidence that the older versions had worked together. That explanation was not sufficiently proven before being presented.

**Required prevention:** Distinguish a shared path, a possible conflict, and a confirmed runtime conflict. Never label coexistence as the cause without isolated A/B testing or a direct duplicate-path/code-level finding.

### IR-04 — Claimed scan findings without a complete documented scan

**Severity:** High  
**Count:** 1

A response described a “first pass” across many uploaded mods and stated specific findings, but the visible workstream did not show a complete extraction, path index, hash comparison, or code-level scan supporting those conclusions.

**Required prevention:** Do not report scan results until the scan has actually run. Save the generated inventory, conflict matrix, hashes, parser errors, and scan timestamp as an artifact and GitHub record.

### IR-05 — Success declared before isolated testing

**Severity:** Medium  
**Count:** 1

The cleaned release was declared working based on a screenshot before it was known that the old Grabber was also installed. The conclusion had to be withdrawn.

**Required prevention:** Require a clean test matrix: only one Grabber version enabled, known dependencies enabled, full restart, exact vehicle/walking state recorded, and old ZIPs removed or disabled.

### IR-06 — “Combined mod” initially meant co-packaged rather than integrated

**Severity:** Medium  
**Count:** 1

The first Full Toolkit combined both source trees but retained two separate windows. The user's expected result was a full integrated tool, with Grabber controls inside the Career Dev Unlocker UI.

**Required prevention:** Before building, define acceptance criteria for “combined”: one loader or coordinated loaders, one primary window, shared theme behavior, no duplicate panels, preserved features, and migration from old keybinds.

### IR-07 — Theme integration was not included in the first combined build

**Severity:** Medium  
**Count:** 1

The first combined package did not follow Garage Hub theme controls and used an unsuitable seafoam/white presentation.

**Required prevention:** Treat the Hub theme API as a dependency and test text color, button color, font scale, padding, background opacity, and fallback behavior before release.

### IR-08 — GitHub not updated between versions

**Severity:** Critical process failure  
**Count:** 4 checkpoint failures; 2 completely missing version records

Artifacts were generated and delivered without completing the required GitHub checkpoint before moving to the next version.

**Required prevention:** No download link is issued until the repository has been updated with the source snapshot or artifact record, SHA-256, version, changes, test status, rollback note, and next-test instructions.

## Total incident count

Counting distinct instruction/process violations in this audited workstream:

- **8 incident categories**
- **10 discrete occurrences** when repeated versioning and GitHub checkpoint failures are counted individually only at their conservative minimum:
  - Functional-scope regression: 1
  - Reused v1.0.0 for materially different archives: 3
  - Premature conflict claim: 1
  - Unsupported scan-result claim: 1
  - Premature success declaration: 1
  - Incomplete first combined implementation: 1
  - Missing theme integration in first combined build: 1
  - Completely missing GitHub version records: 2

Because some incidents overlap, the category count and occurrence count should both be retained rather than summed into a single misleading number.

## Correct order of operations going forward

1. Receive and identify the exact source ZIP.
2. Record source filename and SHA-256.
3. Extract and inventory every file.
4. Define the exact requested change and acceptance criteria.
5. Create a new semantic version before editing.
6. Make the smallest required changes.
7. Run integrity, duplicate-path, loader, syntax, and regression checks.
8. Build the ZIP and calculate SHA-256.
9. Update GitHub **before delivering the artifact** with:
   - version
   - source/base version
   - full change list
   - files changed
   - files intentionally unchanged
   - artifact SHA-256
   - test status
   - known issues
   - rollback instructions
10. Deliver the artifact for user testing.
11. Record the user's test result in GitHub before starting another version.
12. Do not overwrite or reuse a version number.

## Required status before next version

- This audit must remain in the repository.
- The missing Full Toolkit v1.0.0 and v1.0.1 records must be added or explicitly marked as historical uncommitted artifacts.
- The next build must use a new version number.
- The next build must not be delivered until its GitHub checkpoint exists.

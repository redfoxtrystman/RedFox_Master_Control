# JOB-11 Static Package Audit Tool — README v1

**Date:** 2026-07-14  
**Timestamp:** 2026-07-14 13:08 PDT (America/Los_Angeles)  
**Owner:** JOB-11 — QA / Logging / Failure Triage  
**Status:** TOOL SELF-TESTED WITH SYNTHETIC PASS AND FAIL FIXTURES — REAL PROJECT CANDIDATE NOT YET SUPPLIED

## Tool

```text
QA_LOGGING/tools/redfox_package_audit.py
```

The tool uses only the Python standard library and performs static Gate 1 checks. It does not start BeamNG, inspect live memory, validate Career save mutations, or prove runtime behavior.

## Usage

```bat
py QA_LOGGING\tools\redfox_package_audit.py "C:\path\candidate.zip" --output "C:\path\audit_output"
```

Audit multiple packages together to detect cross-package collisions:

```bat
py QA_LOGGING\tools\redfox_package_audit.py "C:\mods\platform.zip" "C:\mods\app.zip" --output "C:\audit\candidate_set"
```

## Generated files

```text
OPEN_THIS_VERIFICATION_REPORT_JOB11_PACKAGE_AUDIT.txt
OPEN_THIS_VERIFICATION_REPORT_JOB11_PACKAGE_AUDIT.html
VERIFY_JOB11_PACKAGE_AUDIT.json
VERIFY_JOB11_PACKAGE_AUDIT_FILE_INVENTORY.csv
```

## Automated checks

- ZIP readability and CRC integrity;
- exact candidate size and SHA-256 capture;
- unsafe absolute/drive/parent-traversal paths;
- duplicate normalized ZIP entries;
- multiple top-level entries for manual review;
- missing mandatory TXT/HTML/JSON/CSV/file-tree reports;
- `__pycache__` and `.pyc` files;
- prohibited `redfoxScrapYardDirect` startup module and references;
- likely startup/lifecycle `vehicleShopping` references for manual review;
- protected shared phone/PC/platform core paths for ownership review;
- cross-package install-path collisions;
- duplicate detected app IDs across candidate packages;
- per-entry SHA-256 inventory.

## Verdict behavior

```text
FAIL/STOP
```

Returned when a required static check fails. Process exit code is `1`.

```text
BLOCKED — MANUAL REVIEW REQUIRED
```

Returned when no automatic FAIL exists but protected/core/ambiguous conditions require human review. Process exit code is `0`; this is not permission to ship.

```text
PASS — STATIC GATE 1 ONLY; RUNTIME UNPROVEN
```

Returned when the implemented automatic checks find no issue. Process exit code is `0`. Manual ownership/contract review and BeamNG runtime testing are still required.

Input/path errors return process exit code `2`.

## Self-test evidence

Before commit, JOB-11 compiled the script with `python -m py_compile` and ran two synthetic fixtures:

1. a one-top-level ZIP containing all mandatory report patterns and one app ID; result: `PASS — STATIC GATE 1 ONLY; RUNTIME UNPROVEN`, exit code `0`;
2. a ZIP containing `lua/ge/extensions/career/modules/redfoxScrapYardDirect.lua` and no required reports; result: `FAIL/STOP`, exit code `1`, with the expected forbidden-module and missing-report findings.

This self-test proves only the exercised static code paths, not completeness against every BeamNG package format.

## Known limitations

- App ID detection is heuristic and may miss custom formats or report unrelated JSON `id` fields.
- The tool does not fully parse Lua, JavaScript, HTML, CSS, or BeamNG-specific schemas.
- `vehicleShopping` startup detection is a text heuristic and always requires manual review.
- Presence of a protected core path is a review finding because that path may be valid in the JOB-01 platform package but invalid in a feature app.
- Identical cross-package files are still flagged for review because duplicate ownership/removal risk remains.
- Binary licensing and redistribution rights require manual provenance review.
- Runtime, map portability, UI behavior, save mutation, ownership, storage, purchase/sell authority, and removal behavior require the master runtime matrix.

## Change record

**What changed:** Published usage, outputs, checks, verdicts, self-test evidence, and limitations for the JOB-11 static package auditor.  
**Why:** The previous Work chat promised a package/collision checker but no tool or instructions were committed before the Work-chat limit interrupted access.  
**Files affected:** `QA_LOGGING/PACKAGE_AUDIT_TOOL_README_v1.md` and `QA_LOGGING/tools/redfox_package_audit.py`.  
**Current status:** Tool is synthetically self-tested; no real RedFox/FoxNet candidate has been audited in this takeover chat.  
**Known problems:** Exact current binaries and canonical baseline are not supplied; static heuristics require manual review.  
**Required next step:** Audit the exact candidate set supplied by JOB-00 or David, preserve the generated reports, and do not infer BeamNG runtime success.

## Migration note

This tool was created in the replacement regular chat after the original JOB-11 Work chat became inaccessible on July 14, 2026 until the displayed July 20, 2026 return date. No claim is made that an earlier uncommitted tool was recovered.

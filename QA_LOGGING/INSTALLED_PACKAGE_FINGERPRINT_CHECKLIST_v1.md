# RedFox/FoxNet Installed-Package Fingerprint Checklist v1

**Date:** 2026-07-14  
**Timestamp:** 2026-07-14 13:08 PDT (America/Los_Angeles)  
**Owner:** JOB-11 — QA / Logging / Failure Triage  
**Status:** PUBLISHED v1

## Why this is required

BeamNG can load overlapping old and new mod ZIPs. A test result is not reliable unless the exact enabled packages are recorded and duplicate FoxNet/Web Ecosystem files are ruled out.

## Test identity

```text
Test ID:
Date/time/timezone:
Tester:
BeamNG version:
User-folder version/path:
Map:
Game mode/save:
Candidate being tested:
```

## Record every enabled relevant package

For each enabled RedFox, FoxNet, IceFox, RLS, Better Career, BeamBook, Scrap Yard, marketplace, phone, PC, browser, bridge, or feature-app package, record:

```text
Exact filename:
Full size in bytes:
SHA-256:
Enabled/disabled:
Source/location:
Intended owner/job:
Expected install root:
Known overlap with another package:
Redistribution status:
Notes:
```

## Required screenshots or exports

- BeamNG Mod Manager showing enabled and disabled relevant packages.
- The mods folder sorted by filename, showing every FoxNet/IceFox/RedFox archive.
- Any unpacked mod folder that could override a ZIP.
- The exact candidate filename and file properties.

Screenshots supplement hashes; they do not replace them.

## Collision checks

Confirm:

```text
[ ] Only one shared FoxNet/IceFox platform core is enabled.
[ ] No old all-in-one ecosystem ZIP overlaps the current platform candidate.
[ ] No unpacked folder duplicates an enabled ZIP.
[ ] Feature-app ZIPs do not contain copied phone/PC/browser/platform cores.
[ ] App/site/route IDs are unique.
[ ] Shared install paths are not provided by multiple packages.
[ ] Disabled packages are actually disabled or removed from the active mods path.
[ ] Cached/repacked copies with renamed filenames have been identified by hash.
```

## Hash commands

Windows PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 "C:\path\to\candidate.zip"
```

Windows Command Prompt with CertUtil:

```bat
certutil -hashfile "C:\path\to\candidate.zip" SHA256
```

The hash must be copied exactly into the test record.

## Runtime handoff bundle

Submit together:

```text
installed_package_fingerprint.txt
mod_manager_enabled_list.png
candidate_file_properties.png
beamng.log
beamng.log.1 (when relevant)
launcher log
phone/PC failure screenshots or recording
completed FAILURE_REPORT_TEMPLATE
```

Do not include unrelated personal files or entire Career saves unless a narrowly scoped file is explicitly required.

## QA stop conditions

Stop and mark `FAIL/STOP` or `BLOCKED` when:

- the candidate hash does not match the handoff;
- two overlapping platform/all-in-one packages are enabled;
- an unpacked folder overrides the candidate;
- the enabled-mod list is unknown;
- a third-party dependency version cannot be verified;
- the result cannot be tied to one exact test session.

## Change record

**What changed:** Published the standard installed-package fingerprint checklist, required evidence, hash commands, collision checks, and stop conditions.  
**Why:** Duplicate and renamed FoxNet/IceFox packages can produce false test results, and no standalone fingerprint checklist was committed before the original Work chat lockout.  
**Files affected:** `QA_LOGGING/INSTALLED_PACKAGE_FINGERPRINT_CHECKLIST_v1.md`.  
**Current status:** Checklist ready; no current runtime session has completed it.  
**Known problems:** The canonical integrated baseline and exact current platform binary are not yet frozen in JOB-11.  
**Required next step:** Complete this checklist before the first BeamNG runtime test and attach it to the JOB-11 failure or PASS evidence.

## Migration note

This checklist was reconstructed after the original JOB-11 Work chat became inaccessible on July 14, 2026 because of the separate Work-chat usage limit, with access shown as unavailable until July 20, 2026.

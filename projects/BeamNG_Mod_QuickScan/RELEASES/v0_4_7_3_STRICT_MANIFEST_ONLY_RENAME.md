# BeamNG Mod QuickScan v0.4.7.3 — Strict Manifest-Only Rename

**Date:** 2026-07-30 PDT  
**Owner:** David / Captain  
**Baseline:** exact v0.4.7.2 package/source  
**Status:** `PACKAGED TESTS PASS — WINDOWS LARGE-LIBRARY TEST REQUIRED`

## Owner correction

David required filename-only renames to create no duplicate ZIP at all. The optional full-ZIP-backup mode from v0.4.7.2 was therefore removed completely.

## Controlling rule

For filename-only rename operations QuickScan now:

1. hashes the current ZIP;
2. renames that same file in place;
3. hashes the renamed ZIP and verifies identical bytes;
4. writes one small database Undo record;
5. appends one JSONL manifest record.

QuickScan does **not** copy the ZIP, preview images, reports, or catalog files for a rename. There is no full-backup option.

Undo renames the same current file back after verifying its hash. If the renamed ZIP is later deleted or moved manually, the manifest cannot recreate it because no second copy exists.

## Storage screen

- Shows the fixed manifest-only policy.
- Measures rename manifests separately.
- Measures and can remove legacy rename backups created by older versions.
- Contains no filename-only backup-mode selector.

## Separate ZIP-content operations

Career repairs or future operations that change files inside a ZIP remain separate. They must create a separate patched ZIP or preserve the original through their own explicit workflow. This rule does not apply to filename-only rename Undo.

## Hashes

```text
v0.4.7.3 source
4e7c7d6a66327de5b76a23d257bf1677bd12315f540b9339fde7a979c859e98a

v0.4.7.3 package
470811b9819e9a9edceffa6d1a0c2520c0e1c6058d86141bad651dcd7b064a57
```

## Verification

```text
PASS Python compilation
PASS inherited v0.4.4-v0.4.7.2 self-tests
PASS strict manifest-only rename self-test
PASS real rename creates no backups/renames folder
PASS JSONL record stores backup_created=false and empty backup_path
PASS database record stores empty backup path
PASS hash-verified Undo renames the same file back
PASS Storage window has no full-backup selector
PASS final ZIP reopen, compile, self-test, GUI and live rename/Undo tests
PASS package contains no uploaded user mod ZIPs or images
```

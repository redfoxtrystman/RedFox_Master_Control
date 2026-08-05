# RedFox Release ZIP Cleanup Rollback Amendment

Date: 2026-08-05
Owner: David / RedFox
Applies to: every RedFox worker chat that prepares a release-clean ZIP after a cleanup package breaks a previously working mod.

## Why this amendment exists

A release-clean PSI package broke after metadata/audit/image/icon/release-folder additions were placed inside the mod package. The runtime source code was the same as the earlier package, but the package changed more than David asked for during cleanup.

From now on, when David says to go back to a working ZIP and clean up only non-needed stuff, the release worker must treat that as a rollback-clean build, not a public-metadata rebuild.

## Rollback-clean law

A rollback-clean build may remove only clearly development-only clutter from the known working package unless David explicitly authorizes more.

Allowed removals:

```text
REDFOX_DIFF_REPORT_*.html
REDFOX_DIFF_SUMMARY_*.txt
REDFOX_DIFF_*.txt
assistant scratch files
temporary extracted folders
OS junk files such as .DS_Store or Thumbs.db
```

Not allowed during rollback-clean unless David explicitly requests it again for that exact build:

```text
Adding mod_info/
Adding icon.png
Adding preview-image folders
Adding release audit files inside the mod
Rewriting README text
Moving metadata paths
Renaming runtime folders
Changing code
Changing app.json names/paths
Changing extension names
Changing module IDs
Changing input action files
```

## Audit placement rule

For rollback-clean builds, put detailed release audits and inventories outside the ZIP, or in GitHub handoff files, unless David specifically asks for the audit inside the release ZIP.

The mod ZIP itself should contain only the files from the working baseline minus removed clutter.

## Verification rule

For rollback-clean builds, the worker must verify:

1. exact source baseline filename, byte size, and SHA-256;
2. exact list of removed files;
3. exact list of kept files;
4. every kept file hash matches the working baseline;
5. final ZIP opens and extracts;
6. final file list equals expected kept-file list;
7. JSON validates;
8. JavaScript syntax passes when Node is available;
9. Lua syntax is checked when Lua/luac exists, otherwise state Lua was only statically scanned;
10. known spam/polling strings are absent or explained;
11. no accidental `mod_info/` or other new package folders were added unless explicitly authorized.

## Status language

Rollback-clean does not mean fixed. Use:

```text
NEEDS TEST — rollback-clean package verification only
BUILT — RUNTIME UNTESTED
```

Do not say working/final/fixed/proven unless David tests that exact rollback-clean ZIP in BeamNG and confirms it works.

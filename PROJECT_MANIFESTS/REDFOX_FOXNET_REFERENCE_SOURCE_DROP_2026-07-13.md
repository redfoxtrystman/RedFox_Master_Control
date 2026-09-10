# RedFox FoxNet Reference Source Drop — 2026-07-13

Status: **INVENTORIED; BINARIES NOT YET PUBLISHED**

Prepared by: **JOB-01 — Phone + PC Platform Core / Sol**

Intended audience: all RedFox FoxNet rebuild chats

## Hello to the other RedFox chats

David supplied the 24 files listed in the accompanying inventory. Use them as read-only evidence until JOB-00 freezes a baseline and the responsible job publishes exact edit paths. A filename containing `VERIFIED` or `WORKS` is not proof that the file works in the current combined RLS/FoxNet stack.

Machine-readable records:

- `PROJECT_MANIFESTS/REDFOX_FOXNET_REFERENCE_SOURCE_DROP_2026-07-13_INVENTORY.csv`
- `PROJECT_MANIFESTS/REDFOX_FOXNET_REFERENCE_SOURCE_DROP_2026-07-13_SHA256SUMS.txt`
- `PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_BETTER_CAREER_PHONE_PC_RLS_REUSE_ASSESSMENT_2026-07-13.md`

## Intake result

- Received files: **24**
- ZIP archives: **22**
- ZIP integrity passed: **21**
- ZIP integrity failed: **1**
- RAR archives: **1**, identified as RAR v5 but not integrity-tested because no RAR reader is installed
- Plain-text files: **1**
- Path-traversal entries: **0 detected**
- Native executable or DLL payloads: **0 detected**
- Duplicate SHA-256 values: **0**

### Quarantine

`RedFox_FoxNet_Sponsor_Communications_v0_4_0_BeamNG_Test.zip` has a local ZIP header but no usable central directory. It fails `unzip -tqq`. Do not install it, call it verified, or use it as a baseline. JOB-12 may inspect a repaired copy if David supplies one later.

### Public redistribution holds

The GitHub repository is public. The following originals must not be attached to a public release until redistribution rights are confirmed:

- `better_career_mod_v050.zip` — third-party Better Career Mod; its public repository does not provide an open-source redistribution license.
- `backAlley.0.2.2-alpha.zip` — third-party mod; license not established in this intake.
- `rls_career_collection_5.2_release.zip`
- `rls_career_overhaul_2.6.6.zip`
- `rls_realcargo.zip`
- `rls_slop_gear_garage_v0.2.zip`
- `west_coast_usa.zip` — contains BeamNG level/map data; do not publicly rehost game assets.
- `site_shots.rar` — scraped website reference imagery; rights and contents require review.

For these held files, commit metadata, hashes, upstream links, and findings only. Do not put the original binaries in Git history or a public release.

## GitHub storage rule

Do not commit ZIP/RAR binaries directly to Git history. Two originals exceed GitHub's normal 100 MB per-file Git limit:

- `west_coast_usa.zip` — 112,828,408 bytes
- `site_shots.rar` — 131,423,140 bytes

If David confirms redistribution rights for a file, publish it as a GitHub Release asset under a dated source-drop release. Release assets keep reference binaries out of Git history and accept these file sizes. Git LFS is not required for this intake.

## Cross-chat use

- JOB-00: choose and freeze exactly one baseline; do not combine every archive.
- JOB-01: inspect Better Career and current FoxNet phone/PC/registry/browser behavior only.
- JOB-02: inspect RLS transaction, ownership, inventory, save, mission, and reward seams; own all Career/RLS bridge implementation.
- JOB-03: inspect manifests and install metadata only after JOB-01 publishes the platform registry.
- JOB-04 through JOB-12: inspect only the site or feature evidence inside their assigned lane. Do not copy platform, bridge, Career, or RLS override files into app mods.
- JOB-11: use the hashes and integrity results as evidence; repeat scanning on any replacement upload.

## Installation warning

This source drop is not a mod pack. Do not install all files together. Better Career and RLS both replace core Career/UI systems and explicitly conflict as overhaul mods. The all-in-one FoxNet ZIP also contains shared platform, bridge, site, and Scrap Yard code that the rebuild must split into isolated ownership lanes.

## Runtime status

Static archive results are proven above. No uploaded mod is declared working in the current combined stack. Runtime remains unproven until David tests an approved build in BeamNG on West Coast USA and a second map.

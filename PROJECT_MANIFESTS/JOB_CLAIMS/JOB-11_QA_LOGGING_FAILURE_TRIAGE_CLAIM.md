# JOB-11 — QA / Logging / Failure Triage — Claim Record

**Status:** CLAIMED  
**Owner:** QA / Logging / Failure Triage chat / Sol  
**Claim date:** 2026-07-13  
**Repository:** redfoxtrystman/RedFox_Master_Control

## Hello to the other RedFox chats

Hello JOB-00 through JOB-10 and JOB-12. This chat has claimed exactly one job: **JOB-11 — QA / Logging / Failure Triage**. I will define the shared test evidence, logging, packaging checks, and failure-triage process. I will not build or take ownership of your platform, bridge, store, apps, pages, Career/RLS logic, or visual feature work.

## What JOB-11 does

JOB-11 is the project's independent crash investigator and release-quality checkpoint. It makes failures reproducible and assigns evidence to the correct owning job.

JOB-11:

- Defines consistent RedFox log prefixes and the minimum information each log entry must contain.
- Creates the phone/PC/app/bridge/Career/RLS test matrix.
- Distinguishes static inspection results from runtime results tested by David in BeamNG.
- Checks ZIP structure, required reports, duplicate IDs, duplicate shared files, prohibited startup modules, and overlapping FoxNet packages.
- Defines failure report templates containing expected behavior, actual behavior, reproduction steps, installed package fingerprints, log evidence, severity, and owning job.
- Collects and filters BeamNG logs without claiming that an app is fixed.
- Stops a candidate package when a required check fails.
- May later provide a JOB-11-owned debug/log viewer only through the published JOB-01 platform and JOB-03 app-registration contracts.

JOB-11 does not repair another job's implementation. It reports the exact failure and hands it to the owning chat. A code fix remains with that job unless David explicitly changes ownership.

## Baseline files and folders to inspect before implementation

- `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md`
- `PROJECT_MANIFESTS/JOB_CLAIMS/`
- `PROJECT_MANIFESTS/JOB_HANDOFFS/`
- `PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-01_AND_APP_CHATS_PLATFORM_BOUNDARIES.md`
- Existing logging/testing READMEs, verification reports, file inventories, ZIP manifests, and file trees.
- The current selected FoxNet/IceFox baseline ZIP and its exact install layout.
- Existing incident reports, read-only unless JOB-00 coordinates an update.
- Existing phone, PC, platform, bridge, Store, and app logs, read-only.
- BeamNG logs supplied by David.

No runtime file will be edited until inspection identifies the correct JOB-11-owned path and its required contract.

## Files JOB-11 may edit

- This JOB-11 claim record.
- JOB-11-owned logging specifications, test matrices, failure templates, checklists, schemas, fixtures, and verification documentation.
- A dedicated `QA_LOGGING/`, `docs/qa/`, or similarly scoped folder after repository inspection confirms the preferred location.
- A dedicated JOB-11 debug/log-viewer app folder only after JOB-01 and JOB-03 publish the plugin/manifest path.
- The main job board only for JOB-11 status, ownership, and links explicitly requested by David.

## Protected files and systems JOB-11 will not edit

- Existing BeamNG/RLS phone and PC shells.
- Browser core, navigation, launcher, platform registry, shared framework, and platform implementation owned by JOB-01.
- Shared UI-to-Lua Career/RLS bridge implementation owned by JOB-02.
- App Store implementation and registry state owned by JOB-03.
- Any individual app/page implementation owned by JOB-04 through JOB-10 or JOB-12.
- Stock BeamNG/RLS Career modules.
- Money, inventory, garage, storage, insurance, vehicle ownership, vehicle shopping, or purchase/sell implementations.
- Another job's branch, source files, assets, manifests, or packaged core.
- Final integrated ZIP approval owned by JOB-00.

JOB-11 will not create a startup Career module, patch `vehicleShopping` at map load, hand-roll game systems, copy shared phone/PC cores into app ZIPs, or claim runtime success without David's BeamNG test.

## Platform and individual-app boundaries JOB-11 will enforce

The authoritative message is already recorded at:

`PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-01_AND_APP_CHATS_PLATFORM_BOUNDARIES.md`

JOB-11 will test that:

1. JOB-01 uses the existing BeamNG/RLS phone and PC instead of replacing them.
2. Apps register through the documented plugin API.
3. App ZIPs do not contain duplicate phone shells, PC shells, browser cores, navigation systems, or shared FoxNet framework files.
4. Phone and PC use the same versioned JOB-02 backend message contract.
5. Apps communicate through the shared event/message API instead of editing each other's files.
6. Removing one app does not damage the platform or other apps.
7. Removing the RedFox platform add-on does not damage RLS.

## Required log prefixes

~~~text
[RedFox][PHONE]
[RedFox][PC]
[RedFox][PLATFORM]
[RedFox][BRIDGE]
[RedFox][BUY]
[RedFox][SELL]
[RedFox][STORE]
[RedFox][SCRAP]
[RedFox][BEAMBOOK]
[RedFox][IMPORT_EXPORT]
[RedFox][CLASSICS]
[RedFox][TOW]
[RedFox][SPONSOR]
[RedFox][FOXMAIL]
[RedFox][FOXTEXT]
[RedFox][QA]
~~~

JOB-11 will propose any new shared prefix through the job board rather than silently requiring it.

## Failure classification

Each failure report must identify the first failing layer when evidence permits:

~~~text
PACKAGING
INSTALL/COLLISION
PHONE
PC
PLATFORM/REGISTRY
APP UI
SHARED EVENT API
CAREER/RLS BRIDGE
STOCK/RLS GAME FUNCTION
DATA/PAYLOAD
RUNTIME UNKNOWN
~~~

If the evidence does not prove a layer, the report must say **RUNTIME UNKNOWN** instead of guessing.

## Initial triage workflow

1. Confirm the exact ZIP name, version, baseline, and installed mod list.
2. Remove duplicate/overlapping FoxNet packages from the test conditions.
3. Record the exact action, screen, game mode, and expected result.
4. Reproduce once with timestamps when safe.
5. Collect `beamng.log`, relevant rotated logs, and launcher log.
6. Filter RedFox prefixes and contract message names without deleting surrounding error context.
7. Identify the earliest provable failing layer.
8. Create TXT and HTML human-readable reports plus structured JSON/CSV evidence where useful.
9. Hand the failure to the owning job.
10. Block shipment when a required check fails.

## Verification plan

Before a candidate package is marked ready for integration, JOB-11 will verify:

1. ZIP integrity and one correct top-level layout.
2. No duplicate phone/PC/browser/platform core inside app packages.
3. No duplicate app IDs, event IDs, Angular/module/window IDs, or shared file collisions.
4. No `redfoxScrapYardDirect` or other prohibited startup Career module.
5. No startup `vehicleShopping` patch.
6. No hand-rolled money, inventory, garage, storage, insurance, or ownership system.
7. Required scope, TXT, HTML, JSON, CSV, file-inventory, and file-tree reports exist.
8. Existing phone, PC, RLS apps, and FoxNet sites are included in the runtime matrix.
9. Phone and PC use the same intended data and JOB-02 messages.
10. Installing, disabling, enabling, removing, and updating an app are covered where applicable.
11. Static results are labeled static.
12. Runtime behavior remains unproven until David tests it in BeamNG.

## Dependencies

- JOB-00 owns integration decisions and final release approval.
- JOB-01 publishes the platform, plugin, registration, theme, navigation, and shared UI event contracts.
- JOB-02 publishes the versioned Career/RLS bridge messages, payloads, and bridge logging.
- JOB-03 publishes the app manifest, Store state, installation, enable/disable, update, and permissions contracts.
- Every app job supplies its exact paths, manifest ID, expected events, protected files, test steps, and expected logs.
- JOB-11 may report a failure immediately but must not silently modify the owning job's source.

## Expected outputs

- Shared logging specification.
- Master static and BeamNG runtime test matrix.
- Standard failure-report template in TXT and HTML.
- Package/file collision and prohibited-file checklist.
- Installed-package fingerprint checklist.
- Per-build QA verdict format: PASS, FAIL/STOP, BLOCKED, or RUNTIME UNPROVEN.
- Optional debug/log viewer specification after platform contracts exist.
- No integrated ZIP until JOB-00 approves it.

## Current action

This update claims and documents JOB-11 only. It does not implement a debug app, change runtime code, or build a ZIP.

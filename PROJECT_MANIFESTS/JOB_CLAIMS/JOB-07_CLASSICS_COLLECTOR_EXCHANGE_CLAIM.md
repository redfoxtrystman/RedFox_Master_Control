# JOB-07 — Classics / Collector Exchange Claim

**Status:** CLAIMED  
**Owner:** Classics / Collector Exchange chat / Sol  
**Claim date:** 2026-07-13  
**Repository:** `redfoxtrystman/RedFox_Master_Control`

## Hello and coordination note

Hello, fellow RedFox job chats. I am the JOB-07 Classics / Collector Exchange chat. I will stay inside the Classics collector-market scope and use the shared contracts published by JOB-01, JOB-02, and JOB-03. I will not copy, replace, or work around another job's platform, bridge, store, or app files.

## Chosen scope

JOB-07 owns the buy-now collector/classic dealer page for:

- old vehicles;
- classics;
- muscle cars;
- rare trims;
- collector lots.

No auction behavior is in scope for the first version.

## Baseline inspection required before implementation

Before editing app code or building any ZIP, JOB-07 will inspect and report:

- the baseline ZIP or source tree approved by David / JOB-00;
- any existing Classics, collector, or classic-dealer page and asset paths;
- the JOB-01 phone/PC registration contract;
- the JOB-02 shared Career/RLS bridge contract;
- the JOB-03 app manifest and store-registration contract;
- the JOB-11 verification/report format when published;
- existing shared styles and images that may be referenced without editing their owners' files.

The exact implementation file list remains unproven until the baseline is supplied and inspected.

## Files JOB-07 may edit after inspection

Only:

- JOB-07-owned Classics / Collector Exchange page files;
- a JOB-07-owned app manifest or registration adapter that conforms to the published shared contracts;
- JOB-07-specific assets;
- JOB-07 change-scope, verification, inventory, file-tree, logging, and testing reports;
- this JOB-07 claim/coordination record.

No integrated FoxNet ZIP will be built until JOB-00 approves integration.

## Protected files and systems

JOB-07 will not edit or replace:

- phone, PC, browser, navigation, launcher, or shared UI shells owned by JOB-01;
- the shared Career/RLS bridge owned by JOB-02;
- App Store core or store state owned by JOB-03;
- Scrap Yard, BeamBook, Import/Export, Insurance/Finance/Garage/Storage, Tow/Recovery, SponsorHub, FoxMail, FoxText, Sponsor Rewards, FoxFax, QA core, or global visual-polish files;
- BeamNG/RLS money, inventory, ownership, garage, storage, finance, or insurance systems;
- startup Career modules or startup vehicle-shopping patches.

JOB-07 will not hand-roll money, inventory, ownership, garage, or storage behavior.

## Dependencies and requests to fellow chats

- **JOB-00:** provide or approve the exact baseline and integration point.
- **JOB-01:** publish the app/page registration and responsive phone/PC contract.
- **JOB-02:** publish the approved vehicle-data and buy-now bridge behavior. JOB-07 will use the existing shared message contract and will not invent a private bridge.
- **JOB-03:** publish the app manifest schema, category rules, permissions, and app-ID coordination process.
- **JOB-11:** publish the shared verification and failure-report format.

## Verification plan

Before any JOB-07 deliverable is offered for integration:

1. List the exact baseline ZIP and every edited file.
2. Confirm the diff contains only JOB-07-owned paths and reports.
3. Confirm the page is buy-now only and contains no auction flow.
4. Confirm phone and PC entry points use the same shared backend contract.
5. Confirm any buy action calls only the JOB-02-approved stock/RLS purchase path.
6. Confirm there is no custom money, inventory, garage, storage, ownership, startup Career module, or startup vehicle-shopping patch.
7. Validate manifest syntax, page assets, internal links, ZIP structure, file inventory, and required logging prefix `[RedFox][CLASSICS]`.
8. Include the required TXT, HTML, JSON, CSV, file-tree, logging, and testing reports.
9. Mark BeamNG runtime behavior unproven until David tests it in game.
10. Stop and report if any required check fails.

## Expected output

A JOB-07-scoped Classics / Collector Exchange page/app package and mandatory verification reports, ready for JOB-00 review and later integration. It will not be represented as runtime-tested until David confirms it in BeamNG.

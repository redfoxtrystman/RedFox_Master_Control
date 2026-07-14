# JOB-01 — Phone + PC Platform Core — Regular-Chat Takeover Record

**Date:** 2026-07-14  
**Timestamp:** 2026-07-14 12:27 PDT (America/Los_Angeles)  
**JOB:** JOB-01 — Phone + PC Platform Core  
**Owner:** one active regular ChatGPT JOB-01 chat / Sol, under David / Captain  
**Status:** CLAIMED — MIGRATION IN PROGRESS; LATEST BUILD IS BUILT — RUNTIME UNTESTED

## What changed

Ownership continuity for JOB-01 was transferred from the original ChatGPT Work chat to a new regular ChatGPT chat. This record does not create a second JOB-01 owner. It replaces the inaccessible chat as the active conversation responsible for the existing JOB-01 lane.

## Why it changed

The RedFox/FoxNet project chats were unintentionally created as ChatGPT Work chats. David was not aware that the entire coordinated project was subject to a separate Work-chat usage limit. On 2026-07-14 the original JOB-01 chat became inaccessible until 2026-07-20, interrupting development and testing. Manual migration was required to preserve continuity.

## Files affected by this change

- Added this takeover record only.
- No JOB-01 source, generated ZIP, RLS file, phone shell, PC shell, Career module, bridge, app-owned page, or other job's files were modified.

## Recovered GitHub state

- Draft PR: `#3` — `JOB-01: IceFox phone + PC platform core v0.2`
- PR branch: `agent/job01-platform-core-v0-1`
- PR head at takeover review: `83da4ad165d6347f7b7588a970f9cd1876df1b98`
- Platform contract: `job01.platform.v1`
- Built-in destination: `redfox.home`
- Current implementation version: `0.2.0`
- Current status: `BUILT — RUNTIME UNTESTED`
- Generated local test ZIP SHA-256 recorded by PR: `ba0ac46f5fefa0b3e59be2a651fcc32582a811f525a669d6ca47c8a86c3aa446`
- Exact RLS build-input SHA-256: `b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b`

## Preserved scope

JOB-01 owns only:

- existing RLS phone IceFox integration;
- existing RLS computer IceFox entry;
- shared phone/PC browser host;
- canonical app/page registration and route contracts;
- platform destination registry;
- host navigation and map-independent routing;
- platform-owned source, reports, and coordination documents.

JOB-01 does not own and must not implement:

- Career/RLS transaction authority or the JOB-02 bridge;
- App Store business logic;
- Scrap Yard, BeamBook, Import/Export, Classics, support, Tow/Recovery, SponsorHub, FoxMail, or FoxText business logic;
- money, inventory, vehicle ownership, garage, storage, insurance, missions, rewards, or save mutations;
- a replacement phone shell or replacement RLS computer shell.

## Current implementation state

The v0.2 source and contracts are preserved in draft PR #3. Static checks recorded by the PR pass for ZIP CRC, duplicate paths, JavaScript parsing, exact manifest/route/layout insertion counts, original IceFox logo identity, and SVG parsing. Runtime rendering and navigation remain unproven.

The build patches exactly two files from the pinned RLS 2.6.6 archive:

1. `ui/ui-vue/dist/index.js`
2. `lua/ge/extensions/ui/phone/layout.lua`

All other emitted runtime files are RedFox-owned JOB-01 files.

## Known problems and unproven items

- The exact v0.2 generated ZIP is not stored in GitHub and must be reuploaded or rebuilt from the pinned RLS archive.
- The original Work-chat transcript could not be retrieved through the available shared-link reader during takeover.
- BeamNG runtime has not been tested for phone icon rendering, phone launch, PC entry, PC launch, registry delivery, navigation controls, return-to-computer behavior, UI/controller behavior, or non-West-Coast map behavior.
- No post-test `beamng.log`, screenshots, or JOB-11 runtime verdict are recorded for v0.2.
- The draft PR is unmerged and must not be presented as a verified release.

## Required next steps

1. Recover or rebuild the exact v0.2 test ZIP and confirm SHA-256.
2. Test only with the pinned `rls_career_overhaul_2.6.6.zip`; disable older all-in-one FoxNet packages and Better Career for the test.
3. Run the documented West Coast USA test and one non-West-Coast map test.
4. Capture phone and PC screenshots plus `beamng.log`.
5. Submit evidence to JOB-11 for collision/logging/runtime review.
6. Keep status `BUILT — RUNTIME UNTESTED` until David tests the exact package.

## Migration note

The original Work chat became inaccessible because the separate Work-chat usage limit was reached. Access was blocked on July 14, 2026 and was shown as unavailable until July 20, 2026. This takeover preserves the existing JOB-01 implementation rather than restarting or replacing it.
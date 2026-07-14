# JOB-10 — Visual Design / Real Website Polish — Claim Record

**Status:** CLAIMED — MIGRATED TO REGULAR CHAT — BLOCKED  
**Owner:** JOB-10 — Visual Design / Real Website Polish regular-chat takeover / Sol, under David / Captain  
**Original claim date:** 2026-07-13  
**Regular-chat takeover date:** 2026-07-14 12:52 PDT

## Hello to the other RedFox job chats

Hello JOB-00 through JOB-12. JOB-10 has claimed the visual-design lane.

JOB-10 will make the RedFox FoxNet / IceFox pages feel like real websites and real phone apps while preserving the functional contracts owned by the other jobs. Send JOB-10 stable page outputs when they are ready; JOB-10 will return presentation-only changes and a visual verification report.

Special coordination with JOB-05: David wants BeamBook to become a Facebook-style social website with a functional vehicle marketplace. The current designed website and the working third-party BeamBook-style mod must both be inspected. JOB-05 owns BeamBook marketplace behavior and its safe integration. JOB-10 owns the approved visual layout, responsive presentation, CSS theme, cards, buttons, icons, and website polish.

## Current baseline inspection result

The control repository was searched for:

```text
BeamBook
redfoxCareerWeb
icefox_front
facebook
```

At the time of the original claim, no BeamBook source, FoxNet website source, CSS baseline, current Facebook-style site, or reference-mod source was present in the control repository.

GitHub now preserves nine BeamBook visual-reference screenshots, BeamBook content packs, exact baseline hashes/inventories, a JOB-05 standalone v0.1.0 runtime-untested candidate, and JOB-01 draft PR `#3` with shared IceFox phone/PC visual source. However, the exact current full IceFox/FoxNet ecosystem ZIP and the original third-party `beamBook.zip` reference binary are still not stored in GitHub.

Therefore JOB-10 remains claimed for coordination, but implementation is blocked until David supplies or identifies both required binaries:

1. David's current full IceFox/FoxNet website baseline.
2. The working third-party BeamBook-style reference mod.

Access to a reference mod is enough to inspect it. Any copied code or art must also be permitted for reuse.

## Files/folders JOB-10 will inspect now

```text
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_CLAIM.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_REGULAR_CHAT_TAKEOVER_2026-07-14.md
PROJECT_ASSETS/JOB-05_BEAMBOOK/
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-05_STANDALONE_BEAMBOOK_FINAL_HANDOFF_v0.1.0_2026-07-14.md
PROJECT_RELEASE_CANDIDATES/JOB-05/5-RedFox_BeamBook_Standalone_v0_1_0_RUNTIME_UNTESTED.zip
JOB-01 draft PR #3 / branch agent/job01-platform-core-v0-1
```

## Files/folders JOB-10 may edit now

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_CLAIM.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_REGULAR_CHAT_TAKEOVER_2026-07-14.md
JOB-10-owned visual documentation after baseline inspection
```

The Coordinator-authorized JOB-10 status fields on shared coordination records may be updated only to record this claim, migration, dependencies, and status.

No website or mod source file is authorized for editing yet. After both baselines are located and inspected, JOB-10 will publish a second scope record listing every exact HTML, CSS, icon, image, and layout file proposed for editing before implementation starts.

## Protected files and behavior

JOB-10 must not edit or replace:

```text
assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
lua/ge/extensions/career/
FoxFax art or FoxFax page files
shared bridge message names or payloads
purchase or sell behavior
money, inventory, garage, storage, insurance, or ownership behavior
phone shell, PC shell, browser shell, launcher, registry, or navigation behavior
BeamBook marketplace generation, persistence, or RLS integration logic
```

If an HTML or JavaScript component mixes layout and functional logic, JOB-10 must coordinate with the owning job and limit changes to approved presentation sections.

## Planned visual scope after baseline approval

- One coherent RedFox/FoxNet visual system across phone and PC.
- Facebook-style BeamBook social shell with vehicle Marketplace integrated into the site presentation.
- Realistic navigation, profiles, posts, seller information, listing cards, search/filter presentation, buttons, status chips, and empty/loading/error states.
- Responsive phone and PC layouts using the same functional backend.
- Shared visual tokens for color, typography, spacing, corners, shadows, focus, hover, disabled, warning, success, and error states.
- App Store presentation polish after JOB-03 stabilizes its behavior.
- Visual consistency passes for Scrap Yard, Import/Export, Classics, support pages, Tow/Recovery, and Sponsor apps after their owners deliver stable pages.
- Preserve David's approved artwork and existing site identity.

## Dependencies and handoffs

JOB-10 waits for:

```text
JOB-00 — baseline approval and integration approval
JOB-01 — stable phone/PC layout and registration boundaries
JOB-02 — shared bridge contract
JOB-03 — stable App Store structure and states
JOB-05 — stable BeamBook behavior and integration boundary
Other page owners — stable functional page handoffs
David — current full ecosystem ZIP and third-party BeamBook reference ZIP
```

JOB-10 may polish other app pages only after their owning job provides a stable page and exact coordination boundary.

## Verification plan

Before any visual build is offered:

1. Record the exact baseline names, sizes, and hashes.
2. Publish the exact file edit list and protected-file list.
3. Verify the diff contains only approved presentation files or approved presentation-only sections.
4. Confirm shared bridge messages and functional event handlers are unchanged.
5. Render and inspect desktop and phone layouts at agreed BeamNG/RedFox target sizes.
6. Check overflow, clipping, scroll behavior, navigation states, empty/loading/error states, keyboard focus, contrast, and asset links.
7. Exercise existing buttons and links to confirm visual changes did not disconnect them.
8. Produce the mandatory TXT, HTML, JSON, CSV inventory, file tree, and logging/testing reports.
9. Mark BeamNG runtime as unproven until David tests it in game.
10. Stop without shipping if a required check fails.

## Expected output

- An exact post-inspection JOB-10 edit manifest.
- Responsive real-website visual polish files.
- Before/after screenshots or mockups.
- Visual regression and scope-verification reports.
- No final or integrated ZIP until JOB-00 approves integration.

## Architecture and start-order acknowledgment — 2026-07-13

JOB-10 confirms and accepts the owner architecture and start order published in:

```text
PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md
```

Directive commit used:

```text
a05e06829548ddc4e7f5e39ac4a060eb57a0ef70
```

Rollcall and board-correction commit verified:

```text
4475437092b7e6012b6174d880210685a1eab928
```

JOB-10's active role remains:

```text
JOB-10 — Visual Design / Real Website Polish
```

JOB-10 accepts these operating boundaries:

- One shared IceFox/FoxNet front-door platform mod.
- Every actual page remains an isolated, removable add-on mod.
- Phone and PC open the same canonical registered destination; only responsive presentation differs.
- Pages must remain available across maps and must not assume a West Coast-only facility.
- App add-ons must not duplicate platform or bridge files.
- JOB-10 does not alter navigation behavior, bridge logic, purchases, money, ownership, storage, garage, insurance, or Career/RLS behavior.
- JOB-10 begins implementation only after JOB-00 freezes the baseline and JOB-01, JOB-02, and JOB-11 publish the required contracts and evidence rules.
- JOB-10 polishes a page only after its owning job provides a stable functional handoff.
- No visual build is called working, fixed, done, or runtime-proven until David tests it.

## Regular-chat takeover update — 2026-07-14 12:52 PDT

### What changed

- Transferred active conversation ownership from the inaccessible Work chat to the replacement regular chat.
- Preserved the exact JOB-10 number, title, scope, and protected boundaries.
- Linked the job-specific recovery record.
- Recorded the newly available GitHub visual references and the still-missing required binaries.
- Kept implementation blocked and did not edit runtime or website source.

### Why it changed

The original Work chat became inaccessible because the project was unintentionally subject to a separate Work-chat usage limit. Manual migration is required to restore continuity and prevent duplicate or conflicting work.

### Files affected

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_CLAIM.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_REGULAR_CHAT_TAKEOVER_2026-07-14.md
```

### Current status

```text
MIGRATED TO REGULAR CHAT — CLAIMED — BLOCKED — EXACT EDITABLE BASELINES MISSING
```

### Known problems

The shared chat is not retrievable; the current full IceFox/FoxNet ZIP and `beamBook.zip` are not stored in GitHub; any uncommitted JOB-10 work may be missing; related platform and BeamBook candidates remain runtime untested.

### Required next steps

1. Reupload the exact current ecosystem ZIP and `beamBook.zip` documented in the takeover record.
2. Perform an inspection-only baseline comparison.
3. Publish the exact editable/protected file manifest and target viewport requirements before code changes.

Takeover record:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_REGULAR_CHAT_TAKEOVER_2026-07-14.md
```

Takeover commit:

```text
1713002ab9344c766a3f8d80af821c8407320b8e
```

Current state: **MIGRATED TO REGULAR CHAT, CLAIMED, AND BLOCKED UNTIL THE EXACT EDITABLE BASELINES ARE INSPECTED.**
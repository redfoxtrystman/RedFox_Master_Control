# JOB-10 — Visual Design / Real Website Polish — Claim Record

**Status:** CLAIMED — MIGRATED TO REGULAR CHAT — VISUAL MOCKUP v0.1.0 BUILT — NOT INTEGRATED  
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

No BeamBook source, FoxNet website source, CSS baseline, current Facebook-style site, or reference-mod source was present in the control repository at the original claim time.

Therefore JOB-10 was initially claimed for coordination but blocked until David supplied or identified both baselines:

1. David's current Facebook-style website design/source.
2. The working BeamBook-style reference mod.

Access to a reference mod is enough to inspect it. Any copied code or art must also be permitted for reuse.

## Files/folders JOB-10 may inspect

```text
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_CLAIM.md
PROJECT_ASSETS/JOB-05_BEAMBOOK/
JOB-01 draft platform source and contracts
David-supplied visual/reference ZIPs in the active JOB-10 chat
```

## Files/folders JOB-10 may edit

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_CLAIM.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-10-owned visual handoffs
JOB-10-owned standalone visual mockup source and reports
Coordinator-authorized JOB-10 status fields on the shared job board
```

No integrated website or mod source file is authorized for editing until the owning job supplies a stable functional handoff and exact presentation-only boundary.

## Protected files and behavior

JOB-10 must not edit or replace:

```text
assets/js/icefox_front.js in the active platform baseline unless JOB-01 explicitly hands off presentation-only sections
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
lua/ge/extensions/career/
shared bridge message names or payloads
purchase or sell behavior
money, inventory, garage, storage, insurance, or ownership behavior
phone shell, PC shell, browser shell, launcher, or registry behavior
BeamBook marketplace generation or RLS integration logic
another job's functional files without written handoff
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
- Retain rotating ad locations for future humorous advertising packs.
- Use real in-game vehicle/configuration thumbnails at runtime rather than unrelated stock vehicle photos.

## Dependencies and handoffs

JOB-10 waits for:

```text
JOB-00 — baseline approval and integration approval
JOB-01 — phone/PC layout and registration boundaries
JOB-02 — shared bridge contract
JOB-03 — stable App Store structure and states
JOB-05 — stable BeamBook behavior and integration boundary
Feature jobs — stable page files and presentation-only edit boundaries
David — visual approval and any missing original artwork
```

JOB-10 may polish other app pages only after their owning job provides a stable page and exact coordination boundary.

## Verification plan

Before any integrated visual build is offered:

1. Record the exact baseline names and hashes.
2. Publish the exact file edit list and protected-file list.
3. Verify the diff contains only approved presentation files or approved presentation-only sections.
4. Confirm shared bridge messages and functional event handlers are unchanged.
5. Render and inspect desktop and phone layouts at agreed BeamNG/RedFox target sizes.
6. Check overflow, clipping, scroll behavior, navigation states, empty/loading/error states, keyboard focus, contrast, and asset links.
7. Exercise existing buttons and links to confirm visual changes did not disconnect them.
8. Produce the mandatory TXT, HTML, JSON, CSV inventory, file tree, and logging/testing reports.
9. Mark BeamNG runtime as unproven until David tests the exact integrated build.
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
- JOB-10 polishes a page only after its owning job provides a stable functional handoff.
- No visual build is called working, fixed, done, or runtime-proven until David tests the exact integrated build.

## Regular-chat migration note — 2026-07-14 12:52 PDT

The original Work chat became inaccessible because the separate Work-chat usage limit was reached. Active conversation ownership was transferred to this regular chat. Full shared-link transcript and attachment recovery was not possible. The project-wide incident and job-specific takeover record preserve the interruption, missing-context risk, duplicate-work risk, coordination problems, and unnecessary delay.

Takeover record:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_REGULAR_CHAT_TAKEOVER_2026-07-14.md
```

## Visual mockup checkpoint — 2026-07-14 14:03 PDT

David supplied the current visual/reference packages, including the combined RedFox website prototype, IceFox browser front page, BeamBook route prototype, the third-party BeamBook reference mod, real-site screenshot reference archive, FoxFax mascot art, RLS Career Overhaul 2.6.6, RLS evidence packs, and West Coast map reference archive.

JOB-10 created:

```text
RedFox_JOB10_Visual_Mockup_v0_1_0.zip
```

SHA-256:

```text
a44f146833dccbb5c17ee31cc6857cf8f3ffe6d1862dd62623bfab3cf2a3c0a6
```

Status:

```text
MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG
```

The standalone HTML prototype includes:

- IceFox browser navigation and address/search behavior;
- responsive desktop and phone presentation;
- BeamBook social feed and Marketplace;
- FoxNet Auctions filters, membership presentation and lot details;
- FoxFax report presentation using the approved female fox mascot;
- XXX Insurance quote presentation aligned to RLS coverage categories;
- Collector Exchange premium docket presentation;
- Parts Exchange search/store presentation;
- nautical Export Yard quote and tracking presentation;
- renameable Recovery company presentation;
- separate BackAlley.help illegal-network presentation;
- rotating humorous ad slots;
- intentional 404 page;
- current-map selector demonstrating that no West Coast-only facility is required.

No BeamNG, RLS, Career, bridge, platform, phone, PC, registry, purchase, money, inventory, ownership, garage, storage, insurance, mission, facility, or vehicle-shopping runtime file was edited or packaged.

Current state: **CLAIMED — MIGRATED — VISUAL MOCKUP v0.1.0 BUILT — AWAITING DAVID VISUAL REVIEW — NOT INTEGRATED.**
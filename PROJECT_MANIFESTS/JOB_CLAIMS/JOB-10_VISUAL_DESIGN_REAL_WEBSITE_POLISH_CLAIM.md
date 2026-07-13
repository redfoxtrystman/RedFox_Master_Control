# JOB-10 — Visual Design / Real Website Polish — Claim Record

**Status:** CLAIMED  
**Owner:** Visual Design / Real Website Polish chat / Sol  
**Claim date:** 2026-07-13

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

No BeamBook source, FoxNet website source, CSS baseline, current Facebook-style site, or reference-mod source is present in this control repository.

Therefore JOB-10 is claimed for coordination, but implementation is blocked until David supplies or identifies both baselines:

1. David's current Facebook-style website design/source.
2. The working BeamBook-style reference mod.

Access to a reference mod is enough to inspect it. Any copied code or art must also be permitted for reuse.

## Files/folders JOB-10 will inspect now

```text
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_CLAIM.md
```

## Files/folders JOB-10 may edit now

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-10_VISUAL_DESIGN_REAL_WEBSITE_POLISH_CLAIM.md
```

The Coordinator-authorized JOB-10 status fields on the shared job board may be updated only to record this claim.

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
phone shell, PC shell, browser shell, launcher, or registry behavior
BeamBook marketplace generation or RLS integration logic
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
JOB-01 — phone/PC layout and registration boundaries
JOB-02 — shared bridge contract
JOB-03 — stable App Store structure and states
JOB-05 — stable BeamBook behavior and integration boundary
David — current website baseline and BeamBook-style reference mod
```

JOB-10 may polish other app pages only after their owning job provides a stable page and exact coordination boundary.

## Verification plan

Before any visual build is offered:

1. Record the exact baseline names and hashes.
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

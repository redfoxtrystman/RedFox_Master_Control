# JOB-04 v0.3.7 + Browser Core v0.1.2 — Welcome Restore Audit

Date: 2026-07-30 PT

## Owner decision

David explicitly assigned this workstream responsibility for both:

- the FoxNet/IceFox welcome page and browser front-page experience;
- JOB-04 Wrecking Yard.

JOB-09 Tow/Recovery and JOB-13 Auction remain owned by their jobs. Their ZIPs were not edited.

## Failure being corrected

Browser Core v0.1.0 + JOB-04 slim v0.3.5 failed at runtime:

- Wrecking Yard loaded an old unstyled `index.html`;
- Wrecking Yard welcome card image was broken;
- the live browser icon appeared reverted;
- one required Wrecking Yard path mirror had been removed;
- browser asset names were reused, allowing stale WebUI route code.

The failed pair is rejected.

## New exact candidates

### Browser Core v0.1.2

`RedFox_FoxNet_Browser_Core_v0_1_2_WELCOME_RESTORE.zip`

- SHA-256: `c5aa126ec6fbc4794623c86111d3d204b4c004a9ada14c4c053bfe87cdf82d8b`
- ZIP bytes: 1,249,756
- Files: 59
- ZIP integrity: PASS
- Duplicate internal paths: 0

### JOB-04 Wrecking Yard v0.3.7

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_v0_3_7_WELCOME_RESTORE_REQUIRES_CORE_v0_1_2.zip`

- SHA-256: `a0dcf04bfe5cc64b938c55c1825b5f198b969c51c05fce6269557738e511d3d5`
- ZIP bytes: 160,935
- Files: 80
- ZIP integrity: PASS
- Duplicate internal paths: 0

## Browser Core corrections

- Restored the approved welcome-page HTML structure and visual design.
- PC CSS is byte-for-byte identical to the last working approved v0.3.4 style.
- Phone CSS is byte-for-byte identical to the last working approved v0.3.4 style.
- Preserved the owner-edited `ui/entrypoints/main/tiles/foxnet-browser.svg` byte-for-byte:
  - SHA-256: `7a835b81ab12dad2301aae4016c1c79ba8d5dab6818e66179b1bad0404056f08`
- Added new cache-safe assets:
  - `icefox_front_v012.css`
  - `icefox_front_v012.js`
  - `icefox_phone_v012.css`
  - `icefox_front_phone_v012.js`
- Converted old unversioned and v0.1.1 JS names into compatibility loaders that load v0.1.2.
- Wrecking Yard welcome card now uses the Core-owned static card asset instead of a cross-ZIP salvage image.
- Wrecking Yard routes to `index_v037.html` on PC and phone.
- Welcome page links to the existing standalone modules without changing them:
  - JOB-09: `ui/modules/apps/redfoxTowPortal/portal.html`
  - JOB-13: `ui/modules/apps/redfoxJob13Auctions_v012/site/index.html`
- Other feature cards retain the approved welcome-page design and show a styled not-installed message instead of loading a broken missing page.

## JOB-04 corrections

- Restored both required Wrecking Yard mounts:
  - `sites/scrap_yard/**`
  - `ui/modModules/redfoxCareerWeb/sites/scrap_yard/**`
- Both mirrors contain exactly the same relative paths and are byte-for-byte identical.
- Added current styled entry point `index_v037.html`.
- `index.html`, `index_v034.html`, `index_v035.html`, and `index_v036.html` are compatible styled entries that load v0.3.7 assets.
- Added compatibility JS names for stale cached HTML:
  - `scrap.js`
  - `scrap_v034.js`
  - `scrap_v035.js`
  - `scrap_v036.js`
- Preserved the approved junk inventory, native price/shop ID behavior, purchase adapter, selling, whole-car scrap, strip-and-scrap, returned parts, part sales, and catalytic-converter scrap.
- No Tow or Auction files are included.

## Collision correction

The two new ZIPs have zero overlapping internal file paths.

Root `info.json` files were removed to avoid a shared mounted root path. Metadata now uses unique paths:

- `mod_info/RedFoxFoxNetCore/info.json`
- `mod_info/RedFoxJOB04/info.json`

Neither new ZIP overlaps any internal path in the exact unchanged JOB-09 v0.4.4.3 or JOB-13 v0.1.2 ZIPs.

## Verification

The source trees passed 167 static checks.

The exact final ZIPs were extracted into fresh folders and passed the same 167 checks again:

- exact build-tree/file/hash parity;
- ZIP integrity;
- no duplicate paths;
- no unsafe paths;
- JSON parsing;
- SVG parsing;
- JavaScript syntax with Node;
- Lua syntax with `texlua loadfile`;
- local HTML references;
- exact Wrecking Yard mirror parity;
- cache compatibility filenames;
- owner icon hash;
- approved CSS hashes;
- PC/phone Wrecking Yard routes;
- installed Tow/Auction route targets when all exact packages are merged;
- no path overlap with JOB-09 or JOB-13.

A Chromium screenshot render was attempted in the analysis environment, but local HTTP and file navigation are blocked by the environment administrator. No visual-runtime claim is made from that attempt.

## Runtime status

`BUILT — STATICALLY VERIFIED — BEAMNG RUNTIME UNPROVEN`

## Required test

1. Remove Browser Core v0.1.0/v0.1.1 and JOB-04 v0.3.5/v0.3.6 plus all older full JOB-04 ZIPs.
2. Install only Browser Core v0.1.2 and JOB-04 v0.3.7.
3. Fully restart BeamNG.
4. Confirm the owner-edited FoxNet browser tile appears.
5. Open the browser and confirm the approved styled welcome page appears.
6. Confirm the Wrecking Yard welcome card image appears.
7. Open Wrecking Yard and confirm the page shows `v0.3.7` with full styling.
8. Confirm inventory loads and the game is not made significantly slower.
9. Test one inexpensive purchase only after the page and performance checks pass.
10. Add JOB-09 and JOB-13 one at a time after the Core + JOB-04 pair passes.

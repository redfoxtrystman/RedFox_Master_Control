# JOB-13 v0.1.7.2 — Phone-Only Direct Career Delivery Critical Repair

Date: 2026-07-31
Owner: David / Captain
Job: JOB-13 — FoxNet Online Vehicle Auctions
Source: `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_7_1_DROPDOWN_VISIBILITY_HOTFIX.zip`
Output: `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_7_2_PHONE_ONLY_DIRECT_CAREER_DELIVERY_FIX.zip`
SHA-256: `688922086ada71f2e7bdfa1635c823bfc1517d84badb759123dba23350c234f9`
ZIP bytes: 170,948
Runtime files: 25
Runtime status: STATIC/HARNESS VERIFIED — BEAMNG RUNTIME TEST REQUIRED

## Owner correction

JOB-13 is phone-only. This build does not add or require a computer-facing auction interface. Career garage systems are used only as the game's authoritative storage and delivery backend.

## Runtime failure repaired

The prior build entered RLS through `openPurchaseMenu` and `buyFromPurchaseMenu`. That menu-oriented dealership lifecycle could remain half-open after an auction vehicle was retrieved, causing repeating interaction sounds, global garage-interface lockout, phone lockout, Escape/menu lockout, severe lag, and blank garage thumbnails.

## Exact repair

- Removed all JOB-13 calls to `openPurchaseMenu` and `buyFromPurchaseMenu`.
- Removed temporary dealership/shop records.
- Removed any settlement call to `career_career.closeAllMenus()`.
- Auction purchase now uses Career/RLS primitives directly: Career cash, exact model/config spawn without auto-enter, native part-condition initialization, inventory add, native garage assignment, default insurance hook, delivery access delay, auction metadata, native thumbnail capture, and save cleanup.
- The temporary world object is removed only after native thumbnail saving finishes, then Career saves again so the vehicle is stored instead of left spawned.
- Persistent request IDs still prevent duplicate charges and duplicate vehicles.

## Preserved behavior

Auction inventory, cached varied pool, bidding, NPC bidding, Quick Bid, upcoming lots, watchlist, phone alerts, membership, fees, and dropdown CSS are unchanged from v0.1.7.1. The four runtime JavaScript/CSS files are byte-for-byte identical.

## Files changed

- `lua/ge/extensions/redfoxJob13Auction.lua`
- JOB-13 version metadata/runtime note
- JOB-13 auction HTML version labels/cache query only
- JOB-13 UI App metadata/version only

No Wrecking Yard, Tow/Recovery, BeamBook, Welcome/Home, phone layout, computer module, RLS source file, or main UI bundle was changed.

## Verification

- Fresh ZIP integrity: PASS
- Duplicate internal paths: NONE
- Lua syntax via Lua 5.4 parser: PASS
- JavaScript syntax: PASS
- JSON parsing: PASS
- Forbidden dealership/menu settlement calls: NONE
- Shared main UI/phone-layout overrides: NONE
- Direct delivery harness: PASS
- Career cash unchanged before native inventory completion: PASS
- Career cash deducted exactly once after inventory completion: PASS
- Exact model/config spawn: PASS
- Auto-enter disabled: PASS
- Native garage assignment: PASS
- Native delivery delay: PASS
- Auction metadata saved to inventory: PASS
- Thumbnail save requested: PASS
- Temporary world object removed after thumbnail save: PASS
- Phone notification sent: PASS
- Repeated settlement request does not charge twice: PASS

## Required runtime test

David must test this exact ZIP in BeamNG. The repair is not considered proven until phone access, Escape/menu access, garage retrieval, vehicle entry/exit, thumbnail generation, and restart persistence all pass.
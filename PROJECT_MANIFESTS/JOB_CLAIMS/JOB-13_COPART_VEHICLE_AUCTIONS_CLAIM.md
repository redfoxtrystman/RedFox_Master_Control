# JOB-13 — Copart-Style Vehicle Auctions — Active Claim

**Date:** 2026-07-29 12:22 PDT  
**Owner:** David / Captain  
**Active chat responsibility:** JOB-13 — Copart-style Vehicle Auctions  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**Status:** BASELINE INSPECTED — RESEARCH / ARCHITECTURE — NO JOB-13 BUILD YET

## Owner assignment

David explicitly assigned a new job on July 29, 2026:

```text
JOB-13 — Copart-style Vehicle Auctions
```

The existing central board currently defines only JOB-00 through JOB-12. This claim records David's direct assignment without renumbering, merging, or taking ownership of another job. A central-board expansion should be coordinated with JOB-00 so the official job map remains internally consistent.

## Exact scope

JOB-13 owns a separate FoxNet auction website/app inspired by the functional patterns of Copart and Bar None Auction / HiBid:

- public vehicle and equipment auction catalog
- auction calendar and sale events
- lot pages and image/details presentation
- watchlist and saved lots
- pre-bidding
- live or timed bidding
- confidential maximum/proxy bids
- NPC bidder competition in single-player BeamNG
- reserve, pure-sale, seller-approval, sold, and no-sale outcomes
- bidder registration or membership
- buyer fees and invoices
- payment settlement through the approved shared RLS/Career bridge
- pickup, storage, delivery, and garage placement through approved shared systems
- player-owned vehicle consignment when explicitly enabled
- optional physical West Coast auction-yard experience

## Scope boundaries

JOB-13 does not own or replace:

- JOB-01 phone/PC platform shell or routing
- JOB-02 shared RLS/Career bridge
- JOB-05 BeamBook private marketplace
- JOB-07 Classics / Collector Exchange
- JOB-08 insurance, finance, garage, or storage systems
- JOB-09 towing/recovery/dispatch systems
- JOB-10 shared visual-design system
- JOB-11 shared QA/logging system

JOB-13 must be packaged as an isolated, removable site/app and must use the same destination and backend messages from both phone and PC.

## Hard architecture rules

1. Do not embed the finished auction business logic in the shared FoxNet root `assets/js/app.js`.
2. Do not create a second phone, PC, browser shell, platform registry, money system, inventory system, garage system, or delivery system.
3. Do not report a spawned vehicle as a completed purchase.
4. A won vehicle is complete only after one real charge, one real ownership record, and one valid storage/delivery result.
5. All transaction operations must be idempotent so a repeated UI callback cannot charge twice or add the same vehicle twice.
6. Online auctions must work on every supported map. The West Coast auction yard may be optional but cannot be required.
7. The web UI is untrusted. All bid validation, balance checks, lot state, settlement, and ownership changes must be enforced in Lua through the shared bridge.
8. No startup patch of `career_modules_vehicleShopping` is approved for JOB-13.
9. No integrated build may be labeled working until David tests the exact ZIP in BeamNG.

## Baseline files inspected

### `1.zip`

- Size: 43,398,480 bytes
- SHA-256: `f6aceaf436af2abf36388b69f287e30a6eb59d3dc0d1089da3f4ac0771f1419b`
- Contains a substantial physical used-car auction implementation:
  - `lua/ge/extensions/career/modules/usedCarAuction.lua`
  - `lua/ge/extensions/career/modules/usedCarAuctionLots.lua`
  - `lua/ge/extensions/career/modules/usedCarAuctionNpcs.lua`
  - `ui/modModules/usedAuction/*`

### `west_coast_usa.zip`

- Size: 117,945,400 bytes
- SHA-256: `01a8a0b54314adeca3bcf5a23df9c081945f8d49b54d10ae4ba4e81cd6464d77`
- Contains the physical Auction House / Vault site, triggers, lights, emitters, `auction.sites.json`, and `auction.filters.json`.

### `RedFox_JOB10_Full_Websites_v0_3_2_REALISTIC_WELCOME.zip`

- Size: 31,275,171 bytes
- SHA-256: `fab5913a9d1b580b0ff32d6ea6d53d8f8983fe2b9ddf9110aa79742c7679b5e5`
- Contains a visual FoxNet Auctions prototype at `https://auctions.foxnet.redfox`.
- The prototype is embedded in the shared root SPA and uses mock/localStorage data. It is reference artwork only, not a transaction backend.

### `beamBook.zip`

- Size: 9,867 bytes
- SHA-256: `2b8ac94018b9ca2c0c04bba597ad4316e177c9a4fd666b408392ad6d5becccc9`
- Contains useful listing-generation and value/mileage patterns.
- Its `vehicleShopping` monkey-patch pattern is not approved for JOB-13.

## Current findings

The physical auction engine already proves or substantially implements:

- eligible configuration generation
- category filters and auction tiers
- spawned lot vehicles and lane movement
- player bids
- NPC personalities and competitive bidding
- anti-snipe timer extension
- real Career payment calls
- free-garage-space checks
- real inventory ownership and garage movement
- player vehicle consignment
- payout and removal of sold consignments
- save hooks and auction UI state

It does not yet provide the required FoxNet online auction service. It is tightly coupled to a West Coast physical venue, spawned vehicles, short live sessions, and its current Angular overlay.

## Protected files

Until integration approval, JOB-13 will not overwrite or package:

- shared phone or PC shell files
- shared FoxNet root app files
- another job's app or website
- shared bridge files owned by JOB-02
- shared garage/storage/insurance files owned by JOB-08
- shared tow/delivery files owned by JOB-09
- shared QA/logging files owned by JOB-11
- stock BeamNG Career modules unless a narrowly scoped compatibility change is separately approved

## Dependencies

- JOB-01: route and app registration contract
- JOB-02: authoritative money, inventory, purchase, sale, and save bridge
- JOB-08: garage capacity, storage, invoice/finance integration if applicable
- JOB-09: optional pickup/towing/delivery integration
- JOB-10: shared FoxNet visual language
- JOB-11: verification, logs, failure reports, and test matrix

## Verification plan

Before any release candidate:

1. Static ZIP integrity and file-inventory audit.
2. No duplicate shared platform or bridge files.
3. Lua syntax checks and JSON validation.
4. Deterministic lot/state serialization tests.
5. Bid validation and proxy-bid unit tests.
6. Repeated-callback/idempotency tests.
7. Insufficient-money and full-garage failure tests.
8. Save/reload during pre-bid, live bidding, invoicing, and delivery.
9. Cross-map test matrix.
10. Exact-ZIP runtime testing by David.

## Next concrete action

Produce the JOB-13 online-auction service specification and exact file/edit inventory, then separate the reusable auction-domain logic from the physical West Coast presentation. The first runtime target should be a standalone, all-map timed auction catalog with real bidding state but no shared-platform overwrite.
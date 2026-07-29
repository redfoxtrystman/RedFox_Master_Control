# JOB-04 — RedFox Wrecking Yard v0.3.1

## Runtime closure for v0.3.0

Exact tested build:

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_2317PT_v0_3_0_DIRECT_NATIVE_PRICES_VERSIONED_ASSETS_CYCLING_FROM_v0_2_9.zip`
- SHA-256: `b8809bce620e2d66e58b2f18cd6be8c17df5463a3c111d2af9c0519f91114d71`

Owner screenshots confirm a **partial pass and working rollback base**:

- Prices vary correctly, including examples at $300, $500, $1,400, $4,100, $5,500, $7,200, $12,700 and $29,000.
- Native listing IDs remain present.
- Negotiation availability remains present.
- Wrecking-yard and Joe's Junk configurations appear.
- Cycle 0 changes to Cycle 1 and the visible cars change.
- 36 cars render quickly from the loaded pool.

Remaining v0.3.0 issues:

- The source pool is BeamBook-only instead of using selected native dealerships.
- Technical/debug wording is visible to the player.
- `Bridge Status`, unfinished quote/scrap controls, native source counts, shop-ID language, cycle counters and unsupported condition wording should not appear in the finished page.

Decision:

- Keep v0.3.0 as the rollback base.
- Build v0.3.1 as a narrow source-pool and player-facing cleanup patch.

## Source

- Source ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_2317PT_v0_3_0_DIRECT_NATIVE_PRICES_VERSIONED_ASSETS_CYCLING_FROM_v0_2_9.zip`
- Source SHA-256: `b8809bce620e2d66e58b2f18cd6be8c17df5463a3c111d2af9c0519f91114d71`
- Source runtime: **PARTIAL PASS / KEEP AS ROLLBACK BASE**

## Output

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-29_0848PT_v0_3_1_MULTI_SOURCE_CLEAN_UI_FROM_v0_3_0.zip`
- SHA-256: `1d75d10ab9c814197f5264d5a9df6042d0269e218d06c323717a724b6c7f4be4`
- Size: `25,465,240 bytes`
- ZIP entries: `1,461`
- Duplicate internal paths: `0`
- ZIP integrity: **PASS**
- Runtime: **UNPROVEN**

## Owner-selected native sources

The RedFox yard pool now recognizes native listings from these sources when present:

- Joe's Junk
- Slop Gear Garage
- Smash Rollers
- Trusted Auto Sales
- Private sellers
- BeamBook/private online listings
- Jefferson Motors
- Soliad Online Dealership
- Import Dealership

Strong project/junk configuration names from other sources may also qualify.

## Architecture

v0.3.1 does not create a new purchase record and does not clone native vehicle listings.

The active page:

1. Reads the current native `vehiclesInShop` list once.
2. Optionally synchronizes BeamBook/private listings when BeamBook is installed.
3. Builds one RedFox-visible yard pool using source allowlist and project/work/age/mileage/value filters.
4. Keeps the native asking price, native `shopId`, mileage, year, seller record and negotiation flag unchanged.
5. Renders 36 cards in two browser batches of 18.
6. Rotates another visible selection locally when `Show Different Cars` is pressed.
7. Re-reads current native stock and refreshes BeamBook/private fallback stock when `Refresh Yard Stock` is pressed.

## Player-facing cleanup

Removed from the active page:

- `Bridge Status`
- Native source-count wording
- Shop-ID wording
- Cycle-number wording
- `Generate New Source Pool`
- `Cycle Yard Inventory`
- Listing ID field
- `Condition class`
- Unfinished quote, scrap-rate, owned-vehicle, services, rules and bridge panels
- Technical payout/source explanations

Replacements:

- `Show Different Cars`
- `Refresh Yard Stock`
- Plain summary: vehicle count and simple browsing instruction
- `Yard category` using factual categories instead of unsupported damage claims
- Clean RedFox-only card branding
- Known source suffixes such as `( Joe's Junk Career )` are removed from the displayed title only; the native record remains unchanged

## Protected behavior

Not changed:

- Native prices
- Native shop IDs
- Native negotiation
- Native mileage/year data
- Online purchase relay
- IceFox welcome-page no-load behavior
- Global Vue bundle
- Selling/scrapping backend

## Exact changed files

Changed:

```text
assets/js/icefox_front.js
info.json
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
```

Added:

```text
sites/scrap_yard/index_v031.html
sites/scrap_yard/assets/js/scrap_v031.js
sites/scrap_yard/assets/config/wrecking_yard_mix_v031.json
ui/modModules/redfoxCareerWeb/sites/scrap_yard/index_v031.html
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap_v031.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/config/wrecking_yard_mix_v031.json
OPEN_ME_FIRST_JOB-04_Wrecking-Yard_2026-07-29_0848PT_v0_3_1.txt
VERIFY_JOB-04_Wrecking-Yard_2026-07-29_0848PT_v0_3_1.json
VERIFY_POST_EDIT_JOB-04_v0.3.1_60_CHECKS.json
docs/job04_v031_multi_source_clean_ui/*
ui/modModules/redfoxCareerWeb/docs/job04_v031_multi_source_clean_ui/*
```

No files were removed.

## Verification

The final ZIP was extracted into a new clean folder and verified from the packaged files.

Passed:

- 60 static and structural checks
- Mirrored HTML identical
- Mirrored JavaScript identical
- Mirrored config identical
- Node syntax for both Wrecking Yard scripts and all three changed route scripts
- JSON parsing
- Versioned v0.3.1 page, script and config routes
- Old v0.3.0 route removed from active route files
- All new HTML local references exist
- No player-facing Bridge Status, native source counts, shop-ID wording, cycle counters, listing IDs or condition-class wording
- No price-field writes
- No shop-ID writes
- Native all-shop data read present
- No BeamBook-only browser filter
- All selected source rules present
- Project and work quotas present
- Duplicate event-listener guard present
- ZIP integrity and duplicate-path checks

Packaged JavaScript fixture test:

```text
110 total simulated native listings
109 eligible candidates
36 selected
16 project entries
5 work/special entries
Cycle 0 and Cycle 1 differ
Native Value priority: PASS
Zero-value fallthrough: PASS
Native shop IDs preserved: PASS
Unknown clean dealer excluded: PASS
Strong project fallback eligible: PASS
```

## Known limits

- Runtime purchase completion still requires BeamNG testing.
- `Refresh Yard Stock` regenerates BeamBook/private fallback listings when available and re-reads all current native dealer stock; it does not forcibly rewrite every dealership's inventory.
- Physical damage, missing parts, rust, stripping and scrapping remain deferred.

## Required runtime test

1. Disable v0.3.0 and all older JOB-04 ZIPs.
2. Install v0.3.1.
3. Fully restart BeamNG.
4. Confirm the small `v0.3.1` badge.
5. Confirm no technical native-source, shop-ID, cycle-counter or Bridge Status text appears.
6. Confirm the list populates quickly.
7. Confirm a broader mix of junk/project vehicles from the selected native sources appears.
8. Press `Show Different Cars` and confirm the visible cars change immediately.
9. Press `Refresh Yard Stock` and confirm the list reloads.
10. Open a negotiable listing.
11. Complete one phone purchase and one PC purchase.
12. Verify money, delivery, ownership, inventory, storage and duplicate spawning.

## Next action

Do not build v0.3.2 until the exact v0.3.1 runtime result is recorded in issue #30 with keep/reject/rollback status.

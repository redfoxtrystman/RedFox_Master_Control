# JOB-04 — RedFox Wrecking Yard v0.3.2

## Source

- Source ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-29_v0_3_1_REDFOX_BROWSER_ICON_ONLY- new phone icon.zip`
- Source SHA-256: `eafbe5618f6e97a14e872d071528f9fd8f450586dc9f7ff28ba55063bda1f4b2`
- Additional catalog source: `Undesireables.zip`
- Undesireables SHA-256: `0236256f77ab4f8e9df5327bff0323d57fe973e7bca65a73b43026abc29e5146`

## Owner request

Keep the fast working v0.3.1 native listing path, but stop showing expensive high-end dump trucks, construction/mining equipment and unrelated specialty vehicles. Make the Wrecking Yard show mostly Joe's Junk, rough/low-value configurations from Undesireables, strong junk/project vehicles and selected tow/recovery vehicles.

## Confirmed v0.3.1 cause

- Nine marketplace/dealership sources were allowed.
- The broad work/special keyword group treated truck, semi, bus, tanker, crane, forklift, crawler, fire truck and ambulance as desirable yard inventory.
- Work/special listings were allowed up to $175,000 and model year 2020.
- This admitted clean or expensive heavy equipment that did not fit the intended wrecking-yard inventory.

## Output

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-29_2120PT_v0_3_2_JUNK_FOCUSED_JOES_UNDESIREABLES_FROM_ICON_v0_3_1.zip`
- SHA-256: `874f817f61bf7c32498d92f0a29d2c34ff1b5d6a01203a3ec94729d86e03cf76`
- Size: `25,408,916 bytes`
- ZIP entries: `1,017`
- Duplicate paths: `0`
- Unsafe paths: `0`
- Runtime: **UNPROVEN** until David tests this exact ZIP in BeamNG.

## Implementation

### Read-only Undesireables catalog

- Parsed all 268 `vehicles/*/info_*.json` configuration records from `Undesireables.zip`.
- Added only a read-only matching catalog containing model, config key, configuration name, description and catalog value.
- Did not copy or modify any Undesireables `.pc`, image or vehicle files.
- Undesireables remains a separate mod.

### New versioned assets

- `sites/scrap_yard/index_v032.html`
- `sites/scrap_yard/assets/js/scrap_v032.js`
- `sites/scrap_yard/assets/config/wrecking_yard_mix_v032.json`
- `sites/scrap_yard/assets/config/undesireables_catalog_v032.json`
- Mirrored copies under `ui/modModules/redfoxCareerWeb/sites/scrap_yard/`

### Junk-focused eligibility

Priority order:

1. Joe's Junk listings under the yard cap with junk/project, catalog, low-price, old-year or high-mileage evidence.
2. Exact low-value Undesireables configuration matches from any native source.
3. Selected tow, wrecker, rollback, flatbed and recovery vehicles within age/mileage/price limits.
4. Strong project/junk/beater/stripped/abandoned configurations.
5. Very limited older/high-mileage fallback inventory from Slop Gear, Smash Rollers, private/BeamBook and Trusted Auto.

Blocked by default:

- dump trucks and dumpers
- mining and quarry vehicles
- concrete/cement mixers
- excavators, loaders, bulldozers, graders and compactors
- forklifts and construction cranes
- airport tugs, aircraft and helicopters
- yachts and speedboats
- race buses, fire trucks and ambulances
- any listing over the absolute $100,000 cap
- clean modern semis/trucks that lack junk, catalog or tow/recovery evidence

### Native behavior preserved

- No price rewriting.
- No synthetic shop IDs.
- No seller rewriting.
- No negotiation override.
- No manual money, ownership, delivery, inventory or storage logic.
- Existing `RedFoxScrapYardOpenPurchaseMenu` bridge preserved.
- `Show Different Cars` remains instant.
- `Refresh Yard Stock` still refreshes the native/BeamBook source pool.
- Owner-updated browser/phone icon preserved byte-for-byte.

## Existing files changed

- `info.json`
- `assets/js/icefox_front.js` — route only: `index_v031.html` → `index_v032.html`
- `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js` — route only
- `ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js` — route only

Protected and unchanged:

- `ui/ui-vue/dist/index.js`
- `ui/entrypoints/main/tiles/foxnet-browser.svg`
- BeamBook source
- Undesireables source
- Career/RLS transaction logic

## Verification

Pre-package verification: **49/49 PASS**.

Post-package fresh extraction:

- Packaged file set exactly matched the build folder: PASS
- All 1,017 packaged file hashes matched: PASS
- ZIP integrity: PASS
- Duplicate/unsafe paths: PASS
- Node syntax for both Wrecking Yard JS copies and three route scripts: PASS
- Mirrored JS/HTML/config/catalog byte identity: PASS
- JSON parsing: PASS
- Catalog entry count 268: PASS
- Owner icon hash unchanged: `7a835b81ab12dad2301aae4016c1c79ba8d5dab6818e66179b1bad0404056f08`
- Active route points only to `index_v032.html`: PASS
- Native price test: `Value=43210` remained `43210`, not fallback `$500`: PASS
- Native shop IDs preserved: PASS
- Cycle produced a different visible selection: PASS

Fixture classifications:

- Joe's rusty beater → `joe`: PASS
- Undesireables `Stowaway (M)` → `undesireable`: PASS
- modern dump truck → excluded: PASS
- mobile crane → excluded: PASS
- old rollback tow truck → `tow`: PASS
- clean modern luxury car → excluded: PASS
- $700,000 mining dump truck → excluded: PASS
- stripped Slop Gear project → `project`: PASS
- old high-mileage BeamBook sedan → `fallback`: PASS
- clean modern premium semi → excluded: PASS

Mixed fixture selected 36 cars from:

- 16 Joe's Junk
- 14 Undesireables
- 8 project cars
- 5 tow/recovery vehicles
- 12 dump trucks present in source but zero admitted

## Runtime test

1. Disable v0.3.1 and every older JOB-04 ZIP.
2. Keep RLS, BeamBook and `Undesireables.zip` enabled.
3. Install the exact v0.3.2 ZIP and fully restart BeamNG.
4. Confirm the visible `v0.3.2` badge.
5. Confirm most visible cars are Joe's Junk, Undesireables oddballs, stripped/project cars or rough tow/recovery vehicles.
6. Confirm expensive dump trucks, mining/construction equipment, aircraft and boats do not appear.
7. Confirm native prices vary and negotiation remains available where supported.
8. Use `Show Different Cars` and confirm another junk-focused selection appears instantly.
9. Use `Refresh Yard Stock` and confirm the source pool refreshes.
10. Complete one phone purchase and one PC purchase; verify money, delivery, ownership, inventory, storage and no duplicate spawn.

## Next gate

Do not build v0.3.3 until this exact v0.3.2 runtime result is recorded in issue #30 with keep/reject/rollback status.

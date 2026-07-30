# JOB-04 v0.3.3 — Owned Vehicle Sales, Scrap, Returned Parts and Catalytic Converters

**Built:** 2026-07-30 11:29 PT  
**Owner:** David / Captain  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Runtime:** UNPROVEN until David tests the exact ZIP in BeamNG

## Source

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-29_2120PT_v0_3_2_JUNK_FOCUSED_JOES_UNDESIREABLES_FROM_ICON_v0_3_1.zip
SHA-256: 874f817f61bf7c32498d92f0a29d2c34ff1b5d6a01203a3ec94729d86e03cf76
```

v0.3.2 browse-inventory tuning was explicitly closed as **UNTESTED / DEFERRED** by owner direction. v0.3.3 preserves its browse selection and moves to owned-vehicle disposition.

## Output

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1129PT_v0_3_3_OWNED_SALES_SCRAP_RETURNED_PARTS_CATS_FROM_v0_3_2.zip
SHA-256: 3ccd8e440c0b74581218cea08c55f72b1480b46b0fbb68d0cbcb6f10af84884f
Size: 25,541,247 bytes
ZIP files: 1,034
Duplicate internal paths: 0
Unsafe paths: 0
ZIP integrity: PASS
```

## Owner request implemented

- Sell owned Career/RLS vehicles.
- Scrap a whole owned vehicle.
- Strip and scrap a vehicle while returning every verified installed part.
- Sell returned parts individually.
- Scrap stored catalytic converters (`cats`).
- Preserve actual part/condition data when available.
- Do not continue browse-stock filtering in this version.

## Customer-facing features

### My Vehicles & Scrap
Loaded only when the player opens the section; no Career inventory enumeration occurs on the IceFox welcome page.

Actions:

```text
Sell Vehicle
Scrap Whole Vehicle
Strip & Scrap Shell
```

`Sell Vehicle` continues through the existing native Career/RLS relay:

```text
career_modules_inventory.sellVehicleFromInventory(inventoryId)
fallback: career_modules_inventory.sellVehicle(inventoryId)
```

JOB-04 does not rewrite the normal sale price.

### Scrap Whole Vehicle

- Uses exact authoritative inventory ID.
- Persists a unique request/transaction ID.
- Removes and verifies the exact vehicle once.
- Credits the scrap payout once.
- Returns no parts, as clearly stated in the confirmation.
- Leaves a persistent payment-pending state if vehicle removal succeeds but payment fails.

### Strip & Scrap Shell

- Requires an exact installed-parts map from the Career inventory record.
- Stages every installed part in persistent RedFox storage **before** destructive vehicle removal.
- Removes and verifies the exact vehicle once.
- Activates all staged parts as player-owned returned parts.
- Credits shell/frame scrap only because the player retains the parts.
- Blocks the action and preserves the vehicle when exact installed-part data is unavailable.
- Does not invent fake parts, damage, engines or transmissions.

### Returned Parts

Each returned part preserves, when available:

```text
part ID
slot
part/config name
source vehicle inventory ID
source vehicle name
condition/wear snapshot
estimated value
catalytic-converter flag
transaction/source reference
```

Actions:

```text
Sell Part
Scrap Cat (verified converter/catalyst parts only)
```

All parts remain in storage until the player explicitly disposes of that individual part.

## Transaction protections

- Persistent request IDs.
- Persistent transaction states and audit log.
- Idempotent replay for completed vehicle transactions.
- Parts staged before vehicle removal.
- Failed vehicle removal rolls staged parts back.
- Part reserved before payment and consumed after payment.
- Non-catalytic parts cannot use Scrap Cat.
- `payment_attempting` is not automatically paid a second time after an interrupted attempt because the previous result may be uncertain.
- Payment-failed vehicle removals can be retried through the pending-transaction panel.

## Browse inventory preservation

The v0.3.2 browse behavior was verified unchanged:

- v0.3.3 mix configuration is byte-identical to v0.3.2.
- v0.3.3 Undesireables catalog is byte-identical to v0.3.2.
- A 120-listing JavaScript fixture produced the same 36 visible shop IDs in v0.3.2 and v0.3.3.
- Native prices, seller records, shop IDs and negotiation remain untouched.

## Changed files

```text
MODIFIED assets/js/icefox_front.js
MODIFIED info.json
MODIFIED lua/ge/extensions/redfox/career/scrapyardBridge.lua
MODIFIED lua/ge/extensions/redfox/career/scrapyardCef.lua
MODIFIED lua/ge/extensions/redfox/career/scrapyardRates.lua
MODIFIED lua/ge/extensions/redfox/career/scrapyardStorage.lua
ADDED sites/scrap_yard/index_v033.html
ADDED sites/scrap_yard/assets/js/scrap_v033.js
ADDED sites/scrap_yard/assets/css/scrap_v033.css
ADDED sites/scrap_yard/assets/config/wrecking_yard_mix_v033.json
ADDED sites/scrap_yard/assets/config/undesireables_catalog_v033.json
MODIFIED ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
MODIFIED ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
ADDED mirrored v0.3.3 HTML/JS/CSS/config/catalog files under ui/modModules/redfoxCareerWeb/sites/scrap_yard/
ADDED embedded TXT/JSON/HTML verification reports and changed-file CSV
```

## Protected files verified unchanged

```text
ui/ui-vue/dist/index.js
SHA-256: c172e9c480354f2b2f84c94a5135bbc78460e4d24c963f15c56ff1df4779e355

ui/ui-vue/dist/index.css
SHA-256: 957da302d3e509968ccd6cd3dea64637779ec0df745f3c1588f890aefb8d6b00

ui/entrypoints/main/tiles/foxnet-browser.svg
SHA-256: 7a835b81ab12dad2301aae4016c1c79ba8d5dab6818e66179b1bad0404056f08
```

The owner-edited phone/browser icon is byte-for-byte preserved.

## Verification performed before packaging

- Five changed/related Lua files parsed through system `liblua5.4`: PASS.
- `scrap_v033.js`: Node syntax PASS.
- PC root shell JS: Node syntax PASS.
- PC mirrored shell JS: Node syntax PASS.
- Phone relay JS: Node syntax PASS.
- JSON parse for info/config/catalog: PASS.
- Mirrored HTML/JS/CSS/config/catalog hashes: PASS.
- Route-only changes point all hosts to `index_v033.html`: PASS.
- No active host route remains on `index_v032.html`: PASS.
- Exact changed-code scope check: PASS.
- No custom native vehicle-sale implementation in active Scrap Yard Lua: PASS.
- Missing exact parts block destructive stripping: PASS.
- No legacy engine/transmission dark-part routing: PASS.

## Runtime mock tests

### Transaction harness

PASS:

```text
owned dashboard enumeration
whole vehicle scrap
exact vehicle removal verification
Strip & Scrap Shell
all exact parts returned
normal part sale
catalytic-converter scrap
money credit
completed-request replay
```

### Safety harness

PASS:

```text
missing part map blocks stripping
blocked stripping preserves vehicle
non-cat Scrap Cat request rejected
rejected cat request preserves part
replayed strip request does not duplicate parts
```

### Failure found and corrected before delivery

The first transaction harness failed because `positiveNumber(...)` passed multiple `select(...)` return values into `tonumber`, causing a Lua argument error. The code was corrected by forcing a single selected value, then all syntax, transaction, safety and packaged tests were rerun and passed. No failed ZIP was delivered.

## Post-package verification

The final ZIP was extracted into a fresh directory and checked again:

```text
1,034 extracted files
exact hash parity with build tree
Lua syntax PASS
JavaScript syntax PASS
transaction harness PASS
safety harness PASS
v0.3.2/v0.3.3 browse parity PASS
owner icon unchanged
protected Vue bundle/CSS unchanged
route checks PASS
embedded verification report PASS
```

## Known limits

- Exact part return depends on the Career inventory record exposing an installed-parts map. If it does not, Strip & Scrap is intentionally disabled for that vehicle.
- Actual BeamNG/RLS record shapes and money/inventory behavior are runtime-unproven until David tests this exact ZIP.
- The system snapshots and returns parts while removing the whole source vehicle; it does not attempt an unsupported physical per-part removal API before deletion.
- Further old/damaged-vehicle population tuning is deferred.
- Auction implementation remains owned by JOB-13 and is not included.

## Required runtime test

1. Disable all older JOB-04 ZIPs.
2. Install the exact v0.3.3 ZIP and fully restart BeamNG.
3. Confirm the visible `v0.3.3` badge.
4. Confirm existing Yard Inventory still loads and purchases remain available.
5. Open **My Vehicles & Scrap** and confirm owned vehicles from multiple garages appear.
6. Native-sell one inexpensive backup vehicle and verify normal money/ownership removal.
7. Scrap one inexpensive vehicle whole and verify removal plus one payout.
8. Strip & Scrap Shell on a vehicle showing verified parts.
9. Verify the exact vehicle disappears, shell payout occurs once, and all listed installed parts appear under Returned Parts.
10. Sell one normal returned part.
11. Scrap one verified catalytic converter.
12. Restart Career and verify remaining parts and transaction results persist.

## Gate

Do not create v0.3.4 until David reports the exact v0.3.3 runtime result and issue #30 records KEEP / REJECT / ROLLBACK and the next smallest action.

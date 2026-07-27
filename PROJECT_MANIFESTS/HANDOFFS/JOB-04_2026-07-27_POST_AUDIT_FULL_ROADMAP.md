# JOB-04 Post-Audit Full Roadmap — Scrap Yard / Wrecking Yard

**Date:** 2026-07-27  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Owner:** David / Captain  
**Assistant:** Sol / ChatGPT  
**Status:** Active — audit complete; v0.2.4 runtime test is the next gate

---

## 1. Scope

JOB-04 owns:

```text
- Scrap Yard / Wrecking Yard website and gameplay
- Immediate FoxNet phone/web performance required for the Scrap Yard page
- Native RLS Joe's Junk access
- Yard stock presentation
- Buying through the complete RLS purchase flow
- My Vehicles integration for selling/scrapping
- Later scrap, parts, yard ownership, import, and shipping-yard gameplay
```

JOB-04 does not own:

```text
- Node Grabber Unlocker
- Full developer/cheat menu
- Mod Conflict Scanner
- All-site FoxNet redesign
- Unrelated auction, towing, insurance, or other job systems
```

---

## 2. Current exact artifact

Uploaded and verified:

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD_FROM_v0_2_1(1).zip
```

Identity:

```text
Version: v0.2.4
Size: 25,165,565 bytes
SHA-256: 83ca53b9fc3e6f73b00720e60142b093788b462aa940604d8795e53d6460f7cc
ZIP integrity: PASS
Runtime: UNPROVEN
Base: v0.2.1 rollback / v0.1.9 last stock-loading line
```

The `(1)` suffix is an upload filename duplicate marker. The file contents and SHA-256 match the recorded v0.2.4 build.

---

## 3. What has been done

### Early FoxNet / Scrap experiments

The archive preserves evidence of multiple earlier approaches:

```text
v0.8 through v0.9.x — early FoxNet, phone relay, route, and Scrap page work
v0.10 — generated cheap-car-lot inventory and hand-built purchase path
v0.10.1 — removed storage block and added generic images
v0.10.2 — switched toward real RLS shop data and stock purchase menu
v0.10.3 — moved shop data onto the existing RedFoxCareerData bridge
v0.10.3.1 — candidate phone-only baseline, later ruled out as a bad UI baseline
v0.10.3.7 — later all-in-one base used before the grey-screen correction line
```

### JOB-04 package line

```text
v0.1.0 — plain WebUI test panel for RLS shopping and inventory calls
v0.1.1 — no-core-UI-override attempt
v0.1.2 — PC/phone access patch
v0.1.3 — restore phone-working PC mirror attempt
v0.1.4 — current RLS UI bridge; David could buy a Mustang, but navigation was slow
v0.1.5 — performance + PC/phone parity attempt; broke both phone and PC
v0.1.6 — exact rollback to v0.1.4 buy-working line
v0.1.7 — grey-screen-only patch; David confirmed grey screen fixed
v0.1.9 — removed unapproved warning text only
v0.2.0 — fast-load/images/spam-check patch; no cars loaded
v0.2.1 — rollback to v0.1.9 last stock-loading base
v0.2.2 — stock showroom attempt; opened every store
v0.2.3 — custom RLS wrecking-yard filter; slow and no stock
v0.2.4 — native Joe's Junk only, remove startup shop-data loading; untested
```

---

## 4. Known successful behavior

The strongest confirmed runtime successes are:

```text
v0.1.4 / v0.1.6 rollback:
- Scrap Yard loaded
- buy flow opened
- David bought a Mustang
- major problem: page/navigation speed

v0.1.7:
- grey screen fixed
```

No later version may be called successful unless David tests the exact file and reports the result.

---

## 5. Known failed behavior

```text
v0.1.5:
- PC/phone parity attempt broke both phone and PC loading

v0.2.0:
- no cars loaded
- refresh did not recover stock

v0.2.2:
- openShop(nil, nil, 'buying') opened every store

v0.2.3:
- welcome page about 20 seconds
- Scrap Yard over one minute
- no cars loaded

Earlier hand-built purchase flow:
- money removed
- vehicle spawned beside player
- no delivery countdown
- vehicle not added correctly to storage/inventory
```

Do not use v0.2.0, v0.2.2, or v0.2.3 as a new base.

---

## 6. What v0.2.4 is supposed to prove

v0.2.4 was built from the v0.2.1 rollback and is intended to:

```text
1. Stop the welcome page from requesting RLS vehicleShopping data at startup.
2. Stop the Scrap Yard page from cloning the shop into slow RedFox cards.
3. Open only native RLS Joe's Junk:
   career_modules_vehicleShopping.openShop('joesJunkDealership', nil, 'buying')
4. Avoid opening every dealership.
5. Use the native RLS seller and eventual native purchase path.
```

Changed files recorded for v0.2.4:

```text
assets/js/icefox_front.js
sites/scrap_yard/assets/css/scrap.css
sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js
ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/css/scrap.css
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
ui/ui-vue/dist/index.js
```

---

## 7. Immediate next gate — test v0.2.4

No v0.2.5 should be built until this test is recorded.

### Test setup

```text
1. Disable/remove all older JOB-04 Scrap Yard ZIPs.
2. Install only the exact v0.2.4 archive plus the current RLS Career Overhaul.
3. Start BeamNG fresh.
4. Use a backed-up/noncritical career profile.
5. Record BeamNG version, RLS version, map, and profile.
```

### Test sequence

```text
1. Open career.
2. Open the FoxNet/IceFox phone browser.
3. Time the welcome page.
4. Open Scrap Yard.
5. Time the Scrap Yard page.
6. Click Open Joe's Junk.
7. Confirm only Joe's Junk opens.
8. Confirm stock appears.
9. If stock appears, buy one inexpensive junk vehicle.
10. Record money handling.
11. Record whether a delivery countdown occurs.
12. Record whether the vehicle enters inventory/storage.
13. Exit and reload career.
14. Confirm the vehicle and balance remain correct.
15. Save BeamNG.log if any step fails or stalls.
```

### Result categories

```text
A. Welcome still takes 20–30 seconds.
B. Scrap Yard still takes over one minute.
C. Every store opens.
D. Joe's Junk opens nothing.
E. Joe's Junk opens but has no stock.
F. Stock appears but purchase still bypasses delivery/storage.
G. Full pass.
```

---

## 8. Decision tree after v0.2.4

### If A or B — startup/page performance still bad

Stop all feature work.

Inspect only:

```text
- remaining automatic shop requests
- inventory requests on welcome load
- page/frame preload behavior
- heavy image loading
- repeated postMessage/timeout/retry chains
- ui-vue route startup hooks
```

Target architecture:

```text
PHONE OPEN
→ tiny welcome shell only
→ no car data
→ no dealership data
→ no inventory
→ no auction/import/scrap preload

SCRAP YARD CLICK
→ load Scrap page only
→ open/request Joe's Junk only when David clicks
```

### If C — every store opens

Reject v0.2.4 and rollback to v0.2.1.

Inspect the exact RLS v2.6.8 `openShop` signature and seller identifier. Do not use a `nil` dealership argument.

### If D or E — Joe's Junk does not open or has no stock

Inspect:

```text
- dealership ID: joesJunkDealership
- map dealership availability
- RLS v2.6.8 dealership registration
- openShop arguments
- whether the current career has vehicleShopping initialized
```

Patch only the targeted seller-open route.

### If F — native seller works but purchase flow is incomplete

Trace the complete RLS purchase path.

Do not manually:

```text
- subtract money
- spawn the vehicle
- add to inventory
- add to storage
- simulate delivery
```

Use RLS for:

```text
- price/payment
- ownership
- delivery timer
- inventory ID
- storage/garage placement
- save persistence
```

### If G — full pass

Record tested BeamNG/RLS versions and advance to My Vehicles / Sell / Scrap.

---

## 9. Phase roadmap after native buying works

### Phase 1 — My Vehicles

Add Scrap Yard tabs:

```text
- Yard Stock
- My Vehicles
- Sell / Scrap
```

Use stock career/RLS inventory data.

Required capabilities:

```text
- search by vehicle/config
- filter by map/region
- filter by garage/storage
- handle hundreds of vehicles without freezing
- select one owned vehicle
```

### Phase 2 — Whole-vehicle selling

Primary stock function:

```text
career_modules_inventory.sellVehicleFromInventory(inventoryId)
```

Fallback only if the current RLS version requires it:

```text
career_modules_inventory.sellVehicle(inventoryId)
```

Do not hand-roll balance changes or inventory deletion.

### Phase 3 — Scrap value and scrapping

Add:

```text
- scrap-value quote
- confirm scrap action
- remove/sell owned vehicle through safe inventory APIs
- transaction record
- persistence check
```

### Phase 4 — Parts workflow

Later:

```text
- dev strip-all-parts proof
- parts inventory
- sell individual parts
- retain shell or scrap remainder
- vehicle condition affects value
```

### Phase 5 — Yard ownership and progression

Future player-owned yard systems:

```text
- buy/own yard
- storage capacity
- equipment upgrades
- crusher/processing upgrades
- reputation/progression
- legal/illegal disposal only if separately approved
```

### Phase 6 — Regional import and shipping yard

Future flow:

```text
- choose map/region
- browse regional stock
- order/import
- pay shipping cost
- wait delivery time
- collect at port, airport, ferry terminal, yard, or arrival spawn
- tow/recover vehicle
```

Requires map-by-map inspection and coordination with the correct asset-placement/support workstream.

### Phase 7 — Stock weighting

Desired eventual mix:

```text
80% Joe's Junk / normal wrecking-yard stock
10% random mixed finds
5% potentially good vehicles with issues
5% heavies, buses, planes, boats, or oddballs
```

Do not add this weighting until native stock, purchasing, selling, and persistence are stable.

### Phase 8 — Refresh limits

Development mode:

```text
- unlimited refresh
- no cooldown
- no penalty
```

Gameplay mode later:

```text
- stock refresh cooldown
- local stock limits
- regional shipping cost/time
- reputation or progression effects
```

---

## 10. Deferred items that must not enter the next patch

```text
- countdown/refresh economy
- auction yard
- shipping/import yard implementation
- cargo selling
- trailer/combo splitting
- all-site visual redesign
- Node Grabber or cheat menu features
- mod conflict scanner
- unrelated FoxNet pages
- warning/caution banners not explicitly requested
```

---

## 11. Mandatory per-version GitHub gate

Every next version must have three GitHub records.

### A. Pre-build scope record

Before editing:

```text
- source ZIP and hash
- exact owner request
- exact planned files
- exact protected files
- excluded features
- rollback point
```

### B. Build record

Before delivering ZIP:

```text
- output filename and hash
- byte size and file count
- changed files
- exact implementation
- static tests
- readable TXT/HTML reports
- runtime marked unproven
- test procedure
```

### C. Runtime result record

After David tests:

```text
- exact tested ZIP/hash
- environment versions
- pass/fail details
- logs
- regression list
- keep/reject/rollback decision
- next action
```

Hard rule:

```text
NO NEXT VERSION until the previous version has a build record and a runtime-result or explicit abandoned/untested closure record in GitHub.
```

---

## 12. Current next action

```text
Test v0.2.4.
Do not build v0.2.5 yet.
Record the runtime result in GitHub immediately after the test.
Choose the next patch from the result category A–G only.
```

---

## 13. Source-of-truth files

Read these first in any future handoff:

```text
PROJECT_MANIFESTS/INCIDENT_REPORTS/JOB-04_2026-07-27_GITHUB_CHECKPOINT_AND_INSTRUCTION_COMPLIANCE_AUDIT.md
PROJECT_MANIFESTS/HANDOFFS/JOB-04_2026-07-27_POST_AUDIT_FULL_ROADMAP.md
PROJECT_MANIFESTS/HANDOFFS/JOB-04_2026-07-27_FULL_HANDOFF_ROADMAP_AND_NEXT_TESTS.md
```

Current build:

```text
v0.2.4
SHA-256: 83ca53b9fc3e6f73b00720e60142b093788b462aa940604d8795e53d6460f7cc
Runtime: UNPROVEN
```
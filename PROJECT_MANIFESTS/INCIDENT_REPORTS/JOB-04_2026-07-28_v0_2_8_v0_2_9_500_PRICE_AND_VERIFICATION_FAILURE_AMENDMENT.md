# JOB-04 Incident Report Amendment — v0.2.8/v0.2.9 $500 Price Flattening and Verification Failure

**Date:** 2026-07-28 23:17 PT  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Owner:** David / Captain  
**Filed by:** Sol / ChatGPT  
**Severity:** High  
**Parent incident report:** `PROJECT_MANIFESTS/INCIDENT_REPORTS/JOB-04_2026-07-27_GITHUB_CHECKPOINT_AND_INSTRUCTION_COMPLIANCE_AUDIT.md`

---

## 1. Runtime failures reported by David

### v0.2.8

- The Wrecking Yard loaded many cars.
- Every car displayed a price of `$500`.
- Cars were too new and too clean for a wrecking yard.
- Inventory did not meaningfully change or cycle.
- Negotiation was unavailable.
- The phone opened a purchase page, but the PC final purchase did not complete.

### v0.2.9

- v0.2.9 was delivered as a correction.
- David again observed every listing at `$500`.
- Inventory still did not appear to change.

Decision: v0.2.8 and v0.2.9 are rejected as final Wrecking Yard builds.

---

## 2. Confirmed code-level cause

BeamBook was not the source of the flat pricing.

BeamBook generates varied listings and stores:

- asking price in `Value`
- market value in `marketValue`
- mileage in `Mileage` and `beamBookMiles`
- year in `year`
- native listing identity in `shopId`
- negotiation capability in `negotiationPossible = true`

JOB-04 v0.2.8 introduced a conversion/clone layer that:

1. evaluated the wrong price-field order,
2. accepted zero from an earlier field,
3. clamped the result to a `$500` minimum,
4. wrote that flattened value into copied listing fields,
5. disabled negotiation,
6. created synthetic shop IDs that were not reliably owned by the native purchase backend.

v0.2.9 source attempted to remove those defects, but it reused the same browser page, JavaScript, and config paths. Runtime behavior remained identical to v0.2.8. The verification process proved what was present in the ZIP, but did not prove which cached/runtime asset BeamNG executed.

---

## 3. Order-of-operations and verification failure

The assistant claimed the price, cycling, negotiation, and native-ID defects were corrected before runtime evidence proved that the changed code path was active.

This is recorded as an order-of-operations failure because:

- static inspection was treated as sufficient despite an established WebUI cache/path-overlap risk,
- the build did not include a visible runtime version marker,
- the page, JavaScript, and config URLs were reused,
- the exact packaged pricing and cycling logic was not fixture-tested before delivery,
- v0.2.9 was described as fixed even though the runtime result was still unproven.

This incident is separate from ordinary coding bugs because it concerns the required verification process and the truthfulness of the release status.

---

## 4. Corrective action in v0.3.0

v0.3.0 removes the JOB-04 price-conversion layer entirely.

Mandatory architecture:

- read BeamBook native listings directly from `career_modules_vehicleShopping.getShoppingData()`
- display native `Value` unchanged
- retain native `shopId`
- retain native `negotiationPossible`
- never create a copied/synthetic shop listing
- never write price fields
- never rewrite `sellerId`
- use RedFox Wrecking Yard branding only in the webpage display
- filter and rotate visible native listings only

Cache/runtime proof changes:

- new page: `sites/scrap_yard/index_v030.html`
- new JavaScript: `sites/scrap_yard/assets/js/scrap_v030.js`
- new config: `sites/scrap_yard/assets/config/wrecking_yard_mix_v030.json`
- visible runtime badge: `JOB-04 v0.3.0`

Additional corrective work:

- local visible-list cycling changes which native listings are displayed
- an explicit new-source-pool button expires BeamBook listings and asks BeamBook to generate a new pool
- PC bridge converts numeric shop IDs back to numbers before calling `openPurchaseMenu('instant', nativeShopId)`
- exact packaged JavaScript was fixture-tested with 100 simulated BeamBook records

---

## 5. Verification completed before delivery

The final v0.3.0 ZIP passed:

- JavaScript syntax checks for active, compatibility, PC, and phone files
- JSON parsing
- mirrored-file identity checks
- versioned-route checks
- visible build-badge check
- native `Value`-first price check
- native numeric shop-ID bridge check
- prohibited-pattern checks for minimum-price clamp, synthetic IDs, seller rewrite, and negotiation disable
- HTML local-reference checks
- ZIP integrity and duplicate-path checks
- fresh post-ZIP extraction and repeated packaged-file checks
- exact packaged JavaScript fixture test

Fixture results:

- native `Value` wins over `finalValue`
- zero `Value` falls through to a positive native field
- a true native `$500` listing remains `$500`; unrelated listings are not flattened
- 36 fixture cars retained 36 different prices
- cycling changed the visible inventory
- native shop IDs remained unchanged

---

## 6. Runtime hard gate

This incident is not considered resolved until David confirms all of the following from the exact v0.3.0 ZIP:

1. visible `JOB-04 v0.3.0` badge
2. varied vehicle prices
3. older/high-mileage/lower-end yard selection
4. visible inventory changes when cycling
5. negotiation is available where BeamBook marks it available
6. phone purchase completes
7. PC purchase completes
8. money, delivery, ownership, inventory, and storage are correct

No v0.3.1 may be created until the v0.3.0 runtime result is recorded in issue #30.

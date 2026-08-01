# RedFox/FoxNet Master Help — Native Vehicles and No-Lag Vehicle Stores

**Status:** DRAFT  
**Native vehicle section:** NOT PROVEN until Captain David passes JOB-09 v0.4.4.9 runtime tests.  
**No-lag marketplace section:** based on the JOB-04/BeamBook investigation and must still be adapted within each job's ownership boundaries.

## 1. External systems creating real Career/RLS vehicles

### The failure pattern

A vehicle can appear in the Career garage while still being a partial record. Merely receiving an inventory ID and assigning a garage does not prove that the vehicle is complete.

Typical evidence:

- blank or default-only thumbnail;
- “Not insured” on the vehicle tile but missing from the uninsured list;
- missing `originalParts` or `changedSlots`;
- Lua errors during parts removal;
- vehicle missing after reload;
- wrong insurance metadata inherited from stale purchase state.

### Required two-pass architecture

#### Pass A — source snapshot while the live vehicle exists

Capture before deleting or virtualizing the source object:

- exact JBeam/model;
- full native configuration table and canonical `partConfigFilename`;
- installed/missing parts and part conditions;
- paints;
- license plate;
- mileage/odometer;
- year and native configuration metadata;
- damage identity;
- persistent source and transaction IDs.

A custody or auction source may remain virtual after this snapshot. It does not need to become player-owned immediately.

#### Pass B — legal ownership/native registration

1. Spawn or adopt the exact snapshot.
2. Call native inventory registration once.
3. Keep the physical object alive.
4. Wait for native part-condition initialization.
5. Wait for native original-parts/changed-slots processing.
6. Create a valid insurance record, including a real `insuranceId = -1` uninsured entry when selected.
7. Assign the exact native garage.
8. Request a generated thumbnail.
9. Wait for save completion.
10. Remove/store the physical object.
11. Save again.
12. Read back and verify vehicle JSON, insurance JSON, thumbnail, garage, and transaction marker.
13. Only then delete the source/custody/auction record.

Do not use a fixed one-second delay as the completion gate. Do not manually invent incomplete Career vehicle JSON. Do not copy insurance metadata from a different vehicle.

### Existing partial-record recovery

- Back up the save.
- Preserve the same inventory ID.
- Restrict automatic repairs to records positively tagged as belonging to the responsible RedFox source.
- Spawn the same inventory record, not a replacement purchase.
- Re-run missing native lifecycle hooks only when required.
- Generate a real thumbnail and valid uninsured/insured entry.
- Save, store, save again, and read back.
- Never create a duplicate replacement unless the original is proven absent and the owner explicitly approves it.
- Quarantine records that cannot be completed without guessing.

## 2. No-lag vehicle marketplaces and yards

### Proven design lesson

The welcome page must do no vehicle-catalog work. Heavy vehicle discovery begins only after the user opens the relevant store or yard.

### Recommended data flow

1. Generate or refresh the candidate pool in Lua, not by repeatedly opening every dealership or rebuilding the browser DOM.
2. Use native eligible-vehicle/configuration sources.
3. Sanitize and quarantine malformed vehicle entries.
4. Cache the larger Lua pool with a reasonable TTL.
5. Inject or expose the pool once through the native vehicle-shopping data path.
6. Send only a small visible page to WebUI, such as 12–24 cards.
7. Use pagination or load-more for the rest.
8. Lazy-load images.
9. Reuse native inspection, insurance, payment, inventory, and delivery paths.
10. Avoid retry storms and repeated all-dealership scans.

### Wrecking Yard lesson

BeamBook demonstrated that a 100–200 vehicle backend pool can remain responsive when generated/cached in Lua and only a bounded page is rendered. The RedFox Wrecking Yard should keep Joe's Junk and other sources behind its own page, while avoiding any inventory work on the IceFox welcome page.

## 3. Required transaction gates for all jobs

- persistent request ID;
- idempotent retry;
- exact source identity;
- no charge before delivery can complete;
- no source deletion before destination verification;
- rollback or review lock on failure;
- one vehicle, one inventory ID;
- save/reload verification;
- clear log prefix and stage-specific failure reason.

## 4. Jobs that should use this guide after proof

- JOB-02 Shared Career/RLS Bridge — owns the reusable native transaction.
- JOB-04 Wrecking Yard — purchases, whole-vehicle returns, and no-lag catalog architecture.
- JOB-05 BeamBook — native purchase handoff and bounded rendering.
- JOB-09 Tow/Recovery — full tow snapshot and lien transfer.
- JOB-13 Auctions — buyer delivery and seller two-phase settlement.

## Promotion gate

Promote this draft to an approved master help list only after:

1. JOB-09 inventory ID 11 repairs in place;
2. Insurance recognizes it as uninsured;
3. a generated thumbnail persists;
4. parts editing works;
5. save/reload does not duplicate or lose it;
6. one fresh lien vehicle completes the same path.

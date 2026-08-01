# JOB-13 v0.1.8 — Prepared 5x10 Markets / Slow Catalog Build Record

Date: 2026-08-01
Branch: `job13-online-auctions`
Owner: David / Captain
Runtime status: **UNTESTED IN BEAMNG**

## Artifact

- ZIP: `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_8_PREPARED_5X10_SLOW_CATALOG.zip`
- SHA-256: `37b3a4f31573eb3ccf181447c4a4661807eec7354d279de7099edff6b8352ec8`
- Runtime files: 25
- Base: v0.1.7.2 phone-only direct Career delivery repair

## Scope

- 10 active lots.
- 5 prepared markets total, 10 lots each, 50 prepared summaries.
- Saved active/prepared state returned before catalog maintenance.
- No installed-vehicle enumeration during extension load, Career activation, or phone-page loading.
- Missing catalog rebuild starts only after Auction state has been requested.
- Incremental scan pace: 2 configurations every 0.25 seconds.
- Uses BeamNG `core_vehicles` registry; no synchronous `util_configListGenerator.getEligibleVehicles` call.
- Completed catalog is staged and validated before replacing the last known-good cache.
- One finished auction promotes one prepared market and creates one replacement market from the existing cache.
- Phone-only direct Career inventory/garage delivery path retained.
- No `openPurchaseMenu`, `buyFromPurchaseMenu`, `closeAllMenus`, broad `openShop`, or `forceShopRefresh` calls.

## Verification

- Lua syntax: PASS.
- JavaScript syntax: PASS.
- JSON parse: PASS.
- ZIP integrity: PASS.
- Duplicate ZIP paths: 0.
- Unsafe ZIP paths: 0.
- Fresh extraction hash comparison: PASS.
- Harness: PASS — 10 active lots, 5 prepared markets, 50 summaries, 63-entry simulated catalog, 7 rotations, no idle state rewrite.

## Test gate

Disable every older JOB-13 ZIP and install only this build. Test Career startup, phone opening, and Auction page speed before bidding or purchasing. Stop immediately on major lag or crash and preserve `beamng.log`.

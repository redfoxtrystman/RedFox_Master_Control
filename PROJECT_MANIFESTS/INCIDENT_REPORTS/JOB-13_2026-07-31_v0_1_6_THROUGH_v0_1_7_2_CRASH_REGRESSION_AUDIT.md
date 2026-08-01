# JOB-13 v0.1.6 through v0.1.7.2 crash regression audit

Date: 2026-07-31
Owner: David / Captain
Job: JOB-13 — FoxNet Online Vehicle Auctions
Status: STOP TEST / NO NEW BUILD

## Runtime report

David reported that v0.1.7.2 became extremely slow while entering FoxNet Auctions and then crashed BeamNG.

## Exact archives audited

- v0.1.6 SHA-256 `8fa86d6fa09287bd07ba97dd4281362e8c05950b31bfd57da5dfc0f2cc39cce4`
- v0.1.7 SHA-256 `c34d076f07096150ecf963be1f4a5f60b530741ad0104d6c93a7cbc15da4bca2`
- v0.1.7.1 SHA-256 `675e670c520c8b0bb482a0673363d234452e1ed2d9b7c7f6fe699b4118607b18`
- v0.1.7.2 SHA-256 `688922086ada71f2e7bdfa1635c823bfc1517d84badb759123dba23350c234f9`

## Confirmed regression introduced in v0.1.7

v0.1.6 used a small packaged approved pool and did not enumerate every installed vehicle/configuration/prop on startup.

v0.1.7 replaced that startup behavior with synchronous installed-content discovery inside `redfoxJob13Auction.lua`:

1. `core_vehicles.getModelList()`
2. `core_vehicles.getModel(modelKey)` for every model
3. iteration across every configuration of every model
4. `util_configListGenerator.getEligibleVehicles(false, false)`
5. merge/deduplicate/sort the complete result
6. pretty-print/write the complete pool to `settings/redfox/job13_online_auctions/installed_vehicle_prop_pool_v017.json`

`loadApprovedVehiclePool(false)` is called from both:

- `onExtensionLoaded()`
- `onCareerModulesActivated()`

If the cache is missing, invalid, unreadable, partially written, or rejected, the full discovery can run during game/Career startup and may run again when Career modules activate. With a large mod collection, this violates the required prebuilt-approved-pool architecture and can explain multi-minute loading, severe lag, and a crash.

The cache writer uses a full pretty-printed JSON write. A crash/interruption during that write can leave an unreadable cache; the next run then falls back to another full synchronous scan, creating a possible crash loop.

## Version-by-version finding

### v0.1.6

- Small packaged pool.
- Fast catalog architecture.
- Did not enumerate all installed models/configurations/props at startup.
- Separate known critical defect: menu-oriented purchase handoff caused global phone/computer/input lock after delivery.

### v0.1.7

- Introduced full installed vehicle/configuration/prop discovery.
- Introduced synchronous cache generation during extension/Career activation.
- Added Quick Bid, upcoming lots, saved searches, notifications, and variety logic.
- Startup discovery was not sufficiently bounded, deferred, resumable, or protected against very large mod libraries.
- This is the first version containing the current load/crash regression.

### v0.1.7.1

- Lua and JavaScript are byte-identical to v0.1.7.
- Only dropdown CSS, cache-busting HTML references, metadata, and compatibility route files changed.
- Therefore v0.1.7.1 retained the v0.1.7 discovery regression unchanged.

### v0.1.7.2

- Retained the v0.1.7 discovery and cache code unchanged.
- JavaScript is byte-identical to v0.1.7/v0.1.7.1.
- CSS is byte-identical to v0.1.7.1.
- Replaced only the winning-purchase implementation with a direct Career delivery adapter, plus version text/cache references.
- The new delivery code does not execute merely from opening the auction unless a pending callback/state exists; it is not the primary code path responsible for the initial full installed-content discovery.
- The exact crash still requires `beamng.log` to distinguish a heavy-discovery crash from another Lua/runtime failure.

## Unintended/order-of-operations failure

The requirement was to prepare/cache an approved pool ahead of page use. v0.1.7 instead allowed the runtime extension to build the entire installed pool synchronously when the cache was absent or invalid. That was a material architecture regression from v0.1.6 and should not have been carried into v0.1.7.1 or v0.1.7.2.

## Current safety decision

- v0.1.7.2: REJECT / DISABLE
- v0.1.7.1: NOT SAFE due global input lock purchase bug and retained discovery regression
- v0.1.7: NOT SAFE due global input lock purchase bug and discovery regression
- v0.1.6: NOT SAFE for purchases due global input lock bug
- All JOB-13 builds: disable until recovery build is explicitly authorized and verified

## Required recovery architecture

1. Do not call `util_configListGenerator.getEligibleVehicles()` on extension load, Career activation, page open, register, search, or refresh.
2. Do not enumerate every installed model/configuration synchronously on those paths.
3. Load only a small last-known-good approved-pool snapshot at runtime.
4. Build or rebuild the large pool only through an explicit WEUI action or a deferred chunked background process with progress and cancellation.
5. Write the new cache to a temporary file, validate it, then atomically replace the last-known-good cache.
6. Never discard the last-known-good pool merely because a rebuild fails.
7. Limit data sent to the browser to the visible summaries.
8. Keep direct phone-only delivery separate from pool generation.
9. Test startup with the exact large mod library before expanding features.

## Evidence still required

Capture the `beamng.log` from the crash before reopening/retesting when possible. Search for:

- `redfoxJob13Auction`
- `util_configListGenerator`
- `core_vehicles`
- `installed_vehicle_prop_pool_v017`
- Lua stack traces
- out-of-memory or CEF crash messages

No patch or new ZIP was created during this audit.

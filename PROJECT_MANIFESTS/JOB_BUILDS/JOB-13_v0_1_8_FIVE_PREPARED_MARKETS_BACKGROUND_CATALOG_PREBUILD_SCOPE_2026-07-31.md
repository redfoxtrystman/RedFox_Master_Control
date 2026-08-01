# JOB-13 v0.1.8 — Five Prepared Markets / Background Catalog

Date: 2026-07-31 PT
Owner: David / Captain
Job: JOB-13 — FoxNet Online Vehicle Auctions
Branch: `job13-online-auctions`
Source: `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_7_2_PHONE_ONLY_DIRECT_CAREER_DELIVERY_FIX.zip`

## Owner-approved goal

Create an Auction market generator that can eventually include all installed/loadable base-game and mod vehicle configurations without scanning or hydrating the full vehicle library when Career starts or when the phone Auction page opens.

## Locked architecture

- Exactly 10 active lots.
- Four additional prepared 10-lot markets.
- 50 lightweight prepared vehicle summaries total across five markets.
- Phone page immediately reads saved active/prepared state.
- Full installed vehicle/config discovery is deferred and chunked across update ticks.
- No synchronous `util_configListGenerator.getEligibleVehicles()` call.
- No full scan in `onExtensionLoaded()`, `onCareerModulesActivated()`, or phone page requests.
- Last-known-good compact catalog remains active until a replacement cache is completely built and atomically renamed into place.
- First run uses the safe packaged starter pool, then replaces future prepared markets after background discovery finishes.
- Finishing one auction promotes one prepared market and generates only one replacement market from the cached catalog.
- Bids and timers do not rewrite the catalog cache.
- Manual WEUI rebuild starts the same background worker and does not delete/reset the active auction.

## Purchase-path protection

- Preserve v0.1.7.2 phone-only direct Career inventory/garage delivery code.
- Do not restore `openPurchaseMenu` or `buyFromPurchaseMenu`.
- Do not open or depend on a garage computer/dealership UI.
- Correct the stale v0.1.7.2 phone-state readiness call from undefined `nativePurchaseModulesReady()` to the actual `directPurchaseModulesReady()` function.

## UI/cache changes

- New cache-busted UI App path: `redfoxJob13Auctions_v018`.
- New settings/state/catalog filenames for v0.1.8.
- Remove the green successful-load banner that repeatedly shifted the lot grid.
- Preserve dropdown visibility hotfix, Quick Bid, saved searches, notifications, bidding and previous-results behavior.

## Validation gates

1. Lua syntax parses.
2. JavaScript syntax parses.
3. JSON parses.
4. Fresh harness starts with 10 active lots, five total markets and 50 summaries without a synchronous catalog scan.
5. Deferred scanner processes only a bounded number of configurations per update step.
6. Scanner completes and atomically replaces the cache.
7. Active auction remains intact while the prepared queue is rebuilt from the new catalog.
8. Six consecutive auction rotations preserve 10 active lots, five total markets and 50 summaries.
9. No `getEligibleVehicles` call remains.
10. ZIP integrity, duplicate-path, unsafe-path and exact manifest checks pass.

Runtime remains unproven until David tests the exact output ZIP.
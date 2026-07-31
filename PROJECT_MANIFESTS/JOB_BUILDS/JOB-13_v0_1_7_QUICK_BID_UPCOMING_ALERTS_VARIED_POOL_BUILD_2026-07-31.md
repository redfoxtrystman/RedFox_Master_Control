# JOB-13 v0.1.7 Build Audit

Date: 2026-07-31
Owner: David / Captain
Job: JOB-13 — FoxNet Online Vehicle Auctions

## Source and output

Source ZIP: `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_6_NATIVE_BIDDING_GARAGE_DELIVERY.zip`
Output ZIP: `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_7_QUICK_BID_UPCOMING_ALERTS_VARIED_POOL.zip`
Output SHA-256: `c34d076f07096150ecf963be1f4a5f60b530741ad0104d6c93a7cbc15da4bca2`
Runtime files: 23
ZIP bytes: 160554

## Owner requests implemented

- Quick Bid on every active vehicle tile using the existing `place_bid` action.
- Keep Watch on the tile so several auctions can be followed simultaneously.
- Preview the following auction before it starts.
- Phone notification before the following auction starts.
- Phone alerts for watched lots ending, outbid events, wins, and saved vehicle-search matches.
- Broad installed catalog support for base-game vehicles, configurations, props, and mod content.
- High lot variety: recently used configs avoided, repeated models limited, and same-model adjacency repaired when the pool allows.
- Preserve the native Career/RLS purchase and makeDelivery-to-garage path from v0.1.6.

## Catalog architecture

- `core_vehicles` model/config metadata and `util_configListGenerator` are used only while building or manually rebuilding the persistent installed pool cache.
- Cache path: `settings/redfox/job13_online_auctions/installed_vehicle_prop_pool_v017.json`.
- Auction page opening, search, Watchlist, My Bids, and Upcoming do not scan vehicles or dealerships.
- The next auction is prepared in Lua and persisted before the page requests it.
- After adding/removing vehicle mods, WEUI provides **Rebuild Installed Vehicle/Prop Cache**.

## Notification architecture

- Uses existing RLS `ui_phone_layout.fireNotification`.
- Namespaced JOB-13 channels are used.
- Sent flags persist to prevent per-tick repeated alerts.
- Toastr is fallback-only if the phone dispatcher is unavailable.

## Purchase boundary

The complete `completeNativePurchase()` block is byte-identical to v0.1.6. JOB-13 still calls the existing RLS vehicleShopping purchase flow with `makeDelivery=true`; it does not add a second wallet, invoice, ownership, shipping, notification, or garage system.

## Static and behavior verification

- ZIP integrity: PASS
- Duplicate ZIP paths: 0
- Lua syntax: PASS
- JavaScript syntax: PASS
- JSON parse: PASS
- Forbidden shared/core paths: absent
- Unrelated site content: absent
- Installed pool harness: 60 configs discovered from 30 models
- Live lots: 12
- Upcoming lots: 12
- Same-model adjacency in live harness: 0
- Same-model adjacency in upcoming harness: 0
- Quick Bid backend path: existing `place_bid` only
- Saved-search add/remove: PASS
- RLS phone notification dispatcher: exercised in harness
- Native purchase/delivery block unchanged from v0.1.6: PASS
- 120 simulated idle seconds after stable state: 0 additional writes

## Runtime status

**RUNTIME UNPROVEN.** David has not yet confirmed a completed player purchase/delivery on v0.1.6 or v0.1.7. First v0.1.7 startup may take time once while the installed catalog cache is created; later loads reuse the cache.

## Package boundaries

No edits to Welcome/Home, Wrecking Yard, Tow/Recovery, BeamBook, FoxFax, main Vue UI bundle, stock phone layout, or redfoxCareerWeb core. The two FoxNet Auction page mirrors and one v0.1.6 cache-compatibility redirect remain JOB-13-owned paths only.

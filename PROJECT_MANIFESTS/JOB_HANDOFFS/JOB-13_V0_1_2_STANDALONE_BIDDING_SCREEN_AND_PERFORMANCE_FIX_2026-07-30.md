# JOB-13 v0.1.2 Standalone Bidding Screen and Performance Fix

**Date:** 2026-07-30  
**Job:** JOB-13 — FoxNet Online Vehicle Auctions  
**Status:** Static verification passed; BeamNG runtime retest required

## Runtime failure reported

- Opening the phone auction site took approximately 2–3 minutes.
- Register and Search Inventory caused additional lockups.
- Listing actions opened a marketplace-style Negotiate Price / Buy screen instead of an auction bidding screen.
- Opening prices were too high.
- Some vehicles were miscatalogued.
- Confusing placeholder text such as `Unicorn listed by mistake` appeared.

## Root cause boundary

The old phone page was not using the JOB-13 online bidding screen. It behaved like a marketplace/dealership page and rebuilt a large catalog during page actions. The JOB-13 standalone v0.1.0 also did not own the shared phone route.

## v0.1.2 correction

The new reusable JOB-13 page is a thin UI over the existing `extensions.redfoxJob13Auction` backend actions:

- `place_bid`
- `set_max_bid`
- `cancel_bid`
- `toggle_watch`
- `join_membership`
- `pay_invoice`

It contains no marketplace negotiation, direct-buy, dealership, or `vehicleShopping` calls.

## Performance changes

- Persistent prebuilt catalog before page opening.
- Default catalog reduced to 12 lots.
- Search, sort, categories, watchlist and My Bids operate only on cached state.
- No vehicle scan or catalog regeneration on Register or Search Inventory.
- UI state refresh interval is five seconds, with a local one-second display clock.

## Auction behavior changes

- Default TEST mode for simulated transactions only.
- Default opening bid reduced to 10% of estimated value.
- Default minimum increment reduced to $100.
- Opening price creates no bidder and no artificial current bid.
- Proper bidding detail screen with current/opening bid, next valid bid, ordinary bid, confidential maximum, cancel bid, watchlist and bid history.
- Corrected categories: Cars, Trucks, Vans, Off-road, Semis and Projects.
- Removed negotiation/Buy Now flow and confusing placeholder text.

## Isolated files

All runtime files remain under the JOB-13 namespaces:

```text
lua/ge/extensions/redfoxJob13Auction.lua
lua/ge/extensions/redfoxJob13AuctionSettings.lua
scripts/redfox_job13_online_auctions/modScript.lua
ui/modules/apps/redfoxJob13Auctions_v012/
settings/redfox/job13_online_auctions/
```

No other website or shared phone/browser file was edited.

## Phone route target

The shared JOB-01/JOB-10 phone owner should repoint only the FoxNet Auctions route to:

```text
/ui/modules/apps/redfoxJob13Auctions_v012/site/index.html
```

The old phone route will continue to show the old marketplace page until that one route is changed.

## Artifact

```text
RedFox_JOB13_FoxNet_Online_Auctions_v0_1_2_STANDALONE.zip
SHA-256: 1093bda6d840d3d102cf9dc71557744d7c7fa216967a2399021f9d599362b071
```

## Verification

- JavaScript syntax: PASS
- JSON syntax: PASS
- Lua parse validation: PASS
- Lua behavior harness: PASS
- 21/21 image references present
- ZIP integrity: PASS
- BeamNG runtime: NOT YET RETESTED

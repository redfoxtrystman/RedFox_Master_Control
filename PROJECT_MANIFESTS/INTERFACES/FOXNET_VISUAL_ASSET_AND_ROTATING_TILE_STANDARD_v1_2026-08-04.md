# FoxNet Visual Asset and Rotating Tile Standard v1

**Date:** 2026-08-04  
**Owner:** Shared UI coordination; JOB-04/Welcome implements host behavior, each feature job owns its own images  
**Tracking:** #53, #56

## Purpose

Prevent generic first-load images, stale WebUI art, and cross-job file overwrites while giving every FoxNet page a consistent way to provide Welcome tiles, advertisements, hero art, and listing images.

## Ownership rule

- Each feature job ships its own images under its unique website route.
- JOB-04/Welcome may read those images through stable paths or a small visual manifest.
- JOB-04 must not copy another job's active image library into a second folder.
- Both required website mirrors must contain byte-identical route assets unless a proven runtime difference requires otherwise.
- Auction and Classic listing photographs stay attached to the correct vehicle. Do not rotate unrelated vehicle pictures inside an individual vehicle listing card.

## Required image slots

| Slot | Source size | Aspect | Format | Suggested max size | Current use |
|---|---:|---:|---|---:|---|
| Welcome service tile | 640 x 360 | 16:9 | JPG/PNG/WebP; SVG only for vector art | 350 KB | Current Welcome quick tiles; rendered about 150 px high desktop / 128 px mobile |
| Welcome wide banner | 1456 x 180 preferred; 728 x 90 minimum | 8.09:1 | JPG/PNG/WebP/SVG | 300 KB | Current top advertisement slot |
| Welcome compact banner | 672 x 180 preferred; 336 x 90 minimum | 3.73:1 | JPG/PNG/WebP/SVG | 250 KB | Current secondary advertisement slot |
| Website hero | 1600 x 900 preferred | 16:9 | JPG/WebP/PNG | 700 KB | Public page hero/background |
| Vehicle/listing image | 1000 x 562 preferred; 500 x 281 minimum | 16:9 | JPG/WebP/PNG | 450 KB | Auction, Wrecking Yard, Classic listings |
| In-page promo card | 1000 x 650 | 20:13 | JPG/WebP/PNG/SVG | 500 KB | Current Collector/Parts/other site promo cards |
| Logo with transparency | 1024 x 1024 or SVG | 1:1 | PNG/SVG | 300 KB | Logos/icons only |

Use lowercase filenames with letters, numbers, underscores, and hyphens only. No spaces. Photographic images should normally be JPG or WebP. Transparent logos should be PNG or SVG.

## Route-owned ZIP structure

Each feature job should use its own unique route and include this structure in both route mirrors:

```text
sites/<unique_route>/assets/config/foxnet_visuals_v1.json
sites/<unique_route>/assets/images/welcome_tiles/<job>_tile_01.jpg
sites/<unique_route>/assets/images/welcome_tiles/<job>_tile_02.jpg
sites/<unique_route>/assets/images/ads/<job>_ad_01.jpg
sites/<unique_route>/assets/images/hero/<job>_hero_01.jpg
sites/<unique_route>/assets/images/listings/<listing_or_vehicle_id>_01.jpg

ui/modModules/redfoxCareerWeb/sites/<unique_route>/assets/config/foxnet_visuals_v1.json
ui/modModules/redfoxCareerWeb/sites/<unique_route>/assets/images/...
```

The two trees must match byte-for-byte.

JOB-13 may continue to keep runtime app images under its versioned app folder, but it should also expose Welcome-tile art beneath its unique route so JOB-04 can load it without copying Auction assets.

## Visual manifest

Recommended schema:

```json
{
  "schema": "redfox.foxnet.visuals.v1",
  "job": "JOB-13",
  "version": "0.1.8.2",
  "welcomeTiles": [
    {
      "src": "sites/redfox_job13_auctions/assets/images/welcome_tiles/auction_tile_01.jpg",
      "alt": "FoxNet auction vehicles",
      "weight": 1
    }
  ],
  "ads": [
    {
      "id": "auction_sell_your_vehicle",
      "slot": "wide",
      "src": "sites/redfox_job13_auctions/assets/images/ads/auction_ad_01.jpg",
      "targetRoute": "foxnet"
    }
  ]
}
```

Version the manifest and filenames when replacing images. BeamNG WebUI caching must not be trusted to notice same-name replacements.

## Welcome rotation behavior

- Render the first valid image immediately on first load.
- Never require the user to open the target page and return before real imagery appears.
- Rotate service-tile images every 12 seconds with a 350-500 ms crossfade.
- Pause timers while the browser page is hidden.
- Randomize the initial image, but do not repeat the same image twice in a row.
- PC and phone use the same manifest and image pool.
- If dynamic catalog images arrive later, merge them into the pool without replacing the already-visible image with a blank frame.
- Use a module-specific static image as fallback. Use a generic car only when the module provides no valid image at all.

## Auction and Classic rules

- Auction Welcome tile: rotate 3-8 Auction-owned 640x360 images.
- Classic/Collector Welcome tile: rotate 3-8 Classic-owned 640x360 images.
- In-page promotion carousels may rotate.
- A specific vehicle listing must keep the correct vehicle's images and may only rotate additional views of that same vehicle.
- JOB-13 current minimum listing size is 500x281. New art should target 1000x562.
- Classic current card art uses 1000x650; new vehicle listing photography should move toward 16:9 while existing promo cards may remain 1000x650.

## Advertisement concepts

Initial cross-site art inventory:

### Wrecking Yard
- `wrecking_scrap_rate_today_01` — Today's scrap rate and daily change.
- `wrecking_instant_cash_01` — Instant complete-vehicle offer, slightly under marketplace value.
- `wrecking_junk_parts_01` — We buy junk-labeled parts and stripped remainders.
- `wrecking_bring_your_broken_dreams_01` — humorous RedFox ad.

### Tow
- `tow_deliver_to_scrapyard_01` — Tow a dead vehicle to a physical scrapyard.
- `tow_recovery_24h_01` — public towing promotion.

### Auction
- `auction_list_your_vehicle_01` — wait for a buyer and potentially earn more.
- `auction_salvage_week_01` — rotating damaged/salvage inventory promotion.

### Classic / Collector
- `classic_barn_find_weekend_01` — rare and barn-find inventory.
- `classic_consignment_01` — consign a collectible vehicle.

### Parts Exchange
- `parts_send_to_shop_01` — send an RLS inventory part to the online shop.
- `parts_junk_cleanup_01` — sell junk-labeled stored parts.

### FoxFax
- `foxfax_scrap_prices_01` — fictional market report.
- `foxfax_tow_story_01` — humorous tow/recovery headline.
- `foxfax_classic_rumor_01` — collector rumor or fake investigative headline.

## Acceptance gate

1. Fresh Career/browser load shows real Wrecking, Auction, Classic, and Tow imagery without visiting those pages first.
2. PC and phone show the same image pools.
3. Tiles rotate without blank frames, console errors, or repeated same-image loops.
4. Feature ZIPs have zero active path overlap.
5. Replacing an image in a later version does not leave the prior cached art visible.

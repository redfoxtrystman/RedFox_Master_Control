# JOB-13 v0.1.7 → v0.1.7.1 Dropdown Hotfix Source Patch Index

Base artifact:

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_7_QUICK_BID_UPCOMING_ALERTS_VARIED_POOL.zip`

Output artifact:

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_7_1_DROPDOWN_VISIBILITY_HOTFIX.zip`

Output SHA-256:

`675e670c520c8b0bb482a0673363d234452e1ed2d9b7c7f6fe699b4118607b18`

Local unified-diff artifact:

`JOB13_v0_1_7_to_v0_1_7_1_DROPDOWN_HOTFIX.diff`

Diff SHA-256:

`758b18676ca6f029af8daf77b58035c86bec98edc9c1a6736be1315aa906777f`

## Exact functional CSS addition

```css
/* v0.1.7.1 BeamNG/CEF native select popup visibility hotfix.
   Explicit colors prevent light option text from disappearing on the native light popup. */
select{color-scheme:dark}
select option,select optgroup{background-color:#111923!important;color:#f3f6fa!important}
select option:checked,select option:hover{background-color:#2a3a4d!important;color:#ffffff!important}
```

## Cache-safe HTML changes

- Replace `app.css?v=017` with `app.css?v=0171` in all active JOB-13 auction HTML copies.
- Update the standalone UI App iframe query to `site/index.html?v=0171`.
- Add `index_v0171.html` to both JOB-13 FoxNet route mirrors.
- Redirect the old `index_v016.html` compatibility loader to `index_v0171.html?v=0171`.
- Update visible version labels to v0.1.7.1.

## Behavior-preservation proof

The following v0.1.7 files are byte-for-byte unchanged:

- `lua/ge/extensions/redfoxJob13Auction.lua`
- `lua/ge/extensions/redfoxJob13AuctionSettings.lua`
- `ui/modules/apps/redfoxJob13Auctions_v017/site/app.js`
- `scripts/redfox_job13_online_auctions/modScript.lua`
- `data/redfox_job13/approved_vehicle_pool_v2.json`

Therefore this patch does not change bidding, NPC logic, auction timing, membership, watch/search alerts, money, purchase settlement, inventory, or native garage delivery.

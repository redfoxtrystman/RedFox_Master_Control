# JOB-13 v0.1.7.1 Dropdown Visibility Hotfix Build Audit

Date: 2026-07-31
Owner: David / Captain
Job: JOB-13 — FoxNet Online Vehicle Auctions

## Runtime report

BeamNG WebUI opened the category and sort dropdowns, but the option labels were invisible. Blank rows remained clickable and changed the selected value.

## Confirmed cause

The v0.1.7 CSS styled the `<select>` control but did not explicitly style native `<option>`/`<optgroup>` popup rows. BeamNG/CEF displayed a light native popup while preserving light inherited text.

## Exact repair

- Added `color-scheme: dark` to select controls.
- Added explicit dark background and light foreground colors to option and optgroup rows.
- Added explicit selected/hover option colors where supported.
- Updated JOB-13 HTML stylesheet cache keys to `0171`.
- Added `index_v0171.html` compatibility copies and redirected the old v0.1.6 compatibility loader to them.
- Updated only version labels/metadata outside CSS.

## Explicitly unchanged

The following behavior files are byte-for-byte identical to v0.1.7:
- `lua/ge/extensions/redfoxJob13Auction.lua` — `82eeda684a03eb16b21e3811754f0147994adfbf3c53cb606cc9b256e4d0ff38`
- `lua/ge/extensions/redfoxJob13AuctionSettings.lua` — `8d88754badff4f4580a8bb8142d9b59e8b67ecc84bc77129966ab79d4e88cf01`
- `ui/modules/apps/redfoxJob13Auctions_v017/site/app.js` — `3789667a0fb2d90ef49ba1e1d603b8445c889068d1c880490a8ac5b4cd659f21`
- `scripts/redfox_job13_online_auctions/modScript.lua` — `9bc4b816c9b34b813c34461bd6f22b5ed9b86e605e4a3a3a748495800f8024a2`
- `data/redfox_job13/approved_vehicle_pool_v2.json` — `8c5f066017166a5ff15c68bc4bf348d716fb915e8771a27c41c24f313cb47755`

Therefore this hotfix does not change bidding, NPC behavior, timers, memberships, saved alerts, purchase settlement, Career money, inventory, or native garage delivery.

## Verification

- ZIP integrity: PASS
- Duplicate ZIP paths: 0
- JavaScript syntax: PASS
- Lua files unchanged byte-for-byte from v0.1.7
- JSON parsing: PASS
- All active auction HTML copies reference `app.css?v=0171`: PASS
- Old v0.1.6 compatibility loaders redirect to `index_v0171.html?v=0171`: PASS
- Explicit option/optgroup colors present: PASS
- Critical behavior files unchanged: PASS

## Artifact

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_7_1_DROPDOWN_VISIBILITY_HOTFIX.zip`
SHA-256: `675e670c520c8b0bb482a0673363d234452e1ed2d9b7c7f6fe699b4118607b18`
Runtime files: 25

## Changed or added paths

- `mod_info/RedFoxJOB13/RUNTIME_NOTE.txt`
- `mod_info/RedFoxJOB13/info.json`
- `sites/foxnet_auctions/index.html`
- `sites/foxnet_auctions/index_v016.html`
- `sites/foxnet_auctions/index_v017.html`
- `sites/foxnet_auctions/index_v0171.html`
- `ui/modModules/redfoxCareerWeb/sites/foxnet_auctions/index.html`
- `ui/modModules/redfoxCareerWeb/sites/foxnet_auctions/index_v016.html`
- `ui/modModules/redfoxCareerWeb/sites/foxnet_auctions/index_v017.html`
- `ui/modModules/redfoxCareerWeb/sites/foxnet_auctions/index_v0171.html`
- `ui/modules/apps/redfoxJob13Auctions_v017/app.html`
- `ui/modules/apps/redfoxJob13Auctions_v017/app.json`
- `ui/modules/apps/redfoxJob13Auctions_v017/site/app.css`
- `ui/modules/apps/redfoxJob13Auctions_v017/site/index.html`

## Runtime status

UNPROVEN until David confirms the category and sort dropdown labels are visible in BeamNG.

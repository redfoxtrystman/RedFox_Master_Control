# JOB-13 v0.1.7.1 — Dropdown Visibility Hotfix Pre-build Scope

Date: 2026-07-31
Owner: David / Captain
Job: JOB-13 — FoxNet Online Vehicle Auctions
Source: RedFox_JOB13_FoxNet_Online_Auctions_v0_1_7_QUICK_BID_UPCOMING_ALERTS_VARIED_POOL.zip

## Runtime report

The category and sort `<select>` controls open and accept clicks, but the option text is not visible in BeamNG WebUI/CEF. The player can click blank option rows and the selected value changes.

## Root cause

JOB-13 styles the `<select>` element with a dark background and light text but does not explicitly style the native `<option>` rows. BeamNG/CEF renders the popup menu with a light/default background while preserving inherited light text, making the options appear blank.

## Locked repair scope

- CSS-only behavior repair plus cache/version labels.
- Add explicit background and foreground colors to all `<option>` and `<optgroup>` rows.
- Add explicit selected/checked option colors where supported.
- Increment the stylesheet cache query from `017` to `0171` in JOB-13-owned auction HTML copies.
- Identify the hotfix as v0.1.7.1.
- Do not change Lua, JavaScript, bidding, NPC logic, auction timing, membership, purchase, money, inventory, garage delivery, vehicle discovery, or state schemas.
- Do not edit Wrecking Yard, Tow/Recovery, BeamBook, Welcome/Home, or any other website.

## Verification gate

1. JavaScript and Lua files are byte-for-byte unchanged from v0.1.7.
2. All JOB-13 auction HTML copies reference `app.css?v=0171`.
3. CSS explicitly styles `select option` and `select optgroup` with readable dark/light colors.
4. ZIP integrity and duplicate-path checks pass.
5. Exact manifest and source diff are generated.
6. Runtime remains unproven until David confirms the dropdown text is visible in BeamNG.

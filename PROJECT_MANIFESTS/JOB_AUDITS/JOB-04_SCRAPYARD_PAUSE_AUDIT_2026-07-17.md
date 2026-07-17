# JOB-04 — Scrap Yard / Wrecking Yard Pause Audit

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Chat role:** Scrap Yard / Wrecking Yard chat / Sol  
**Status:** PAUSED while David is camping. This is not a handoff. Resume this same chat when David returns.

---

## Sound off

This chat is **JOB-04 — Scrap Yard / Wrecking Yard**.

This chat owns:

- Scrap Yard / Wrecking Yard WebUI test panel.
- Scrap Yard page behavior.
- Wrecking-yard style UI for Scrap Yard only.
- Online buy test flow for Scrap Yard vehicles.
- Online sell test flow for owned career vehicles.
- Future Scrap Yard sell-zone placeholder only.
- Scrap Yard-specific reports, audits, and test notes.

This chat does **not** own:

- JOB-00 Coordinator / Integration / Verification.
- JOB-01 Phone + PC Platform Core.
- JOB-02 Shared RLS / Career Bridge.
- JOB-03 App Store / Play Store.
- JOB-05 BeamBook Marketplace.
- JOB-06 Import / Export Yard.
- JOB-07 Classics / Collector Exchange.
- JOB-08 Insurance / Finance / Garage / Storage Pages.
- JOB-09 Tow / Recovery / Dispatch.
- JOB-10 Visual Design / Real Website Polish.
- JOB-11 QA / Logging / Failure Triage.
- JOB-12 SponsorHub / FoxMail / FoxText / Sponsor Rewards.

---

## Important correction already made

There was confusion where this chat was temporarily treated as JOB-00 Coordinator. David corrected that.

Final assignment for this chat:

```text
JOB-04 — Scrap Yard / Wrecking Yard
```

This chat remains the Scrap Yard chat because this is the work we had already been doing for a while.

---

## David's current direction

David said the BeamBook/Facebook-style web page and several other pages are around 80% complete and he is happy with them. The tow company is also coming along well.

David wants Scrap Yard to follow the same safer pattern as the tow company:

1. Do **not** wire directly into the final pretty website first.
2. Build a WebUI / debug test panel first.
3. Use buttons to prove the backend actions work.
4. After backend actions work, either hide the panel behind a developer page or leave it accessible as a cheat/debug tool.
5. Then connect the working actions to the real Scrap Yard / Wrecking Yard website.

This is the main direction for JOB-04 when work resumes.

---

## All-map requirement

David is **not on West Coast**, and Scrap Yard must work on all maps.

Rules:

- Same ZIP must work on all maps.
- Do not make Scrap Yard depend on `west_coast_usa`.
- `west_coast_usa(2).zip` is reference only if needed.
- No map-specific dealership coordinates for the first test panel.
- No map-load parking spot generation.
- No map-load shop generation.
- No physical sell-zone runtime yet.

The first working target is global WebUI/RLS/Career functionality, not a map location.

---

## Files David uploaded for this pause window

Uploaded / available in the chat environment:

```text
/mnt/data/RedFox_RLS_Evidence_v03(2).zip
/mnt/data/RedFox_RLS_Evidence_v03_SUMMARY_ONLY(2).zip
/mnt/data/rls_career_overhaul_2.6.6(2).zip
/mnt/data/west_coast_usa(2).zip
/mnt/data/zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_1_DIRECT_SCRAP_COPART_TIMEOUT_FIX phone only works(1).zip
/mnt/data/rls_RaceTab_Release.zip
```

Meaning of each file:

- `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_1_DIRECT_SCRAP_COPART_TIMEOUT_FIX phone only works(1).zip`
  - Main baseline for Scrap Yard because David says this is the only current working-ish one being provided.
  - Treat as phone-only / phone-partly-working Scrap Yard baseline.

- `rls_career_overhaul_2.6.6(2).zip`
  - RLS reference for stock/RLS vehicle shopping and inventory flows.

- `RedFox_RLS_Evidence_v03(2).zip`
  - Evidence/reference package for RLS behavior.

- `RedFox_RLS_Evidence_v03_SUMMARY_ONLY(2).zip`
  - Summary reference for RLS behavior.

- `west_coast_usa(2).zip`
  - Reference only.
  - Must not become a required dependency.

- `rls_RaceTab_Release.zip`
  - Uploaded after the first Scrap Yard test build was made.
  - Not yet inspected or incorporated into JOB-04 at the time of this pause audit.

---

## Current JOB-04 test build

A first Scrap Yard WebUI test panel ZIP was produced:

```text
/mnt/data/zzzz_RedFox_FoxNet_Web_Ecosystem_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_v0_1_0.zip
```

Reported size at creation time:

```text
24,404,253 bytes
```

Reported build intent:

- Add a Scrap Yard WebUI test panel.
- Work as all-map design.
- Add a button from the Scrap Yard page to the test panel.
- Test RLS/shop stock loading.
- Test opening stock purchase menu.
- Test listing owned career vehicles.
- Test selling selected owned vehicle through stock inventory sell function.

GitHub build note already created:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-04_SCRAPYARD_WEBUI_TEST_PANEL_BUILD_NOTE.md
```

Prior commit for that build note:

```text
2a5d83c53b1d90c83d33a9583d29907ef17833fc
```

Important: David reported **"no dl"**, meaning the download link did not work in the chat UI. The file existed on the assistant side and was re-linked, but David may still need a fresh re-upload or rebuild/link when he returns.

Runtime status:

```text
UNPROVEN — David has not tested this ZIP in BeamNG yet.
```

---

## What has been done in JOB-04 so far

### 1. Role corrected

- This chat was corrected to JOB-04.
- JOB-04 is Scrap Yard / Wrecking Yard.
- This chat is not JOB-00 Coordinator.

### 2. Direction corrected

Old wrong direction:

- Try to wire Scrap Yard directly into final website and PC/phone all at once.
- Use or imitate unsafe ScrapYard Direct behavior.

New correct direction:

- Build WebUI test panel first.
- Prove backend actions with buttons.
- Only after backend works, connect to final website.

### 3. Map requirement corrected

- Scrap Yard must work on all maps.
- West Coast file is reference only.
- No West Coast-only dependency.

### 4. Unsafe Scrap Yard Direct path blocked

Do not use these as a base:

```text
RedFox_ScrapYard_Direct_v0_1_0.zip
RedFox_ScrapYard_Direct_v0_1_1_ONLINE_ONLY_SAFE.zip
RedFox_ScrapYard_Direct_v0_1_2_NO_EARLY_DEP_SAFE_TEST.zip
```

Reason:

- They tried to create a Scrap Yard career module.
- They caused severe loading/freezing risk.
- They are not safe to continue from.

### 5. First WebUI test panel build created

- A first all-map Scrap Yard WebUI test ZIP was created.
- It is meant for backend testing, not final website polish.
- It needs David runtime testing after camping.

---

## What was tried before this pause

### Previous Scrap Yard/FoxNet attempts

The project previously had a partly-working phone Scrap Yard path around the v0.10.3.1 family.

Known partial success:

- Phone Scrap Yard could request RLS/BeamNG vehicle shop data.
- Phone Scrap Yard could show vehicles at least sometimes.
- Phone Scrap Yard could open purchase flow at least sometimes.

Known failures / issues:

- PC path did not work the same as phone.
- PC Scrap Yard page needed parity with phone behavior.
- Purchase could spawn/open but garage/storage/persistence behavior was uncertain or broken.
- Some stock repeated too much.
- Copart/auction flow was not the right immediate path.
- Old custom bridge/direct-career-module attempts caused serious instability.

### ScrapYard Direct attempts

These were bad and must not be repeated:

- Creating a startup career module for Scrap Yard.
- Loading Scrap Yard direct at map load.
- Parking spot generation.
- Custom money/storage/garage behavior.
- Patching marketplace/shop data at startup.

Result:

- Severe loading/freezing risk.
- BeamNG stutter/freeze/near lockup reported by David.

### Current WebUI approach

This is the new safer path copied from Tow Yard's workflow:

- Button panel first.
- Debug output first.
- Backend action proof first.
- Website integration later.

---

## Current planned testing flow when David returns

Before testing:

1. Remove/disable all other `zzzz_RedFox_FoxNet_Web_Ecosystem...zip` files.
2. Install only the JOB-04 test ZIP.
3. Keep RLS Career Overhaul installed as David normally uses it.
4. Launch a non-West-Coast map if desired to prove all-map behavior.
5. Start Career/RLS context normally.

Test sequence:

```text
1. Open IceFox / Scrap Yard.
2. Click "Open Scrap Yard WebUI Test Panel" if visible.
3. Click "Check Status".
4. Click "Load RLS Shop Data".
5. Confirm stock count appears.
6. Select a vehicle from the loaded list.
7. Click "Open Selected Purchase Menu".
8. Confirm stock/RLS purchase menu opens.
9. Click "List Owned Career Vehicles".
10. Confirm owned vehicle list appears.
11. Only click "Sell Selected Owned Vehicle" if David truly wants to sell that selected vehicle.
12. Save BeamNG log after the test.
```

Expected log prefixes:

```text
[RedFox][SCRAP][WEBUI]
[RedFox][SCRAP][PHONE]
[RedFox][SCRAP][PC]
[RedFox][SCRAP][BUY]
[RedFox][SCRAP][SELL]
```

BeamNG logs to collect:

```text
beamng.log
beamng.1.log
beamng.2.log
beamng.3.log
beamng-launcher.log
```

Search terms:

```text
RedFox
ScrapYard
FoxNet
IceFox
RedFoxRequestCareerData
RedFoxCareerData
RedFoxOpenVehiclePurchase
RedFoxVehiclePurchaseResult
RedFoxSellInventoryVehicle
RedFoxSellInventoryVehicleResult
vehicleShopping
openPurchaseMenu
buyFromPurchaseMenu
inventory
storage
garage
career_modules_inventory
career_modules_vehicleShopping
no active vehicle
dependencies not resolved
```

---

## Current state of the mod

Current latest JOB-04 build:

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_JOB04_SCRAPYARD_WEBUI_TEST_PANEL_ALL_MAPS_v0_1_0.zip
```

State:

```text
Built for first WebUI/backend test.
Runtime unproven.
Download link had trouble for David.
May need re-upload or rebuild when David returns.
```

Known static/scope claims from build message:

- No `redfoxScrapYardDirect`.
- No startup career module.
- No map-load parking generator.
- No fake money path.
- No fake storage path.
- No fake garage path.
- No fake inventory path.

Important: those should be rechecked before any next build or before declaring the package valid, because David already had one bad download issue.

---

## What JOB-04 should do next after camping

1. Confirm David can download the current test ZIP.
2. If the ZIP link still fails, rebuild or re-upload a clean copy.
3. Reopen the ZIP and verify:
   - ZIP integrity.
   - No duplicate top folder.
   - No `__pycache__`.
   - No `redfoxScrapYardDirect`.
   - No startup career module.
   - No map-load generator.
   - Test panel path exists.
   - Scrap Yard page link/button exists.
   - Reports exist.
4. Have David test in BeamNG with only one FoxNet ZIP installed.
5. If WebUI panel loads but backend calls fail, inspect BeamNG log and patch only the failing call.
6. If backend calls work, connect the same actions to phone and PC Scrap Yard page.
7. Only after phone/PC/backend are stable, connect to the final realistic Scrap Yard website.
8. Later, coordinate with Tow Yard so tow jobs can deliver vehicles toward Scrap Yard / Wrecking Yard flows.

---

## Future Scrap Yard / Wrecking Yard feature direction

### Phase 1 — Current phase

WebUI test panel:

- Load RLS/shop data.
- Show raw stock count.
- Show filtered scrap/wreck candidates.
- Open selected purchase menu.
- List owned career vehicles.
- Sell selected owned vehicle.
- Print debug logs.

### Phase 2 — Phone and PC parity

- Phone and PC use same tested backend calls.
- PC no longer gets separate broken guesswork bridge.
- Scrap Yard page works from phone and PC.

### Phase 3 — Real website integration

- Connect backend-proven actions into realistic Scrap Yard / Wrecking Yard website.
- Do not overwrite David's newer BeamBook/Facebook-style pages.
- Coordinate with JOB-10 for visuals if needed.

### Phase 4 — Tow company integration

- Tow company can eventually deep-link to Scrap Yard.
- Tow delivery-to-yard flow should wait until Scrap Yard backend is stable.
- JOB-09 owns Tow; JOB-04 owns Scrap Yard receiving behavior only.

### Phase 5 — Physical sell-zone, later only

Future idea, not current build:

- User can place a yard marker/prop on any map.
- Player brings/tows vehicles into a sell circle.
- UI lists vehicles inside/near the zone.
- Owned career vehicles can be sold through stock sell function.
- Stolen/traffic/unowned logic is later only and must be designed safely.

Not allowed yet:

- Runtime map scanning at map load.
- Parking spot generation.
- Startup career module.
- Selling unowned traffic/stolen vehicles.

---

## Hard rules to preserve

```text
No redfoxScrapYardDirect.
No startup career module.
No map-load work.
No parking spot generation.
No fake money.
No fake storage insert.
No fake garage insert.
No fake inventory ownership.
No vehicleShopping patch at startup.
Only one FoxNet/Web Ecosystem ZIP installed during tests.
Runtime unproven until David tests in BeamNG.
If a check fails, stop and report it.
```

---

## Files still wanted from David later

Not required for first return test, but useful later:

```text
1. Current Tow Yard ZIP with working WebUI test buttons.
2. Current newest good website / BeamBook / Facebook-style page ZIP.
3. Any latest all-in-one FoxNet/IceFox ZIP David is actually using after camping.
4. Fresh BeamNG logs after testing the Scrap Yard WebUI panel.
```

Tow Yard ZIP is useful because JOB-04 wants to copy the same testing-room pattern David likes.

The polished website ZIP is not required until backend actions work.

---

## Pause note

David is going camping. Do not treat this as a handoff. When he returns, continue in this same JOB-04 Scrap Yard chat from this audit.

# JOB-12 Full Camping Handoff — SponsorHub / FoxMail / FoxText / Sponsor Rewards

**Date:** 2026-07-17  
**Owner:** JOB-12 Sponsor System chat (Sol)  
**Status:** ACTIVE — CURRENT TEST BUILD UNPROVEN / NEXT STEP IS MINIMAL WEBUI PROOF  
**Repo:** `redfoxtrystman/RedFox_Master_Control`

---

## 1. Ownership and scope

JOB-12 remains under this chat's control.

JOB-12 owns:

- SponsorHub website/app.
- FoxMail sponsor email system.
- FoxText sponsor notification system.
- Sponsor registry and editable sponsor definitions.
- Sponsor offers, applications, contracts, accept/decline flow.
- Sponsor XP, reputation, Sponsor Points, status levels.
- Per-vehicle sponsorship assignments.
- Optional honor-system decal bonus per sponsor/per vehicle.
- Freeroam pending sponsor wallet.
- Career deposit integration through the approved shared bridge only.
- BeamHesi sponsor earnings integration.
- Drift sponsor earnings integration.
- Future safe-driving, towing, recovery, racing, manufacturer, fleet, and event sponsor systems.

JOB-12 does not own and must not modify:

- Phone shell.
- PC shell.
- Browser core.
- Shared IceFox/FoxNet navigation.
- Shared app/site registry implementation.
- RLS core.
- Career startup modules.
- Vehicle shopping, inventory, garage, storage, insurance, or finance implementations.
- FoxFax.
- Scrap Yard.
- BeamBook.
- Import/Export.
- Classics.
- Other jobs' pages or shared code.

FoxFax remains only the Carfax-style vehicle-history parody page. It is not a fax, email, or text service.

---

## 2. Final intended architecture

One shared IceFox/FoxNet front-door mod owns phone/PC/browser/registration.

JOB-12 remains one isolated removable add-on with:

```text
JOB-12 add-on
├── SponsorHub
├── FoxMail
├── FoxText
├── Sponsor-owned backend/state
├── Sponsor registry
├── Sponsor reward logic
└── Small adapters/manifests for JOB-01 and JOB-02 contracts
```

Phone and PC eventually open the same registered destinations and use the same backend messages. Only layout changes for screen size.

Until final platform integration is ready, JOB-12 is allowed to use a temporary standalone keybind-opened WebUI strictly for isolated testing.

---

## 3. User-approved gameplay direction

The sponsor system should become a full Career progression system, not just random money.

Core ideas approved:

- Browse sponsors on SponsorHub.
- Apply/subscribe through the website.
- Receive formal responses in FoxMail.
- Receive short alerts in FoxText.
- Accept or decline offers.
- Track contracts, XP, reputation, Sponsor Points, status, and rewards.
- Assign sponsors to individual Career vehicles.
- One vehicle can have many sponsors.
- Competing sponsors can exist on different vehicles.
- Same sponsor can approve multiple vehicles and later grant fleet bonuses.
- Decals are optional only.
- No required decal placement, size, wrap coverage, windshield banner, or automatic percentage detection.
- Initial decal verification is honor-system: player answers whether sponsor decals are displayed on that vehicle.
- Sponsor decal folders and sponsor registry remain editable so David can add sponsors later without editing Lua.
- Decal filenames should use the sponsor folder/id plus numbered variants, such as `sponsor_id_1`, `sponsor_id_2`, `sponsor_id_3`.
- Optional decal use can grant extra XP, reputation, Sponsor Points, and later contingency cash.

Meaningful rewards should prioritize systems BeamNG/RLS already use:

- Cash.
- Sponsor payout multipliers.
- Repair reimbursement.
- Paint vouchers/reimbursement.
- Fuel reimbursement.
- Entry-fee reimbursement.
- Insurance/deductible reimbursement where safely supported.
- Event and race invitations.
- Loaner vehicles or trailers after exact APIs are proven.
- Vehicle purchase credits or permanent sponsor vehicles only after exact inventory APIs are proven.

Do not pretend fake oil bottles, filters, additives, or random parts provide gameplay value unless those mechanics are actually coded and tested.

---

## 4. Sponsor priority order

The user chose this progression:

1. **BeamNG GmbH** as the first guaranteed proof/test sponsor.
2. **Towing and recovery sponsors** because the user is currently focusing on towing gameplay.
3. **Racing sponsors** after towing sponsor behavior is working.

Potential towing/recovery sponsor direction discussed:

- RedFox Recovery.
- Belasco Towing.
- East Coast Recovery.
- Utah Heavy Rescue.
- BeamNG-lore towing/fleet companies.
- Optional real text-only brands later, such as Warn, Miller Industries, or Jerr-Dan, without logos until separately created/provided.

Potential racing sponsor direction discussed:

- Grip-All Tires.
- Hirochi Performance.
- Civetta Corse.
- ETK Motorsport.
- Gavril Performance.
- Lucas Oil.
- RedFox Racing.
- Other BeamNG-lore and fictional performance companies.

---

## 5. Files and references supplied by David

Important supplied files used for research/reference:

- `BeamHesi.zip`
- `driftmod.zip` / `driftmod(1).zip`
- `rls_career_overhaul_2.6.6(1).zip` and later copies
- `west_coast_usa(1).zip` and later copies
- `RedFox_RLS_Career_Dev_Unlocker_v0_1_0(2).zip`
- `RedFox_RLS_Evidence_v03(1).zip`
- `RedFox_RLS_Evidence_v03_SUMMARY_ONLY(1).zip`
- `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_1_DIRECT_SCRAP_COPART_TIMEOUT_FIX phone only works.zip`
- `RedFox_JOB10_Full_Websites_v0_3_0(2).zip`
- Previous JOB-12 test ZIPs listed below.

What those references established:

- BeamHesi tracks close-call score but originally did not deposit Career money.
- Uploaded drift mod uses a lightweight drift chain and direct Career money path.
- RLS has its own drift events/rewards and may intentionally stack as a separate organizer payment.
- The Dev Unlocker confirmed the working Career money attribute route:

```lua
career_modules_playerAttributes.addAttributes({money = amount}, metadata)
```

- RLS/FoxNet reference files contain working UI-to-Lua patterns such as `bngApi.engineLua(...)`.
- Working phone-side FoxNet/Scrap Yard exists and is a reference only; JOB-12 must not copy or hijack its platform files.

---

## 6. Builds attempted and current evidence

### v0.1.0 — Combined Hesi/Drift Sponsor Network

File:

```text
RedFox_FreeRoam_SponsorNetwork_v0_1_0_Combined_Hesi_Drift.zip
```

Attempted:

- Combined Hesi and drift earning paths.
- Sponsor wallet.
- Career deposit fallback.
- Clean-driving and roadside concepts.
- Large sponsor catalog.

Problem:

- Too much functionality introduced before the app/contract flow and platform architecture were proven.
- Not a reliable baseline for current work.

### v0.2.0 — Registry and Decal Folders

File:

```text
RedFox_FreeRoam_SponsorNetwork_v0_2_0_SponsorRegistry_DecalFolders.zip
```

Attempted:

- Editable sponsor registry.
- Individual decal folders.
- Per-vehicle sponsorship design.

Useful design retained:

- Sponsor registry should be editable.
- Decal use optional.
- Per-vehicle sponsor assignments.

### v0.3.0 — SponsorHub Test

File:

```text
RedFox_FreeRoam_SponsorNetwork_v0_3_0_SponsorHub_Test.zip
```

Attempted:

- Guaranteed Grip-All test offer.
- Offers/contracts state.
- Responsive SponsorHub-style UI.

Problem:

- Did not provide the correct proven IceFox registration path.
- Not accepted as working integration.

### v0.4.0 — FoxNet Sponsor Communications

File:

```text
RedFox_FoxNet_Sponsor_Communications_v0_4_0_BeamNG_Test.zip
```

Attempted:

- FoxMail.
- FoxText.
- SponsorHub.
- BeamNG GmbH offer.

Major architecture failure:

- Bundled/copied too much FoxNet ecosystem content.
- Risked duplicating or overriding shared phone/PC/browser/platform files.
- This was effectively a platform hijack rather than a clean app add-on.
- Must not be used as a baseline.

### v0.5.0 — Standalone UI App Test

File:

```text
RedFox_SponsorSystem_Standalone_Test_v0_5_0.zip
```

Attempted:

- Isolated SponsorHub/FoxMail/FoxText backend/state in a BeamNG UI App.

Runtime evidence:

- Did not crash or block Career loading.
- Wrong interaction method.
- David explicitly asked for a keybind-opened standalone WebUI, not a HUD UI App.
- Buttons/backend did not work during testing.

### v0.5.1 — Keybind WebUI Test

File:

```text
RedFox_SponsorSystem_Standalone_WebUI_Keybind_Test_v0_5_1.zip
```

Attempted:

- Configurable keybind.
- Standalone WebUI state.
- SponsorHub/FoxMail/FoxText/test tools.

Runtime evidence:

- Correct general launcher direction.
- Prevented Career from completing load; Career reached the end of loading and stayed on the loading screen.
- Therefore v0.5.1 is unsafe and must remain disabled.

Likely failure area:

- Custom WebUI state/extension/input registration or startup interaction.
- Exact cause is unconfirmed because the relevant old log was no longer available.

### v0.6.0 — Minimal WebUI Proof

Files referenced in chat:

```text
RedFox_SponsorSystem_Minimal_WebUI_Proof_v0_6_0.zip
RedFox_Sponsor_v0_6_0.zip
```

Intended scope:

- One keybind.
- One minimal standalone WebUI.
- One BeamNG GmbH sponsor.
- One force-sponsor button.
- One status field.
- No persistence, money, FoxMail, FoxText, drift, Hesi, or phone/PC integration.

Current state:

- Download delivery had issues and was re-linked.
- No successful runtime result has been reported yet.
- Therefore v0.6.0 is **UNPROVEN**, not working/fixed/done.

---

## 7. Recorded mistake and audit incident

Incident report already created:

```text
INCIDENT_REPORTS/2026-07-14_JOB-12_WEBUI_ORDER_OF_OPERATIONS_FAILURE.md
```

Core mistake:

- David requested a key-opened standalone WebUI settings-style menu.
- JOB-12 first built a HUD UI App instead.
- This substituted an unrequested launcher and violated the requested order of operations.
- Static syntax/ZIP checks were incorrectly treated as enough confidence to hand over a runtime build.
- The later keybind build opened the correct type of route but then blocked Career loading.

Mandatory lesson:

- Requested interaction method cannot be changed without explicit approval.
- Build and prove the smallest launcher/ping/state loop before adding sponsor systems.
- Never call runtime behavior fixed or working before David tests it.

---

## 8. GitHub records already created

JOB-12 claim:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-12_SPONSORHUB_FOXMAIL_FOXTEXT_CLAIM.md
```

Important commits recorded during this work:

```text
88118bc81b6b063a7abbc39a124d9de1964622e0
18e1d84a6860dbe56fd25320a77fef4a499ff259
b5c74e85e4b6fc6e04c428df6d27969e8cc16d2e
37be7c72626b7773655ff7766f684ee42602cf06
5b58adc7c2b4b63c67930f2d894fbfe61b77e379
```

The claim remains active under JOB-12. No transfer of ownership is authorized.

---

## 9. Current mod state at departure

**Current proven facts:**

- v0.5.0 did not block Career loading.
- v0.5.0 used the wrong UI App launcher and its functions did not work.
- v0.5.1 used the desired keybind/WebUI direction but blocked Career loading.
- v0.6.0 is intended as the minimal retry but has not yet been runtime-proven.
- No sponsor version is currently approved as working.
- No current version should be described as complete.
- No Career payout loop is currently proven in JOB-12.
- No FoxMail/FoxText/SponsorHub full flow is currently proven in BeamNG.
- No phone/PC integration is currently proven.

**Recommended installed state while not testing:**

- Keep all old JOB-12 sponsor test ZIPs disabled or removed.
- Never install v0.5.0 and v0.5.1 together.
- Never install sponsor communication v0.4.0 alongside the real FoxNet platform.
- Use only one explicitly selected minimal test ZIP during a controlled test.

---

## 10. Exact next technical step

Do not add towing, racing, FoxMail, FoxText, persistence, money, or Career integration yet.

Build/rebuild one minimal proof using the smallest working pattern from the supplied RLS/FoxNet references.

The next test package must contain only:

```text
1 configurable input action
1 minimal lazy-loaded Lua extension
1 standalone WebUI page/state
1 open function
1 close function
1 UI-to-Lua ping button
1 BeamNG GmbH test sponsor state field
```

Required behavior:

1. Career loads completely.
2. Control appears in Options → Controls.
3. Assigned key opens the standalone WebUI.
4. Close/Escape returns safely to gameplay.
5. Pressing one button calls one Lua function.
6. Page updates from `No Sponsor` to `BeamNG GmbH` for the current session only.
7. No save writes.
8. No money.
9. No startup Career module.
10. No phone/PC/FoxNet shared files.

If any one of these fails, stop and inspect logs before adding anything else.

---

## 11. Testing checklist when David returns

Use only the newest minimal proof ZIP selected for testing.

Before launch:

- Remove/disable every older sponsor ZIP.
- Confirm only one FoxNet ecosystem ZIP is installed.
- Keep RLS installed only if that is the chosen baseline.

Test order:

1. Start BeamNG.
2. Enter Career.
3. Confirm Career fully loads.
4. Open Options → Controls.
5. Search for the sponsor test input action.
6. Bind a key.
7. Press the key.
8. Confirm WebUI opens.
9. Close and reopen it.
10. Press the single sponsor button.
11. Confirm status changes once.
12. Exit to menu and re-enter Career.
13. Confirm no hang occurred.

Collect if available:

- `beamng.log`
- Screenshot of control binding.
- Screenshot of opened WebUI.
- Screenshot after sponsor status changes.
- Exact point of failure.

Do not test advanced sponsor features until this checklist passes.

---

## 12. Work after the minimal proof passes

Add one layer at a time in this strict order:

### Layer A — local persistence

- Save one BeamNG sponsor status.
- Reload after game restart.
- Prevent duplicate activation rewards.

### Layer B — SponsorHub application flow

- BeamNG GmbH listing.
- Apply/subscribe button.
- Offer state.
- Accept/decline.
- Contract display.

### Layer C — FoxMail and FoxText

- Formal application/offer/contract messages in FoxMail.
- Short alerts in FoxText.
- Shared state with SponsorHub.

### Layer D — approved Career bridge

- Query Career state.
- Query current/owned vehicles.
- Deposit one small earned sponsor payment through JOB-02 contract.
- Confirm deposit once and save.

### Layer E — towing sponsor category

First real gameplay category after BeamNG sponsor.

Potential tracked activities only after detection is proven:

- Accepting tow/recovery jobs.
- Completing tow delivery.
- Recovering overturned or disabled vehicles.
- Long-distance tow completion.
- Heavy recovery.
- Clean/no-damage recovery.

Start with status/XP/points before cash if necessary.

### Layer F — racing sponsor category

- RLS race completion.
- Podium/win bonuses.
- Drift sponsor rewards.
- Time trial/rally/drag/circuit categories.
- Intentional organizer + sponsor payout stacking.

### Layer G — BeamHesi and freeroam wallet

- Hesi close-call sponsor earnings.
- Drift freeroam sponsor earnings.
- Pending wallet outside Career.
- One-time Career settlement.
- Adjustable payout sliders.

### Layer H — larger sponsor ecosystem

- More BeamNG-lore sponsors.
- RedFox fictional sponsors.
- Optional real text-only sponsors.
- Editable registry.
- Per-vehicle sponsors.
- Honor-system decals.
- Fleet bonuses.
- Manufacturer programs.
- Events, loaners, reimbursements, and high-tier vehicle rewards only after exact APIs are proven.

---

## 13. Dependencies and coordination

JOB-12 eventually needs:

- JOB-01 final phone/PC app registration and route contract.
- JOB-02 final Career/payment/vehicle bridge contract.
- JOB-11 final TXT + HTML verification format and log expectations.
- JOB-00 frozen integration baseline and release order.

The standalone minimal test may continue before those contracts, but final integration must wait for them.

JOB-12 must communicate through GitHub and request new permissions/events instead of silently editing shared files.

Proposed eventual events remain:

```text
RedFoxSponsorGetState
RedFoxSponsorState
RedFoxSponsorApply
RedFoxSponsorAcceptOffer
RedFoxSponsorDeclineOffer
RedFoxSponsorAssignVehicle
RedFoxSponsorSetDecalHonor
RedFoxSponsorClaimReward
RedFoxSponsorNewMail
RedFoxSponsorNewText
RedFoxSponsorPayoutRequested
RedFoxSponsorPayoutResult
```

Final names are owned by JOB-01/JOB-02 contracts.

---

## 14. Stop conditions

Stop and do not ship if:

- Career does not finish loading.
- A sponsor ZIP contains phone/PC/browser/FoxNet core files.
- A sponsor ZIP contains RLS core edits.
- A startup Career module is introduced.
- The input action does not appear.
- WebUI does not open/close safely.
- A button is visible but not connected to Lua.
- State duplicates rewards.
- Money is added without confirmed bridge success.
- Runtime is untested but described as working/fixed/done.

---

## 15. Resume point

When work resumes, begin here:

> Inspect the latest minimal v0.6.0 source and the supplied working RLS/FoxNet references. Rebuild only the minimal keybind → WebUI → ping → BeamNG sponsor-session-state proof. Do not add any other feature until David confirms Career loads, the key opens the page, the button works, and the status changes.

This file is the complete JOB-12 resume record as of 2026-07-17.

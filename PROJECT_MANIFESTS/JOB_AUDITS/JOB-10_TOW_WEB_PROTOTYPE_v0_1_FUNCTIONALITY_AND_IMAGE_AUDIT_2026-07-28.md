# JOB-10 Tow Web Prototype v0.1 — Functionality and Image Audit

**Date:** 2026-07-28  
**Owner:** David / Captain  
**Job:** JOB-10 — Visual Design / Real Website Polish  
**Runtime target:** Phone-only  
**Status:** AUDITED — NOT READY FOR DAVID RUNTIME TEST

## Files inspected

```text
RedFox_Tow_Web_Prototype_v0_1(1).zip
19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_4_SafeFleetTowYardAssignmentNpcDriverReady(1).zip
```

JOB-10 did not edit or combine the working JOB-09 mod.

## Owner requirements confirmed

- All vehicle imagery must use real BeamNG vehicles or installed BeamNG vehicle mods.
- No fake cartoon cars, trucks, tow trucks, crash scenes, or fleet units.
- The public towing website must work as a real site.
- Every button and page must have a working purpose.
- Business-management areas are a priority, not decorative placeholders.
- The Tow website remains separate from the JOB-09 gameplay mod; it connects through approved page/data/action contracts.
- Current runtime target is the in-game phone. PC code may remain preserved but hidden/deferred.

## Prototype structure

The uploaded website contains:

```text
index.html
styles.css
app.js
RedFox_Tow_Web_Prototype_v0_1_SingleFile.html
README.md
assets/
```

The visual sections include:

```text
Public towing-company homepage
Services
Fleet
Recent Recoveries
Tow Yards
About
Request Service modal
Company Portal
Dispatch Center
Scene Builder
Records & History
Tow Yard Inventory
Company Fleet
Tow Yard Management
Invoices
Settings & Tools
```

## Current button audit

Total HTML buttons found:

```text
98
```

Buttons currently connected only to local visual navigation, theme switching, section switching, or opening/closing prototype modals:

```text
34
```

Buttons with no action handler in the prototype:

```text
64
```

Examples of currently nonfunctional controls:

```text
Route to Target
Route to Yard
Request Selected Call
Accept Scene
Save Full Adjusted Scene
Replay Saved
Reject & Regenerate
Record filters
Yard inventory filters
Retrieve from Yard
Search Vehicle
Claim & Transfer
Sell / Auction / Scrap
View Record
Fleet filters
Register Current Vehicle
Open Unit
Rename Yard
Change Yard Color
Open Yard Computer
Dispatch type choices
```

The responsive menu button also exists visually but does not currently have a JavaScript handler.

## Current game-data status

The prototype README correctly labels the page as standalone and not connected to BeamNG.

Current website bridge:

```javascript
setGameData(payload = {}) {
  console.info('[RedFoxTowWeb] future game data received', payload);
}
```

This is a console-only stub. It does not populate the portal or call JOB-09.

Therefore the current Tow website must not be described as functional, connected, or ready for BeamNG testing.

## JOB-09 actions already available for connection

The inspected JOB-09 v0.3.4 extension already exports real operations that a future phone-site adapter can call:

```text
openWindow
closeWindow
toggleWindow
isWindowOpen
openSettingsWindow
openGameUI
getModuleStatus
requestRandomCall
requestAbandonedCall
requestTowCall
requestCarTowCall
requestCarRecoveryCall
requestSemiRolloverCall
requestAccidentCall
registerCurrentFleetVehicle
updateFleetUnitFromCurrentVehicle
getFleet
getCompanyGarage
transferCurrentFleetUnitToCompanyGarage
retrieveCompanyVehicle
returnCompanyVehicle
getHazardSiteScan
setYardHere
addYardHere
moveYardHere
navigateToYard
captureCurrentScene
```

These are owned by JOB-09. JOB-10 may design controls and a website-side adapter that calls approved exports, but must not rewrite JOB-09 gameplay behavior.

## Missing web-facing business contracts

The website requests more business operations than the current public JOB-09 export list provides. JOB-09 needs to confirm or expose stable actions/data for:

```text
Read current pending call and active event
Accept or decline selected call
Read dispatch queue/history
Route to active target
Route to selected yard
Read saved scene templates
Load/replay selected saved scene
Accept/reject/regenerate scene
Read complete records/history with filters
Read Tow Yard custody inventory
Retrieve selected custody vehicle
Search/select custody vehicle
Claim and transfer selected vehicle
Disposition: release, sell, auction, salvage, scrap
Read disposition eligibility and remaining wait time
Read/update tow-yard names and colors
Read yard capacity, custody count, fleet count, ownership and location
Read invoices and payment status
Create/finalize invoice where appropriate
Read/update settings used by the website
Push state-change events back into the phone page
```

No fake local browser database should be substituted for these Career/gameplay operations.

## Website-side work JOB-10 can do now

JOB-10 can proceed without modifying JOB-09 by:

1. Replacing every drawn vehicle/scene with replaceable image slots.
2. Designing the mobile-only public website and Company Portal.
3. Making all browser-only navigation, tabs, filters, dialogs, confirmation windows and empty/error/loading states work.
4. Creating one central website adapter file with named actions matching JOB-09-approved exports.
5. Providing demo data only under a clearly labeled browser-preview mode.
6. Disabling or marking actions unavailable when the BeamNG adapter is not present instead of pretending they succeeded.
7. Preparing a complete button-to-action matrix for JOB-09.

## Real BeamNG screenshot replacement list

All screenshots should be taken in BeamNG using real stock vehicles or installed mods. Use clean UI-free screenshots when possible.

Recommended files and subjects:

```text
assets/images/tow/hero-recovery.webp
  Wide hero image: branded tow truck recovering a damaged vehicle on a roadway.

assets/images/tow/service-light-duty.webp
  Rollback or light-duty tow carrying a passenger car.

assets/images/tow/service-medium-duty.webp
  Medium-duty tow involving a van, box truck, bus, or RV.

assets/images/tow/service-heavy-recovery.webp
  Heavy wrecker/rotator recovering a semi, bus, or heavy machine.

assets/images/tow/service-accident-scene.webp
  Multi-vehicle crash with tow truck, police/support vehicle, cones and debris.

assets/images/tow/fleet-light-duty.webp
assets/images/tow/fleet-rollback.webp
assets/images/tow/fleet-heavy-wrecker.webp
assets/images/tow/fleet-rotator.webp
assets/images/tow/fleet-support.webp
  Individual clean fleet-unit images.

assets/images/tow/recovery-rollover.webp
  Real rollover recovery scene.

assets/images/tow/recovery-impound.webp
  Street-race or police impound scene with several real vehicles.

assets/images/tow/recovery-heavy-transport.webp
  Semi, trailer, heavy equipment, or lowboy transport.

assets/images/tow/yard-main.webp
assets/images/tow/yard-port.webp
assets/images/tow/yard-heavy.webp
  Tow-yard exterior/interior images showing stored vehicles and company fleet.

assets/images/tow/portal-dispatch.webp
  Optional live dispatch/scene image.
```

Recommended capture format:

```text
16:9 or wider for hero/recovery images
4:3 or 3:2 for fleet and yard cards
1920x1080 minimum when practical
No unrelated real-world vehicle photographs
No cartoon silhouettes
No UI text unless intentionally part of the game scene
```

## Phone-only design requirement

The owner-approved architecture is phone-only. The next Tow website preview must be designed and verified primarily at the actual phone viewport/container supplied by JOB-01.

Desktop code may remain as dormant reference code, but:

```text
PC pages stay hidden/deferred
PC parity is not a release requirement
No current cycles should be spent implementing a PC host
```

## Required next order

```text
1. Keep the uploaded Tow prototype as the visual baseline.
2. Create the replaceable real-image folder and image manifest.
3. Replace all drawn vehicles and CSS crash scenes with image slots.
4. Make every local page, tab, dialog, filter and confirmation flow work in browser preview.
5. Create the JOB-10 website adapter and exact action matrix.
6. JOB-09 supplies/approves missing business-management actions and read models.
7. Connect one read-only status action first.
8. Connect one harmless real action next, such as requestRandomCall or navigateToYard.
9. Test phone open, close, back and state refresh.
10. Add mutating business actions one at a time.
11. JOB-11 verifies logs, errors, rollback and second-map behavior.
12. David tests the exact ZIP before any working claim.
```

## Current decision for David

```text
DO NOT TEST THE TOW WEBSITE IN BEAMNG YET.
```

David may begin taking and uploading the real BeamNG screenshots listed above. JOB-10 can continue the mobile website and browser-side functionality while JOB-09 prepares the missing stable business-management contract.

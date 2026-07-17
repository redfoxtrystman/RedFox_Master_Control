# JOB-03 Pause Audit — RedFox App Store / Play Store

**Date:** 2026-07-17  
**Owner:** JOB-03 — RedFox App Store / Play Store chat / Sol  
**User:** David / Captain  
**Status:** BLOCKED / PAUSED — CLAIMED AND DOCUMENTED, NO MOD BUILD YET  
**Purpose:** Camping pause audit so David can resume after returning without losing context.

This is **not a handoff**. This is a pause record for the same JOB-03 chat.

---

## Sound off

This chat is currently assigned to:

```text
JOB-03 — RedFox App Store / Play Store
```

This chat is no longer assigned to Scrap Yard. Another chat owns:

```text
JOB-04 — Scrap Yard / Wrecking Yard
```

JOB-03 must work directly with:

```text
JOB-01 — Phone + PC Platform Core
```

Reason: the Store must install, enable, disable, update, and open apps through the same phone/PC app registry and launcher model that JOB-01 owns. JOB-03 must not create a second launcher or fork the phone/PC shell.

---

## Git records already created

### Active JOB-03 claim

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-03_REDFOX_APP_STORE_PLAY_STORE_CLAIM.md
```

Commit:

```text
cdd7d875dd053caa73b4ea1ebc253d07518bab2a
```

### Earlier temporary JOB-03 claim note

```text
PROJECT_MANIFESTS/CHAT_CLAIMS/2026-07-13_JOB-03_RedFox_AppStore_PlayStore_SOL.md
```

Commit:

```text
7c3d3fd78acca0236dd032db8dc7c4249727ebbe
```

That earlier temporary claim was part of reassignment confusion. The standard active claim is the `JOB_CLAIMS/JOB-03...` file above.

### Old JOB-04 claim released

This chat originally touched JOB-04 assignment discussion, then David reassigned JOB-03 to this chat. The old JOB-04 claim was released so the Scrap Yard chat can own JOB-04 cleanly.

Release commit:

```text
720ff155b6a5282b630b96cccb373522324fe183
```

---

## What has been done in this chat since the multi-chat switch

No runtime mod code has been changed. No ZIP has been built. No baseline has been inspected yet.

Completed coordination/documentation work:

1. Read and acknowledged the RedFox rebuild job-board structure.
2. Initially claimed JOB-04 when this chat was focused on Scrap Yard planning.
3. David clarified another chat already owns JOB-04.
4. This chat released JOB-04.
5. David reassigned this chat to JOB-03 — RedFox App Store / Play Store.
6. Created the active JOB-03 claim file in GitHub.
7. Documented that JOB-03 must work with JOB-01.
8. Defined JOB-03 ownership boundaries.
9. Defined proposed Store tabs.
10. Defined proposed Store buttons.
11. Listed the expected RedFox apps/pages that should appear in the Store.
12. Proposed an app manifest schema for JOB-01 review.
13. Proposed an installed/enabled app-state schema for JOB-01 review.
14. Listed protected files and systems that JOB-03 must not touch.
15. Listed dependency requirements before implementation.

---

## What has been tried

### Tried / corrected

- Tried assigning this chat to JOB-04 first because the live conversation had Scrap Yard context.
- David corrected that another chat already has JOB-04.
- This chat moved to JOB-03.
- Git claim records were created to prevent duplicate assignment confusion.

### Not tried yet

The following have **not** been attempted yet:

```text
No Store UI implementation.
No Store ZIP package.
No install/enable/disable runtime code.
No launcher integration.
No phone-mod inspection.
No GMUI inspection.
No music app implementation.
No games implementation.
No app download simulation.
No BeamNG runtime test.
No baseline ZIP inspection.
```

---

## Current user direction before camping

David found two or three other phone mods, including one that is a **GMUI**. David said this means RedFox can technically have its own phone completely.

David will upload those phone mods after camping.

New future requirements to preserve:

```text
1. Inspect uploaded phone mods when David returns.
2. Check whether the GMUI phone mod can support a full RedFox-owned phone shell.
3. Still coordinate with JOB-01 because JOB-01 owns phone/PC platform rules.
4. Build RedFox App Store / Play Store after the launcher/registry path is clear.
5. App Store should support apps used on phone and PC.
6. App Store should eventually support games.
7. App Store should eventually support music ability.
```

Important: these are future requirements, not completed work.

---

## Current JOB-03 mod state

```text
No JOB-03 mod exists yet.
No JOB-03 ZIP exists yet.
No JOB-03 files have been edited in a baseline package.
No runtime behavior has been proven.
```

Current honest status:

```text
BLOCKED / PAUSED — documentation and claim complete; implementation awaits baseline, JOB-01 contract, and uploaded phone mods.
```

Runtime status:

```text
RUNTIME UNPROVEN
```

Do not call JOB-03 working, fixed, or done.

---

## JOB-03 scope

JOB-03 owns:

```text
RedFox App Store / Play Store page/app
App manifest schema
Store categories and tabs
App cards
Install / Enable / Disable / Open / Update controls
Installed/enabled app state
Permission display
View logs links/buttons
Store-specific verification reports
Safe app metadata/fingerprinting rules
```

JOB-03 does **not** own:

```text
Phone shell core
PC shell core
Shared RLS/Career Bridge core
RLS original files
Scrap Yard page logic
BeamBook page logic
Import/Export page logic
Classics page logic
Insurance/Finance/Garage/Storage page logic
Tow/Recovery/Dispatch app logic
SponsorHub/FoxMail/FoxText/Sponsor Rewards logic
QA shared test format
Startup-loaded career modules
Money, inventory, garage, storage, insurance, ownership, or purchase-completion logic
```

---

## Cross-mod dependencies

JOB-03 is a cross-mod/support system because it must list and manage apps made by other jobs.

Required dependencies:

### JOB-01 — Phone + PC Platform Core

JOB-01 must define:

```text
Where app manifests live
Where installed/enabled state lives
How phone launcher reads enabled apps
How PC launcher/browser reads enabled pages
How Store opens an installed app/page
How disabled apps are hidden from normal launcher/home
How apps declare phoneEnabled and pcEnabled
How app IDs, icons, permissions, versions, and categories are validated
```

### JOB-02 — Shared RLS / Career Bridge

JOB-02 must define approved bridge permissions/capabilities and shared message names. JOB-03 should not invent its own bridge names.

Known shared message names already listed elsewhere:

```text
RedFoxRequestCareerData
RedFoxCareerData
RedFoxOpenVehiclePurchase
RedFoxVehiclePurchaseResult
RedFoxGetOwnedVehicles
RedFoxOwnedVehicles
RedFoxSellInventoryVehicle
RedFoxSellInventoryVehicleResult
RedFoxLogEvent
```

### JOB-04 through JOB-09 and JOB-12 — App/page owners

Each app owner must eventually provide:

```text
App ID
App name
Version
Category
Description
Phone enabled true/false
PC enabled true/false
Entry path
Icon path
Permissions
Status
Dependencies
Expected logs
Known limitations
```

### JOB-10 — Visual Design

JOB-10 may later polish the Store visually, but JOB-03 owns Store behavior and manifest/state rules.

### JOB-11 — QA / Logging

JOB-11 will need a JOB-03 QA intake packet once a build exists.

### JOB-00 — Coordinator

JOB-00 must approve integration order and combined release.

---

## Proposed Store tabs

The Store target should support:

```text
Home
Installed
Updates
Vehicle Markets
Services
Jobs
Tools
Experimental
Developer / Logs
```

Future additions after David approves:

```text
Games
Music
Media
Phone Themes
Utilities
```

---

## Required Store buttons

The Store should support these app-card buttons:

```text
Install
Enable
Disable
Open
Update
View permissions
View logs
```

Possible future buttons:

```text
Uninstall
Pin to phone
Pin to PC
Repair app
Reset app data
View changelog
Check compatibility
```

These future buttons should not be implemented until the registry/state model is safe.

---

## Expected app/page catalog

Initial app catalog should include entries for:

```text
redfox.scrapyard              Scrap Yard / Wrecking Yard
redfox.beambook               BeamBook Marketplace
redfox.import_export          Import / Export Yard
redfox.classics               Classics / Collector Exchange
redfox.vehicle_services       Insurance / Finance / Garage / Storage
redfox.tow_recovery           Tow / Recovery / Dispatch
redfox.sponsorhub             SponsorHub
redfox.foxmail                FoxMail
redfox.foxtext                FoxText
redfox.sponsor_rewards        Sponsor Rewards
redfox.developer_logs         Developer / Logs
```

Future app types requested by David:

```text
Games
Music player / music ability
Possible RedFox-owned phone shell if GMUI/other uploaded phone mods prove usable
```

Final app IDs must match the contracts published by JOB-01, JOB-02, and the owning app chats.

---

## Proposed manifest shape for JOB-01 review

```json
{
  "id": "redfox.scrapyard",
  "name": "RedFox Scrap Yard",
  "version": "0.1.0",
  "category": "Vehicle Markets",
  "description": "Online salvage and wrecking yard store.",
  "phoneEnabled": true,
  "pcEnabled": true,
  "entry": "sites/scrap_yard/index.html",
  "icon": "assets/icons/scrapyard.png",
  "permissions": ["vehicleShopping", "inventorySell"],
  "status": "experimental"
}
```

Possible future media/game fields:

```json
{
  "mediaCapabilities": ["audioPlayback"],
  "gameCapabilities": ["localGame", "noCareerAccess"],
  "requiresInternetLikeUI": false
}
```

Those future fields are proposals only.

---

## Proposed installed/enabled state for JOB-01 review

```json
{
  "schemaVersion": 1,
  "apps": {
    "redfox.scrapyard": {
      "installed": true,
      "enabled": true,
      "phonePinned": true,
      "pcPinned": true,
      "lastOpened": null,
      "installedVersion": "0.1.0"
    }
  }
}
```

JOB-01 may change this shape. JOB-03 must follow the final JOB-01 launcher/registry contract.

---

## Proposed permissions

Known/expected permissions:

```text
careerData
vehicleShopping
inventorySell
notifications
mapLocation
yardSellZone
experimentalProps
mail
textMessages
sponsorRewards
```

Possible future permissions for games/music:

```text
audioPlayback
mediaLibrary
gameLocalSave
controllerInput
phoneTheme
```

Future permissions must be approved by JOB-01/JOB-02/JOB-11 before implementation.

---

## Phone mods / GMUI restart plan

When David returns and uploads the phone mods:

1. Inspect each uploaded phone mod as a baseline/reference only.
2. Identify whether each mod is:
   - phone shell,
   - UI framework,
   - app launcher,
   - GMUI integration,
   - standalone app,
   - or unrelated.
3. List exact files inside each phone mod.
4. Identify whether any mod can safely support:
   - RedFox-owned phone shell,
   - app launching,
   - app install state,
   - music UI,
   - games UI,
   - PC/browser sharing,
   - BeamNG-safe logging.
5. Report conflicts with existing IceFox/FoxNet phone.
6. Coordinate with JOB-01 before using any phone-shell files.
7. Do not copy code blindly. Inspect license/reuse permission first if supplied.
8. Do not replace the existing phone unless David and JOB-01 approve.
9. If a RedFox-owned phone is approved, JOB-01 owns the shell and JOB-03 owns the Store inside it.

---

## Implementation phases when work resumes

### Phase 0 — Baseline and contracts

Required before coding:

```text
Receive/upload exact baseline ZIPs
Receive/upload phone mods / GMUI mods
JOB-01 publishes registry/open-route contract
JOB-02 publishes permission/capability naming
JOB-11 publishes testing evidence rules
JOB-00 confirms whether JOB-03 is still paused/deferred or now active
```

### Phase 1 — Static Store mockup only

Build a non-runtime Store page that:

```text
Loads catalog JSON
Shows tabs
Shows app cards
Shows permissions
Shows Install/Enable/Disable/Open buttons visually
Does not alter launcher yet
Does not alter RLS/career
Does not claim runtime success
```

Status label for this phase must be:

```text
MOCKUP / PLACEHOLDER — NOT FUNCTIONAL
```

unless David explicitly approves functional Store work.

### Phase 2 — Registry-connected Store

After JOB-01 approves the registry/state path:

```text
Read manifests
Read installed/enabled state
Write install/enable/disable through approved path
Open app/page through approved route
Log [RedFox][STORE]
```

### Phase 3 — App Store + PC page manager

Add phone/PC filtering:

```text
phoneEnabled apps show on phone
pcEnabled pages show on PC
both-enabled apps can be opened from both
disabled apps hidden from normal launcher/home
Store still shows installed/disabled apps
```

### Phase 4 — Updates / version checks

Add update behavior only after safe metadata rules exist:

```text
availableVersion
installedVersion
updateAvailable
changelog
compatibility warning
```

### Phase 5 — Games and music

After David uploads phone mods and approves media/game work:

```text
Games category
Music/media category
Audio playback test page if BeamNG UI permits it
Simple safe game app entry
No career/RLS permissions for games unless needed
No startup modules
```

---

## Files likely needed when David returns

David should upload or identify:

```text
1. Current exact FoxNet/IceFox baseline ZIP.
2. Current exact JOB-01 phone/PC platform build, if separate.
3. Current exact JOB-02 bridge contract or build, if separate.
4. The two or three other phone mods David found.
5. The GMUI phone mod.
6. Any existing RedFox app/site icons.
7. Any current Scrap Yard / BeamBook / Import / Classics / Tow / Sponsor app builds that need Store entries.
8. Any GitHub commit from JOB-01 that defines registry/open-route contract.
9. Any GitHub commit from JOB-11 that defines required QA packet format.
```

---

## Protected rules to remember after camping

```text
Do not build a ZIP until baseline is inspected.
Do not edit phone shell unless JOB-01 approves.
Do not create a second launcher.
Do not copy platform or bridge files into app mods.
Do not edit RLS originals.
Do not add startup career modules.
Do not fake money, storage, garage, inventory, ownership, or purchase completion.
Do not say working/fixed/done until David tests in BeamNG.
```

---

## Current restart checklist

When David returns, continue with:

```text
1. Ask David to upload the current baseline ZIP and phone mods.
2. Inspect uploaded zips.
3. List file trees.
4. Identify phone/PC launcher files owned by JOB-01.
5. Identify Store-owned possible files.
6. Compare GMUI/phone mods against IceFox/FoxNet needs.
7. Draft final JOB-03 manifest schema for JOB-01 review.
8. Draft Store page file plan.
9. Wait for JOB-01 route/registry contract before functional install/open code.
10. Build only after planned edit list and verification plan are posted.
```

---

## Short restart summary

JOB-03 is claimed and paused. No mod has been built. The next real work is to inspect David's uploaded phone mods, especially the GMUI one, then coordinate with JOB-01 so the RedFox Store installs/enables apps into the real phone/PC launcher system instead of making a competing launcher. Games and music are future Store categories/apps after the phone platform decision is made.

# JOB-03 Claim — RedFox App Store / Play Store

**Date:** 2026-07-13
**Claiming chat:** JOB-03 — RedFox App Store / Play Store chat / Sol
**Status requested:** CLAIMED / ACTIVE

## Hello to the other RedFox chats

Hello, fellow RedFox rebuild chats. This chat is claiming **JOB-03 — RedFox App Store / Play Store** only.

This chat will work with **JOB-01 — Phone + PC Platform Core** so the Store installs/enables apps through the shared phone/PC registry and launcher model instead of creating a competing launcher.

## Why this claim exists

The current central rollcall still lists JOB-03 as unclaimed because an earlier temporary reassignment was released. David has now reassigned this chat to JOB-03 and explicitly said this chat must work with JOB-01.

This file is the active Git evidence that JOB-03 is now claimed.

## JOB-03 owns

- RedFox App Store / Play Store page/app.
- App manifest schema.
- Store categories and tabs.
- App cards.
- Install / Enable / Disable / Open / Update controls.
- Installed/enabled app state.
- Permission display.
- View logs links/buttons.
- Store-specific verification reports.
- Safe app metadata/fingerprinting rules.

## Must work with JOB-01

JOB-01 owns:

- phone shell
- PC shell
- launcher/home behavior
- app/page registration model
- canonical app registry path
- open-app/open-page routing
- responsive phone-vs-PC host behavior

JOB-03 must consume JOB-01's final registry/launcher contract and must not replace or fork it.

Required JOB-01/JOB-03 shared agreement:

```text
1. Where app manifests live.
2. Where installed/enabled state lives.
3. How phone launcher reads enabled apps.
4. How PC launcher/browser reads enabled pages.
5. How Store opens an installed app/page.
6. How disabled apps are hidden from normal launcher/home.
7. How apps declare phoneEnabled and pcEnabled.
8. How app IDs, icons, permissions, versions, and categories are validated.
```

## Store target behavior

The Store must support:

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

Required buttons:

```text
Install
Enable
Disable
Open
Update
View permissions
View logs
```

## Apps/pages expected in Store

Initial app/page catalog should include entries for:

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

Actual final app IDs must match the contracts published by JOB-01, JOB-02, and the owning app chats.

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

JOB-01 may change this shape. JOB-03 will follow the final JOB-01 launcher/registry contract.

## Files/folders this chat will inspect

```text
PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md
PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-01_AND_APP_CHATS_PLATFORM_BOUNDARIES.md
Existing FoxNet/IceFox baseline ZIP when provided
Existing phone/PC launcher paths when provided
Existing manifest/registry files when provided
Existing app/page folders for metadata only
```

## Files/folders this chat may edit only after baseline inspection

```text
RedFox Store page/app files
Store-specific CSS/JS/assets/icons
JOB-03-owned manifest schema files
JOB-03-owned Store catalog files
JOB-03-owned installed/enabled state file if JOB-01 approves path
JOB-03 verification reports
```

## Protected files/folders this chat must not touch

```text
Phone shell / PC shell core unless instructed by JOB-01
Shared RLS/Career Bridge core unless instructed by JOB-02
RLS original files
Scrap Yard page logic
BeamBook page logic
Import/Export page logic
Classics page logic
Insurance/Finance/Garage/Storage page logic
Tow/Recovery/Dispatch app logic
SponsorHub/FoxMail/FoxText/Sponsor Rewards app logic
QA shared test format
Any startup-loaded career module
Money, inventory, garage, storage, insurance, ownership, or purchase-completion logic
```

## Hard rules accepted

- Store installs/enables apps/pages; it does not replace the phone or PC shell.
- Store feeds JOB-01's launcher/registry system.
- Store must not create a second launcher.
- Store must not copy platform or bridge files into app mods.
- No startup career modules.
- No RLS original edits.
- No fake money, inventory, garage, insurance, storage, ownership, or purchase completion.
- Disabled apps remain installed but hidden from normal launcher/home where the JOB-01 launcher supports that behavior.
- No final ZIP until baseline is inspected, planned edit list is published, and verification plan is written.

## Verification plan before any build

1. Confirm one exact FoxNet/IceFox baseline ZIP.
2. Confirm phone and PC registry/open-route contract from JOB-01.
3. Confirm permission names and bridge capability names from JOB-02.
4. Confirm Store can list app manifests.
5. Confirm Install / Enable / Disable state persists through approved path.
6. Confirm Open routes to the correct app/page without changing that app's internal logic.
7. Confirm disabled apps are hidden from normal launcher/home if launcher supports it.
8. Confirm Store does not alter RLS, career, money, inventory, garage, storage, or ownership behavior.
9. Confirm Store package includes TXT + HTML verification reports.
10. Mark runtime unproven until David tests exact build in BeamNG.

## Dependencies

- JOB-01 must publish platform/registry/open-route contract.
- JOB-02 must publish bridge permissions/capability names.
- App/page owner chats must publish final app IDs, icons, entry paths, versions, and permissions.
- JOB-11 must publish shared testing/evidence rules.
- JOB-00 must approve integration order and combined release.

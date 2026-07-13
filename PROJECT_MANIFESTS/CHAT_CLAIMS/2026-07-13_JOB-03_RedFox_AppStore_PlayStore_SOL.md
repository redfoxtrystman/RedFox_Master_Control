# Chat Claim — JOB-03 RedFox App Store / Play Store

**Date:** 2026-07-13
**Chat name:** Sol / RedFox App Store support chat
**Chosen job:** JOB-03 — RedFox App Store / Play Store
**Status requested:** CLAIMED by this chat unless David reassigns it.

## Hi to the other RedFox chats

Hi fellow RedFox rebuild chats. This chat is taking the RedFox App Store / Play Store lane only. I will not hijack phone shell, PC shell, RLS core, Scrap Yard core, BeamBook, Import/Export, Classics, Tow/Dispatch, or QA work.

## Goal

Build the app store used by the RedFox phone and PC so apps/pages can be discovered, installed/enabled, disabled, updated, opened, and inspected for permissions.

This store should include any RedFox app/page used on the phone or PC, including but not limited to:

- Scrap Yard / Wrecking Yard
- BeamBook Marketplace
- Import / Export Yard
- Classics / Collector Exchange
- Tow / Recovery / Dispatch
- Insurance / Finance / Garage / Storage pages
- FoxMail / FoxText / SponsorHub if assigned later
- Developer / Logs tools

## What this job owns

- RedFox Store / Play Store page/app.
- App manifest format.
- App cards.
- Install / Enable / Disable / Open / Update buttons.
- Installed/enabled app state.
- Store categories and tabs.
- Permission display for each app.
- Safe app fingerprinting metadata.
- Store-specific verification reports.

## Files/folders this chat will inspect

- `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md`
- Existing FoxNet/IceFox web ecosystem zip when provided
- Existing phone/PC launcher paths when provided
- Any existing app manifest or registry files when provided
- Shared bridge contract output from JOB-01/JOB-02 when available
- Existing app/page folders for metadata only

## Files/folders this chat may edit only after baseline inspection

- Store page/app files
- Store-specific CSS/JS/assets/icons
- App manifest/registry files, if JOB-01 defines the location or David approves the path
- Store installed/enabled state file if safe
- Store verification reports

## Protected files/folders this chat must not touch

- Phone shell / PC shell core unless instructed by JOB-01
- Shared RLS/Career Bridge core unless instructed by JOB-02
- RLS original files
- Scrap Yard page logic
- BeamBook page logic
- Import/Export page logic
- Classics page logic
- Tow/Recovery/Dispatch app logic
- QA shared test format
- Any startup-loaded career module

## Required store tabs

- Home
- Installed
- Updates
- Vehicle Markets
- Services
- Jobs
- Tools
- Experimental
- Developer / Logs

## Required app card buttons

- Install
- Enable
- Disable
- Open
- Update
- View permissions
- View logs

## Required app manifest fields

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

## App permissions to support

- `careerData`
- `vehicleShopping`
- `inventorySell`
- `notifications`
- `mapLocation`
- `yardSellZone`
- `experimentalProps`

## Hard rules accepted

- Store installs/enables apps/pages; it does not replace the phone or PC shell.
- No startup career modules.
- No RLS original edits.
- No hand-rolled money, inventory, garage, insurance, or storage.
- Store can show permissions but cannot invent app capabilities.
- Disabled apps should remain installed but hidden from normal launcher/home unless the Store shows them.
- No final ZIP until baseline is inspected and verification plan is written.

## Boundary with other jobs

- JOB-01 owns the phone/PC app/page loading model and shared registry path.
- JOB-02 owns the shared RLS/Career Bridge.
- JOB-04 owns Scrap Yard behavior after the Store opens it.
- JOB-05 owns BeamBook behavior after the Store opens it.
- JOB-06 owns Import/Export behavior after the Store opens it.
- JOB-07 owns Classics behavior after the Store opens it.
- JOB-09 owns Tow/Recovery/Dispatch behavior after the Store opens it.
- JOB-10 owns visual polish if assigned.
- JOB-11 owns shared QA/logging format.

## Verification plan before any build

1. Confirm only one FoxNet/Web Ecosystem ZIP is intended for test.
2. Confirm phone and PC launch/open paths from JOB-01 or baseline.
3. Confirm store can list app manifests.
4. Confirm Install / Enable / Disable state persists safely.
5. Confirm Open button routes to the correct app/page without changing that app's internal logic.
6. Confirm disabled apps are hidden from normal launcher/home if the launcher supports that behavior.
7. Confirm permissions display matches app manifest only.
8. Confirm no RLS/career startup module is added.
9. Include TXT and HTML verification reports in any package.

## Dependency notes

This chat depends on:

- JOB-01 for phone/PC launcher integration and registry location.
- JOB-02 for approved bridge permissions naming.
- Individual app chats for final app metadata, icons, and entry paths.

If JOB-01 is not ready, this chat can still build the Store page and manifest schema, but must not force launcher changes outside its lane.

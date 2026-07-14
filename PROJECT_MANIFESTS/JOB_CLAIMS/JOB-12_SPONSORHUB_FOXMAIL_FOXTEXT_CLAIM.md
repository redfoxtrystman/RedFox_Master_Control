# JOB-12 Claim — SponsorHub / FoxMail / FoxText / Sponsor Rewards

**Status:** CLAIMED — BUILDING STANDALONE TEST HARNESS / WAITING ON SHARED CONTRACTS FOR FINAL INTEGRATION  
**Owner chat:** Sponsor System chat (Sol)  
**Date:** 2026-07-13  
**Architecture directive acknowledged:** commits `a05e06829548ddc4e7f5e39ac4a060eb57a0ef70` and `4475437092b7e6012b6174d880210685a1eab928`

Hello to the other RedFox rebuild chats. I am taking the sponsor-system application job and will coordinate through this repository rather than editing anyone else's platform, bridge, or app code.

## Scope owned by this chat

- SponsorHub website/app.
- FoxMail sponsor email page/app.
- FoxText sponsor notification page/app.
- Sponsor registry and editable sponsor definitions.
- Sponsor applications, offers, accept/decline flow, contracts, XP, reputation, sponsor points, vehicle approvals, optional honor-system decal bonus, sponsor payouts, and freeroam pending-wallet logic.
- Combined BeamHesi + drift sponsor earning integration, using approved Career bridge/payment calls only.
- First guaranteed test sponsor: BeamNG GmbH Community Driver Program.

## Architecture commitment

JOB-12 is an isolated removable add-on. It will not carry or replace the shared FoxNet/IceFox front door.

The required layout is:

```text
Shared IceFox/FoxNet front-door mod
└── JOB-12 removable add-on
    ├── SponsorHub destination
    ├── FoxMail destination
    ├── FoxText destination
    ├── Sponsor-owned data/backend
    └── Sponsor manifests for the shared registry
```

Phone and PC will open the same registered SponsorHub/FoxMail/FoxText destinations and use the same bridge messages. Only responsive screen layout may differ.

## New approved intermediate step — standalone WebUI test harness

David approved a temporary standalone testing route so JOB-12 can be built and tested before JOB-01 finishes phone/PC registration.

The standalone test build may add only its own BeamNG WebUI app and Sponsor-owned backend. It must not modify, replace, copy, or bundle the phone shell, PC shell, IceFox browser core, shared navigation, FoxNet registry implementation, or RLS core.

Temporary test launch method:

```text
BeamNG UI Apps → RedFox Sponsor System Test
```

A configurable hotkey may be added later only if it uses a normal user-bindable input action and does not patch protected platform files.

The standalone WebUI contains tabs for:

- SponsorHub
- FoxMail
- FoxText
- Developer/Test Tools

This harness is intended for reuse by other isolated app chats: an app can prove its own UI/state/backend in a removable WebUI app, then later swap only the platform adapter/manifest when JOB-01 and JOB-02 publish final contracts.

The standalone harness is not the final phone/PC integration and must never be represented as such.

## Files/folders to inspect

- Current sponsor prototypes supplied by David.
- Current FoxNet/IceFox app manifest and registration contract after JOB-01 publishes it.
- Shared RLS/Career bridge contract after JOB-02 publishes it.
- QA/report templates after JOB-11 publishes them.
- Existing RLS Career reward/payment APIs only for compatibility research; no RLS core edits.

## Files/folders this job may edit

A dedicated app-owned folder only, subject to JOB-01's final manifest convention, expected to resemble:

```text
apps/sponsorhub/
apps/foxmail/
apps/foxtext/
sponsor_data/
```

For the standalone test harness, unique app-owned BeamNG paths are also permitted:

```text
ui/modules/apps/RedFoxSponsorSystemTest/
lua/ge/extensions/redfox_sponsorSystemTest.lua
scripts/RedFox_Sponsor_System/
```

Expected runtime-owned paths will use unique Sponsor identifiers and will be finalized only after the platform contract is published.

## Protected files/folders this job will not edit

- Phone shell or launcher.
- PC shell or browser core.
- Shared navigation.
- Shared app/site registry implementation.
- `ui/modModules/redfoxCareerWeb/phone/` platform files.
- Shared FoxNet/IceFox front-end bridge files.
- RLS core files.
- Career startup modules.
- Vehicle shopping, inventory, garage, storage, insurance, or money implementations.
- Scrap Yard, BeamBook, Import/Export, Classics, FoxFax, App Store, or other app-owned code.

FoxFax remains the vehicle-history/Carfax parody site. It will not be used as messaging.

## Dependencies / current hold point

JOB-12 can build and package the standalone WebUI harness now. Final phone/PC integration still waits for:

1. JOB-11 publishes the required TXT + HTML verification format.
2. JOB-01 publishes the phone/PC app registration, route, and navigation contract.
3. JOB-02 publishes the shared Career bridge/payment contract.
4. JOB-03 confirms app-store manifest requirements if/when the App Store job is activated.
5. JOB-00 freezes the exact baseline and approves integration order.

The standalone test build must not guess or modify shared integration files while these contracts are unresolved.

## Current JOB-12 work plan

### Milestone 0 — standalone test harness

- One isolated BeamNG WebUI app.
- SponsorHub, FoxMail, FoxText, and Developer Tools tabs.
- No phone/PC/FoxNet core files.
- Local Sponsor-owned persistence.
- Reset/reload/generate-offer test controls.
- Verification reports clearly marking final IceFox and Career integration as unproven.

### Milestone 1 — one complete sponsor loop

- One guaranteed BeamNG GmbH sponsor listing.
- Apply/subscribe from SponsorHub.
- Offer appears in SponsorHub and FoxMail.
- Short alert appears in FoxText.
- Accept or decline exactly once.
- Accepted contract persists.
- Sponsor XP, reputation, sponsor points, and status persist.
- No fake parts, oil, inventory, vehicle ownership, or service rewards.

### Milestone 2 — earned cash loop

- BeamHesi close-call activity produces sponsor earnings.
- Drift activity produces sponsor earnings.
- Optional safe-driving and recovery activity can be added only after their detection is proven.
- Freeroam earnings are held as pending sponsor claims.
- Career deposit uses the approved JOB-02 bridge/payment contract.
- Deposits clear only after confirmed success and do not duplicate.
- RLS event payouts may stack intentionally as separate sponsor/organizer payments.

### Milestone 3 — contracts and vehicles

- Sponsorship is assigned per Career vehicle.
- One vehicle may have multiple sponsors.
- Competing companies may sponsor different vehicles.
- The same sponsor may approve multiple vehicles and grant a fleet bonus.
- Decal use is optional and honor-system only.
- No decal location, size, coverage, windshield-banner, or wrap-percentage requirements.
- Sponsor decal folders and registry entries remain editable so David can add companies later.

## Communication events requested from shared platform

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

Names are proposals only; JOB-01/JOB-02 own the final shared contract.

## Verification plan

- Confirm the app contains no phone shell, PC shell, browser core, or duplicate FoxNet ecosystem files.
- Confirm all IDs, paths, events, and storage keys are Sponsor-specific.
- Confirm FoxMail, FoxText, and SponsorHub share one Sponsor backend state.
- Confirm one guaranteed BeamNG GmbH test offer appears exactly once.
- Confirm accept and decline persist without duplicate rewards.
- Confirm developer tools cannot repeatedly grant acceptance rewards without an explicit reset.
- Confirm standalone state survives UI app reload and game restart where the save path permits.
- Confirm sponsor rewards use the approved bridge and never hand-roll Career money in final integration.
- Confirm freeroam pending earnings deposit once and clear only after confirmed success.
- Confirm RLS event payments may stack intentionally without modifying RLS.
- Confirm optional decal representation is an honor-system per sponsor/per Career vehicle, with no size/location requirement.
- Confirm pages work through the same registered destinations on phone and PC after final integration.
- Confirm no West Coast-only shop, facility, or map assumptions exist.
- Include TXT and HTML verification reports, file tree, protected-file report, contract commit used, and unproven-runtime list.
- Stop and do not ship if any protected path is present or any dependency is falsely represented as complete.

## Message to fellow chats

Hi, everyone. JOB-12 is actively claimed for SponsorHub, FoxMail, FoxText, and sponsor gameplay only. David approved a reusable standalone WebUI test-harness step: app chats may prove isolated UI/state/backend behavior before final phone/PC integration, provided they do not copy or patch shared platform or RLS files. JOB-12 will use that method now, then consume JOB-01/JOB-02 contracts later through small adapters only. Please publish your final manifest, route, bridge, and QA contracts in GitHub when stable.
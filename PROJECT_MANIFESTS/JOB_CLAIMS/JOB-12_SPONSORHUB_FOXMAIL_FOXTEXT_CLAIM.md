# JOB-12 Claim — SponsorHub / FoxMail / FoxText / Sponsor Rewards

**Status:** CLAIMED
**Owner chat:** Sponsor System chat (Sol)
**Date:** 2026-07-13

Hello to the other RedFox rebuild chats. I am taking the sponsor-system application job and will coordinate through this repository rather than editing anyone else's platform, bridge, or app code.

## Scope owned by this chat

- SponsorHub website/app.
- FoxMail sponsor email page/app.
- FoxText sponsor notification page/app.
- Sponsor registry and editable sponsor definitions.
- Sponsor applications, offers, accept/decline flow, contracts, XP, reputation, sponsor points, vehicle approvals, optional honor-system decal bonus, sponsor payouts, and freeroam pending-wallet logic.
- Combined BeamHesi + drift sponsor earning integration, using approved Career bridge/payment calls only.
- First guaranteed test sponsor: BeamNG GmbH Community Driver Program.

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

## Dependencies / blocked items

This job can design its app-local data and UI now, but must not produce an integration ZIP until:

1. JOB-01 publishes the phone/PC app registration and navigation contract.
2. JOB-02 publishes the shared Career bridge/payment contract.
3. JOB-11 publishes the required TXT + HTML verification format.
4. JOB-03 confirms app-store manifest requirements, if SponsorHub/FoxMail/FoxText are installable through the store.

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
- Confirm sponsor rewards use the approved bridge and never hand-roll Career money.
- Confirm freeroam pending earnings deposit once and clear only after confirmed success.
- Confirm RLS event payments may stack intentionally without modifying RLS.
- Confirm optional decal representation is an honor-system per sponsor/per Career vehicle, with no size/location requirement.
- Include TXT and HTML verification reports, file tree, protected-file report, and unproven-runtime list.
- Stop and do not ship if any protected path is present or any dependency is unresolved.

## Message to fellow chats

Hi, everyone. I own SponsorHub, FoxMail, FoxText, and sponsor gameplay only. Please post your final manifest/bridge/report contracts in GitHub when stable. I will consume those contracts and will not patch your files. If SponsorHub needs a new permission, event, or deep link, I will request it here first instead of silently editing platform code.

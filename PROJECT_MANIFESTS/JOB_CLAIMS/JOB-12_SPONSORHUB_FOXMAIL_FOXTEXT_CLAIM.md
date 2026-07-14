# JOB-12 Claim — SponsorHub / FoxMail / FoxText / Sponsor Rewards

**Status:** CLAIMED — STANDALONE TEST BUILD PUBLISHED / FINAL PHONE-PC INTEGRATION PENDING  
**Owner chat:** Sponsor System chat (Sol)  
**Date:** 2026-07-13  
**Architecture directive acknowledged:** commits `a05e06829548ddc4e7f5e39ac4a060eb57a0ef70` and `4475437092b7e6012b6174d880210685a1eab928`

Hello to the other RedFox rebuild chats. I own the sponsor-system application job and coordinate through this repository rather than editing anyone else's platform, bridge, or app code.

## Scope owned by this chat

- SponsorHub website/app.
- FoxMail sponsor email page/app.
- FoxText sponsor notification page/app.
- Sponsor registry and editable sponsor definitions.
- Sponsor applications, offers, accept/decline flow, contracts, XP, reputation, Sponsor Points, vehicle approvals, optional honor-system decal bonus, sponsor payouts, and freeroam pending-wallet logic.
- Combined BeamHesi + drift sponsor earning integration, using approved Career bridge/payment calls only in final integration.
- First guaranteed test sponsor: BeamNG GmbH Community Driver Program.

## Architecture commitment

JOB-12 is an isolated removable add-on. It does not carry or replace the shared FoxNet/IceFox front door.

```text
Shared IceFox/FoxNet front-door mod
└── JOB-12 removable add-on
    ├── SponsorHub destination
    ├── FoxMail destination
    ├── FoxText destination
    ├── Sponsor-owned data/backend
    └── Sponsor manifests for the shared registry
```

Phone and PC will eventually open the same registered SponsorHub/FoxMail/FoxText destinations and use the same bridge messages. Only responsive layout may differ.

## Published intermediate step — standalone test launcher

David approved a temporary standalone testing route so JOB-12 can be built and tested before JOB-01 finishes phone/PC registration.

Published build:

```text
RedFox_JOB12_SponsorHub_Standalone_Test_v0_5_0.zip
```

Temporary launcher:

```text
Controls → search "RedFox Sponsor"
RedFox Sponsor Standalone Toggle
```

The window also opens on first extension load. It contains:

- Home/status
- Offers
- FoxMail
- FoxText
- Contracts
- Developer test claim and deposit controls

The standalone build contains no phone shell, PC shell, FoxNet/browser core, shared navigation, shared registry implementation, Angular UI app folders, or Career startup modules.

This pattern is reusable by other isolated app chats: prove app-owned UI/state/backend with a unique normal input action or app-owned test surface, then replace only the launcher/adapter when JOB-01 and JOB-02 publish final contracts. It must never be represented as final phone/PC integration.

## Current standalone test flow

1. Install only the current standalone JOB-12 ZIP; disable older sponsor ZIPs.
2. Bind `RedFox Sponsor Standalone Toggle` in Controls.
3. Open Home and generate/restore the BeamNG GmbH offer.
4. Open Offers and accept or decline.
5. Confirm accepted status is `BeamNG Community Test Driver`.
6. Confirm rewards: 500 Sponsor XP, 250 reputation, 250 Sponsor Points.
7. Reload the game and verify persistence.
8. Add a small earned test claim.
9. Enter Career and test pending-wallet deposit.
10. Report `beamng.log` evidence before calling runtime behavior working.

## App-owned paths in the standalone build

```text
lua/ge/extensions/redfox_sponsors.lua
lua/ge/extensions/redfox_sponsorStandalone.lua
lua/ge/extensions/core/input/actions/redfox_sponsor_actions.json
scripts/RedFox_JOB12_Sponsor_Standalone/modScript.lua
scripts/RedFox_FreeRoam_Sponsors/sponsor_registry.json
art/redfox_sponsors/decals/<sponsor-folder>/
mod_info/REDFOX_JOB12_SPONSOR_STANDALONE/info.json
README.txt
VERIFICATION_REPORT.txt
VERIFICATION_REPORT.html
```

## Protected files/folders this job does not edit

- Phone shell or launcher.
- PC shell or browser core.
- Shared navigation.
- Shared app/site registry implementation.
- `ui/modModules/redfoxCareerWeb/phone/` platform files.
- Shared FoxNet/IceFox front-end bridge files.
- RLS core files.
- Career startup modules.
- Vehicle shopping, inventory, garage, storage, insurance, or ownership implementations.
- Scrap Yard, BeamBook, Import/Export, Classics, FoxFax, App Store, or other app-owned code.

FoxFax remains the vehicle-history/Carfax parody site. It is not messaging.

## Final integration dependencies

The standalone system can be tested now. Final phone/PC integration still waits for:

1. JOB-11 required TXT + HTML verification format.
2. JOB-01 phone/PC app registration, route, icon, and navigation contract.
3. JOB-02 shared Career bridge/payment contract.
4. JOB-03 App Store manifest requirements if that job is activated.
5. JOB-00 frozen baseline and approved integration order.

The final build must not guess or patch shared integration files.

## Milestones

### Milestone 0 — standalone test launcher

- Published for runtime testing.
- One guaranteed BeamNG GmbH offer.
- SponsorHub/FoxMail/FoxText state in one Sponsor-owned backend.
- Normal user-bindable input actions.
- Local persistence under `settings/redfoxFreeRoamSponsors/`.
- Developer claim/deposit test controls.
- TXT and HTML verification reports.

### Milestone 1 — one complete sponsor loop

- Browse/apply or generate the BeamNG GmbH listing.
- Offer appears in SponsorHub and FoxMail.
- Short update appears in FoxText.
- Accept or decline exactly once.
- Contract, XP, reputation, Sponsor Points, and status persist.
- No fake parts, oil, inventory, ownership, or service rewards.

### Milestone 2 — earned cash loop

- BeamHesi close-call sponsor earnings.
- Drift sponsor earnings.
- Optional safe-driving and recovery activities only after detection is proven.
- Freeroam earnings held as pending sponsor claims.
- Career deposit through JOB-02's approved bridge/payment contract.
- Clear pending balance only after confirmed success.
- RLS organizer payouts may stack intentionally with sponsor payments.

### Milestone 3 — contracts and vehicles

- Sponsorship assigned per Career vehicle.
- One vehicle may have multiple sponsors.
- Competing companies may sponsor different vehicles.
- Same sponsor may approve multiple vehicles and grant a fleet bonus.
- Decal use remains optional and honor-system only.
- No location, size, coverage, windshield-banner, or wrap-percentage rules.
- Sponsor registry and decal folders remain editable.

## Requested shared events

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

## Verification state

Structural checks passed for v0.5.0:

- ZIP integrity: passed.
- Protected path violations: none found.
- Phone shell included: no.
- PC shell included: no.
- FoxNet/browser core included: no.
- Career startup module included: no.
- TXT + HTML verification reports included.

Runtime remains unproven until David tests it in BeamNG. Nobody may call it working, fixed, or done based only on static checks.

## Message to fellow chats

Hi, everyone. JOB-12 is actively claimed for SponsorHub, FoxMail, FoxText, and sponsor gameplay only. David approved and JOB-12 has now published a reusable standalone test-launcher step. Other app chats may use the same isolation pattern to prove their own UI/state/backend before final phone/PC integration, provided they use unique app-owned paths and do not copy or patch the shared platform, bridge, RLS, or another app. JOB-12 will consume JOB-01/JOB-02 contracts later through small adapters only.
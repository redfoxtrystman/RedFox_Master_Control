# Runtime Milestone — PC and Phone Auction/Wrecking Yard Purchases Working

**Date/time:** 2026-08-02 01:19 PT  
**Owner/tester:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Status:** DAVID-TESTED WORKING IN CURRENT INSTALLED ENVIRONMENT — EXACT ACTIVE PACKAGE SET NOT YET IDENTIFIED

## Confirmed owner runtime result

David reports that both the Career/PC access path and the in-game phone access path currently work for purchasing vehicles from:

- JOB-04 — Scrap Yard / Wrecking Yard;
- JOB-13 — FoxNet Online Vehicle Auctions.

The owner reports that purchases are working from both interfaces and authorizes continued use of the current working PC and phone paths.

## Important uncertainty

David does not yet know exactly what changed or which exact combination of active ZIPs/files restored this behavior.

Therefore this record does **not** assign the result to a specific build hash yet. It is a verified runtime-environment milestone, not final artifact acceptance.

## Immediate freeze rule

Until the exact active package set is captured:

```text
DO NOT refactor the current PC/phone host paths.
DO NOT remove PC access merely because an older directive deferred it.
DO NOT replace the working Wrecking Yard or Auction purchase relays.
DO NOT combine, split, rename, or clean shared runtime files blindly.
DO NOT claim a specific ZIP is the cause without evidence.
```

Preserve backups of the current working mod folder and user-folder state before further changes.

## Required capture before the next integration build

Record:

```text
BeamNG version
RLS version
Current Career profile/save backup
Every enabled mod ZIP exact filename
Every enabled mod ZIP byte size
Every enabled mod ZIP SHA-256
Loose/unpacked mod folders
Relevant user-folder overrides
PC route/page used for Wrecking Yard
Phone route/page used for Wrecking Yard
PC route/page used for Auction
Phone route/page used for Auction
One purchase result from each of the four paths
Money result
Inventory ID result
Garage/delivery result
Reload persistence result
beamng.log from the successful session
```

## Acceptance boundaries

Confirmed now:

```text
PC -> Wrecking Yard purchase: OWNER-REPORTED WORKING
Phone -> Wrecking Yard purchase: OWNER-REPORTED WORKING
PC -> Auction purchase: OWNER-REPORTED WORKING
Phone -> Auction purchase: OWNER-REPORTED WORKING
```

Not yet proven by this report:

- exact responsible build/version;
- Wrecking Yard selling, stripping, scrapping, or returned parts;
- Auction seller settlement, relisting, No Sale return, or duplicate prevention;
- JOB-09 lien-vehicle native registration/repair;
- all other FoxNet pages;
- full PC/phone parity as a project-wide requirement.

## Architecture effect

For JOB-04 and JOB-13, the current PC and phone access paths are now protected working behavior.

This does not require a new browser split or a broad architecture rewrite. It means future work must preserve both working paths unless David explicitly removes one after an exact replacement passes testing.

The earlier phone-only directive remains historical context, but it must not be used as justification to delete the currently working PC paths for Wrecking Yard or Auction.

## Next action

1. Freeze and inventory the current working installation.
2. Capture exact package identities and successful runtime evidence.
3. Continue feature work only from that frozen baseline.
4. JOB-09/JOB-02 vehicle-registration repair must not disturb the working Auction or Wrecking Yard purchase paths.

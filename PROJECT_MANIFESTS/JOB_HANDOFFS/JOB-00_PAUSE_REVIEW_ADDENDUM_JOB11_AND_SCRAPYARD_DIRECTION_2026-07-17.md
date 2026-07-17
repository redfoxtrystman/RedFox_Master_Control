# JOB-00 — Pause Review Addendum: JOB-11 Status and Scrap/Wrecking Yard Direction

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Record type:** OWNER CORRECTION AND NEW DIRECTION  
**Status:** ACTIVE PROJECT RECORD — PAUSE REMAINS IN EFFECT

---

## 1. Correction to the consolidated pause review

The earlier coordinator review described the absence of a new JOB-11 camping audit as a documentation gap. David clarified that this was intentional:

```text
David has not yet done anything with JOB-11.
David is not yet sure what specific work to assign JOB-11.
David therefore did not send the camping sound-off request to JOB-11.
```

Correct interpretation:

- JOB-11 did not miss or ignore an owner request.
- JOB-11 is intentionally parked / on-call.
- No new JOB-11 pause audit is required until David assigns work or sends the chat a direct instruction.
- Existing JOB-11 QA framework files remain available and valid as project tools.
- JOB-11 should be activated when an exact candidate ZIP, source package, integration build, or failure investigation is ready for independent QA.

This addendum supersedes only the earlier statement that JOB-11 “owes” a July 17 pause audit. It does not alter JOB-11 ownership or delete its existing QA work.

---

## 2. New owner direction for JOB-04

David has expanded the long-term Scrap Yard / Wrecking Yard concept.

The Scrap Yard should eventually be:

```text
BUYABLE OR BUILDABLE
PLAYER OWNED
OPERABLE AS A BUSINESS
LEGAL OR ILLEGAL DEPENDING ON PLAYER CHOICES
CONNECTED TO TOWING, PARTS, CRUSHING, SCRAP PROCESSING, AND FREIGHT
```

This is a major gameplay expansion, but it must not interrupt the immediate backend-first proof.

Immediate priority remains:

```text
Get the existing partially working Scrap Yard purchase/sell backend working reliably.
Prove the same backend through the development WEUI.
Then make phone and PC use that same backend.
```

Full staged direction is recorded in:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-04_PLAYER_OWNED_SCRAP_WRECKING_YARD_EXPANSION_DIRECTIVE_2026-07-17.md
```

---

## 3. Coordinator interpretation

This expansion gives the Scrap Yard a reason to exist beyond another vehicle marketplace.

The intended gameplay loop becomes:

```text
Acquire or build yard
-> receive/buy/tow vehicles
-> inspect and decide whether to resell, dismantle, store, or crush
-> recover valuable parts and materials
-> sell parts or processed scrap
-> haul scrap loads to buyers on the same or another map
-> optionally accept illegal disposal work with added risk and rewards
-> upgrade the yard and equipment
```

The legal and illegal loops must remain distinguishable in UI, save records, payouts, and risk systems.

---

## 4. Cross-job relationship

- JOB-04 owns the Scrap/Wrecking Yard business rules and feature backend.
- JOB-09 owns tow/recovery jobs and deliveries to the yard.
- JOB-06 may later own export-market destinations or freight endpoints for processed scrap.
- JOB-02 owns shared Career/RLS money, ownership, inventory, and transaction contracts.
- JOB-01 owns phone/PC route registration.
- JOB-10 owns final page appearance.
- JOB-11 remains parked until exact QA work is assigned.
- JOB-00 approves shared contracts and final integration.

No other job may silently absorb the Scrap Yard ownership, crusher, dismantling, or disposal gameplay.

---

## 5. Pause status

This is a planning and ownership update only.

```text
NO NEW SCRAP YARD RUNTIME BUILD APPROVED
NO PROPERTY SYSTEM IMPLEMENTED
NO CRUSHER ECONOMY IMPLEMENTED
NO ILLEGAL DISPOSAL SYSTEM IMPLEMENTED
NO CROSS-MAP FREIGHT SYSTEM IMPLEMENTED
```

Work resumes after David returns and the current Scrap Yard WEUI/backend candidate is recovered and tested.

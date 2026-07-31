# JOB-13 — FoxNet Online Vehicle Auctions — Active Claim

**Date:** 2026-07-30  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Active regular-chat owner:** the dedicated JOB-13 FoxNet Online Vehicle Auctions chat  
**Status:** CLAIMED — SOLE ACTIVE JOB-13 OWNER

## Owner assignment

David has explicitly created and assigned:

```text
JOB-13 — FoxNet Online Vehicle Auctions
```

This job is now recognized by the RedFox/FoxNet GitHub coordination system. Earlier documents that said the official map ended at JOB-12 are superseded for current work.

JOB-13 is not SUPPORT-01 and does not renumber any existing job.

## Sole ownership

The dedicated JOB-13 chat owns:

- online timed vehicle auctions;
- multi-lot auction state;
- bid ledgers and proxy maximum bidding;
- watchlists and outbid status;
- bid cancellation before lot close;
- memberships, fees and shipping rules;
- No Sale, return and relist behavior;
- In Transit and garage-delivery state;
- auction history/result presentation;
- JOB-13 webpage and feature-owned Lua/JS/assets;
- prepare/confirm integrations with JOB-04 and JOB-09;
- LIVE buyer/seller settlement only through approved JOB-02/Career/RLS operations.

## Protected boundaries

JOB-13 must not:

- edit JOB-04 authoritative Wrecking Yard records directly;
- edit JOB-09 Tow custody/yard records directly;
- replace Browser Core, phone layout or global UI files;
- duplicate JOB-04 scrap/strip/parts systems;
- duplicate JOB-09 Tow/Recovery/Dispatch systems;
- fake LIVE money, ownership, inventory, settlement or delivery;
- treat browse listings as legally owned seller vehicles;
- delete a source vehicle before prepare/confirm settlement succeeds.

## Dependencies

```text
JOB-01 — Phone + PC Platform Core: shared phone Browser Core and route registration
JOB-02 — Shared RLS / Career Bridge: real money, ownership, inventory, settlement and delivery
JOB-04 — Scrap Yard / Wrecking Yard: eligible Wrecking Yard source records and disposition handoff
JOB-09 — Tow / Recovery / Dispatch: eligible Tow/lien source records and custody handoff
JOB-10 — Visual Design / Real Website Polish: mobile auction-page redesign
JOB-11 — QA / Logging / Failure Triage: package, persistence and duplicate-transaction QA
JOB-00 — Coordinator / Integration / Verification: cross-job approval
```

## Current candidate

```text
RedFox_JOB13_FoxNet_Online_Auctions_v0_1_2_STANDALONE.zip
SHA-256: 1093bda6d840d3d102cf9dc71557744d7c7fa216967a2399021f9d599362b071
Status: BUILT — RUNTIME UNTESTED IN THE CURRENT FOUR-MOD MATRIX
```

Important limitation:

```text
Standalone v0.1.2 defaults to TEST mode and simulated money.
It is not the final LIVE Career/RLS auction integration.
```

## Required read-first records

```text
PROJECT_MANIFESTS/00_READ_FIRST_MODULAR_BROWSER_FEATURE_ARCHITECTURE_2026-07-30.md
Issue #40 — JOB-13 coordination/version ledger
Issue #41 — Shared Browser Core integration ledger
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_TO_JOB-13_COPART_AUCTION_HANDOFF_2026-07-29.md
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-04_TO_JOB-13_WRECKING_YARD_ONLINE_AUCTION_AND_SHARED_SELL_INVENTORY_HANDOFF_2026-07-29.md
PROJECT_MANIFESTS/INTERFACES/redfox_auction_bridge_v1.schema.json
```

## Claim rule

No other chat may claim, rename, merge or implement JOB-13 without David explicitly reassigning it.

JOB-09 auction-related source code is an integration source/legacy internal feature, not ownership of JOB-13.

JOB-04 auction-related page remnants or records are not ownership of JOB-13.

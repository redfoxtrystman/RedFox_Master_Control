# JOB-13 — FoxNet Online Vehicle Auctions — Active Chat Ownership Reaffirmation

**Date/time:** 2026-07-30 20:38 PDT  
**Job:** JOB-13 — FoxNet Online Vehicle Auctions  
**Owner:** David / Captain  
**Active development chat:** Current regular ChatGPT project chat  
**Status:** ACTIVE — EARLY TEST/PATCH DEVELOPMENT — NOT RELEASE READY

## Ownership

David explicitly reaffirmed that this chat owns JOB-13 and authorized a narrowly scoped patch to the standalone auction mod.

This ownership does not transfer or absorb any other job. JOB-13 remains responsible only for the online auction system.

## Current locked scope

JOB-13 is an online-only, multi-lot timed auction system with:

- multiple simultaneous lots and staggered closing times,
- watchlists and multiple active player bids,
- player bid cancellation until a lot closes,
- no positive reserves and no seller-approval flow,
- confidential maximum/proxy bidding,
- NPC bidding,
- membership tiers, buyer fees, buying-power limits and shipping discounts,
- damaged/missing-part vehicle condition and Fox Facts,
- shipping / In Transit delivery,
- one previous-auction results archive.

It does not own or package:

- JOB-01 phone/PC/browser shell or route registration,
- JOB-02 Career/RLS money and ownership bridge,
- JOB-04 Wrecking Yard files,
- JOB-05 BeamBook,
- JOB-07 Collector Exchange,
- JOB-09 Tow/Recovery,
- shared `redfoxCareerWeb`, phone layout, or BeamNG/RLS core UI bundles.

## Superseding corrections to the original July 29 claim

Earlier planning mentioned reserves, seller approval, pickup/storage, physical auction-yard intake, and an optional West Coast physical experience. David later rejected those for JOB-13. The current online-only rules above supersede those earlier planning items.

## Current artifact lineage

Rejected as release-ready but retained as source baseline:

```text
RedFox_JOB13_FoxNet_Online_Auctions_v0_1_2_STANDALONE.zip
SHA-256: 1093bda6d840d3d102cf9dc71557744d7c7fa216967a2399021f9d599362b071
```

Current patch awaiting BeamNG runtime testing:

```text
RedFox_JOB13_FoxNet_Online_Auctions_v0_1_3_SLIM_PATCH.zip
SHA-256: 660f6fb5eae9f54cae4173590ac08d1de7655ca3ccfc7e14b8fa7f72ed2dee1e
```

## Known status

- v0.1.2 had an unconditional full-state write approximately every two seconds while idle.
- v0.1.3 replaces that behavior with dirty-state persistence and removes unnecessary runtime material.
- Static checks pass.
- BeamNG runtime result is still pending.
- LIVE Career/RLS transactions remain intentionally locked.

## Next gate

David must test the exact v0.1.3 ZIP before any further feature build or release claim. If the narrow patch remains unstable, restarting the early JOB-13 implementation is allowed, but no restart is authorized until the patch test is recorded.

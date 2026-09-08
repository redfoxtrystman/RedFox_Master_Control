# ALL CHATS HANDOFF — RLS 2.7.1 MIGRATION / SHARED ADAPTER POLICY

**Date:** 2026-09-08

Read first:
`PROJECT_MANIFESTS/00_READ_FIRST_RLS_WEEKLY_UPDATE_COMPATIBILITY_POLICY_2026-09-08.md`

## Version status

- RLS 2.7.0.1 = current production baseline.
- RLS 2.7.1 = new migration target being reconstructed/audited.
- RLS updates frequently; do not scatter new direct RLS dependencies through job code when a compatibility boundary can own them.

## Mandatory direction

Prefer:

```text
RedFox job/business logic -> shared RLS compatibility/native vehicle transaction adapter -> exact supported RLS APIs
```

All chats touching Career inventory, garages, Recovery, save, businesses, facilities, insurance, Part Inventory/originalParts, or native vehicle creation must inspect the exact RLS version before changes and must not claim compatibility until exact-source audit + owner runtime test.

## Cross-job source references

- Car Lot 64A contains a proven native Career pseudo-location pattern preserving the same inventory ID.
- KoParts 64A contains useful real-vehicle creation code, but owner reports roughly 15 vehicles stuck in Bought Vehicles and unable to transfer. Do not copy that delivery/repair state machine without auditing the failure.
- Tow v0.5.0.39 remains JOB-09 fallback. 40b/40c are failed branches.
- Tow first narrow target: custody -> any currently-owned native garage, no hardcoded Commercial Garage.
- Tow Fleet later: Car-Lot-style pseudo-location preserving same native Career inventory ID.
- Audit RLS 2.7.1 Recovery vehicle award/current-condition system before inventing replacement lifecycle code; it may provide the safest common native path for Tow and KoParts.

## Deferred items

- Startup/unlock costs/progression for Tow, Car Lot, and KoParts so new saves do not get all money-making businesses for free.
- Tow employee RPG/NPC workforce: dispatchers, drivers/operators, recovery specialists, yard/service staff, managers; keep employee data mostly RedFox-owned and decoupled from RLS internals.

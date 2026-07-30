# JOB-09 v0.4.4.2 — Simple-Error and Per-Yard Storage Audit

Date: 2026-07-30

## Incident corrected

v0.4.4.1 allowed `storeAbandonedTarget()` to reference the local `findYardLocation()` before that local function was declared. Lua compiled the earlier reference as a global lookup. This could make **Place on Abandoned Vehicle Hold** fail while Immediate Salvage continued to work.

## Storage corrections

- Every yard/shop now has a stable `levelId::yardId` storage identity.
- Custody/impound, company/shop bays, and claimed-sales staging are counted separately for each exact yard.
- Capacity upgrades alter only the selected yard.
- Failed capacity saves restore the old capacity and refund the Career money transaction.
- Legacy records are assigned automatically only when there is exactly one possible yard; multiple yards are never silently merged into the first shop.
- Abandoned and unpaid custody records are written, saved, re-read, and verified before the live vehicle is deleted.
- Failed custody writes roll back the record and leave the vehicle and active call unchanged.
- Portal yard actions now include the exact map ID as well as the yard ID.

## Full simple-error audit

The source and independently re-extracted ZIP each passed 60 checks covering:

- all Lua compilation;
- all JSON parsing;
- all JavaScript and embedded JavaScript syntax;
- image readability;
- no local function compiled as an accidental global;
- expected BeamNG/Lua global API allowlist;
- duplicate function-name checks;
- no accidental global helper aliases;
- no `M.M` typo;
- Lua main-chunk local-variable limit;
- exact storage-key counting;
- custody transaction ordering and rollback;
- portal action parity and exact map/yard payloads;
- no native executables, unsafe paths, stock Career/RLS overrides, or copied Random Events modules;
- mocked two-yard storage and upgrade rollback;
- mocked full abandoned-hold success and failed-save safety.

## Result

- Source checks: **60 passed / 0 failed**
- Packaged-copy checks: **60 passed / 0 failed**
- Source/re-extracted ZIP comparison: **155 exact file hashes matched**
- Runtime status: **UNTESTED IN BEAMNG BY DAVID**

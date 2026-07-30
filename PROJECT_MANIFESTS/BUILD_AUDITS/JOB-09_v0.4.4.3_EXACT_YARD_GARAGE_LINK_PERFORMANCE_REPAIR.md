# JOB-09 v0.4.4.3 — Exact-Yard Garage-Link and Performance Repair

## Runtime finding

David confirmed v0.4.4.2 can store abandoned vehicles. Claiming an eligible lien vehicle displayed: `Link this RedFox yard to a real purchased RLS garage before claiming a lien vehicle.`

The claim financials and lien eligibility were valid. The failure occurred at the exact-yard purchased-garage gate.

## Code findings

1. The message is correct when the exact custody yard was never linked to a purchased RLS/Career garage.
2. v0.4.4.2 compared saved and live garage IDs without canonical conversion. JSON may store `"101"` while the live API returns numeric `101`, making a valid saved link appear missing.
3. Purchased-garage enumeration could repeat on claim and yard-manager UI frames.
4. `ensureProfile()` repeated complete profile normalization on routine UI reads.
5. claimed-shop reconciliation queried Career inventory repeatedly while the shop UI was open.
6. Scene Builder resolved every item identity every frame.
7. The linked portal rebuilt/deep-copied full state every 0.75 seconds.
8. Empty scene-placement and Random Events update paths were still entered each frame.

## Repair

- Canonical string comparison for saved/live garage IDs.
- Protected support for both observed `getFacilitiesByType` argument orders.
- Two-second purchased-garage cache with invalidation on map/link changes.
- Exact link states: linked, not linked, and stale saved link.
- Direct link button when exactly one purchased garage is detected.
- Final exact-yard link revalidation before inventory transfer.
- Profile normalization fast path and diagnostic counter.
- Shop reconciliation throttled to once per two seconds.
- Scene Builder identity cache refreshed at 0.25 seconds while drawing remains per-frame.
- Portal refresh changed from 0.75 to 2 seconds.
- Empty placement and Random Events work skipped.

## Boundary

The purchased-garage requirement remains intentional. Custody storage is virtual. Claiming creates one real Career/RLS owned vehicle and moves the same inventory ID into the linked garage. Direct sale, auction settlement, and scrap remain separate flows.

## Verification

- 47 source/static/mocked checks passed; 0 failed.
- Four garage-link mocks passed: string/number ID compatibility, unlinked diagnostic, stale-link diagnostic, direct link action.
- Profile normalization stayed at one across 100 routine status reads.
- Shop reconciliation ran once across 20 repeated portal reads.
- 500 idle `onUpdate` frames passed.
- Packaged ZIP CRC/path/payload checks passed.
- All 164 packaged files exactly matched the verified source after re-extraction.
- All packaged Lua, JSON, JavaScript, embedded JavaScript, and images passed.
- BeamNG runtime remains untested.

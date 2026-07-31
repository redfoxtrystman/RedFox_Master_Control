# JOB-09 v0.4.4.4 Build Audit — Active-Call Performance, Emergency Filtering and Same-Yard Claim

**Date:** 2026-07-30  
**Owner:** David / Captain  
**Job:** JOB-09 — Tow / Recovery / Dispatch  
**BeamNG runtime:** UNTESTED  
**Distribution classification:** STATIC/MOCK VERIFIED — BEAMNG RUNTIME TEST REQUIRED

## Order-of-operations chain

1. Approved base scope: commit `992e5e3ac07f791e0e2237d3f4808dd8822668b2`
2. Initial source checkpoint: commit `ee6e2acb38ee747f352e4504055cb3e9eac09d5e`
3. Approved performance/emergency scope addendum: commit `4175fc68a97f94ba9e8707c57da0b1dac915c860`
4. Final source checkpoint before packaging: commit `296628f962ddb2c7ab53437b105c48a8c131b7a6`
5. Package built only after final source checkpoint.

The earlier pre-addendum v0.4.4.4 local package was never distributed and was deleted before this final artifact was built.

## Exact base

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_3_ExactYardGarageLinkPerformanceRepair.zip`

- SHA-256: `61f870dbe354cda5ad6ff15b3f1a6a81c2376250108b4a7bc82d17c23fc9201e`
- Exact base hash verified before modification.

## Exact final artifact

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_4_4_ActiveCallPerformanceEmergencyFilterSameYardClaimRuntimeSlim.zip`

- SHA-256: `61b1ef9e746f5978bba2cd7e7a4368aef4c19d2fe17f6c1207142d4fd3a4f6ad`
- ZIP bytes: `881,684`
- Runtime files: `16`
- Uncompressed bytes: `1,414,870`

## Package reduction versus v0.4.4.3

| Measurement | v0.4.4.3 | v0.4.4.4 final |
|---|---:|---:|
| ZIP files | 164 | 16 |
| ZIP bytes | 1,762,242 | 881,684 |
| Uncompressed bytes | 4,690,822 | 1,414,870 |

The final package contains only the allowlisted GE extension, input action, module metadata, mod script, mod metadata, Tow Portal runtime, and Tow Portal images.

Excluded from the playable ZIP:

- historical reports and verification files;
- diffs and file inventories;
- development notes and source backups;
- external catalog-manager files;
- Random Events source;
- Browser Core/shared phone/UI paths;
- JOB-04 and JOB-13 files;
- stock Career/RLS overrides.

## Implemented functional repairs

### Same-yard lien claim

- Custody claim moves into the exact yard's virtual company/shop storage.
- No personal purchased garage prerequisite.
- Transaction ID, persistent staging, charge verification and rollback.
- Crash-before-charge and crash-after-charge reconciliation.
- Optional Personal/RLS Garage transfer remains separate.
- Legacy incomplete Career-inventory claims remain blocked for manual review rather than automatically deleted or duplicated.

### Random Events routing and outcomes

- Normal paid tow remains default.
- Minority payer-default flow remains.
- Lienable defaults enter custody.
- Non-lienable defaults close as found property.
- Spawn context is applied/restored when supported.
- Tunnel/enclosed imports are rejected by default with bounded retries.
- Rail/Train token matching is boundary-aware.

### Active-call freeze/stutter repair

Source review identified two recurring active-call operations that matched David's report that freezing stopped immediately after drop-off:

- route/marker path rebuilding every eight seconds;
- full active-job scene snapshot and JSON write every ten seconds.

Corrections:

- route/marker updates are phase/movement driven;
- pickup-route refresh requires elapsed time plus meaningful movement;
- delivery route is set at the phase transition and is not periodically rebuilt;
- manual route buttons force an update;
- active-job checkpoint default changed to 30 seconds;
- legacy untouched 10-second setting migrates to 30 seconds under settings schema 14;
- 15-second hard minimum;
- identical checkpoint fingerprints skip disk writes;
- periodic checkpoint logs suppressed;
- no complete Career inventory scan during periodic truck snapshot;
- known support metadata reused instead of repeatedly resolving identity;
- snapshot construction is protected by a re-entry/error guard;
- completed Random Events bridge scenes only run per-frame updates when explicitly marked `keepTick`.

Runtime testing is required. Static review cannot prove the freeze is fully eliminated.

### Emergency vehicle call eligibility

- Expanded police/fire/EMS detection includes Fire Department, Fire Dept, Fire Service, Fire Brigade, Ambulance Service, Municipal Police and related names.
- Emergency/service vehicles cannot enter abandoned calls or ordinary private-lien/title acquisition.
- Strong emergency metadata overrides accidental broad heavy-target classification for this safety decision.
- Emergency vehicles remain eligible for appropriate agency-paid breakdown, accident and recovery calls.
- Emergency-target chance is controlled by call type: 6% tow, 10% recovery, 12% accident.
- One emergency target starts an eight-selection cooldown.
- Civilian pool exhaustion cannot force an emergency streak.
- Emergency target calls force government/emergency-services agency payment and cannot randomly default into a private lien.
- Saved civilian scene templates do not reroll into emergency vehicles unless the saved target itself was emergency service.

## Verification

### Source verification

- Exact base SHA-256: PASS
- Approved changed-path gate: PASS
- Lua compilation: PASS
- Tow Portal `app.js` syntax: PASS
- Tow Portal `portal.js` syntax: PASS
- All JSON parse: PASS
- Git whitespace: PASS
- Claim/personal-transfer ownership boundary: PASS
- Legacy claim safety: PASS
- Random Events payment/context/tunnel/retry paths: PASS
- Rail/Train Lua token cases: PASS
- Emergency-service Lua token cases: PASS
- Route deduplication and old eight-second rebuild removal: PASS
- Checkpoint 30-second default / 15-second minimum / fingerprint / re-entry guard: PASS
- Live Random Events bridge update gating: PASS
- Transaction recovery models: PASS
- Focused source assertions: **116 passed**

### Package verification

- ZIP CRC: PASS
- Duplicate internal paths: 0
- Unsafe paths: 0
- Directory entries: 0
- Executable/native payloads: 0
- Runtime file allowlist: exact 16/16
- Source-to-re-extracted file SHA-256 matches: 16/16
- Re-extracted Lua compile: PASS
- Re-extracted JavaScript checks: PASS
- Re-extracted JSON checks: PASS
- Re-extracted images readable: PASS
- Required Tow Portal references: PASS
- Stale v0.4.4.3/runtime-backup text: absent
- Independent package assertions: **112 passed**

## Cross-package path comparison

Exact final JOB-09 active file paths compared with:

- Browser Core v0.1.0: 0 overlaps
- JOB-04 slim v0.3.5: 0 overlaps
- JOB-13 v0.1.2: 0 overlaps

This does not replace BeamNG runtime compatibility testing.

## Known deferred defect

Saved-job crash recovery detects the unfinished job but may fail to reconstruct/resume the live scene. This remains documented and deliberately deferred from v0.4.4.4.

## Required first runtime gate

1. Back up Career and `settings/redfox/`.
2. Disable every older JOB-09 ZIP.
3. Install only this exact v0.4.4.4 ZIP.
4. Fully restart BeamNG.
5. Test one ordinary Standard Tow for active-call freezing before opening other RedFox apps.
6. Test several abandoned calls and confirm no police/fire/EMS target.
7. Test ordinary paid completion and payer-default/lien completion separately.
8. Test same-yard lien claim and verify no personal-garage requirement.
9. Continue Random Events payment and tunnel/reroll tests.
10. Return `beamng.log` immediately if the freeze remains or any ownership/money/storage error occurs.

Do not mark this build runtime-proven until David completes those tests.
# 19 — JOB-09 — Tow / Recovery / Dispatch Integration — Claim Record

**Status:** CLAIMED — v0.2.1 BUILT — RUNTIME UNTESTED  
**Owner/chat title:** 19 — JOB-09 — RedFox Tow / Recovery / Dispatch — Regular Chat Workstation  
**Claim/transfer date:** 2026-07-14  
**Repository:** `redfoxtrystman/RedFox_Master_Control`

## Owner transfer directive

David explicitly transferred JOB-09 from the former Work-project chat to this regular ChatGPT workstation on 2026-07-14. This regular chat is now the sole active JOB-09 implementation and coordination owner.

The former Work chat is historical/read-only. It must not continue making JOB-09 changes unless David explicitly reverses this transfer.

## Hello to the other RedFox chats

Hello JOB-00 through JOB-12. This workstation claims exactly one role: **JOB-09 — Tow / Recovery / Dispatch Integration**.

JOB-09 owns the isolated RedFox Tow & Recovery dispatcher, tow-call generation, recovery scenes, tow-yard test locations, route-to-scene/dropoff behavior, tow-history records, impound/storage-lien test records, and future approved delivery adapters.

JOB-09 will not replace or fork the shared phone, PC, IceFox browser, platform registry, Career/RLS bridge, money, ownership, garage/storage, Scrap Yard, Import/Export, or another job's code.

## Transferred build inventory

### v0.2.0 — previous test build

`19-RedFox_TowRecoveryDispatch_v0_2_0_CallChooserYard.zip`

- Size: 29,438 bytes
- SHA-256: `217bc62ef0573feb888cf630c4d002fa49996a2fc0aa1cddc06a58e2720cc9ea`
- ZIP integrity: PASS
- Files: 27
- Runtime status in this regular chat: not independently reverified
- Known transferred concern: an accepted abandoned-vehicle call previously failed to provide a usable destination/route.

### v0.2.1 — current candidate

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_1_RolloverScenesMultiYard.zip`

- Size: 48,909 bytes
- SHA-256: `357c44f4494f7199071282ef3ec7e8e0a2f747ee19c8a12b25ed40da9e0ae2b1`
- ZIP integrity: PASS
- Files: 31
- Status: **BUILT — RUNTIME UNTESTED**
- David stated on 2026-07-14 that he had not yet tested this new build.

The exact transfer record and test plan are in:

`PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-09_WORK_CHAT_TO_REGULAR_CHAT_TRANSFER_2026-07-14.md`

## Current product scope

JOB-09 currently owns:

- Manual Standard Car Tow calls.
- Rolled Car Recovery calls.
- Semi Rollover Recovery calls.
- Multi-Vehicle Accident Cleanup calls.
- Abandoned Vehicle Recovery calls.
- Random dispatch selection with per-call-type settings.
- Scene-to-destination routing and manual route retry controls.
- Reusable relative crash-scene layouts.
- Multiple persistent player-selected tow-yard test locations per map.
- Closest-yard selection for yard-bound calls.
- Outbound response mileage plus tow mileage in quoted charges.
- Paid versus unpaid test outcomes.
- Impound lien/storage/asking-price records.
- Persistent Tow History Book entries.
- A destination-provider registration API for future approved integrations.

## Important current limitations

- v0.2.1 is not proven in BeamNG until David tests the exact ZIP.
- Tow-yard locations in v0.2.1 are free test locations, not purchased Career properties.
- Towing-company banking and transfer behavior are deferred to the real shared Career/RLS bank contract.
- Exact deformation/broken-part scene serialization is not implemented.
- Integrated IceFox phone/PC routing remains subject to JOB-01 and JOB-02 contracts.
- Scrap Yard and Import/Export delivery behavior remains owned by JOB-04 and JOB-06.

## Files JOB-09 may edit

Only JOB-09-owned files and documentation, including:

- `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`
- `lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/**`
- `lua/ge/extensions/core/input/actions/redfox_tow_recovery_dispatch.json`
- `scripts/redfox_tow_recovery_dispatch/**`
- `mod_info/redfox_tow_recovery_dispatch/**`
- JOB-09 README, changelog, testing checklist, verification reports, inventories, trees, transfer notes, and release candidates
- JOB-09 claim/status entries and JOB-09 coordination issue

## Protected files and systems

JOB-09 must not edit or package:

- JOB-01 phone/PC shell, shared IceFox browser, registry, navigation, or platform core
- JOB-02 Career/RLS bridge implementation
- JOB-03 App Store implementation
- JOB-04 Scrap Yard core
- JOB-05 BeamBook core
- JOB-06 Import/Export core
- JOB-08 insurance/finance/garage/storage core
- JOB-10 shared visual system without coordination
- JOB-11 QA core
- JOB-12 SponsorHub/FoxMail/FoxText/Rewards core
- BeamNG/RLS original money, ownership, inventory, garage, storage, insurance, property, or vehicle-shopping modules
- copied phone/PC/platform/bridge files

## Required coordination

- **JOB-00:** acknowledge this sole active claim and enforce boundaries.
- **JOB-01:** provide the canonical manifest/route/phone-PC host contract before integrated IceFox registration.
- **JOB-02:** provide approved Career/RLS actions and result/error shapes before replacing any temporary or direct behavior.
- **JOB-04:** later provide the approved Scrap Yard delivery/deep-link interface.
- **JOB-06:** later provide the approved Import/Export delivery interface.
- **JOB-10:** may polish JOB-09 presentation without changing tow logic.
- **JOB-11:** verify package boundaries, logs, route tests, all-map tests, and runtime evidence.

## Immediate test gate

David must test the exact v0.2.1 ZIP with older JOB-09 ZIPs disabled. Minimum checks:

1. Add at least one tow-yard location on the active map.
2. Accept an abandoned-vehicle call.
3. Confirm an orange route appears to the scene.
4. Use **Route to Current Target** if the route does not appear automatically.
5. Move the target more than 10 metres and confirm routing changes to the yard/dropoff.
6. Test a rolled-car and semi rollover scene for post-spawn orientation.
7. Test save/reload persistence for yard locations and Tow History Book.
8. Send the BeamNG log and screenshots for any missing route, upright rollover, Lua error, or persistence failure.

No runtime feature will be labeled working until David tests the exact candidate.

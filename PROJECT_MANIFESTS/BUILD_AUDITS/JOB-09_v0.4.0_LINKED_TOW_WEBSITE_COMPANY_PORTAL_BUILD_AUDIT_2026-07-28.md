# JOB-09 v0.4.0 — Linked Tow Website / Company Portal Build Audit

Date: 2026-07-28

## Artifact

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_0_LinkedTowWebsiteCompanyPortal.zip`

- SHA-256: `44cfe1a07628bf6a2c37a6d12388e682be2dbfccefba26207a93abf7dba8ee05`
- Size: 1,083,728 bytes
- ZIP entries: 103
- ZIP integrity / CRC: PASS
- Duplicate ZIP entries: none
- Unsafe archive paths: none
- Metadata version: 0.4.0
- Status: **BUILT — STATIC VERIFIED — BEAMNG / INSTALLED RLS RUNTIME UNTESTED**

## Static checks

- Main Lua syntax parse: PASS
- Mocked Lua extension load: PASS
- `app.js` JavaScript syntax: PASS
- `portal.js` JavaScript syntax: PASS
- All JSON parsing: PASS
- HTML duplicate-ID, local-reference, anchor, and page-panel mapping checks: PASS
- UI-to-Lua portal action bridge: 30 actions, all handled
- CSS brace balance: PASS
- Image manifest, formats, and dimensions: PASS
- Required Garage Hub function contract: PASS
- Protected stock BeamNG/RLS path scan: PASS
- Native EXE/DLL/library payload scan: PASS
- Direct per-frame save/log scan in `onUpdate`: PASS
- Exact packaged ZIP re-extraction and repeat checks: PASS
- Packaged key-file SHA-256 verification: PASS

## Main scope

- Converts the approved RedFox tow website prototype into a linked BeamNG UI app.
- Adds the animated public towing page and Company Portal.
- Wires dispatch, Scene Builder, records, custody inventory, fleet, tow yards, invoices, and settings to live JOB-09 state/actions.
- Adds Request Tow for the current owned vehicle through dynamic installed BeamNG/RLS recovery-prompt discovery with exact diagnostic logging.
- Adds scene X/Y/Z, yaw, pitch, roll, compass direction, move/rotate/exact-rotation controls, undo, equipment placement, required roster saving, saved-scene management, and scene history.
- Adds local replaceable screenshot slots with exact file paths, names, dimensions, ratios, and formats.
- Extends persistent shuffled model/configuration pools to all supported selection paths.
- Includes record-close and searchable-status corrections found during v0.3.5 testing.

## Runtime proof required

1. Add the `RedFox Tow Web Portal` UI app once.
2. Open/close JOB-09 through Garage Hub.
3. Test Request Tow and capture `[RedFox][TOW][PLAYER_TOW_REQUEST]` namespace/function/attempt.
4. Verify portal actions against live Career data.
5. Verify scene position/rotation, props, required roster save/replay, and logs.
6. Verify vehicle rotation against David's installed large vehicle library.

## Safety boundary

The build does not enable company garage movement, custody Claim & Transfer, lien/title payments, auctions/sales/scrap, or NPC-driver job execution. No stock BeamNG Career or RLS file is included or replaced.

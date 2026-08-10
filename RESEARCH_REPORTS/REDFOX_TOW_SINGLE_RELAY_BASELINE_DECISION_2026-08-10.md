# RedFox Tow Single-Relay Baseline Decision

Generated local time: 2026-08-10

Purpose:
Record the safest Tow/FoxNet web repair baseline before any mod edits are made.

## Status

This was a read-only static inspection.

No BeamNG game files were edited.
No active mod files were edited.
No ZIP files were modified.
No Tow files were copied into the active mods folder.

Verification labels:

- `static_checked`
- `code_compared`
- `zip_integrity_checked`
- `awaiting_user_test`

Runtime status:
`awaiting_user_test`

## Runtime Evidence Check

No fresh BeamNG runtime log exists after the clean-lane setup.

Latest observed log:
`D:\Games\Steam\steamapps\common\----new mods folder-----\current\beamng.log`

Latest observed log time:
2026-08-09 10:36:48 AM

Current active mod lane remains:

- `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`
- `37_racebuilder_v0_4_16_5_gate_editing_race_library.zip`

## Tow ZIPs Compared

Folder:
`D:\Games\Steam\steamapps\common\WEB PAGE TESTING DID NOT WANT TO RENAME ALL THE SZIPS`

Compared JOB09 Tow builds:

- `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_4_PC_PHONE_SAME_TOW_BRIDGE.zip`
- `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_5_GLOBAL_WEUI_FOXNET_BRIDGE.zip`
- `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_6_PC_PHONE_TYPED_BRIDGE.zip`
- `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_6_SINGLE_RELAY_WORKING_WEB_PAGES.zip`
- `19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_7_PC_PHONE_TYPED_BRIDGE_MERGED.zip`

## Important Structural Finding

All inspected JOB09 Tow ZIPs are missing:

`ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js`

They do include:

- `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`
- `ui/modules/apps/redfoxTowPortal/app.js`
- `ui/modules/apps/redfoxTowPortal/portal.html`
- `ui/modules/apps/redfoxTowPortal/assets/js/portal.js`
- `ui/modModules/redfoxCareerWeb/sites/redfox_job09_towing/app.html`
- `ui/modModules/redfoxCareerWeb/sites/redfox_job09_towing/index.html`

Implication:
If BeamNG tries to load the legacy module path `/ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js`, the JOB09 Tow ZIP alone cannot satisfy it. A small loader/adapter may be needed later, but that should be added only after a fresh runtime log proves the path is still requested.

## Best Repair Baseline

Use this as the Tow web repair baseline:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_6_SINGLE_RELAY_WORKING_WEB_PAGES.zip`

Reason:
Its web page uses one clean relay path:

1. The iframe page posts requests to the parent app.
2. The parent app calls BeamNG Lua through `engineLua`.
3. The parent app replies with state.
4. The iframe page renders that state.

This keeps PC and phone/web views closer to the same data contract.

## Single-Relay Evidence

In `v0_4_9_6_SINGLE_RELAY_WORKING_WEB_PAGES`:

`ui/modules/apps/redfoxTowPortal/assets/js/portal.js`

- `postToHost()` sends messages to `window.parent`.
- `requestPortalState()` sends `{source:'redfox-tow-portal', type:'state-request', requestId}` to the parent.
- `sendCompanyAction()` sends `{source:'redfox-tow-portal', type:'action', requestId, action, payload}` to the parent.
- The page script has zero direct `engineLua` calls.

`ui/modules/apps/redfoxTowPortal/app.js`

- `runState()` calls `getWebPortalStateJson()` through BeamNG Lua.
- `runAction()` calls `webPortalActionJsonResult(action, payloadJson)` through BeamNG Lua.
- `onMessage()` handles iframe `ready`, `state-request`, and `action`.
- Replies include the original request id when present.

## Merged-Build Risk

Avoid using this as the next baseline:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_7_PC_PHONE_TYPED_BRIDGE_MERGED.zip`

Risk:
The merged build changed the bridge shape.

`ui/modules/apps/redfoxTowPortal/assets/js/portal.js`

- Searches parent/ancestor windows for `bngApi.engineLua`.
- Tries a typed Lua proxy through `bridge.lua.extensions`.
- Builds direct Lua expressions from inside the page.
- Falls back to parent messages only after direct attempts fail.

`ui/modules/apps/redfoxTowPortal/app.js`

- Adds a global bridge listener.
- The directive-local `onMessage()` handles iframe `ready`, but no longer directly handles `state-request` or `action`.

Implication:
The merged build may work in one UI context and fail in another because the iframe page tries to become its own Lua bridge client. That is likely why PC and phone/web behavior split.

## Repair Direction After Runtime Test

Do not edit Tow yet. First complete:

1. Clean-lane runtime test.
2. Isolated RLS base runtime test.
3. Fresh `beamng.log` inspection.

If Tow repair is approved after those gates:

1. Create a workspace copy from `v0_4_9_6_SINGLE_RELAY_WORKING_WEB_PAGES`.
2. Preserve its parent-relay architecture.
3. Add only the smallest missing loader/adapter that the fresh log proves is needed.
4. Do not merge in JOB04 global Vue dist files.
5. Do not merge in JOB04 phone layout override while RLS is also being tested.
6. Retest with one Tow build active, not multiple Tow/FoxNet/JOB versions.

Do not call the repair stable until David tests it in BeamNG.

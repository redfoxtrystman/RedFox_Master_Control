# Tow v0.4.9.6 To v0.4.9.7 Surgical Diff Repair Plan

Generated local time: 2026-08-10

Purpose:
Narrow the RedFox JOB-09 Tow web/phone/PC bridge repair to the exact files that changed between the last likely working single-relay web build and the later merged bridge build David reported as breaking both PC and phone web.

This is a read-only analysis report.

No BeamNG files were edited.
No active mod files were edited.
No ZIP files were modified.
No user settings were modified.

Verification labels:

- `static_checked`
- `code_compared`
- `awaiting_user_test`

Runtime status:
`awaiting_user_test`

## ZIPs Compared

Likely working web bridge baseline:

`D:\Games\Steam\steamapps\common\WEB PAGE TESTING DID NOT WANT TO RENAME ALL THE SZIPS\19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_6_SINGLE_RELAY_WORKING_WEB_PAGES.zip`

Reported broken merged bridge:

`D:\Games\Steam\steamapps\common\WEB PAGE TESTING DID NOT WANT TO RENAME ALL THE SZIPS\19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_7_PC_PHONE_TYPED_BRIDGE_MERGED.zip`

## Entry Counts

v0.4.9.6 contains 65 file entries.

v0.4.9.7 contains 78 file entries.

The extra v0.4.9.7 entries are `_redfox_dev_notes/` documentation files only.

## Runtime Files With Different Content

Common entries with different SHA256 hashes:

- `lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json`
- `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`
- `mod_info/redfox_tow_recovery_dispatch/info.json`
- `sites/redfox_job09_towing/app.html`
- `sites/redfox_job09_towing/index.html`
- `ui/modModules/redfoxCareerWeb/sites/redfox_job09_towing/app.html`
- `ui/modModules/redfoxCareerWeb/sites/redfox_job09_towing/index.html`
- `ui/modules/apps/redfoxTowPortal/app.js`
- `ui/modules/apps/redfoxTowPortal/app.json`
- `ui/modules/apps/redfoxTowPortal/assets/js/portal.js`
- `ui/modules/apps/redfoxTowPortal/portal.html`

Important correction:
Some same-size files changed by content hash, so size-only comparison is not enough.

## Files That Only Changed Version Or Cache Tags

These appear low-risk based on line-index comparison:

- `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`
- `lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json`
- `ui/modules/apps/redfoxTowPortal/portal.html`
- `sites/redfox_job09_towing/app.html`
- `sites/redfox_job09_towing/index.html`
- `ui/modModules/redfoxCareerWeb/sites/redfox_job09_towing/app.html`
- `ui/modModules/redfoxCareerWeb/sites/redfox_job09_towing/index.html`

Observed Lua differences in `redfoxTowRecoveryDispatch.lua`:

- line 3: `v0.4.9.6` to `v0.4.9.7`
- line 2966: `version = "0.4.9.6"` to `version = "0.4.9.7"`
- line 11744: `version = "0.4.9.6"` to `version = "0.4.9.7"`
- line 12454: `version = "0.4.9.6"` to `version = "0.4.9.7"`
- line 13112: log message version string changed

Observed module manifest difference:

- `redfox_module.json` line 13 changed version only.

Observed HTML differences:

- cache-bust query strings changed from `?v=0496` to `?v=0497`
- visible footer/title version changed from `0.4.9.6` to `0.4.9.7`

Conclusion:
The Lua data owner and HTML shell should not be the first repair target unless a fresh BeamNG log shows a real Lua/runtime error.

## Main Bridge Difference

The likely breakage is concentrated in:

- `ui/modules/apps/redfoxTowPortal/app.js`
- `ui/modules/apps/redfoxTowPortal/assets/js/portal.js`

### v0.4.9.6 Working Pattern

`app.js` is the single authoritative bridge host.

Flow:

1. The Angular UI app owns access to BeamNG Lua through `bngApi.engineLua` or a compatible host bridge.
2. The iframe portal page sends `postMessage` requests upward.
3. The Angular app receives only messages from its own iframe.
4. The Angular app calls:
   - `getWebPortalStateJson`
   - `webPortalActionJsonResult`
5. The Angular app posts the resulting state back down to the iframe.

Key v0.4.9.6 behavior:

- `portal.js` has `postToHost(message)` only.
- `requestPortalState()` sends `{source:'redfox-tow-portal', type:'state-request', requestId}` to the parent.
- `sendCompanyAction()` sends `{source:'redfox-tow-portal', type:'action', requestId, action, payload}` to the parent.
- `app.js` handles `ready`, `state-request`, and `action` in the directive message listener.
- `app.js` replies with `contractVersion='redfox.tow.web.v1'` state payloads.
- `app.js` keeps request IDs so replies can map to portal requests.

### v0.4.9.7 Broken Pattern

The merged build added another global bridge path before the Angular directive and also made the portal page try direct/typed Lua access.

In `app.js`:

- Adds `installRedFoxTowGlobalBridge()`.
- Adds a global `window.addEventListener('message', ...)`.
- The global listener also handles `ready`, `state-request`, and `action`.
- The directive listener no longer runs state/action itself; it mostly forwards open/close/state.
- Error text changes to `IceFox host`, which is probably copied from another bridge attempt and may confuse diagnostics.

In `portal.js`:

- Adds ancestor scanning through `bridgeWindows()`.
- Adds direct `bngApi.engineLua` search through ancestors.
- Adds typed proxy search through `bridge.lua.extensions`.
- Adds direct calls to:
  - `getWebPortalStateJson`
  - `webPortalActionJsonResult`
- Adds `postToAncestors(message)`.
- `requestPortalState()` now tries direct Lua first, typed proxy second, and parent messaging only as fallback.
- `sendCompanyAction()` now tries direct Lua first, typed proxy second, and parent messaging only as fallback.

Likely failure mode:

The page and the host both attempt to own the same state/action bridge. In BeamNG/WEUI/phone contexts, one path can be missing, sandboxed, or pointing at the wrong window. That can leave PC and phone behaving differently even when the Lua data owner is fine.

## Surgical Repair Direction When Edits Are Allowed

Do not start from scratch.

Do not merge JOB04/JOB09/JOB13 broadly.

Do not move gameplay into Hub.

Do not edit Hub files for this repair unless David explicitly asks.

Recommended first repair build:

1. Start from the v0.4.9.6 single-relay baseline, not v0.4.9.7 merged.
2. Preserve the v0.4.9.6 `app.js` single host bridge model.
3. Preserve the v0.4.9.6 `portal.js` parent-only state/action model.
4. Carry forward only safe version/documentation notes as needed.
5. If a v0.39 runtime log proves BeamNG is requesting a missing loader path, add the smallest possible `ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js` loader/adapter.
6. Keep the adapter focused on loading the existing Tow portal and forwarding state/action to the existing JOB-09 Lua APIs.
7. Do not ship global `ui/ui-vue/dist/index.js` or `ui/ui-vue/dist/index.css` overrides.

## Exact Files To Inspect Before Editing

When David approves Tow edits, inspect these files inside the chosen baseline first:

- `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`
- `lua/ge/extensions/redfox/modules/redfox_tow_recovery_dispatch/redfox_module.json`
- `ui/modules/apps/redfoxTowPortal/app.js`
- `ui/modules/apps/redfoxTowPortal/assets/js/portal.js`
- `ui/modules/apps/redfoxTowPortal/portal.html`
- `ui/modules/apps/redfoxTowPortal/app.json`
- `ui/modModules/redfoxCareerWeb/sites/redfox_job09_towing/app.html`
- `ui/modModules/redfoxCareerWeb/sites/redfox_job09_towing/index.html`

If adding the missing loader, create only:

- `ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js`

Only create that file if the fresh BeamNG log or UI routing evidence shows it is needed.

## Runtime Test Order

This Tow repair should not be runtime-tested until the clean lane and isolated RLS base are understood.

Tow test order:

1. Test Tow gameplay-safe baseline first if gameplay/state is unknown.
2. Test v0.4.9.6 single-relay web bridge as the first web baseline.
3. If PC/phone still fail, read the fresh BeamNG log and browser/UI errors.
4. Add the smallest missing loader/adapter only if the log proves that path is requested.
5. Test PC web and phone web separately.

## Current Status

This report is a static comparison only.

No runtime result exists yet for the clean lane, RLS base, or Tow bridge after the current BeamNG v0.39 recovery setup.

Runtime status remains:
`awaiting_user_test`

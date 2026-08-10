# RedFox Tow / FoxNet Web Bridge Supplemental Findings

Timestamp: 2026-08-10
Chat ID: RF-DOC01
Chat Name: Codex Desktop
Message type: read-only supplemental scan report
Assigned role: recovery coordinator

Screen status = 🟨 NEEDS TEST

No BeamNG game files were edited.
No mod files were edited.
No ZIP files were edited.
No active mod files were moved, copied, created, deleted, or replaced.

Local full supplemental report:
`D:\RedFoxMods\reports\beamng_v039_backup_compare_20260809_232401\TOW_WEB_BRIDGE_SUPPLEMENTAL_FINDINGS_2026-08-10.md`

Verification labels:

- `static_checked`
- `code_compared`
- `zip_integrity_checked`
- `awaiting_user_test`

There is still no fresh BeamNG runtime log after the clean-lane setup. Runtime verification is waiting for David to test in BeamNG.

## Key Finding

The RedFox Tow web/phone failure appears to be a bridge/loader problem, not a reason to rewrite Tow from scratch.

JOB09 v0.4.9.6 already exports useful JSON bridge APIs:

- `getWebPortalStateJson`
- `webPortalActionJsonResult`
- `getWebPortalState`
- `webPortalAction`
- `pushWebPortalState`
- `openWebPortal`
- `closeWebPortal`

JOB09 v0.4.9.6 also has a UI app parent bridge:

- `ui/modules/apps/redfoxTowPortal/app.js`
- `ui/modules/apps/redfoxTowPortal/portal.html`
- `ui/modules/apps/redfoxTowPortal/assets/js/portal.js`

The portal page posts iframe messages to its parent:

- `source: redfox-tow-portal`
- `type: ready`
- `type: state-request`
- `type: action`

The parent bridge answers through `bngApi.engineLua(...)` by calling JOB09 Lua.

## Missing Legacy Loader

Current BeamNG v0.39 still supports legacy Angular module imports through:
`D:\Games\Steam\steamapps\common\BeamNG.drive\ui\entrypoints\main\angularModules.js`

If the game sees:
`/ui/modModules/redfoxCareerWeb`

It imports:
`/ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js`

Priority RedFox web ZIPs checked do not include that file.

This matches the earlier runtime log symptom where BeamNG requested:
`ui/modModules/redfoxCareerWeb/redfoxCareerWeb.js`

and got NOT_FOUND.

## Priority ZIP Matrix

| Build | Has `redfoxCareerWeb.js` | Has JOB09 UI app bridge | Ships global Vue dist | Recommendation |
|---|---|---|---|---|
| JOB09 v0.4.5.0 good before web split | no | older portal app exists | no | gameplay-safe baseline candidate |
| JOB09 v0.4.9.6 single relay | no | yes | no | best web data/bridge reference |
| JOB09 v0.4.9.6 PC/phone typed | no | yes | no | compare with single relay |
| JOB09 v0.4.9.7 merged | no | partial/merged | no | avoid as active baseline |
| JOB04 v0.3.2.4.9 single tow relay | no | no JOB09 app bridge | yes | reference only until global overrides removed |
| JOB13 auctions v0.1.9.5 | no | no Tow bridge | no | working page pattern reference only |

## JOB04 Risk

JOB04/FoxNet is useful as a reference for pages, catalog, phone shell, and `redfox-browser` behavior, but it is risky as an active baseline because it ships:

- `ui/ui-vue/dist/index.js`
- `ui/ui-vue/dist/index.css`
- `lua/ge/extensions/ui/phone/layout.lua`

Those can collide with BeamNG v0.39 and RLS's own v0.39 phone/router system.

## RLS Finding

RLS 2.7.0 has v0.39-aware route registration through:

- `lua/ge/extensions/overhaul/uiRoutes.lua`
- `ui/ui-vue/mods/rls_career_overhaul/index.js`

RLS registers many `phone-*` routes with `ui_router_routeManager.registerModRoutes(...)`.

RLS does not appear to ship the `redfox-browser` app by itself. The RedFox browser/app behavior likely comes from JOB04/FoxNet.

## Refined Repair Strategy

Do not start from scratch.
Do not merge JOB04 into JOB09 blindly.
Do not merge JOB13 into JOB09.
Do not ship global `ui/ui-vue/dist/index.js` or `index.css`.
Do not overwrite RLS phone layout wholesale.

Repair direction:

1. Keep JOB09 as the Tow records/state/action owner.
2. Use JOB09 v0.4.9.6 single relay as the web bridge reference.
3. Use JOB09 v0.4.5.0 as gameplay rollback baseline if v0.4.9.6 fails.
4. Add/repair a small `redfoxCareerWeb` loader only if runtime confirms BeamNG/RLS still requests it.
5. That loader should host or redirect to the existing JOB09 `redfoxTowPortal` bridge, not duplicate business logic.
6. Add a v0.39 RedFox-owned Vue adapter under `ui/ui-vue/mods/redfoxCareerWeb/` if PC/phone route integration requires v0.39 routing.
7. Keep PC and phone views separate only at the shell/view level.
8. Both PC and phone should call the same JOB09 JSON functions.

## Next Action

David needs to run BeamNG with the current clean lane and exit. Codex should then read the fresh log before any mod edits.

Coordinator action needed = yes

# BeamNG 0.39 / RLS Career Overhaul 2.7.0 Hotfix — Cross-Job UI + Save Compatibility Findings

**Date:** 2026-08-10  
**Owner:** David / Captain  
**Purpose:** Shared evidence for all RedFox jobs affected by BeamNG 0.39 UI, phone, routing, Career-save, or startup changes.

## Inspected owner-supplied inputs

### RLS Career Overhaul

`rls_career_overhaul_2.7.0_hotfix.zip`

- SHA-256: `53e439792b92d5efd65604e1476daffc3506ede3e36a37bfb61a3f6bf7f0568f`
- ZIP bytes: `40,595,505`
- Archive entries: `843`
- Internal metadata identifies: `RLS Career Overhaul v 2.7.0_hotfix`

### West Coast RLS map/content

`west_coast_usa.zip`

- SHA-256: `a0bbe40876a8f6c164b37f191d3be83b8afe1b30023900f4fc3215c526212d06`
- ZIP bytes: `93,548,270`
- Archive entries: `1,493`

No RedFox mod was modified during this source audit.

---

# 1. Critical 0.39 UI finding: old `App.vue` VFS override assumptions are no longer safe

RLS 2.7.0 contains a new official mod entry point:

`ui/ui-vue/mods/rls_career_overhaul/index.js`

Its own source comment explicitly records the reason:

- BeamNG 0.39 serves the Vue shell from `ui-vue/dist`;
- VFS `App.vue` overrides do not execute as the old mod expected;
- supported mod entry points under `ui/ui-vue/mods/` do execute.

RLS uses that mod entry point to wait for the main Vue app context, load a `.vue` component through the mod manager, create a VNode, attach the existing BeamNG Vue app context, and render the overlay into a host element.

## RedFox implication

Any RedFox job currently depending on overriding:

- `ui/ui-vue/src/App.vue`,
- a source-only Vue file that is expected to be rebuilt automatically,
- or old Angular/HUD injection timing

must be re-audited for BeamNG 0.39.

For new overlays/components, prefer an isolated `ui/ui-vue/mods/<redfox-module>/index.js` style entry point rather than replacing BeamNG's global `App.vue`.

Do **not** copy RLS's global source overrides into RedFox. Use the architecture pattern, not a competing copy of RLS/BeamNG core files.

---

# 2. Critical 0.39 routing finding: Lua router is authoritative in release builds

RLS adds:

`lua/ge/extensions/overhaul/uiRoutes.lua`

The source explicitly says that in 0.39 the Lua router is authoritative and Vue routes existing only in a mod are not automatically discovered in a normal release build.

RLS registers custom screens through:

`ui_router_routeManager.registerModRoutes(sourceId, routes)`

and unregisters them on extension unload.

Every custom route gets runtime metadata including a `luaRoute.backTarget`.

For a legacy Angular route, RLS explicitly sets:

- `meta.uiTypes = {"angular"}`
- `meta.uiTypesFilter = "only"`

This is important: a custom screen existing in HTML/JS/Vue files is no longer enough by itself. The runtime router also has to know the route.

## RedFox implication

For JOB-01/04/05/07/08/09/13 and any future phone/native UI page:

1. define the Vue/Angular screen;
2. register the matching runtime route in Lua;
3. give nested routes correct Back targets;
4. do not rely on URL/iframe state alone to represent navigation;
5. unregister mod-owned routes cleanly on unload.

A page that loads assets but never becomes an authoritative route can appear blank, reconnect forever, open and immediately close, or have broken Back/navigation behavior after 0.39.

---

# 3. New primary Vue ↔ Lua pattern

RLS's Vue views now commonly use BeamNG's bridge directly:

`import { lua } from '@/bridge'`

Examples in the supplied source call Lua modules through the bridge and navigate through:

`lua.extensions.ui_router.navigate(...)`

RLS also contains a fallback helper for mod-defined Lua namespaces that may not be represented in BeamNG's generated bridge object. The fallback ultimately calls `engineLua` only when the normal bridge has no generated method.

## RedFox implication

For a new BeamNG 0.39 native/Vue RedFox screen:

- primary path: BeamNG `@/bridge` Lua proxy + bridge events;
- navigation: `ui_router` / Lua-authoritative route;
- optional narrowly-scoped fallback for a RedFox-owned extension method if it is absent from the generated proxy;
- avoid iframe ancestor hunting and multi-level `postMessage` relay stacks for new native UI work.

Existing FoxNet webpages can remain webpages where that architecture is still intentionally required, but the old bridge path should not be assumed to be the best way to build new operational Career UI.

---

# 4. Phone architecture changed materially

RLS 2.7.0 has a full Vue phone implementation under:

`ui/ui-vue/src/modules/career/`

Notable patterns:

- Phone apps are manifest-driven.
- `phoneAppRegistry.js` reads app manifests.
- A manifest has an app ID, name, icon/tile, route, category, default position, optional unlock rules, and optional notification channels.
- Phone navigation resolves a Vue route, then asks Lua's authoritative router to navigate.
- `gameplay_phone.openRoute()` is a Lua-side phone route opener and calls `extensions.ui_router.navigate(...)`.
- Phone notifications are dispatched through `ui_phone_layout.fireNotification(...)` rather than each feature manually owning a notification popup.

## RedFox implication

The longer-term clean path for FoxNet phone apps is now clear:

```text
RedFox app manifest
        +
RedFox Vue view/component
        +
registered Lua runtime route
        +
RedFox Lua backend through @/bridge
```

This is more robust for 0.39 than treating every operational app as a nested browser iframe.

Do not mass-port everything at once. Prove one RedFox route/app first.

---

# 5. Legacy Angular is not completely dead, but it now needs explicit compatibility handling

RLS still contains the Used Car Auction under:

`ui/modModules/usedAuction/`

The supplied `usedAuction.js` still mounts into the Angular compatibility root and calls Lua from there. RLS therefore proves that Angular can still coexist with the 0.39 Vue shell.

However, RLS's new routing code explicitly marks its Angular-only route type, and the new Vue shell contains a dedicated legacy Angular host.

## RedFox implication

For an old JOB-13/JOB-09 Angular UI wrapper:

- adding an icon or retry timer is not the complete 0.39 solution;
- the route/host type must also be valid under the 0.39 Lua router;
- the Angular compatibility host has to be the actual context running the wrapper.

This is directly relevant to JOB-13 v0.1.9.6: that build improved startup tolerance, but it was created before this 2.7.0 hotfix source was supplied. Its runtime route/host assumptions now need re-audit against this evidence.

---

# 6. Career save API / identity findings

RLS 2.7.0 overrides the Career save system and now internally uses profile terminology:

- `currentProfile`
- `currentSavePath`
- `currentDisplayName`
- `creationDateOfCurrentProfile`

Its `getCurrentProfile()` returns:

```text
first return  = currentProfile
second return = currentSavePath
```

RLS keeps `getCurrentSaveSlot` only as a compatibility alias to `getCurrentProfile`.

Therefore the established RedFox rule remains correct for this RLS hotfix:

```lua
local _, savePath = career_saveSystem.getCurrentSaveSlot()
```

or, preferably when targeting this new API explicitly:

```lua
local _, savePath = career_saveSystem.getCurrentProfile()
```

The **second return remains the filesystem save path**.

### Additional identity evidence

RLS persists `creationDate` in the Career save's `info.json` and exposes `currentDisplayName` separately from the sanitized profile key.

This is useful for the RedFox same-slot-recreation problem. A path by itself is not a strong enough Career-instance identity. Where possible, RedFox persistence should record a composite identity such as:

```text
profile key
+ save path
+ authoritative profile creationDate
```

and reject/reset stale process-memory state when those do not all match.

RLS also emits an `onSetProfile(currentSavePath, profile)` hook when the profile changes. RedFox modules with per-Career runtime registries should use the profile-change lifecycle to clear/re-key in-memory state.

---

# 7. Career creation bridge signature changed

In RLS's 0.39-updated Vue profile store, the source notes that Career creation now uses:

```text
(name, autosave, startingOptionsObject)
```

rather than old positional arguments after the third parameter.

## RedFox implication

Any developer utility or Career helper calling Career creation/loading with old long positional signatures must be audited. Passing a legacy boolean/string where 0.39 expects an options object can fail or be misinterpreted.

---

# 8. Startup/load-order changes are real

RLS's `modScript.lua` deliberately delays loading its extension manager because the mod manager temporarily wraps `extensions.load` while executing `modScript`.

RLS's 0.39 extension manager also registers runtime routes before its override manager reloads the UI.

Its override manager documents another important change: several core/UI extensions are already alive before a mod's `modScript` runs in 0.39, so blindly unloading/reloading early core modules can tear through dependencies.

## RedFox implication

- Do not assume `modScript.lua` runs before relevant UI/core extensions exist.
- Avoid reloading core router/UI modules as a compatibility fix.
- Load RedFox-owned extensions explicitly and idempotently.
- Register routes before opening them.
- If startup order matters, use a bounded deferred load of RedFox-owned code rather than replacing/reloading BeamNG core modules.

---

# 9. West Coast evidence still useful

The supplied `west_coast_usa.zip` confirms these RLS content identifiers remain present:

- `joesJunkDealership`
- `usedCarAuctionEntry`
- `auctionCounter_1`
- `auctionCounter_2`

The auction map assets/triggers and Joe's Junk facility remain useful integration evidence for JOB-04/JOB-13. The main breakage from 0.39 is UI/routing/startup compatibility, not disappearance of these West Coast content IDs.

---

# 10. Required cross-job action

Every RedFox job with UI should classify itself into one of these buckets before another 0.39 patch:

### A — Pure Lua/no custom UI
Audit only startup/save API compatibility.

### B — Legacy Angular/HUD App
Verify Angular compatibility host + explicit runtime route + app metadata. Do not assume old app injection alone is sufficient.

### C — FoxNet iframe/webpage
Verify the host route itself survives 0.39. If the shared host is broken, stop feature-specific rewrites and repair the owning host job.

### D — New/native Vue UI
Use:

- `ui/ui-vue/mods/<module>/index.js` when an isolated mod entry point is appropriate;
- BeamNG `@/bridge` for Vue ↔ Lua;
- Lua `ui_router_routeManager.registerModRoutes` for custom runtime routes;
- route-aware Back targets;
- RedFox-owned extension/state only.

---

# 11. Immediate JOB-13 consequence

Do not call JOB-13 v0.1.9.6 a confirmed 0.39 fix yet.

It remains **runtime unproven**, and this new RLS 2.7.0 source shows two areas that v0.1.9.6 did not fully prove:

1. explicit Lua runtime-route registration for the Auction screen/host;
2. whether the route should remain legacy Angular or move to an isolated native Vue mod entry point.

Next JOB-13 work should start from the exact v0.1.9.5/1.9.6 source diff and add only the smallest route/host correction proven by this RLS source. Do not rewrite bidding/economy/save code to solve a UI routing problem.

---

# Acceptance proof for one RedFox 0.39 native UI

Before broad migration, prove one tiny app:

1. RedFox Lua extension loads.
2. Lua registers one unique runtime route.
3. One `ui/ui-vue/mods/<module>/index.js` or route-backed Vue component loads.
4. Vue calls one read-only RedFox Lua function through `@/bridge`.
5. Lua returns one literal value.
6. UI displays it.
7. Back closes/navigates correctly.
8. F5 UI reload restores the route/app without duplicate registration.
9. Ctrl+L Lua reload does not break the route.
10. Career Save A → Save B → Save A keeps state isolated.

Only after that proof should additional FoxNet operational pages be migrated.
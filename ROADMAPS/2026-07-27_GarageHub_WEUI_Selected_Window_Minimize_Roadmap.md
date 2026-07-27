# RedFox GarageHub / WEUI Selected-Window Minimize Roadmap

**Date/time:** 2026-07-27 16:32 PDT / America-Los_Angeles  
**Project:** RedFox GarageHub native ImGui/WEUI window control  
**Current production baseline:** `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`  
**Current isolated test:** `RedFox_WEUI_Windows_Minimize_Test_v0_2_0_ONE_KEY.zip`  
**Incident report:** `INCIDENT_REPORTS/2026-07-27_GarageHub_WEUI_Minimize_GitHub_Order_Of_Operations_Failure.md`  
**Incident-report commit:** `b3e339e2bb7657f7c545aa1702a9ce8dbab88113`  
**Runtime status:** partial behavior observed; production behavior not proven

---

## 1. Final user objective

GarageHub must act as the control center for selected BeamNG native ImGui/WEUI windows without requiring the other mods to be edited.

David must be able to:

- drag normal gameplay ImGui windows together and dock them without using F11;
- open a connected mod window from a GarageHub tile/menu entry;
- choose which connected windows participate in group minimize;
- mark windows such as Career Dev as `Keep Open` so they remain visible during testing;
- minimize selected windows with one key or one visible Hub button;
- restore only the windows that were open before the minimize action;
- avoid reopening every connected app during restore;
- see only Hub-connected/registered windows in the Hub's own window dropdown;
- preserve the native dock arrow and X behavior instead of attempting a fragile Dear ImGui internal title-bar replacement;
- keep the other mods unchanged unless one proves impossible to control externally and David explicitly approves an exception.

---

## 2. Work completed before this audit

### GarageHub baseline capabilities already present in v0.5.11

The uploaded Hub already contains:

- `lua/ge/extensions/redfox/modulesHub.lua`;
- `lua/ge/extensions/auto/redfoxModulesHubAuto.lua`;
- a Module Manager;
- an Adapter / Manual Link Manager;
- `settings/redfox/garage_hub/adapter_registry.json`;
- known adapter attempts for Spawner, VTOL, Dynamic/Random Gravity, PSI/Tire, Race Manager, Flood, and other modules;
- generic extension loading and common open/toggle function probing;
- support for `setShowUI(true)` and `setShowUI(false)` patterns;
- limited close-function mapping;
- saved Hub settings and remembered modules;
- Spawner and Race/Event bridge behavior;
- the global UI settings provider;
- the existing theme/readability system.

The Hub already has enough foundation to become the window controller. A separate cross-mod bridge framework is not the default next step.

### v0.1.1 test findings

`RedFox_WEUI_Docked_Minimize_Test_v0_1_1_KEYBINDS.zip` was inspected and found to have:

- three separate keybinds instead of one group action;
- action commands that referenced a loader without ensuring it was loaded;
- no extension under `lua/ge/extensions/auto`;
- editor-path callbacks;
- a fake minimize state that only reduced window contents instead of hiding the docked tab/window.

### v0.2.0 isolated test

`RedFox_WEUI_Windows_Minimize_Test_v0_2_0_ONE_KEY.zip` added:

- one action/key for all three test windows;
- normal GELua `onUpdate()` ImGui drawing;
- one auto-loader;
- three stable hidden ImGui IDs;
- per-window hide controls;
- group hide and restore controls;
- static diff and ZIP verification.

This proved the basic Hub-controlled visibility concept but not the production integration.

---

## 3. Runtime observations and failed assumptions

David's screenshots and testing established:

1. Normal gameplay windows can be docked by dragging them together; F11 is not required.
2. The built-in down arrow changes into a docked-tab list when multiple windows share a dock node.
3. A master action can hide some windows, but the current Hub cannot close every external window.
4. Dynamic Gravity and Node Grabber remained visible when other windows disappeared.
5. Career Dev must be able to remain open while other selected windows minimize.
6. A universal unconditional `hide all` action is the wrong production behavior.
7. There is currently no visible one-click minimize control in the Hub.
8. The native dock-arrow dropdown lists dock-node windows, not the filtered list of Hub-connected apps David wants.
9. The Hub must not guess that a successful open function also provides a safe close function.
10. Restore must use the exact pre-minimize open state, not `open all connected apps`.

---

## 4. Locked production design

### 4.1 Hub-owned Linked Window Registry

GarageHub will maintain a registry entry for each connected app. The Hub ZIP is the only file changed by default.

Each entry must support these fields:

```text
id
name
category
extension load candidates
open function candidates
close/hide function candidates
toggle function candidates
window title / stable ImGui ID when known
control level
includeInGroup
keepOpen
restoreWithGroup
lastKnownVisible
wasOpenBeforeGroupMinimize
status / last error
```

Control levels:

```text
FULL       = definite open plus definite close/hide
TOGGLE     = toggle only; state must be tracked carefully
OPEN_ONLY  = Hub can open but cannot safely close
UNMAPPED   = actual mod must be inspected before control is promised
```

The UI must show the control level plainly. No app may be described as fully controllable until its exact installed code proves that.

### 4.2 Hub Windows dropdown

Add a dedicated top-bar menu:

```text
Hub  Windows  Spawner  Race/Event  Flood  Infection  VTOL  Tire/PSI  Gravity  View  Theme  Help
```

The `Windows` dropdown must list only registered/connected Hub apps, not every Dear ImGui window in the dock node.

Each row must provide:

- visible/open status;
- `Open` or `Restore` action;
- `Close` or `Minimize` action when supported;
- `Minimize with Hub` checkbox;
- `Keep Open` checkbox;
- `Restore with Hub` checkbox;
- control-level status;
- last failure text when a call did not work.

The settings must persist in the normal RedFox settings location.

### 4.3 One-click and one-key behavior

Add one visible compact Hub control, preferably a `—` button at the right end of the Hub menu bar. Do not patch Dear ImGui internal title-bar code.

One global action and the visible button must call the same Hub function.

When the selected group is open:

1. Snapshot the visibility of every registered app.
2. Ignore every app marked `Keep Open`.
3. Act only on apps marked `Minimize with Hub`.
4. Hide/close only apps that were open.
5. Record exactly which apps were successfully hidden.
6. Reduce GarageHub to its compact restore state or leave a small Hub restore strip/gear.
7. Do not falsely mark unsupported apps as minimized.

When restoring:

1. Restore GarageHub.
2. Reopen only apps that were open before the group minimize.
3. Do not open apps that were previously closed.
4. Continue leaving `Keep Open` apps untouched.
5. Report any app whose restore call failed.

Mixed-state behavior must not blindly open all windows. The Hub should display the state and let the user explicitly choose minimize or restore when the group is mixed.

---

## 5. Read-only target-mod audit required before coding

Before the next Hub version, inspect the exact installed ZIPs for:

- RedFox Spawner Control Panel v0.1.29;
- RedFox VTOL Drive Tuning v55;
- Dynamic Gravity v0.2;
- RedFox Node Grabber Unlocker;
- RedFox Career Dev Unlocker;
- RedFox Tow & Recovery Dispatch;
- any Correspondent app David wants connected;
- any additional native ImGui/WEUI app selected for the first group.

For each mod, record:

- extension path and BeamNG extension table name;
- exact keybind command;
- exact open function;
- exact close/hide function;
- exact toggle function;
- whether visibility is private/local;
- window title and hidden ID;
- whether it draws in `onUpdate`, editor callbacks, vehicle Lua, or another path;
- whether Hub-only control is possible;
- whether the action is statically verified or runtime proven.

The mods remain read-only. A mod edit is considered only when it exposes no external close/hide/toggle path, and only after David explicitly approves that exception.

---

## 6. Version plan

The next version number is not assigned until the GitHub pre-build status is committed and the exact Hub baseline is confirmed. Do not assume `v0.5.12` or reuse an unrelated `v0.6.x` branch without reconciling the repository history.

### Phase A — Repository reconciliation

- Read all current RF-HUB01 status files and newer/parallel Hub branches.
- Determine whether the uploaded `v0.5.11` is the correct production baseline or whether a later proven Hub exists.
- Identify duplicate or conflicting Hub version lines.
- Commit the selected baseline and rollback point before editing.

### Phase B — External app control audit

- Inspect each target mod read-only.
- Produce a control matrix.
- Do not create a Hub build until the matrix identifies which apps are `FULL`, `TOGGLE`, `OPEN_ONLY`, or `UNMAPPED`.
- Commit the matrix to GitHub.

### Phase C — Hub registry implementation

- Extend the existing adapter/manual-link system rather than replacing it.
- Add selection, pin/keep-open, visibility snapshot, and restore-state fields.
- Preserve all current Hub adapters and bridge behavior.
- Add no gameplay logic to Hub.

### Phase D — Hub Window Manager UI

- Add the `Windows` dropdown.
- Add per-app selection and keep-open controls.
- Add a compact visible group-minimize button.
- Follow the RedFox auto-resize, wrap, scroll, save-position, and safe-size law.

### Phase E — One global action

- Replace test-only actions with one GarageHub-owned action.
- Use the same function for the key and visible button.
- Do not add separate keys for each app unless David asks later.

### Phase F — Static verification

Before packaging:

- inspect the selected baseline;
- list protected files/functions/IDs/settings paths;
- generate a side-by-side colored diff;
- verify only intended Hub files changed.

After packaging:

- reopen the ZIP;
- verify extension paths/names;
- verify window IDs;
- verify input action ID and default input map;
- verify adapter registry preservation;
- verify Module Manager and Manual Link Manager preservation;
- verify Race/Event and Spawner bridge preservation;
- verify theme/global UI provider preservation;
- verify no target mod files were included or modified;
- calculate and record SHA-256.

### Phase G — Runtime test gate

David's first test must check:

1. Hub opens normally.
2. All target apps still open independently.
3. Docking works through normal gameplay drag-docking.
4. `Keep Open` Career Dev remains visible.
5. Selected windows minimize from the Hub button.
6. The same selected windows minimize from the one key.
7. Unselected windows remain untouched.
8. Restore reopens only windows that were previously open.
9. Closed apps stay closed.
10. Dock positions return where BeamNG's saved ImGui layout supports it.
11. Repeated minimize/restore cycles do not invert toggle-only apps.
12. Closing one app manually does not corrupt the stored group state.
13. Restarting BeamNG preserves selection/keep-open settings.
14. No duplicate windows, action IDs, settings files, or extension names appear.

Runtime results must be committed before another version is created.

---

## 7. Mandatory GitHub sequence for every future version

### Before coding

Commit:

- timestamp;
- chat/job ID;
- exact baseline ZIP and SHA-256;
- requested change;
- protected behavior;
- files expected to change;
- known limitations;
- intended version number.

### After source changes, before ZIP delivery

Commit:

- changed-file list;
- why each file changed;
- source diff summary;
- updated roadmap;
- static status;
- unresolved questions.

### After ZIP creation

Commit:

- artifact filename;
- SHA-256;
- reopened-ZIP verification results;
- exact runtime test list;
- `RUNTIME UNTESTED` status.

### After David's test

Commit:

- pass/fail result for every test;
- screenshots/log errors described by David;
- last known good and first bad version;
- rollback decision;
- exact next step.

No next version begins until that runtime-result commit exists.

---

## 8. Protected features and exclusions

The next Hub build must preserve:

- visible name `RedFox Garage Hub`;
- current extension and auto-loader paths;
- existing Module Manager;
- existing Adapter / Manual Link Manager;
- external adapter registry;
- current theme/readability/settings behavior;
- global UI provider;
- Spawner bridge;
- Race/Event bridge;
- existing known adapters;
- unique IDs and settings paths;
- legacy/fallback UI behavior where present;
- no ownership of module gameplay.

Do not:

- replace the native dock arrow;
- patch Dear ImGui internals;
- force-close every open ImGui window;
- modify Career Dev or other target mods by default;
- assume a toggle function is safe without state tracking;
- reopen all registered apps during restore;
- change unrelated Hub menus, themes, gameplay bridges, or layout systems;
- claim runtime success from static ZIP checks.

---

## 9. Current stop point

Audit and roadmap are now recorded in GitHub. The next action is not another ZIP. The next action is repository reconciliation plus read-only inspection of the exact target mods, followed by a committed control matrix and pre-build status.

# RF-HUB01 GarageHub Takeover — Pre-Build Status

**Timestamp:** 2026-07-27 19:00 PDT / America-Los_Angeles  
**Chat:** BeamNG current mods / GarageHub minimize and discovery takeover  
**Owner:** Sol / GPT-5.6 Thinking  
**Status:** PRE-BUILD — NO NEW HUB ZIP CREATED  
**Repository:** `redfoxtrystman/RedFox_Master_Control`

---

## User-approved direction

David instructed this chat to take over RedFox GarageHub and make it useful again. The approved direction is:

1. Remove the old hard-coded top menu names for mods that are not currently installed or used, including Flood and Infection.
2. Preserve the Hub's useful theme/accessibility/global UI control behavior.
3. Replace placeholder and stale mod menus with actual discovered/connected mods.
4. Search for RedFox-compatible mods and add discovered apps to a dynamic top/window list.
5. Open connected mod windows from the Hub without editing the external mods whenever their exported functions/keybind commands permit it.
6. Add selected minimize/restore behavior with per-window exclusions such as `Keep Open` for Career Dev.
7. Update GitHub at every patch boundary: before coding, after source edits, after packaging, and after David's runtime test.
8. A clean rewrite is allowed only if it reuses and preserves the proven core data/functions rather than discarding working behavior.

---

## Source baseline currently available

```text
1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip
SHA-256: af1d1f11691377717d3bc15db4c28ed89cda6cb3b6d93a0f5ff48aeedda69fe1
```

This is the only complete Hub source artifact currently uploaded to the active chat.

Protected files from this baseline:

```text
lua/ge/extensions/redfox/modulesHub.lua
lua/ge/extensions/auto/redfoxModulesHubAuto.lua
settings/inputmaps/keyboard_redfox_modules_hub.json
settings/redfox/garage_hub/adapter_registry.json
info.json
mod_info/REDFOX_MODULES_HUB/info.json
```

Protected capabilities:

- readable native ImGui Hub window;
- theme presets and custom theme controls;
- font, button, padding, contrast, and DPI/global ImGui scaling controls;
- settings save/load paths;
- `getGlobalUISettings()` and global theme provider functions;
- current Hub extension/autoload identities;
- current Race Manager and Spawner bridge knowledge as reference data;
- Module Manager and Manual Link Manager concepts;
- unique RedFox IDs and no module gameplay inside Hub.

---

## Important repository reconciliation finding

GitHub contains an older parallel CleanCore branch:

```text
1-RedFox_GarageHub_v0_6_0_CleanCore.zip
1-RedFox_GarageHub_v0_6_1_CleanCore_UIRestore.zip
1-RedFox_GarageHub_v0_6_2_Core_UI_Cleanup.zip
```

Repository records say v0.6.1/v0.6.2 removed old mod-specific dropdowns/adapters while preserving the normal readable Hub UI and theme system. However, those complete ZIP/source artifacts are not currently available in this chat or stored as source files in the repository records inspected here. Only status text is available.

Therefore:

- do not pretend v0.6.2 source is available;
- do not blindly continue the v0.5.x number line or v0.6.x number line yet;
- use uploaded v0.5.11 as the auditable source baseline;
- use the CleanCore records as architecture guidance;
- assign the next version only after the clean-core source design is reconciled and the target-mod control matrix is completed.

---

## Current v0.5.11 audit findings

The uploaded `modulesHub.lua` is approximately 2,184 lines and contains substantial useful code mixed with stale placeholders and hard-coded assumptions.

### Useful core to preserve/refactor

- JSON settings read/write and mirrored settings paths;
- theme/accessibility controls;
- native ImGui window and mode handling;
- generic extension call helper;
- manifest parsing fields for open, close, toggle, minimize, restore, visibility, settings, and game UI functions;
- adapter/manual-link serialization;
- Module Manager and Manual Link Manager UI foundations;
- extension loading and one-key action foundations;
- current Spawner/Race function knowledge.

### Code to remove from active UI/core

- static `moduleMenus` entries for Flood, Infection, VTOL, Tire/PSI, Gravity and other unused placeholders;
- hard-coded placeholder gameplay menus;
- menu-manager behavior for stale top menus;
- active known adapters for mods not actually detected/approved;
- startup auto-opening based on placeholder menu entries;
- claims that remembered modules are active merely because the Hub attempted to open them;
- stale version/help text referring to v0.5.3/v0.5.8 inside v0.5.11.

### Discovery weakness to replace

The existing scanner is partly dynamic but still depends heavily on:

- a hard-coded list of known manifest paths;
- RedFox mods already containing `redfox_module.json`;
- a small list of scan roots and manifest names;
- manual links or guessed known adapters for mods without manifests.

The next design must perform a real VFS search for compatible manifests and action/extension metadata, while clearly separating:

```text
DISCOVERED + FULL CONTROL
DISCOVERED + TOGGLE ONLY
DISCOVERED + OPEN ONLY
DISCOVERED + UNMAPPED
MANUAL CONNECTION
```

No unsupported app may be described as fully controllable.

---

## Locked clean architecture

The new Hub core will have only these permanent top-level menus/controls:

```text
Hub | Apps/Windows | Theme | Help | [group minimize button]
```

`Apps/Windows` is generated from actual discovery and saved manual connections. No Flood, Infection, VTOL, Gravity, PSI, Spawner, Race/Event, or other mod gets a permanent top-level menu merely because old code knows its name.

A discovered app entry may contain:

```text
id
visible name
version
category
source manifest/action/manual adapter
extension load path
open command/function
toggle command/function
close/hide command/function
minimize command/function
restore command/function
visibility query function
window title/ID
control level
minimize with Hub
keep open
restore with Hub
last known state
last error
```

Apps appear automatically when discovered, but they are not automatically opened.

---

## Patch sequence

### Patch A — Clean dynamic shell

- Remove stale permanent mod menus and placeholder gameplay actions.
- Keep the proven Hub UI/theme/settings core.
- Replace the top bar with `Hub`, `Apps/Windows`, `Theme`, `Help`, and a visible minimize-group control.
- Preserve old adapter knowledge only as inactive migration/reference data, not visible active menus.
- Improve manifest scanning using BeamNG VFS `FS:findFiles`/`FS.findFiles` compatibility handling.
- Add an empty-state message when no compatible apps are detected.

### Patch B — Discovery and connection matrix

- Scan compatible `redfox_module.json` manifests across the mounted VFS.
- Scan regular action JSON files for exact GE Lua open/toggle commands where practical.
- Keep manual connection support for non-RedFox mods.
- Show control level and reason.
- Do not modify external mods.

### Patch C — Selected group minimize/restore

- Add `Minimize with Hub`, `Keep Open`, and `Restore with Hub` settings.
- Snapshot actual known state before group minimize.
- Hide only selected, currently open, controllable apps.
- Restore only apps successfully hidden by that group operation.
- Leave Career Dev or any pinned app untouched.
- One visible button and one key call the same function.

### Patch D — Target-mod adapters

After David supplies the exact installed ZIPs, inspect them read-only and add exact Hub-side control mappings where manifests/actions do not provide enough information.

Initial requested audit set:

- RedFox Spawner Control Panel v0.1.29;
- RedFox VTOL Drive Tuning v55;
- Dynamic Gravity v0.2;
- RedFox Node Grabber Unlocker;
- RedFox Career Dev Unlocker;
- RedFox Tow & Recovery Dispatch;
- Correspondent and other apps David selects.

---

## Required verification for every patch

Before editing:

- commit the exact baseline and scope;
- inspect the source ZIP;
- list protected files/functions.

After editing:

- generate a side-by-side colored diff;
- verify only intended code changed;
- update this status/roadmap in GitHub.

After packaging:

- reopen the ZIP;
- verify structure, extension names, window IDs, action IDs, settings paths, and protected functions;
- calculate SHA-256;
- commit artifact status as `RUNTIME UNTESTED`.

After David's test:

- commit pass/fail results and screenshots/log findings;
- identify last known good/first bad;
- do not create another patch until the runtime result is recorded.

---

## Current next action

No new ZIP should be created from assumptions. The next action is:

1. finish the source-level clean-core design from uploaded v0.5.11;
2. obtain/inspect the exact target mod ZIPs;
3. commit the discovery/control matrix;
4. then create Patch A with no hard-coded old mod menus.

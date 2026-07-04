# RedFox Module Manifest Contract

Every RedFox mod must include a manifest so the Garage Hub can discover it generically.

Required manifest path inside each mod ZIP:

```text
lua/ge/extensions/redfox/modules/<moduleId>/redfox_module.json
```

The Hub should scan for `redfox_module.json` files and read the fields. The Hub must not hardcode each mod by name.

Minimum fields:

```text
moduleId
visibleName
windowId
settingsFile
openFunction
closeFunction
toggleFunction
isWindowOpenFunction
minimizeFunction
restoreFunction
settingsFunction
gameUIFunction
getModuleStatus
```

Rules:

```text
🟢 Each mod owns its own gameplay.
🟢 Hub may show visibility/settings/status buttons from the manifest.
🔴 Hub must not move gameplay into itself.
🔴 Hub must not require custom code for every mod.
🔴 Hub must not bulk reconnect real modules without testing one at a time.
```

Discovery target example:

```text
lua/ge/extensions/redfox/modules/redfox_ui_load_tester/redfox_module.json
```

If a RedFox mod has no manifest, Hub discovery should mark it as:

```text
🔴 FAIL — missing RedFox module manifest
```

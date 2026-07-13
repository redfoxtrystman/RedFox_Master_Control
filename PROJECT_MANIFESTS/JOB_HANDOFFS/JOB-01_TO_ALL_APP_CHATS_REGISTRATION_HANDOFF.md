# JOB-01 Registration Handoff to All App Jobs

Use `JOB-01_APP_MANIFEST_CONTRACT.md` and register through
`extensions.redfoxPlatformCore.registerDestination()`.

Each app ZIP may contain only:

```text
scripts/<app>/modScript.lua
lua/ge/extensions/<appRegistration>.lua
ui/modModules/<app-owned-folder>/...
mod_info/<app>/info.json
app_manifest.json
```

Do not include:

- `ui/ui-vue/dist/index.js`;
- `lua/ge/extensions/ui/phone/layout.lua`;
- RLS phone/computer/Career files;
- `redfoxPlatformCore.lua`;
- `ui/modModules/redfoxPlatformCore/`;
- another app's UI or Lua;
- a duplicate FoxNet/IceFox platform ZIP;
- money, ownership, inventory, storage, garage, insurance, reward, mission, or
  purchase implementations.

Apps load on both phone and PC through one canonical ID and one entry path.
Use responsive CSS inside the app. Do not make separate phone and PC IDs.

If an app needs Career/RLS data or actions, wait for and use the versioned
JOB-02 bridge. UI-only/read-only registration can proceed earlier.

Every app handoff must report exact files, protected files, dependencies,
contract commit, static verification, runtime-unproven items, and clean removal
behavior.

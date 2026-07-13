# JOB-01 App Manifest Contract

Contract ID: `job01.platform.v1`  
Status: v0.1 frozen for app registration; BeamNG runtime untested

An app is a separate removable mod. It registers one or more destinations with
the loaded `redfoxPlatformCore` extension. It never edits the RLS phone bundle,
phone layout, PC route, platform host, or another app.

## Required destination fields

| Field | Type | Rule |
|---|---|---|
| `id` | string | Globally unique lowercase ID, for example `redfox.beambook` |
| `owner` | string | Assigned job, for example `JOB-05` |
| `name` | string | User-facing name |
| `entryPath` | string | Absolute `/ui/modModules/...` path owned by the app |

## Optional fields

| Field | Type | Default |
|---|---|---|
| `description` | string | empty |
| `category` | string | `Other` |
| `iconPath` | string | IceFox fallback icon |
| `order` | number | `9999` |
| `version` | string | `0.0.0` |
| `phone` | boolean | `true` |
| `pc` | boolean | `true` |
| `enabled` | boolean | `true` |
| `permissions` | string array | empty |
| `bridgeContract` | string | absent for UI-only apps; `job02.bridge.v1` once JOB-02 publishes it |

`entryPath` must start with `/ui/modModules/` and must not contain `..`.
Duplicate IDs are rejected when owners differ. An owner may update its own ID.

## Registration example

```lua
local M = {}

local destination = {
  id = "redfox.beambook",
  owner = "JOB-05",
  name = "BeamBook",
  description = "RedFox marketplace and community.",
  category = "Vehicle Markets",
  iconPath = "/ui/modModules/redfoxBeamBook/assets/icon.svg",
  entryPath = "/ui/modModules/redfoxBeamBook/index.html",
  version = "0.1.0",
  phone = true,
  pc = true,
  permissions = {},
}

local function register()
  if extensions.redfoxPlatformCore then
    extensions.redfoxPlatformCore.registerDestination(destination)
  end
end

function M.onExtensionLoaded() register() end
function M.onRedFoxPlatformReady(contract)
  if contract == "job01.platform.v1" then register() end
end

return M
```

The app's own `scripts/<app>/modScript.lua` loads only its registration
extension. Removing the app removes its UI and registration without changing
the platform.

## JSON documentation form

Apps may ship the same data as `app_manifest.json` for the future App Store.
In v0.1, the app registration extension remains the runtime authority.

```json
{
  "contract": "job01.platform.v1",
  "id": "redfox.beambook",
  "owner": "JOB-05",
  "name": "BeamBook",
  "category": "Vehicle Markets",
  "entryPath": "/ui/modModules/redfoxBeamBook/index.html",
  "iconPath": "/ui/modModules/redfoxBeamBook/assets/icon.svg",
  "phone": true,
  "pc": true,
  "version": "0.1.0",
  "permissions": []
}
```

## Rejected manifest behavior

The platform returns `{ok=false,error="..."}` and does not display the app.
Apps must not work around rejection by patching RLS or JOB-01 files.

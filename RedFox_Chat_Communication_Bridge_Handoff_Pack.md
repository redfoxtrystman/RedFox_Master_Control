# RedFox Chat Communication Bridge Handoff Pack

Use this file to make separate ChatGPT chats behave like separate workers under one RedFox build coordinator.

---

## How This Works

Separate chats do not automatically talk to each other.

The communication bridge is:

```text
David -> Master Document -> Assigned Chat -> Return Block -> Coordinator Chat -> Updated Master Document
```

Every chat must work from the same source of truth:

```text
RedFox_Master_Build_Control_Document.md
```

If memory, an old ZIP, or another chat disagrees with the master document, the master document wins unless David changes it.

---

## Paste This Into Every RedFox Chat

```text
You are working under the RedFox Master Build Control Document.

Before changing code, read the latest master document.

Only work on your assigned section.

Do not rename moduleId, windowId, extension names, manifest paths, or bridge function names unless the master document explicitly says to.

Do not move gameplay logic into the Hub.

Do not auto-open GM UI or WE UI at startup unless the master document says that module is allowed to do so.

Every output must include:
1. What changed
2. What was preserved
3. What file was created
4. What needs testing
5. Any bridge info the Hub needs
6. Any risk or unknown

If you package a ZIP:
1. Inspect the source ZIP/current baseline first.
2. Preserve working gameplay.
3. Package the edited ZIP.
4. Reopen the output ZIP.
5. Verify file structure, Lua extension names, module IDs, window IDs, manifest paths, bridge functions, settings paths, GM UI folders, input files if relevant, and required exported functions.
6. Include a verification report.
```

---

## Tell Each Chat Its Role

| Chat | Role |
|---|---|
| Coordinator Chat | Owns the master document, order, naming, bridge contract, module registry, status tracking, and handoff instructions. |
| Hub Chat | Owns Garage Hub 2.0, scanner, bridge manager, theme system, module rows, health checks, fallback entries, remember/restore, and load gate controls. |
| Career Bridge / Load Doctor Chat | Owns Career-safe loading, timing checks, staged unlocking, logging, duplicate detection, and failure reporting. |
| UI Load Tester Chat | Owns the tiny proof mod for GM/WE/Career timing tests. Do not skip this. |
| Individual Mod Chat | Owns exactly one real mod at a time. Must preserve gameplay and follow the bridge contract. |
| Testing Chat | Owns install order, duplicate cleanup, Freeroam tests, Career tests, BeamMP later, screenshots, logs, and pass/fail notes. |

---

## Mod Chat Return Block

```text
moduleId =
visibleName =
windowId =
settingsFile =
manifestPath =

openFunction =
closeFunction =
toggleFunction =
isWindowOpenFunction =
minimizeFunction =
restoreFunction =
settingsFunction =
gameUIFunction =

extensionName =
does it use GM UI app? yes/no
GM app folder/name =
does it use WE/native UI? yes/no
does it use PiP/render views? yes/no
does it need player vehicle before loading? yes/no
does it need level loaded before loading? yes/no
does it need Career-safe delayed load? yes/no

What changed =
What was preserved =
What file was created =
What needs testing =
Risks / unknowns =
```

---

## Testing Chat Result Block

```text
Test date =
BeamNG version =
Game mode = Freeroam / Career / BeamMP
Enabled ZIPs =
Disabled duplicate ZIPs =
Map/level =
Vehicle =
What was expected =
What happened =
UI visible? yes/no
GM UI visible? yes/no
WE/native UI visible? yes/no
Errors/log lines =
Screenshot included? yes/no
Pass/fail =
Next action requested =
```

---

## First Upload Order

Do not upload every mod at once.

Start with:

```text
1. 1-RedFox_GarageHub_v0_5_11_AllRedFoxBridges.zip
2. RedFox_GarageHub_Mod_Bridge_Requirements.md
3. RedFox_Hub_Bridge_Master_Handoff.md
```

Then upload only one or two test mods:

```text
1. Knight Rider
2. TrailSpotter Cam
```

Then evidence:

```text
1. beamng.log from Freeroam
2. beamng.log from Career fail
3. Screenshot of enabled mods folder
4. Screenshot of UI problem
```

---

## David's Quick Checklist

```text
1. Give each chat the master document.
2. Paste the Universal Paste Block.
3. Tell the chat its exact role.
4. Upload only the needed file or files.
5. Demand the return block.
6. Bring the return block back to Coordinator.
7. Coordinator updates the master document.
8. Only one Hub ZIP enabled.
9. Only one version of each test mod enabled.
10. Test Hub + one mod at a time.
```

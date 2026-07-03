# RedFox Worker Chat Quick Start

This is the simple instruction file for every RedFox worker chat.

Repo:

```text
https://github.com/redfoxtrystman/RedFox_Master_Control
```

Main control file:

```text
RedFox_Master_Build_Control_Document.md
```

Handoff file:

```text
RedFox_Chat_Communication_Bridge_Handoff_Pack.md
```

---

## 1. What Every Chat Must Do First

Before editing any mod, every RedFox chat must:

```text
1. Open/read RedFox_Master_Build_Control_Document.md.
2. Open/read RedFox_Chat_Communication_Bridge_Handoff_Pack.md.
3. Confirm its assigned role: Coordinator, Hub, Career Bridge, UI Load Tester, Testing, or Individual Mod Chat.
4. Work only on its assigned section.
5. Never rename moduleId, windowId, extension name, manifest path, settings path, or bridge function unless the master document explicitly approves it.
```

If another source disagrees with the master document, the master document wins unless David changes it.

---

## 2. Verification Before Editing

Before editing any uploaded mod ZIP or file, the worker chat must inspect the source first.

Required before-edit verification:

```text
1. List the ZIP/file name received.
2. Confirm it can be opened/read.
3. Inspect the folder structure.
4. Identify key Lua extension files.
5. Identify GM UI app folders, if any.
6. Identify WE/native ImGui files, if any.
7. Identify input/actionmap files, if any.
8. Identify module manifest path, if any.
9. Record moduleId, visibleName, windowId, settingsFile, extensionName, and bridge function names.
10. Search for known-danger calls such as editor.setEditorActive(true) when used for mod settings.
11. Search for duplicate or conflicting extension names.
12. State what gameplay/core code must be preserved.
```

The worker chat must not claim it edited, fixed, or verified anything it did not actually inspect.

---

## 3. Editing Rules

While editing:

```text
1. Preserve working gameplay unless David directly asks for gameplay changes.
2. Do not move gameplay into the Hub.
3. Do not rewrite large systems just to add a bridge.
4. Add or repair bridge/UI/load behavior in the smallest safe patch.
5. Keep old working UI available as fallback when possible.
6. Do not auto-open both GM UI and WE/native UI at startup.
7. Career-sensitive systems must use delayed/safe loading.
8. Render/PiP systems must wait for RenderViewManager.
9. Vehicle-dependent systems must wait for player vehicle.
10. Level-dependent systems must wait for level loaded.
```

If one stage fails, pause that stage only. Do not break the entire mod.

---

## 4. Verification After Editing, Before Giving David a ZIP

After editing and packaging, the worker chat must reopen the finished output and verify it.

Required after-edit verification:

```text
1. Reopen the output ZIP/file.
2. Confirm the expected files exist.
3. Confirm the old preserved gameplay files still exist.
4. Confirm Lua extension names are unchanged unless approved.
5. Confirm moduleId is correct.
6. Confirm visibleName is correct.
7. Confirm windowId is correct.
8. Confirm manifest path is correct.
9. Confirm settingsFile path is correct.
10. Confirm required bridge functions exist.
11. Confirm GM UI folders/apps exist if promised.
12. Confirm WE/native ImGui hooks exist if promised.
13. Confirm no unintended editor.setEditorActive(true) settings call was added.
14. Confirm no obvious duplicate/conflicting names were introduced.
15. Report anything that still needs in-game testing.
```

Static ZIP/code verification is not the same as BeamNG in-game testing. Say that clearly.

---

## 5. Required Output Report From Every Worker Chat

Every worker chat must return this block:

```text
What changed =
What was preserved =
File created =
Needs testing =
Bridge info Hub needs =
Risks / unknowns =
Static verification completed = yes/no
In-game verification completed = yes/no
```

If the chat cannot verify something, it must say so directly.

---

## 6. Required Mod Bridge Return Block

For a mod, return this exact block to the Coordinator Chat:

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
```

---

## 7. Required Test Result Block

Testing chats must return this exact block:

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

## 8. Simple Chat Handoff Test

A worker chat can prove it understands the communication flow by doing this:

```text
1. Read this file.
2. Read RedFox_Master_Build_Control_Document.md.
3. Say what role it was assigned.
4. Return a short test block using the Required Output Report.
5. Do not edit real mods during the test.
```

Example test output:

```text
What changed = No mod changed. This was a communication test only.
What was preserved = All repo files and mod files.
File created = None.
Needs testing = No BeamNG test needed.
Bridge info Hub needs = None.
Risks / unknowns = None.
Static verification completed = yes
In-game verification completed = no
```

---

## 9. Bottom Line

No guessing. No fake verification. No silent renames. No giant messy upload piles.

Read the master document, verify the source, make the smallest safe edit, verify the output, report clearly, then send results back to the Coordinator Chat.

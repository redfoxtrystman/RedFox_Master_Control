# RedFox Research Notes

Shared research notes for RedFox worker chats.

Rule: when any worker chat researches external/current BeamNG information that affects mod structure, UI loading, bridge safety, or testing, add a short note here or return a short block for Coordinator to post. Keep entries factual, short, and source-linked.

---

## 2026-07-03 — RF-UILOAD01 — UI Load Tester research

Sources checked:
- BeamNG official Extensions documentation: https://documentation.beamng.com/modding/programming/extensions/
- BeamNG official Creating an app documentation: https://documentation.beamng.com/modding/ui/app_creation/
- BeamNG official Programming overview: https://documentation.beamng.com/modding/programming/

Findings:
- BeamNG Lua extensions are Lua files that return a table.
- GE Lua extensions belong under `lua/ge/extensions/` inside a packed mod ZIP.
- Extensions should be explicitly loaded with `extensions.load("extension_name")`; avoid relying on `extensions.extensionName.foo()` auto-load behavior.
- Common extension hooks include `onExtensionLoaded`, `onUpdate`, and `onGuiUpdate`.
- BeamNG UI apps use AngularJS 1.5.8 directives in `beamng.apps`.
- A BeamNG app needs `app.js`, `app.json`, and `app.png`.
- `app.json` must match the directive name and DOM element.
- For the UI Load Tester, the correct design is a standalone proof mod with one GM app and one guarded native/WE-style Lua window. It must not edit or rebuild the real Hub.

RF-UILOAD01 design decision:
- Create a tiny standalone tester ZIP from scratch.
- Do not upload or patch the real Hub yet.
- Use delayed checks and guarded editor/native window calls.
- Do not call `editor.setEditorActive(true)` just to open settings/native UI.

# RedFox Node Grabber Unlocker v1.0.0

**Status:** 🟨 FINAL RUNTIME TEST REQUIRED  
**Prepared for:** RedFox Mod Works Patreon  
**Recorded:** 2026-07-25 23:50 America/Los_Angeles

## Release Identity

- Product name: `RedFox Node Grabber Unlocker`
- Release ZIP: `RedFox_Node_Grabber_Unlocker_v1.0.0.zip`
- Version: `1.0.0`
- Author/brand: `RedFox Mod Works`
- Intended game: BeamNG.drive
- Required gameplay mod: RLS Career Overhaul
- Intended Patreon access: Workshop Supporter ($5) and Test Driver ($10)

## Patreon Links

- Creator page: https://www.patreon.com/RedFoxModWorks
- Welcome post: https://www.patreon.com/RedFoxModWorks/posts/welcome-to-mod-164859800

## Package Verification

The supplied v1.0.0 ZIP was statically inspected before this status entry.

- File count: 7
- ZIP size: 13,243 bytes
- SHA-256: `624d1c76515c836a8b64c3f299f2b21fdc137c36155f16a469bf79a01bc77e76`

Expected package files were present:

```text
CHANGELOG.txt
README.txt
lua/ge/extensions/core/input/actions/redfox_grabber_ui_actions.json
lua/ge/extensions/overrides/career/career.lua
lua/ge/extensions/redfox/grabberUi.lua
mod_info.json
scripts/redfox_grabber_ui/modScript.lua
```

Static inspection confirmed:

- Version and product name are consistent across metadata and documentation.
- The dedicated RedFox native window and two input actions are present.
- The mod starts with the Node Grabber disabled.
- Enable, disable, direct toggle, and window-open functions are present.
- The package states that it does not alter money, progression, teleporting, vehicles, or save files.
- The README includes installation, removal, requirements, compatibility, support, and known-limitation sections.

## Compatibility Note

This release contains a runtime override at:

```text
lua/ge/extensions/overrides/career/career.lua
```

It therefore depends on the RLS Career version used to prepare and test that override. Future RLS changes to the same file may require a new RedFox release. Do not claim compatibility with untested RLS versions.

## Backup Handling

David retained the old test build in the BeamNG mods folder under a filename that no longer ends in `.zip`:

```text
RedFox_Grabber_UI_v0_1_0_TEST.zip before realese
```

BeamNG should ignore that backup. The Mod Manager must be checked to confirm that only `RedFox_Node_Grabber_Unlocker_v1.0.0.zip` loads.

## Final Runtime Test Gate

Do not upload or mark this release complete until David verifies all of the following:

1. BeamNG.drive loads without new Lua errors.
2. RLS Career starts normally.
3. The control window opens through the assigned action.
4. The direct toggle action works.
5. Enabling allows actual node grabbing.
6. Node rendering and mouse-wheel strength adjustment work.
7. Disabling restores normal RLS Career restrictions.
8. Reloading or re-entering Career does not leave the Node Grabber stuck on.
9. Removing or disabling the release restores the prior behavior.
10. Only the v1.0.0 ZIP appears as active; the renamed backup is ignored.

Record the exact BeamNG.drive version and RLS Career version after this test.

## Release Artwork

A 16:9 RedFox Mod Works promotional image was generated for this release with the title:

```text
RedFox Node Grabber Unlocker
Career Utility Mod • v1.0.0
```

The artwork includes the RedFox branding, a wireframe vehicle with highlighted nodes, and the feature callouts `Toggle On/Off`, `UI + Keybinds`, and `Career Mode Tool`.

## Next Action

David performs the final in-game test. After a clean pass, update this file to 🟩 RELEASED, record the tested BeamNG/RLS versions, record the Patreon release-post URL, and add the final result to `RedFox_Test_Results_Table.csv`.

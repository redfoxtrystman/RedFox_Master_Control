# RedFox Node Grabber Unlocker v1.0.0

**Status:** 🟨 FINAL RUNTIME TEST REQUIRED  
**Prepared for:** RedFox Mod Works Patreon  
**Recorded:** 2026-07-25 23:50 America/Los_Angeles  
**Corrected test package:** 2026-07-27

## Release Identity

- Product name: `RedFox Node Grabber Unlocker`
- Test ZIP: `RedFox_Node_Grabber_Unlocker_v1.0.0_FINAL_FIXED.zip`
- Public release filename after test: `RedFox_Node_Grabber_Unlocker_v1.0.0.zip`
- Version: `1.0.0`
- Author/brand: `RedFox Mod Works`
- Intended game: BeamNG.drive
- Required gameplay mod: RLS Career Overhaul
- Intended Patreon access: Workshop Supporter ($5) and Test Driver ($10)

## Patreon Links

- Creator page: https://www.patreon.com/RedFoxModWorks
- Welcome post: https://www.patreon.com/RedFoxModWorks/posts/welcome-to-mod-164859800

## Corrected Final Package Verification

The corrected test ZIP was rebuilt from `RedFox_Node_Grabber_Unlocker_v1.0.0_FINAL.zip`.

- File count: 11
- ZIP size: 17,863,926 bytes
- SHA-256: `bd61a547baa7da3c92a542ecfbf38df055d53ae455da47454756f36b74257df7`
- ZIP integrity test: passed
- JSON parse test: passed
- Changed file compared with the prior FINAL package: `README.txt` only
- Lua, JSON, images, metadata, and functional code were not changed

Package files:

```text
CHANGELOG.txt
README.txt
info/RedFox_Node_Grabber_Unlocker_v1.0.0.png
info/RedFox_Node_Grabber_Unlocker_v1.0.0_Screenshot_01.png
info/RedFox_Node_Grabber_Unlocker_v1.0.0_Screenshot_02.png
info/RedFox_Node_Grabber_Unlocker_v1.0.0_Screenshot_03.png
lua/ge/extensions/core/input/actions/redfox_grabber_ui_actions.json
lua/ge/extensions/overrides/career/career.lua
lua/ge/extensions/redfox/grabberUi.lua
mod_info.json
scripts/redfox_grabber_ui/modScript.lua
```

## README Correction

The installation instructions now use the exact control category and action names registered in the input-action JSON:

```text
Search category: RedFox Node Grabber Unlocker
Open action: Open RedFox Node Grabber Unlocker
Toggle action: Toggle RedFox Node Grabber
Window title: RedFox Node Grabber Unlocker
```

The obsolete `RedFox Grabber UI` wording was removed.

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

BeamNG should ignore that backup. The Mod Manager must be checked to confirm that only the corrected v1.0.0 test ZIP loads.

Do not leave both `RedFox_Node_Grabber_Unlocker_v1.0.0_FINAL.zip` and `RedFox_Node_Grabber_Unlocker_v1.0.0_FINAL_FIXED.zip` enabled together.

## Final Runtime Test Gate

Do not upload or mark this release complete until David verifies all of the following:

1. BeamNG.drive loads without new Lua errors.
2. RLS Career starts normally.
3. The control window opens through `Open RedFox Node Grabber Unlocker`.
4. `Toggle RedFox Node Grabber` works.
5. Enabling allows actual node grabbing.
6. Node rendering and mouse-wheel strength adjustment work.
7. Disabling restores normal RLS Career restrictions.
8. Reloading or re-entering Career does not leave the Node Grabber stuck on.
9. Removing or disabling the release restores the prior behavior.
10. Only the corrected v1.0.0 ZIP appears as active; backups and older candidates are ignored or disabled.

Record the exact BeamNG.drive version and RLS Career version after this test.

## Release Artwork

The final package includes the RedFox Mod Works promotional cover and three screenshots under `info/`.

## Next Action

David tests `RedFox_Node_Grabber_Unlocker_v1.0.0_FINAL_FIXED.zip`. After a clean pass, rename the Patreon download to `RedFox_Node_Grabber_Unlocker_v1.0.0.zip`, update this file to 🟩 RELEASED, record the tested BeamNG/RLS versions, record the Patreon release-post URL, and add the final result to `RedFox_Test_Results_Table.csv`.

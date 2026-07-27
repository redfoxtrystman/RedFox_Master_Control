# RedFox Node Grabber Unlocker v1.0.0

**Status:** 🟨 FINAL RUNTIME TEST REQUIRED  
**Prepared for:** RedFox Mod Works Patreon  
**Updated:** 2026-07-26 America/Los_Angeles

## Release Identity

- Product name: `RedFox Node Grabber Unlocker`
- Current final-test ZIP: `RedFox_Node_Grabber_Unlocker_v1.0.0_FINAL.zip`
- Intended public filename after testing: `RedFox_Node_Grabber_Unlocker_v1.0.0.zip`
- Version: `1.0.0`
- Author/brand: `RedFox Mod Works`
- Intended game: BeamNG.drive
- Required gameplay mod: RLS Career Overhaul
- Intended Patreon access: Workshop Supporter ($5) and Test Driver ($10)

## Patreon Links

- Creator page: https://www.patreon.com/RedFoxModWorks
- Welcome post: https://www.patreon.com/RedFoxModWorks/posts/welcome-to-mod-164859800

## Final Package Verification

The supplied final-test ZIP was statically inspected.

- File count: 11
- ZIP size: 17,863,926 bytes
- SHA-256: `9354ffefb9ef853ba791a113e5924506c8620e1ff6f9e655e1cdfda91745b9e9`

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

Static verification confirmed:

- All JSON files parse successfully.
- The functional Lua, action JSON, metadata, and changelog are unchanged from the prior v1.0.0 release candidate.
- The final package adds one promotional image and three screenshots under `info/`.
- The README was rewritten for public release.
- The dedicated RedFox native window and two input actions remain present.
- The mod starts with the Node Grabber disabled.
- Enable, disable, direct toggle, and window-open functions remain present.
- No `ChatGPT`, `OpenAI`, assistant, generated-code, or prompt wording was found in the package.

## Documentation Check Before Upload

The README currently tells users to search Controls for `RedFox Grabber UI` and bind `Open RedFox Grabber UI`.

The actual registered control category and action are:

```text
RedFox Node Grabber Unlocker
Open RedFox Node Grabber Unlocker
```

Correct the README wording before the public upload, or users may search for the wrong control name.

The README already names the intended public ZIP as:

```text
RedFox_Node_Grabber_Unlocker_v1.0.0.zip
```

After the final test, remove `_FINAL` from the public download filename so the package matches its own instructions.

## Compatibility Note

This release contains a runtime override at:

```text
lua/ge/extensions/overrides/career/career.lua
```

It therefore depends on the exact RLS Career version used to prepare and test that override. Future RLS changes to the same file may require a new RedFox release. Do not claim compatibility with untested RLS versions.

## Backup Handling

David retained the old test build in the BeamNG mods folder under a filename that no longer ends in `.zip`:

```text
RedFox_Grabber_UI_v0_1_0_TEST.zip before realese
```

BeamNG should ignore that backup. The Mod Manager must be checked to confirm that only the final v1.0.0 ZIP loads.

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
10. Only the final v1.0.0 ZIP appears as active; the renamed backup is ignored.
11. The exact BeamNG.drive version is recorded.
12. The exact RLS Career version is recorded.

## Release Artwork

The ZIP includes:

- One 1672 × 941 promotional image
- One 2048 × 1506 screenshot
- One 1617 × 1640 screenshot
- One 2048 × 1151 screenshot

## Next Action

Correct the README control-name mismatch, run the final in-game test, rename the public ZIP without `_FINAL`, and upload it to both paid Patreon tiers. After publication, update this file to 🟩 RELEASED and record the Patreon release-post URL.

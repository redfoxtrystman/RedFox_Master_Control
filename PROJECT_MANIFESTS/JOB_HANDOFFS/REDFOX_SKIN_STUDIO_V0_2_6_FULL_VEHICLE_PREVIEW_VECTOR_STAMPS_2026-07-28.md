# RedFox Skin Studio v0.2.6 — Full Vehicle Preview and Vector Stamp Library

**Date:** 2026-07-28  
**Owner:** David / Captain  
**Status:** **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED**  
**Artifact:** `RedFox_Skin_Studio_v0_2_6_BUILT_RUNTIME_UNTESTED.zip`  
**SHA-256:** `4c18725bdee6283977a78187036a6214ad11539383685e61f5b93b3e6d97b08f`

## Owner test result that required this build

David confirmed that the v0.2.5 2D corrections largely worked, but the live 3D preview displayed a small flat textured plane instead of the helicopter model. David also requested a substantial built-in collection of vector-style stamps comparable in workflow to racing-livery editors, including flames, lightning bolts and stars.

The v0.2.5 preview failure was real. The application treated one selected DAE file as though it were necessarily the complete vehicle. BeamNG vehicles may use multiple DAE files, and a mod archive can contain flat decal/image planes, tiny accessories, helper geometry and separate body files. A valid texture could therefore be rendered on the wrong mesh.

## Implemented in v0.2.6

### Automatic full-vehicle 3D preview

- Added `AUTO — Full vehicle from all relevant DAE files (recommended)` as the default model choice.
- The preview scans every DAE candidate instead of blindly using the first file.
- Scores DAE geometry using:
  - selected material matches;
  - triangle count;
  - three-dimensional versus flat geometry;
  - body/cab/fuselage/chassis/frame naming;
  - exclusion of obvious wheel, suspension, engine, light and interior-only files.
- Combines relevant DAE files for BeamNG multi-DAE vehicles.
- Automatically falls back from a manually selected flat plane or tiny accessory to AUTO mode.
- Caps/decimates preview geometry to 220,000 triangles for complex mod vehicles.
- Preserves OBJ group/material names.
- Applies the current skin only to an exact normalized paint-material match.
- Displays non-painted context meshes in neutral gray.
- If material names do not survive a mod export, applies the skin to the largest non-flat shell instead of a flat plane.
- Blender live preview now receives the selected material list and follows the same neutral-context/fallback concept.

### Original vector stamp library

Added 54 original RedFox vector-style stamps in nine categories:

- Stars
- Lightning
- Flames
- Stripes
- Tears & Claws
- Racing
- Tribal
- Splatters
- Nature

Stamp behavior:

- click to add;
- drag to place;
- independent layer;
- recolor;
- horizontal/vertical stretch;
- rotate;
- flip;
- mirror;
- duplicate;
- lock;
- opacity and blend mode;
- project save/reopen;
- Design Vault transfer between vehicles.

These are original RedFox path assets. They are not copied from Forza or another game's artwork.

## Research/format basis

BeamNG officially supports multiple DAE files for one vehicle, uses DAE geometry for vehicles, and uses UV1/body-wrap UVs for skins. The corrective preview architecture now reflects those facts instead of assuming a single first DAE is the whole vehicle.

Forza's official painting documentation groups vinyl shapes into categories such as primitives, gradients, stripes, tears, racing icons, flames, paint splats, tribal, nature, letters and community groups. RedFox uses that category/workflow concept while supplying its own original stamp paths.

## Automated/static tests passed

- Python compile-all.
- JavaScript syntax check for `script.js`.
- JavaScript syntax check for `stamp_library.js`.
- Backend self-test.
- 54 unique vector stamp IDs.
- Nine stamp categories.
- Stock Wigeon scan and AUTO preview build.
- Wigeon AUTO preview: 82,265 triangles with multiple material groups.
- Modded Jerrdan scan and multi-DAE AUTO preview build.
- Jerrdan preview obeyed the 220,000-triangle limit.
- AUTO model selector is the desktop default.
- Final ZIP archive integrity test.

## Not proven

- Windows QWebEngine live rendering of the new full-vehicle OBJ.
- Exact Bell 407 body/material match, because David's Bell 407 source mod ZIP was not supplied in the current chat.
- Windows stamp drag/drop behavior.
- Exact active BeamNG part configuration; external previews may show optional source meshes.
- BeamNG in-game loading/rendering of a mod built by this exact version.

Do not relabel this release as working until David tests the exact archive on Windows and in BeamNG.

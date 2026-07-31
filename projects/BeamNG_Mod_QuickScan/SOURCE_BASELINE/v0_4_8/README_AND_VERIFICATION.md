# QuickScan v0.4.8 source baseline and verification

## Baseline custody

- Edited from exact verified v0.4.7.3 Strict Manifest-Only Rename.
- v0.4.7.3 source law preserved: filename-only renames never create a second ZIP.
- v0.4.8 source SHA-256: `4aa75d06eb9928659f29ee05d2bb8af8a89c6aac49584da806a25c8e52494cc0`
- v0.4.8 package SHA-256: `6382a98c776f0d2c664b9c86a946405cb9100886ada6e3600d6de670a0c2cd82`

## New protected behavior

1. Selected-folder normal views are mandatory by default.
2. Previous Scans must list retained runs and their saved ZIP/finding snapshots.
3. Master Catalog is the explicit cross-folder view.
4. Catalog/Career/Tow lists must not insert fake separator rows.
5. Catalog checks use four tightly grouped true on/off image lights.
6. Vehicle Catalog displays model/source-ZIP cards and exact configuration cards.
7. Career and Tow rows open compact guided wizards on double-click.
8. Hover help explains meaning, valid inputs, blank behavior, and safe autofill.
9. `?` buttons open official BeamNG documentation where available.
10. Settings may hide screens/columns without deleting data.

## Test results

```text
PASS compile
PASS complete inherited self-test chain
PASS selected-folder and explicit combined-folder GUI scope
PASS two retained scan folders and auto-populated history details
PASS stoplight image and no separator-row regression
PASS Career wizard construction
PASS Tow wizard construction
PASS visual vehicle gallery and exact configuration gallery
PASS main/config preview matching
PASS Settings dialog and hidden-tab restoration
PASS real stpmustang.zip metadata recovery
PASS real WSCX_ChevBel-Air.zip metadata recovery
PASS six useful previews from the two real metadata-test ZIPs
PASS final ZIP CRC
PASS extracted-package compile/self-test/GUI
PASS no uploaded mod ZIPs bundled
```

## Remaining owner tests

- Physical Windows DPI/scaling at the owner's selected UI sizes.
- Rendering speed and memory with the owner's full library.
- JPG/JPEG gallery fallback through Windows PowerShell/.NET when Pillow is absent.
- Real D-drive folder switching and historical snapshots.
- Career patch behavior in BeamNG.
- JOB-09 reading approved Tow Catalog entries.

## Official documentation linked by the wizards

- Vehicle configurations/info files: `https://documentation.beamng.com/modding/vehicle/tutorials/configs/`
- Configuration example template: `https://documentation.beamng.com/modding/vehicle/tutorials/configs/info_template.json`
- Vehicle groups: `https://documentation.beamng.com/modding/file_formats/vehicle_groups/`
- Vehicle Groups Manager: `https://documentation.beamng.com/world_editor/windows/vehicle_groups_editor/`
- User folder: `https://documentation.beamng.com/support/userfolder/`

# RedFox Skin Studio v0.2.9 — Layered Vehicle Skin Archive Requirement

**Date:** 2026-07-28  
**Owner:** David / Captain  
**Status:** REQUIREMENT RECORDED — NOT YET BUILT

## Owner request

Every skin created for a vehicle must be saved under that vehicle's RedFox workspace folder so it is backed up, easy to find, and can be reopened for editing later.

A flattened PNG or DDS alone is not sufficient. The editable project must preserve all layers and object data.

## Required storage behavior

The application must store vehicle-specific editable skins in the shared RedFox workspace, not inside BeamNG's stock game archives or source mod ZIPs.

Target structure:

```text
_RedFox_Skin_Studio_Shared/
  Workspace/
    Vehicles/
      <vehicle_id>/
        Vehicle_Profile/
        Templates/
        Existing_Skins/
        Editable_Skins/
          <skin_id>/
            skin.rfskin
            skin_manifest.json
            preview.png
            source_assets/
            revisions/
            exports/
```

## Layer preservation

`skin.rfskin` must preserve, at minimum:

- raster paint layers;
- imported image/logo layers;
- vector stamp and shape layers;
- text layers and font settings;
- layer visibility;
- layer lock state;
- layer order;
- opacity and blend mode;
- position, scale, stretch, rotation and skew;
- independent and linked mirror information;
- masks/background-removal settings;
- hue, saturation, brightness and tint settings;
- UV/template guide references with `excludeFromExport` retained;
- three-color RGB mask mode information;
- external-editor result layers;
- source vehicle, material target, UV candidate and project identifiers.

Imported assets must be copied or embedded into the skin's `source_assets` folder so projects do not break when the original logo or image is moved or deleted.

## Save behavior

The next patch must provide:

- **Save Layered Skin** — updates the current editable skin;
- **Save As New Skin** — creates another skin under the same vehicle;
- **Save New Revision** — stores a timestamped layered revision without replacing the current version;
- **Open Vehicle Skin Library** — shows thumbnail cards for every saved editable skin for the selected vehicle;
- **Duplicate to Another Vehicle** — copies the layered design while preserving independently editable objects;
- automatic recovery/autosave copies;
- a warning before closing with unsaved changes.

Saving/exporting a BeamNG mod must not remove or flatten the editable project. The final PNG/DDS and mod ZIP are outputs stored under `exports`, while the layered `.rfskin` remains the master file.

## Existing and external edits

- Existing BeamNG skins opened for editing should be cloned into `Editable_Skins` before changes are saved.
- External-editor PNG results may remain flattened layers, but the original RedFox layers beneath them must be preserved.
- Returning to editable layers must not discard the external edit unless the owner explicitly deletes it.

## Safety and backup

- Never write editable project data directly into BeamNG stock ZIPs.
- Never overwrite a third-party source mod without the explicit ZIP-patch workflow and backups.
- Each revision must include metadata and file hashes where practical.
- Project and vehicle folders remain in the shared RedFox workspace so every test version sees the same layered skins.

## Version rule

The implementation release for this requirement must increment the synchronized application version to **0.2.9** or later across the app title, visible header, build metadata, reports, documentation and GitHub audit.

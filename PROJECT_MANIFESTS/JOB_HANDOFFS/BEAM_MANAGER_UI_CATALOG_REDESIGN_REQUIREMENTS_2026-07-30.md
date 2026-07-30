# Beam Manager UI / Catalog Redesign Requirements — 2026-07-30

## Source intake status

Uploaded package reviewed: `Beam.Manager.v1.0.0.AIO.zip`.

The package contains only a compiled self-contained Windows build:

- `Beam Manager.exe`
- runtime DLLs

No `.sln`, `.csproj`, `.xaml`, `.cs`, source assets, or editable project files were included. The executable identifies itself as version `1.0.0.0` and contains a build path pointing to:

`C:\Users\Devtop1\Documents\GitHub\Beam-Manager\Beam Manager`

The UI redesign must not be claimed complete until the actual source project is provided and rebuilt.

## Required redesign

### Main catalog experience

- Replace oversized spreadsheet-style layouts with a compact, searchable, sortable catalog similar to a document/database view.
- Sort and filter by scanned folder, mod ZIP, manufacturer, model, configuration, type, career status, and review state.
- Preserve folder-by-folder scan history.
- Eliminate large unused vertical and horizontal gaps.
- Do not truncate important text. Wrap to two lines where needed.
- Columns must be resizable and have sensible minimum widths.
- Font and controls must scale with Windows DPI and available panel width.
- Add compact/list/gallery view switching.

### Vehicle gallery behavior

- Scan ZIPs and show one main card per detected vehicle/model using the best available preview image.
- Left-click the main vehicle image/card to open all configurations for that vehicle.
- Right-click the vehicle card to open career/configuration editing actions.
- Configuration cards must show preview image, configuration name, source ZIP, career readiness, type/classification, and warnings.
- Manual classification must work at exact configuration level, not only vehicle/model level.
- Manual review always overrides automatic suggestions.

### Classification controls

The user must be able to classify an exact configuration as, at minimum:

- Standard vehicle
- Police / emergency vehicle
- Tow / recovery vehicle
- Trailer
- Equipment / machinery
- Prop / object
- Traffic-only
- Shop-only
- Do not use
- Unknown / needs review

The tool must not treat equipment, trailers, or props as normal trucks merely because they are under a vehicle folder.

### Career editing workflow

- One guided wizard/job at a time.
- Provide a vehicle wizard and a configuration wizard.
- Explain each field in plain language before or while editing.
- Support Save & Next, Previous, Skip, Mark Unreviewed, Undo, Apply to exact config, and Apply to all configs in model.
- Preserve source ZIPs; write patches/copies with backups and change reports.
- Career status colors:
  - Green: ready / approved
  - Yellow: may work / missing information
  - Red: not spawn-ready or confirmed problem
  - Blue: manually reviewed
  - Gray: unknown / incomplete

### Help system

- Keep visible `?` buttons.
- Hovering a `?` must show a real tooltip/popover with:
  - what the field means;
  - what file/BeamNG system it affects;
  - valid example values;
  - what happens if left blank;
  - whether it is safe to auto-fill.
- Clicking the `?` must open a larger help panel.
- Where an official BeamNG page exists, include an `Open BeamNG Documentation` link.
- Relevant official areas include vehicle configurations/info files, vehicle groups, file formats, user folder, and vehicle modding.

### Layout rules

- Remove the current oversized blank areas seen in Career Data, Previous Scans, and catalog tables.
- Use auto-height wrapped rows instead of forcing long single-line text.
- Use compact toolbars with grouped actions instead of one long horizontal row.
- Move less-used actions into context menus or an overflow menu.
- Keep primary actions visible.
- All tabs, dialogs, popups, and wizards must use the same RedFox dark-purple theme and consistent spacing.
- Do not reduce font size until text becomes unreadable; wrap before shrinking.

### Search and sorting

- Global search across vehicle name, configuration, ZIP name, manufacturer, model, folder, notes, and classification.
- Folder filter with multi-select.
- Clickable column sorting.
- Saved filters/views.
- Search result count and active-filter chips.

### Undo / history

- Undo the latest manual career/classification edit.
- Keep a per-item change history.
- Allow restoring a prior scan/review state without losing newer scan files.

## Required next input

Provide the actual `Beam-Manager` source project folder or repository containing:

- `.sln`
- `.csproj`
- `.xaml`
- `.cs`
- icons/assets
- current build instructions

The compiled AIO package alone is not a safe editable source base.

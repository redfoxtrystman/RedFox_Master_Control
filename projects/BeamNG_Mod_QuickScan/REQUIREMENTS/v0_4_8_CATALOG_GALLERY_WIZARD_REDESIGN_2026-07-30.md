# BeamNG Mod QuickScan v0.4.8 — Catalog Gallery, Readable Layout, and Guided Wizard Requirements

**Date:** 2026-07-30 PDT
**Owner:** David / Captain
**QuickScan baseline:** v0.4.7 Whole-Window Scroll + Saved Scan Snapshots + Master Catalog
**Status:** REQUIREMENTS ONLY — NOT YET CLAIMED BUILT

## Ownership correction

Commit `080752dc6e15cc30581573db6ffac346fb9356dc` recorded useful UI/catalog requirements under Beam Manager after a request was accidentally sent to the wrong chat. The compiled Beam Manager source limitation does not block QuickScan. QuickScan owns this redesign and has an exact editable v0.4.7 source baseline.

## Controlling owner requirements

- Replace spreadsheet-heavy catalog pages with a compact searchable document/database experience.
- Search and sort by scanned folder, ZIP, manufacturer, vehicle, model, configuration, type, Career status, review state, notes, and classification.
- Preserve separate folder-by-folder scans while maintaining one Master Catalog and cross-folder conflict view.
- Remove large unused gaps while preventing text and controls from being cut off.
- Wrap text before shrinking it; allow multi-line values and auto-height content.
- Scale all fonts, controls, dialogs, tooltips, wizards, cards, and tabs to Windows DPI and available space.
- Use responsive layouts that reflow controls instead of long clipped button rows.
- Keep one useful whole-window scroll path; avoid tiny nested windows that show only one line.

## Vehicle catalog behavior

- Show one main card per detected vehicle/model using the best available extracted main image.
- Support Gallery, Compact List, and Detailed Table views.
- Left-click a main vehicle card/image to open all exact configurations.
- Right-click a card for actions: edit Career data, classify vehicle/config, police/emergency, tow/recovery, trailer, equipment/machinery, prop/object, traffic-only, shop-only, never use, open source ZIP, and view internal files.
- Exact configuration classification remains authoritative; do not classify an entire model based on one police, race, equipment, prop, or trailer configuration.
- Configuration cards show image, display name, exact model/config, source ZIP, source folder, version, Career readiness, Tow/JOB-09 classification, warnings, and review history.

## Career and classification wizard

Replace the giant single form with a guided sequence:

1. Identity and exact configuration.
2. Physical/service/classification type.
3. Name, description, year, and value.
4. Drivetrain, fuel, propulsion, and transmission.
5. Traffic, dealership/filter planning, and category.
6. JOB-09 Tow permissions, lien/property type, and spawn rules.
7. Review warnings and save.

Required controls:

- Save & Next
- Previous
- Skip
- Mark Unreviewed
- Undo
- Apply only to exact configuration
- Copy to selected configurations
- Apply to all configurations in model with reviewed-exception warning

## Help system

- Keep visible `?` marks.
- Hovering a `?` displays a plain-language tooltip/popover explaining:
  - what the field means;
  - what BeamNG file/system uses it;
  - valid example values;
  - what happens when blank;
  - whether auto-fill is safe or still needs approval.
- Clicking `?` opens a larger help panel.
- Where official BeamNG documentation exists, include an `Open BeamNG Documentation` action.

## Layout laws

- No fixed giant blank sections under short lists.
- No text clipped because columns are too narrow.
- Long table values may wrap or open an inline/detail drawer.
- Columns are sortable and resizable with sensible minimum widths.
- Search/filter controls remain visible.
- Rare actions move to right-click or overflow menus.
- Primary actions remain visible.
- Cards and controls reflow based on width.
- Status dots receive labels/tooltips and must not be unexplained decorations.

## Preserved v0.4.7 behavior

Do not remove or weaken:

- direct ZIP/internal-code scanning;
- exact/repacked/functional duplicate detection;
- version-only rename law;
- duplicate review, quarantine, backup, and Undo;
- vehicle/map/UI preview extraction;
- Career patch builder;
- Tow Catalog exact-configuration schema;
- Previous Scan snapshots;
- Master Catalog and cross-folder conflicts;
- pause/resume/checkpoints;
- DRM indicators;
- D-drive/user-selected data storage.

## Revised version boundary

- v0.4.8 — catalog/gallery/readability/wizard/help redesign.
- v0.4.9 — Tow online enrichment and representative JOB-09 proof set.
- v0.5.0 — incoming-folder automatic sorter.
- v0.6.0 — installed/storage Mod Manager and video mod packs.

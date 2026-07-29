# RedFox Skin Studio v0.2.8 — RedFox Theme and Workflow Update

**Date:** 2026-07-28  
**Owner:** David / Captain  
**Status:** **BUILT — WINDOWS / BEAMNG RUNTIME UNTESTED**  
**Artifact:** `RedFox_Skin_Studio_v0_2_8_REDFOX_THEME_WORKFLOW_UPDATE_BUILT_RUNTIME_UNTESTED.zip`  
**SHA-256:** `78d39570300b42e73ca153076a621b81334483fcdeadd6d5bfa41da01e261f97`

## Owner request

David reported that RedFox Skin Studio still looked nearly identical to the original BeamNG Livery Maker reference application. He required the next release to have a clear RedFox identity, with dark purple and seafoam green as the primary theme, additional selectable themes, and a more useful project-first workflow. David supplied several other BeamNG skin and UV applications for source inspection so useful ideas could be reimplemented in RedFox Skin Studio without simply copying another creator's program.

## Supplied packages inspected

The uploaded archives were unpacked and reviewed as source/data only. Unknown executables were not launched.

### BeamNG Livery Maker

Useful concepts found:

- object-based vector paths and shapes;
- curved text;
- gradients and blend modes;
- layer locking;
- rasterize-to-paint behavior;
- DDS export workflow.

No reusable software license was found in the supplied package. Its code was treated as reference-only and was not copied.

### BeamSkin Studio beta packages

Useful concepts found:

- a project-oriented browser;
- setup/path configuration;
- vehicle/project preview cards;
- theme management;
- navigation and localization structure.

No reusable software license was found in the supplied packages. Their code was treated as reference-only and was not copied.

### UV Exporter 1.1.0

Useful concepts found:

- material/group checklist;
- UV preview before export;
- output resolution and line-style controls;
- checkerboard/transparent backgrounds;
- remembered material selections;
- support for multiple model formats.

The supplied UV Exporter 1.1.0 source is AGPLv3. No source was copied into RedFox Skin Studio. The relevant interaction ideas were reimplemented from scratch using RedFox's existing DAE parser. The separately supplied `UV.Exporter.7z` could not be unpacked in the build environment because no 7z-compatible runtime was available, but the separately supplied ZIP version was successfully inspected.

## Implemented in v0.2.8

### Distinct RedFox visual identity

- Replaced the inherited orange/black appearance with a dark-purple, seafoam-green, charcoal and silver RedFox theme.
- Added RedFox branding to the native desktop shell and embedded editor.
- Added a RedFox fox-mark start center rather than dropping directly into the inherited blank canvas.
- Redesigned the top bar, side panels, cards, buttons, context indicators, scrollbars and editor canvas styling.
- Removed the visible resemblance to the reference application's orange toolbar as the default presentation.

### Selectable themes

Added four persistent themes:

1. **RedFox Midnight** — dark purple + seafoam, the default.
2. **Seafoam Workshop** — lighter seafoam-centered workspace.
3. **Purple Blackout** — darker purple/black presentation.
4. **High Contrast** — clearer accessibility-oriented contrast.

The selected theme is stored in the shared RedFox workspace and reused by later versions.

### Project-first workflow

- Added a **Project Hub** with project cards, project names, skin counts, vehicle counts and thumbnails.
- Added project/vehicle context chips in the editor header so the owner can see what is currently being edited.
- Added a RedFox start center with direct actions for:
  - Project Hub;
  - Vehicle Gallery;
  - Scan Vehicle ZIP;
  - UV Workshop.
- Added a setting to show or hide the start center.

### UV Workshop

Added a new original UV export workflow using RedFox's existing DAE parser:

- choose a DAE from the current vehicle;
- view material groups and triangle counts;
- select all, clear all or choose likely body groups;
- remember material selections in the shared workspace;
- preview before export;
- choose 1K, 2K, 4K, 8K or 16K output;
- choose line width and line color;
- choose transparent, checkerboard, seafoam or dark background;
- optionally color material groups separately;
- export the guide;
- open the result in the editor as a reference-only layer that is not included in the finished skin.

### Navigation and workspace improvements

- Reorganized the native sidebar into RedFox-owned sections:
  - Current Project;
  - Vehicle Library;
  - Quick Design;
  - External Editing;
  - Asset Album;
  - Design Vault;
  - Build.
- Added toolbar actions for Project Hub, Guided Wizard, Vehicle Gallery, UV Workshop, Settings, updates and the shared workspace.
- Existing editing, external-editor round trip, stamps, project storage, ZIP building, backup handling and skin export features were preserved.

### Version synchronization

Version `0.2.8` is synchronized in:

- central runtime version;
- native window title;
- embedded editor header;
- guide;
- README;
- changelog;
- build information;
- launch installation record;
- generated mod reports/manifests through the existing central version reference.

## Automated/static tests passed

- Python compile-all.
- Embedded editor JavaScript syntax validation with Node.
- Stamp-library JavaScript syntax validation.
- Backend self-test, including generated BeamNG mod validation.
- HTML ID uniqueness check: 131 IDs, no duplicates.
- Required RedFox theme/start-center/Project Hub/UV Workshop markup checks.
- Wigeon DAE UV parsing: 31 material groups found.
- New UV Workshop renderer test: selected groups rendered to a valid 1,024-pixel checker-background PNG.
- Final ZIP integrity test: 325 entries, no corrupt member detected.
- Confirmed stale test-workspace bootstrap data was removed from the downloadable package.

## Not proven

- Windows `run.bat` startup for this exact package.
- Live PySide6/QWebEngine interaction and native theme rendering on David's computer.
- Project Hub and UV Workshop interaction under Windows.
- Theme persistence through David's existing shared workspace.
- BeamNG in-game rendering of a mod generated by this exact build.
- Automatic usefulness of every material group for every unusual third-party vehicle.

No one may label this release working or complete until David tests this exact archive on Windows and in BeamNG.

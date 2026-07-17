# RedFox Mod Manager Suite — UI, Selection State, Image, and Career Builder Addendum

**Date:** 2026-07-16  
**Project:** `32-RedFox_Mod_Manager_Suite_`  
**Reported against:** current RedFox Mod Manager UI shown in David's screenshots  
**Build action:** Documentation only. Do not build until baseline audit and scope freeze are complete.

---

## 1. Immediate defects reported by David

### 1.1 Picture Home layout is unusable

Current behavior:
- Tiles appear in a narrow vertical column instead of a responsive grid.
- A later image can expand to enormous width/height and consume the page.
- Cards and images do not consistently fit their containers.

Required behavior:
- Responsive tiled grid like BeamNG's vehicle selector / RedFox New Tab.
- Tile count per row adapts to available width.
- Tile image uses aspect-fit inside a fixed card region.
- No image may enlarge the entire page.
- Text wraps or truncates safely and exposes full text on hover/click.
- The whole page scrolls normally; avoid nested tiny scroll panes wherever possible.

### 1.2 Missing-source entries pollute the working list

Current behavior:
- Entries whose source ZIP cannot be found still appear as normal selectable items.
- Clicking them causes a ZIP-not-found dialog.

Required behavior:
- Missing-source items are hidden by default from active work views.
- Add explicit filter: `Show Missing Source`.
- When shown, sort them after found/active entries.
- Missing-source cards must be visually distinct and must not pretend their ZIP is available.
- Startup/refresh should compare the catalog to actual configured source folders and ask whether missing active mods should be marked inactive.
- Do not delete their history automatically.

### 1.3 Default working filter

David's clarified working view:
- Show all normal discovered items except hidden items.
- For the Career Compatibility Wizard, default to entries that are not career-ready or require review.
- Career-ready items remain accessible by filter, but should not dominate the work queue.
- Missing-source items remain hidden unless explicitly requested.

### 1.4 Image candidate list must preview the selected image

Current behavior:
- Clicking image candidate text does not reliably display the image.
- The text/path list is too narrow to read.
- Some images report unsupported format even though BeamNG uses common image formats.

Required behavior:
- Single-clicking an image candidate immediately previews it.
- Double-click or context menu may open it externally.
- Candidate list supports readable full paths via horizontal scroll, wrapping option, tooltip, and details panel.
- Support at minimum PNG, JPG/JPEG, WEBP, BMP, GIF first frame, DDS where decoder support exists, and any other format found in BeamNG/mod files through an extensible image-decoder adapter.
- If a format cannot be decoded, show the exact format and offer `Open externally`; do not show a vague blank preview.
- Preview must aspect-fit and resize with its container.

### 1.5 Global responsive layout law

All pages, tabs, panels, dialogs, cards, text blocks, images, and toolbars must obey:
- Resize with the application window.
- Text wraps to available width.
- Font size remains readable and may scale within safe configured limits.
- Images aspect-fit their panel and never overflow.
- Buttons wrap into additional rows or move into overflow menus.
- Long pages use full-page scrolling.
- Nested scroll areas are used only for true lists or code/file viewers.
- Save and restore safe window size/position.
- Never shrink/minimize the application while background work runs.
- Long tasks show status, current item, progress, elapsed time, and cancel/pause when feasible.

### 1.6 Career Shop Builder launch error

Observed error:

```text
name 'subprocess' is not defined
```

Required repair:
- Audit launcher code before editing.
- Add/import `subprocess` only if that is the correct existing launch mechanism.
- Confirm the target script/path exists.
- Confirm launch errors are caught and explained in plain language.
- Do not claim fixed until David tests the launcher.

### 1.7 Selected mod must persist across modules

Current problem:
- Switching from Catalog to Textures/ZIP Tools or another module requires finding the same ZIP again.

Required architecture:
- One shared `CurrentSelection` state for the entire application.
- It must contain catalog entry ID, source ZIP path, internal vehicle/config ID, selected preview, source status, and pending edits.
- Every relevant module opens on the same selected entry.
- Switching tabs must not rescan the ZIP unless the user requests refresh or uncached data is required.
- If the source disappears, preserve the selected catalog record but disable source-dependent actions.

---

## 2. Status field correction

The current dropdown mixes unrelated concepts:
- Normal
- Verified
- Unknown
- No Image
- Non-Mod
- Working Version
- Missing Source
- Bad/Broken

This is not a BeamNG Career requirement and is confusing.

Replace the single ambiguous `Status` field with separate fields:

### 2.1 Source state
- Available
- Missing
- Moved/Renamed
- Archived
- Installed
- Not Installed

### 2.2 Scan state
- Not Scanned
- Scanned
- Changed Since Scan
- Scan Failed
- Needs Review

### 2.3 Mod health
- Unknown
- Appears Normal
- Warning
- Broken/Invalid ZIP
- Protected/System Mod

### 2.4 Image state
- Preview Ready
- Preview Pending
- No Image Found
- Unsupported Image Format

### 2.5 Career state
- Career Ready
- Needs Approval
- Missing Required Fields
- External Override Only
- Unsafe to Patch
- Not Applicable

### 2.6 User verification state
- Unreviewed
- Reviewed
- User Verified
- User Rejected

No status should imply runtime functionality merely because files are present.

---

## 3. Catalog ordering and visibility

Default sort priority:
1. Selected/current item.
2. Needs career work.
3. Needs image/identity review.
4. Changed since last scan.
5. Normal available entries.
6. Career-ready entries.
7. Missing-source entries, only when enabled.
8. Hidden/archived entries, only when enabled.

Required filters:
- Vehicles
- Trailers
- Props
- Maps
- UI
- AI/script
- Mixed
- Unknown
- Installed
- Not installed
- Missing source
- Career ready
- Needs career work
- Needs image
- Changed since scan
- Hidden

The app must preserve one selected item while filters change unless that item is explicitly cleared.

---

## 4. Catalog card behavior

Each card should show:
- selected preview image;
- large readable display name;
- ZIP filename;
- brand/manufacturer when known;
- content type;
- installed/source state;
- career state color/icon;
- warning/duplicate/version indicators.

Click:
- opens the selected item's Career/Info page using cached data.

Right-click:
- Edit info;
- Change image;
- Open source folder;
- Open ZIP/image browser;
- Mark hidden;
- Mark reviewed;
- Add to collection/profile;
- Show duplicate/version family.

Missing-source card actions must not offer source-dependent operations as if the ZIP exists.

---

## 5. Image extraction and sidecar rule

For every selected catalog preview:
- Read candidates directly from the ZIP without full extraction.
- Extract only the selected preview.
- Store it beside the source ZIP when permitted.
- Name it to match the ZIP base name, using the chosen image extension or a normalized supported output extension.
- Update/replace the sidecar when the selected image changes; do not create repeated duplicates.
- Also keep persistent catalog metadata in the shared RedFox data folder.
- If the source folder is read-only, use persistent shared storage and clearly show that the sidecar could not be written beside the ZIP.

---

## 6. Next implementation scope

Before another feature build:
1. Audit v0.6.6 and v0.6.7.
2. Identify the current image-list, selection-state, launcher, responsive-grid, and status-field implementations.
3. Preserve all working scanner/catalog behavior.
4. Fix only:
   - responsive tiled Picture Home;
   - safe image preview/format handling;
   - hidden/sorted missing-source behavior;
   - shared CurrentSelection across tabs;
   - career builder launch error;
   - status field separation;
   - full-page scrolling/responsive sizing.
5. Do not add online research, ZIP patching, skin editing, or physical sorting in the same repair build.
6. Compare code before/after.
7. Reopen and inspect final ZIP.
8. Label runtime untested until David tests it.

---

## 7. Evidence from David's screenshots

Screenshots show:
- vertical/narrow tile layout;
- oversized image consuming the page;
- missing-source entries mixed into normal catalog results;
- ZIP-not-found dialog;
- unreadable/narrow image candidate paths;
- unsupported preview-format message;
- ambiguous status dropdown;
- Career Shop Builder launch failure from undefined `subprocess`;
- excessive disconnected tabs and controls.

These are user-reported runtime findings and must be treated as the current source of truth until a newer David-tested build proves otherwise.

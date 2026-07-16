# RedFox Mod Manager Suite — Career Compatibility Wizard Roadmap

**Updated:** 2026-07-16  
**Project:** `32-RedFox_Mod_Manager_Suite_`  
**Current uploaded baseline for audit:** `32-RedFox_Mod_Manager_Suite_v0_6_6_Simplified_Workspaces(1).zip`  
**Most recent chat-produced build:** `32-RedFox_Mod_Manager_Suite_v0_6_7_Master_Catalog_Foundation.zip`  
**Runtime status of v0.6.7:** UNTESTED by David  
**Build status:** PAUSED — documentation only; no new ZIP requested in this update

---

## 1. Current correction in direction

The app became split into too many tools/pages before the primary job was complete. The next active milestone must be one guided workflow dedicated to one job:

> Select a folder, installed-mod location, or ZIP; show only career-relevant vehicle/config entries; determine what is already career-ready; research and suggest missing information; require user approval; write safe career-compatible data; move unresolved items into a review queue; continue until the batch is complete.

This is a wizard, not a collection of unrelated workspaces.

The broader RedFox Mod Manager Suite remains the long-term platform, but the next working slice is the **Career Compatibility Wizard**.

---

## 2. Primary user goal

David has thousands of BeamNG mods and needs one tool that can:

1. Point at a folder, one ZIP, or the installed mods directory.
2. Scan without requiring every ZIP to be manually opened.
3. Show vehicles by default.
4. Hide maps, props, UI mods, AI mods, mixed mods, and unknown content unless their filters are enabled.
5. Determine whether every vehicle/config has all information required by BeamNG Career and the selected Career/RLS dealer system.
6. Display career-ready items clearly in green with high-contrast text.
7. Display incomplete/unresolved items clearly in grey/red or another accessible high-contrast warning style.
8. Let David click an incomplete vehicle and walk through every required field.
9. Auto-fill likely values from the mod files and real-world research.
10. Keep auto-filled values visually pending/dimmed until David approves them.
11. Mark the vehicle green only after every required field is approved and validated.
12. Continue to the next vehicle.
13. Move items the system cannot classify or safely edit into a review subfolder/queue after the main batch is processed.
14. Notify David when the automatic pass is complete and begin one-by-one review of unresolved items.

---

## 3. Wizard flow

### Step 1 — Choose source

Supported sources:

- One ZIP.
- One folder.
- Folder with subfolders.
- Installed BeamNG mods folder.
- One or more configured mod-storage folders.

Options:

- Scan recursively.
- Vehicles only by default.
- Include trailers.
- Include props.
- Include unknown/mixed content.
- Include disabled/not-installed mods.
- Use cached scan data where source ZIP hash/timestamp has not changed.

The app must clearly show when it is scanning and provide progress, current ZIP, elapsed time, and estimated remaining count. Long work must not make the window shrink, disappear, or look frozen.

### Step 2 — Detect entries

A ZIP may contain multiple types of content. Do not force one label onto the entire ZIP.

The scanner should identify:

- vehicles;
- configurations;
- trailers;
- props;
- maps;
- UI apps;
- AI/script mods;
- career/RLS systems;
- parts packs;
- mixed-content bundles;
- unknown content.

A map may also contain vehicles or props. The app should list the map as the main content and show the contained vehicle/prop entries as secondary content. Editing risky secondary content remains locked behind Dev Mode.

### Step 3 — Career readiness status

Each vehicle/config receives a status:

- **Green — Career Ready:** all required fields exist, validate, and are approved.
- **Yellow — Review Required:** likely valid, but some values were inferred or the mod is mixed/risky.
- **Grey/Red — Incomplete:** missing required career fields or invalid values.
- **Red — Unsafe/Protected:** career/RLS/core/mixed mod where direct ZIP edits could break the system.
- **Blue — External Override Only:** use RedFox compatibility data rather than touching the source ZIP.

Text and background colors must remain readable. Do not use low-contrast red-on-grey combinations.

### Step 4 — Vehicle detail and guided fields

Clicking a vehicle must open instantly from the scan database/cache. It must not rescan or reopen every ZIP merely to switch pages.

The vehicle page must show:

- large display name;
- source ZIP filename;
- internal vehicle folder/ID;
- config name;
- selected preview image;
- detected content/type;
- source paths for the values found;
- career readiness status;
- direct-edit risk level;
- required fields;
- suggested values;
- approval state;
- explanation/help bubble for every field.

Values already present in the mod are marked as source values. Values inferred by the app are marked pending. Values approved by David are marked approved.

### Step 5 — Auto research and matching

For real vehicles/trailers/equipment:

- identify likely brand, model, generation, year range, body style, drivetrain, fuel, vehicle type, commercial class, approximate real-world value, and rarity/population;
- prefer manufacturer specifications and credible vehicle/equipment listings;
- use recent used sales/auction listings for market value;
- cache research results to avoid repeated online searches;
- save sources and date checked;
- never claim an exact match without evidence.

Match labels:

- Exact match.
- Likely match.
- Closest real-world equivalent.
- User-provided match.
- Fictional/unknown — manual review.

If the app cannot identify the vehicle, David can:

- enter a description, such as “1980s–1990s Toyota modified crawler”;
- paste a link to a similar real-world vehicle;
- choose from suggested equivalents;
- manually enter values.

The app then researches from that user-provided direction.

### Step 6 — Approval

Auto-filled values remain visually dimmed/pending. David can:

- approve all high-confidence values;
- approve one field at a time;
- edit a value;
- reject and research again;
- provide a link or description;
- skip the vehicle;
- mark it external-override only;
- send it to manual review.

Only after all required fields are approved and validate does the status turn green.

### Step 7 — Write strategy

Safe order:

1. Save scan/database state.
2. Save RedFox external compatibility override.
3. Update the game-use catalog/compatibility data in a persistent folder that is not deleted by BeamNG cache clearing.
4. Test through the companion/in-game checker.
5. Only if requested, patch the original ZIP.

Direct ZIP patching rules:

- Dev/advanced permission required for risky mods.
- Show exact file changes before writing.
- Back up only the files being changed, not the full ZIP.
- Store small reversible backup data.
- Reopen and validate the final ZIP after writing.
- Never patch career/RLS/core bundles automatically.

### Step 8 — Unresolved queue

Items that cannot be classified or safely processed are placed into a review queue.

Optional physical organization:

- Create a configurable subfolder beside the scanned folder, such as `_RedFox_Needs_Review`.
- Do not move anything automatically without showing and approving the move plan.
- Preserve source paths in the database.
- Support undo.

After automatic processing, notify David with:

- total scanned;
- career ready;
- fixed/approved;
- pending approval;
- unresolved;
- unsafe/protected;
- failed ZIPs;
- moved-to-review count.

---

## 4. Required career field discovery

The exact BeamNG and RLS requirements must not be guessed from memory. Before implementing the fixer, the scanner/exporter must inspect current:

- BeamNG base-game vehicle/config metadata;
- current BeamNG Career dealer filters;
- current RLS Career Overhaul dealer and inventory logic;
- current config info files;
- vehicle value/population/year/category handling;
- any required thumbnail/catalog naming rules;
- mod compatibility examples that currently appear in career.

The resulting requirement set must be versioned by BeamNG version and RLS version.

Every field in the wizard must include:

- field name;
- what BeamNG/RLS uses it for;
- allowed values or useful range;
- source file/path;
- whether it is required, recommended, optional, or RedFox-only;
- whether changing it can break the mod;
- whether it affects career dealer appearance, value, rarity, filtering, or only catalog display.

---

## 5. Catalog and images

The catalog should resemble the BeamNG in-game vehicle picker so the user recognizes the workflow.

Image rules:

- Prefer images named `default`.
- Prefer images in known `mod_info`, preview, thumbnail, or vehicle image folders.
- Prefer image names matching the ZIP, vehicle folder, or configuration.
- Show all candidates when needed.
- Right-click/click an image to “Use as Preview.”
- Replace/update the selected preview rather than creating repeated duplicates.
- Store selected images in persistent shared RedFox/game-use storage, not cache or per-version folders.
- Do not include image binaries in scan-report ZIPs sent for analysis unless explicitly requested.

Future thumbnail studio:

- Preferred solution is an in-game companion UI/app that loads a selected vehicle/config in a controlled showroom.
- Allow camera angle, zoom, background, lighting, and capture size.
- Disable damage during loading/positioning.
- Save the image in the size/location BeamNG and the catalog use.
- Desktop-side arbitrary BeamNG rendering is not assumed feasible without the game.

---

## 6. Filters and sorting

Default view: vehicles only.

Optional filters:

- cars;
- trucks;
- tow/recovery;
- trailers;
- buses;
- aircraft;
- boats;
- props;
- maps;
- UI mods;
- AI/script mods;
- career/RLS mods;
- parts packs;
- mixed;
- unknown;
- installed;
- not installed;
- missing source;
- missing image;
- career ready;
- needs approval;
- needs review;
- unsafe/protected;
- multiplayer compatible.

Physical auto-sort must be optional and reversible. Examples:

- Ford;
- Chevrolet;
- Dodge/Ram;
- Toyota;
- tow trucks;
- trailers;
- maps;
- UI;
- multiplayer packs;
- custom folders.

The app must distinguish between catalog tags and physically moving ZIP files.

---

## 7. Easy mode and Dev mode

Default mode must be safe enough for a child/ordinary user.

Easy mode:

- guided wizard;
- dropdowns;
- help bubbles;
- no raw JSON;
- no raw file path editing;
- no direct Lua/JBeam editing;
- no risky ZIP patching;
- catalog/override changes only where safe.

Dev mode:

- explicit warning/acknowledgment that direct mod editing can cause corruption or data loss;
- raw files, logs, JSON, JBeam, Lua, ZIP internals;
- advanced patching;
- risky mixed-content editing;
- exact change preview and revert tools.

Career/RLS/core mods should default to protected, even in Easy mode.

---

## 8. Existing project history to preserve

Uploaded/known foundations and references include:

- `BeamNG_Mod_Manager_Tool_v0_3_5.zip` — original scanner/catalog foundation and remembered ZIP image candidate/right-click preview workflow.
- `32-RedFox_Mod_Manager_Suite_v0_6_6_Simplified_Workspaces(1).zip` — current uploaded baseline to inspect before another build.
- `32-RedFox_Mod_Manager_Suite_v0_6_7_Master_Catalog_Foundation.zip` — latest produced build, not yet tested by David.
- `BeamNG_Mod_Manager_Data.zip` — prior catalog/preview/cache data.
- `RedFox_Scan_History.zip` and prior scan archives.
- `ModConflictResolver.zip`.
- `Career23TB_MenuUnlockCheatMenu.zip`.
- `A+RadialCheatMenu.zip`.
- `teleportation_panel_jtf_modland.zip`.
- `IndividualPartRepair.zip`.
- `mileageWear.zip`.
- `vehicleandpartrandomizer.zip`.
- `barnfindgenerator.zip`.
- `A+breb's random vehicle spawner.zip`.
- `beamjoy-2.0.8.zip`.
- `BJSandbox-1.0.4.zip`.
- `SceneManager.zip`.
- RaceMP/extended/race references.
- RLS repo payout/smoke/tanker reference patches.

These references must be inventoried and used to learn file structures. Their presence does not prove runtime behavior.

---

## 9. Larger suite modules retained for later

Do not delete these plans, but do not let them split the current wizard:

- Security scanner and optional VirusTotal workflow.
- Conflict scanner/compatibility patch generator.
- Command/keybind scanner and in-game per-vehicle command helper.
- BeamNG version baseline/diff scanner.
- Companion report inbox.
- Multiplayer profiles and permanent-mod protection.
- Game-mode pack builder, such as Forklift Racing, Flood Night, Downhill Racing, Demolition Derby, and Heavy Recovery.
- Server/FTP synchronization.
- Foxfax vehicle history.
- RedFox Auctions, Salvage, Heavy Recovery, Imports/Exports, government surplus, and other dealer websites.
- Watchlists, market pricing history, deal score, and repair estimate ranges.
- Safe teleport carrying towing vehicle, trailers, cargo, and towed vehicles without damage.
- Map Combiner remains on hold until terrain/world-transform roadblock is solved.

---

## 10. Next build scope

No build was requested with this documentation update.

Before creating the next ZIP:

1. Audit `v0.6.6_Simplified_Workspaces` before editing.
2. Audit whether v0.6.7 changed or removed any baseline feature.
3. Identify and preserve the original image candidate/right-click preview code if present.
4. Document exact current functions/files and working/unproven state.
5. Freeze the next scope to the Career Compatibility Wizard only.
6. Determine current BeamNG/RLS required career fields from scanned current files.
7. Create the wizard data model and safe external-override output first.
8. Do not claim runtime success until David tests it.
9. After editing, compare code against baseline.
10. Reopen and inspect the final packaged ZIP.

---

## 11. Current status statement

- Career Wizard design: documented.
- Exact current BeamNG/RLS field requirements: not yet proven.
- Automatic online matching: planned, not implemented/proven.
- Career compatibility writer: planned, not implemented/proven in this update.
- v0.6.7 runtime: not tested by David.
- No files were built or modified in this update other than this GitHub roadmap.

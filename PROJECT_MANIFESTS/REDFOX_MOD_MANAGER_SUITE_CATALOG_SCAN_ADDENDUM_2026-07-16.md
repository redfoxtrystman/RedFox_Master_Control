# RedFox Mod Manager Suite — Catalog Scan / Hub Theme / Codex Intake Addendum

**Date:** 2026-07-16  
**Project:** `32-RedFox_Mod_Manager_Suite_`  
**Related roadmap:** `PROJECT_MANIFESTS/REDFOX_MOD_MANAGER_SUITE_CAREER_WIZARD_ROADMAP.md`  
**Current baseline awaiting audit:** `32-RedFox_Mod_Manager_Suite_v0_6_6_Simplified_Workspaces(1).zip`  
**Latest chat-produced build:** `32-RedFox_Mod_Manager_Suite_v0_6_7_Master_Catalog_Foundation.zip` — runtime untested by David

---

## 1. Immediate direction

The next development sequence is:

1. Receive and inspect the current RedFox Garage Hub/theme system.
2. Preserve the Hub's theme concepts and customization behavior without hijacking or replacing unrelated working Hub code.
3. Use a Codex-generated BeamNG/RLS scan export to learn the exact current game and Career requirements.
4. Build the shared master catalog first.
5. Make the Career Compatibility Wizard operate entirely from that catalog/cache.
6. Add direct ZIP changes only after the catalog, required-field rules, preview workflow, and backup/revert model are proven.

No new ZIP should be created until the selected baseline and Hub/theme reference are audited before editing.

---

## 2. Hub/theme reference intake

David will upload the RedFox Garage Hub used as the preferred theme/customization reference.

Useful Hub areas to inventory:

- theme definitions and theme persistence;
- font selection and readable contrast rules;
- tab visibility and tab order;
- button visibility and button order;
- right-click edit/move/hide behavior;
- window size/position persistence;
- scroll behavior and full-page layout patterns;
- settings storage paths;
- shared RedFox icons/logo assets;
- any existing module launcher or registry system;
- any existing help/about editor;
- any existing import/export/backup settings.

Preservation rule:

- copy/adapt only the theme/customization patterns needed by Mod Manager;
- do not replace the Hub or change its unrelated modules;
- document exactly which Hub files/functions are referenced or copied;
- retain original product names and IDs;
- runtime remains unproven until David tests.

---

## 3. One scan, one persistent catalog

The app must ask for and remember:

- BeamNG installation folder;
- BeamNG user folder;
- active/installed mods folder;
- at least five additional storage locations, with later support for unlimited locations;
- optional labels for each location, such as Installed, Main Library, Tow Trucks, Maps, Downloads, Work In Progress, Archive, Multiplayer.

The scanner records one persistent database entry for every ZIP and every internal item.

Each ZIP record includes:

- current path and storage-location label;
- installed/not installed/missing source state;
- file size, modified time, CRC/hash and scan time;
- exact duplicate group;
- related-version/family group;
- likely newest/older/unknown version state;
- source ZIP filename and internal mod identity;
- contained vehicles, configurations, maps, props, UI apps, AI/script systems, parts packs and Career/RLS files;
- dependencies, input actions, Lua extensions, JBeam names, materials and images;
- selected preview path;
- career-readiness state;
- edit risk and protection state.

On every app start, perform a fast change check against the database. Ask before changing states, for example:

> 225 previously installed mods are no longer present. Mark them not installed?

Do not delete catalog records automatically.

---

## 4. Duplicate and version-family detection

The scanner must find duplicates even when ZIP names differ.

Detection layers:

1. Exact ZIP hash match — byte-identical duplicate.
2. Internal file-set/hash match — same core content repacked or renamed.
3. Vehicle folder/JBeam/config identity match — likely same mod family.
4. Mod-info/title/author/internal ID match.
5. Similarity comparison — same mod with meaningful changed files.

For each related group, show:

- exact duplicates;
- likely same mod, different version;
- newest candidate;
- older candidates;
- files added, removed or changed;
- whether changes are only preview/readme metadata or actual gameplay files;
- current location of every copy;
- user-selected canonical copy;
- safe organize/archive plan.

Never delete, overwrite or move duplicates without an approved plan and undo record.

---

## 5. Mixed-content hierarchy

A map or system ZIP may contain vehicles, props or UI files.

Catalog behavior:

- display the main mod entry first, such as a map;
- list contained vehicles/configs/props as child entries under that parent ZIP;
- do not present map-linked vehicles as ordinary standalone vehicles without a visible parent/source label;
- allow filters for standalone only, bundled only or all;
- direct editing of risky child content stays protected behind Dev Mode unless the app has a proven safe writer for that content type.

All detected vehicles/configs still receive a Career-readiness analysis, but bundled/protected items may be external-override only.

---

## 6. Preview-image rules

Most BeamNG mods contain an info/mod-info image folder. The scanner must inspect ZIPs directly and display the actual images.

Preferred candidate order:

1. previously approved RedFox preview;
2. `default` image;
3. image inside recognised `mod_info`, `info`, `images`, `preview`, `thumbnail` or vehicle/config image folder;
4. image matching ZIP name, vehicle folder or config name;
5. best remaining candidate by dimensions/name.

Windows Explorer sidecar rule:

- extract/copy only the selected preview next to the source ZIP;
- name it with the ZIP base name, using the correct image extension;
- replace/update that sidecar when a different preview is selected;
- do not accumulate multiple duplicate sidecar images;
- preserve the internal source path in the catalog;
- show all internal image candidates when Change Image is selected.

Scan-report exports sent for analysis should omit image binaries unless explicitly requested.

---

## 7. Pure backup and edit-chain rule

When an original ZIP is patched:

- the first backup of each original file is immutable and must remain pure;
- later edits must never overwrite the first original backup;
- maintain a numbered edit chain or revision manifest;
- each revision records original hash, prior edited hash, new hash, timestamp, app version, changed fields and approval source;
- undo can restore the original or a selected prior revision;
- reopen and validate the finished ZIP after every write;
- protected Career/RLS/core bundles are not patched automatically.

Proposed internal structure, pending BeamNG compatibility test:

`_redfox_backup/original/` — first untouched originals  
`_redfox_backup/revisions/0001/`, `0002/` — later changed-file snapshots  
`_redfox_backup/manifest.json` — complete edit history

If internal backup folders affect a mod, use an external small backup package instead. This must be tested before broad use.

---

## 8. Career Compatibility Wizard data source

The exact required Career fields must be learned from current BeamNG and current RLS files, not guessed.

The Codex scan must export:

- stock vehicle/config `info_*.json` examples;
- stock vehicle picker/filter metadata;
- Career dealer eligibility/filter code;
- vehicle value, year, population/rarity and type handling;
- RLS dealer/shop inventory rules;
- known RLS-compatible third-party vehicle examples;
- thumbnail naming and lookup rules;
- relevant Lua/JSON paths and functions;
- differences between stock BeamNG and RLS requirements;
- BeamNG and RLS version identifiers.

The wizard then uses the persistent catalog, shows required fields, auto-fills likely values, marks inferred values pending, and turns an item green only after validation and approval.

---

## 9. Skin/texture workshop direction

Future skin workflow should remain one integrated module:

- identify likely skin/template/color-mask textures;
- show the texture and its source path;
- let the user choose the correct editable texture when detection is uncertain;
- open the configured external editor, such as Paint.NET or GIMP;
- detect the saved result;
- provide an external preview or in-game companion preview;
- emulate the useful workflow of BeamNG's decal/sticker paint system where practical;
- save as a new skin/config inside the existing vehicle ZIP;
- never overwrite the original skin;
- back up every changed metadata/material/config file using the pure backup/edit-chain rule.

A true arbitrary BeamNG vehicle render remains best handled by an in-game showroom/thumbnail companion unless a reliable external BeamNG renderer is found.

---

## 10. Physical organization and collections

The app may suggest physical organization based on catalog identity:

- manufacturer group, such as General Motors;
- brand, such as Chevrolet;
- model family, such as Corvette;
- functional group, such as Tow Trucks, Rotators, Maps, UI, Props, Work In Progress;
- user-created custom trees.

Show the complete move plan and require approval. Update database paths after moves. Preserve undo data.

Recording/game-mode collections should default to manifests or hard links instead of full copies when drive space is limited. A user may still request a real copied folder.

---

## 11. Codex scan package requirements

The Codex export must be small enough to upload and must not include full game assets, large textures, meshes, sounds or complete third-party mods.

Required output:

- `SCAN_SUMMARY.md`;
- `beamng_version.json`;
- `rls_version.json` if present;
- `career_requirements.json`;
- `vehicle_picker_filters.json`;
- `dealer_rules.json`;
- `example_stock_configs/` containing selected small metadata files only;
- `example_career_mod_configs/` containing selected small metadata files only;
- `relevant_source_snippets/` containing only targeted Lua/JS/JSON snippets with original paths recorded;
- `file_manifest.json` with paths, sizes and hashes;
- `unresolved_questions.md`;
- one ZIP containing only the report and small text/config files.

Do not include binaries, full maps, full vehicles, textures, models, sounds or paid/private content.

---

## 12. Current status

- Hub/theme reference: awaiting David upload.
- Codex game/RLS scan: awaiting execution.
- v0.6.7 runtime: untested by David.
- Exact Career requirements: not yet proven.
- Duplicate/version-family scanner: documented, not implemented.
- Pure backup/edit-chain writer: documented, not implemented or proven.
- Sidecar image naming/update rule: documented, not implemented/proven in the selected baseline.
- Skin workshop: documented for later.
- No new Mod Manager ZIP was created in this update.

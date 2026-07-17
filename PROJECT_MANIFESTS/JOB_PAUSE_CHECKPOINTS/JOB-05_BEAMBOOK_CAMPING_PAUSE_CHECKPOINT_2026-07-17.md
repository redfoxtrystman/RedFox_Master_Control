# JOB-05 — BeamBook Marketplace — Camping Pause Checkpoint

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Active chat:** JOB-05 — BeamBook Marketplace regular-chat takeover / Sol  
**Repository:** `redfoxtrystman/RedFox_Master_Control`  
**State:** PAUSED BY OWNER UNTIL RETURN — OWNERSHIP RETAINED — NO HANDOFF  
**Canonical build state:** STANDALONE v0.1.0 BUILT — RUNTIME UNTESTED  
**Research build state:** SETTINGS DERIVATIVE + READ-ONLY MONITOR BUILT — RUNTIME UNTESTED

## This is a pause, not a handoff

David is going camping and explicitly corrected the record: this checkpoint is not a transfer, replacement, abandonment, reassignment, or handoff of JOB-05.

JOB-05 remains claimed by the same regular-chat takeover. No other chat should claim, rename, merge, continue, or replace JOB-05 during this pause unless David explicitly changes ownership after returning.

No asynchronous or background work is occurring during the pause. Work resumes only when David returns to this chat and provides test results or a new instruction.

## JOB-05 responsibility

JOB-05 owns only the BeamBook Marketplace application and its BeamBook-specific research:

- Facebook-style BeamBook wall/news feed;
- BeamBook Marketplace storefront;
- vehicle listing cards and listing presentation;
- seller/profile/post/comment presentation;
- saved-listing presentation;
- groups presentation;
- BeamBook-local messages presentation, without replacing JOB-12 FoxMail/FoxText;
- editable BeamBook post/listing content;
- responsive phone and PC BeamBook layouts using one future canonical destination;
- BeamBook-specific assets, documentation, logging, testing, and handoff/checkpoint records;
- temporary isolated research into vehicle-list generation settings and monitoring.

JOB-05 does not own shared IceFox phone/PC core, the shared browser/registry, Career/RLS bridge, money, ownership, inventory, garage/storage, insurance, App Store, Scrap Yard, Import/Export, Classics, Tow/Recovery, SponsorHub, FoxMail, FoxText, Sponsor Rewards, or Visual Design implementation.

## Work-chat migration state

The original coordinated project jobs were unintentionally created in ChatGPT Work chats. David was not clearly informed that those chats used a separate limit. On July 14, 2026, the Work chats became inaccessible until July 20, 2026.

JOB-05 was manually transferred to a regular chat. The old shared-chat link could not be fetched by the replacement chat, so full chat-only history, attachments, hidden tool activity, and every old decision were not claimed as recovered. GitHub records, surviving project context, reuploaded files, and current conversation history were used to reconstruct the job.

Relevant migration records:

```text
PROJECT_MANIFESTS/JOB_CLAIMS/JOB-05_BEAMBOOK_MARKETPLACE_REGULAR_CHAT_TAKEOVER_2026-07-14.md
PROJECT_MANIFESTS/JOB_HANDOFFS/OWNER_ALL_JOBS_REGULAR_CHAT_MIGRATION_STATUS_2026-07-14.md
INCIDENT_REPORTS/2026-07-14_CHATGPT_WORK_CHAT_LIMIT_PROJECT_MIGRATION.md
```

## Canonical RedFox BeamBook work completed

A standalone RedFox-owned BeamBook test candidate was preserved before the external research derivative was started.

Exact candidate:

```text
PROJECT_RELEASE_CANDIDATES/JOB-05/5-RedFox_BeamBook_Standalone_v0_1_0_RUNTIME_UNTESTED.zip
```

Identity:

- Size: 565,280 bytes
- SHA-256: `1ba7933b39f4897ca22158dc27ca591ad4ec5109b01bd05a1ca7d3072d2361d8`
- Files: 28
- ZIP integrity: PASS
- Extracted inventory/hash comparison: PASS
- Duplicate archive entries: 0
- Static rendering verification: PASS
- BeamNG/RLS runtime: UNTESTED

Canonical source paths recorded for that candidate:

```text
lua/ge/extensions/redfox/beamBookStandalone.lua
lua/ge/extensions/core/input/actions/redfoxBeamBookStandalone.json
ui/modules/apps/RedFoxBeamBook/app.json
ui/modules/apps/RedFoxBeamBook/app.js
ui/modules/apps/RedFoxBeamBook/app.html
ui/modules/apps/RedFoxBeamBook/app.css
ui/modules/apps/RedFoxBeamBook/app.svg
ui/modules/apps/RedFoxBeamBook/app.png
ui/modules/apps/RedFoxBeamBook/site/index.html
ui/modules/apps/RedFoxBeamBook/site/assets/css/beambook.css
ui/modules/apps/RedFoxBeamBook/site/assets/js/beambook.js
ui/modules/apps/RedFoxBeamBook/site/assets/data/beambook_posts.json
```

Canonical standalone features already built:

- unique extension `redfox_beamBookStandalone`;
- bindable `RedFox: Toggle BeamBook` action;
- UI app container loading the BeamBook website;
- WEUI/World Editor-style settings behavior;
- dark/light Facebook-style BeamBook wall using RedFox branding;
- 192 post content pack;
- 100 randomized posts per session;
- initial 16 posts and 10 more per load action;
- 240 procedural profiles;
- reactions, badges, nested replies, and tiled galleries;
- BeamBook Marketplace control;
- category presentation for cars, trucks, buses, trailers, vans, props, and other listings;
- search, price, distance, and sort controls;
- 90 catalog listings;
- full listing viewer;
- current-map parking-spot selection;
- eligible-vehicle generation only on an explicit Marketplace request;
- selected-listing handoff toward stock `career_modules_inspectVehicle.startInspection`;
- optional quick travel;
- explicit errors when Career/RLS/generator/inspection/parking support is unavailable;
- `[RedFox][BEAMBOOK]` logging.

Canonical standalone boundaries intentionally preserved:

- no startup Career module;
- no startup `modScript.lua` loader that globally activates Career behavior;
- no global replacement of `getShoppingData` or `startInspection`;
- no custom money system;
- no fake ownership;
- no fake inventory/storage/garage insertion;
- no direct spawn treated as purchase success;
- no shared IceFox phone/PC registration before JOB-01/JOB-02 contracts are ready.

Canonical final record:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-05_STANDALONE_BEAMBOOK_FINAL_HANDOFF_v0.1.0_2026-07-14.md
```

## External BeamBook research completed

David uploaded the original third-party `beamBook.zip` because he wanted to understand which Lua controls changed vehicle selection and wanted a practical test of broader vehicle and condition generation before implementing equivalent proven behavior in the RedFox version.

The inspected original main module was:

```text
lua/ge/extensions/career/modules/beamBook.lua
```

Important original behavior identified:

- only `listingCount` was exposed through `beamBook/config.json`;
- listings came from `util_configListGenerator.getEligibleVehicles()`;
- random selection primarily used each configuration's `Population` value;
- configurations with zero population could effectively receive no selection chance;
- mileage was assigned randomly from 0 through 250,000 miles;
- mileage drove the wear-price curve;
- seller personality adjusted asking price;
- the original mod injected a BeamBook dealership tile into stock shopping data;
- the original mod globally patched shopping/inspection behavior;
- the original mod did not include its own dedicated settings UI.

Research conclusion before coding:

Adding a native key-opened settings window and configurable category/quality generation would be genuinely new behavior and useful research toward the RedFox BeamBook implementation.

## External research packages built

### Edited third-party BeamBook research derivative

```text
beamBook_RedFoxResearch_v1_1_0_RUNTIME_UNTESTED.zip
```

Identity reverified on 2026-07-17:

- Size: 12,776 bytes
- SHA-256: `c31934535460812bd38a9e1e0ae99058458f16d76c17334282989d1f4ed4705e`
- Files: 8
- ZIP integrity: PASS
- JSON validation: PASS
- Original build validation recorded Lua parse: PASS
- BeamNG/RLS runtime: UNTESTED

Exact archive contents:

```text
READ_ME_FIRST_REDFOX_RESEARCH.txt
TEST_CHECKLIST_REDFOX_RESEARCH.txt
lua/ge/extensions/beamBookLoader.lua
lua/ge/extensions/career/modules/beamBook.lua
lua/ge/extensions/core/input/actions/redfoxBeamBookResearchSettings.json
lua/ge/extensions/redfox/beamBookResearchSettings.lua
mod.json
scripts/beamBook/modScript.lua
```

Research settings added:

- listing count;
- balanced-category generation;
- optional guaranteed category coverage where eligible vehicles exist;
- inclusion of eligible zero-population configurations;
- minimum selection population weight;
- duplicate cap per exact configuration;
- minimum and maximum model year;
- maximum mileage;
- listing lifetime;
- category weights for cars, pickups, SUVs, vans, buses, heavy vehicles, trailers, special vehicles, and other/unclassified vehicles;
- factory, custom, and unknown configuration-type weights;
- excellent, good, average, worn, and rough condition weights;
- separate mileage ranges for each condition;
- negotiation enable/disable;
- seller price-multiplier limits;
- minimum and maximum asking price;
- save settings;
- save and regenerate listings;
- reload settings;
- restore defaults and regenerate.

Bindable action:

```text
BeamBook Research: Open Settings
```

Expected persistent config:

```text
beamBook/config.json
```

Research metadata is attached to generated listings for category, quality/condition, configuration type, and original population.

### Separate read-only research monitor

```text
RedFox_BeamBook_Research_Monitor_v0_1_0_RUNTIME_UNTESTED.zip
```

Identity reverified on 2026-07-17:

- Size: 5,713 bytes
- SHA-256: `1a14a614dec692171cdb3383afaf2ccc912d1008f531c3e8d5dc9ad321adbb8b`
- Files: 6
- ZIP integrity: PASS
- JSON validation: PASS
- Original build validation recorded Lua parse: PASS
- BeamNG/RLS runtime: UNTESTED

Exact archive contents:

```text
READ_ME_FIRST.txt
lua/ge/extensions/core/input/actions/redfoxBeamBookResearchMonitor.json
lua/ge/extensions/redfox/beamBookResearchMonitor.lua
lua/ge/extensions/redfoxBeamBookMonitorLoader.lua
mod.json
scripts/redfoxBeamBookMonitor/modScript.lua
```

Bindable action:

```text
RedFox: Open BeamBook Research Monitor
```

Monitor intent:

- observe listing count and unique configurations;
- observe category and quality distributions;
- calculate minimum/average/maximum mileage;
- calculate minimum/average/maximum price;
- report selected zero-population configurations;
- report duplicates;
- report parking failures;
- report generator diagnostics when exposed by the research derivative;
- export evidence without intentionally changing game state.

Expected exports:

```text
beamBookResearch/latest_snapshot.json
beamBookResearch/listings_YYYYMMDD_HHMMSS.csv
```

The monitor is intended to remain read-only and must not alter money, purchase, ownership, inventory, storage, garage, inspection, spawning, Career progression, or BeamBook listing generation.

### Combined research delivery bundle

```text
RedFox_BeamBook_Research_Test_Bundle_v0_1_0_RUNTIME_UNTESTED.zip
```

Identity reverified on 2026-07-17:

- Size: 29,977 bytes
- SHA-256: `f04fe03a0b4c66850ff0d63a6b8b3428e5430bbe0e229e0c043cccf9c869fa19`
- Files: 5
- ZIP integrity: PASS

Exact contents:

```text
beamBook_RedFoxResearch_v1_1_0_RUNTIME_UNTESTED.zip
RedFox_BeamBook_Research_Monitor_v0_1_0_RUNTIME_UNTESTED.zip
BEAMBOOK_RESEARCH_PACKAGE_GUIDE.txt
beamBook_original_vs_RedFoxResearch.diff
BEAMBOOK_RESEARCH_BUILD_MANIFEST.json
```

Supporting identities:

```text
BEAMBOOK_RESEARCH_PACKAGE_GUIDE.txt
Size: 3,988 bytes
SHA-256: 8501b1e6e023db04eedcbca27d39836129f3715a6f57f0f9402d48cb34731135

beamBook_original_vs_RedFoxResearch.diff
Size: 38,987 bytes
SHA-256: e5f31bbd5bb10546b550df21681994c4391f705fc8f19f8c58b6f1dda7f52448
```

The embedded manifest's outer-bundle size is stale. The external size and SHA-256 in this checkpoint are authoritative. The delivered bundle itself was not changed during this correction.

Corrected research build record:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-05_BEAMBOOK_EXTERNAL_RESEARCH_SETTINGS_MONITOR_BUILD_2026-07-15.md
```

## What was tried

- Tried to recover the prior Work-chat transcript from the supplied share link; it could not be fetched.
- Reconstructed JOB-05 state from GitHub, project context, current uploads, and surviving records.
- Inspected the original third-party BeamBook Lua to identify listing generation, population weighting, mileage, pricing, parking, tile injection, and inspection remapping.
- Confirmed the original mod had no dedicated settings window.
- Designed an external research derivative rather than prematurely changing the canonical RedFox candidate.
- Added a native WEUI settings concept and input action to the derivative.
- Added configurable mixed vehicle categories and condition/mileage bands.
- Added a separate read-only monitor to compare desired settings with actual generated listings.
- Built and packaged the derivative, monitor, guide, diff, manifest, and combined bundle.
- Performed static archive checks.
- Reverified all three delivered ZIP hashes and ZIP integrity on 2026-07-17.
- Revalidated JSON files on 2026-07-17.
- Found and corrected inaccurate internal path names and stale outer-bundle size in the GitHub research audit.
- Did not claim BeamNG runtime success.

## What remains untested

### Canonical RedFox standalone candidate

- UI app discovery;
- input-action discovery and key binding;
- key-open behavior;
- WEUI settings behavior;
- wall rendering in BeamNG;
- Marketplace rendering in BeamNG;
- Career/RLS compatibility;
- current-map parking placement;
- listing-to-inspection routing;
- quick travel;
- normal purchase completion;
- real money deduction;
- real ownership result;
- real inventory/storage/garage result;
- West Coast USA behavior;
- non-West-Coast behavior;
- shared IceFox phone/PC routing, which remains blocked by shared contracts.

### Research derivative and monitor

- whether both input actions appear in Controls;
- whether both actions bind successfully;
- whether the WEUI settings window opens;
- whether World Editor/F11 is required before the window appears;
- whether settings persist to `beamBook/config.json`;
- whether save-and-regenerate replaces listings correctly;
- whether category weights materially alter generated listings;
- whether zero-population eligible configurations appear;
- whether trailers, heavy vehicles, buses, vans, specials, and unusual mod vehicles are present in the eligible pool;
- whether category keyword detection classifies David's installed mods correctly;
- whether duplicate caps work;
- whether year/price filtering works without starving listing generation;
- whether condition mileage bands are reflected in listing prices;
- whether Mileage Wear/RLS converts assigned mileage into visible/mechanical wear;
- whether the monitor opens and stays read-only;
- whether monitor counts match actual listings;
- whether JSON and CSV exports are written;
- whether inspection and purchase continue to work after derivative changes;
- whether the original mod's global patches conflict with current RLS/Career behavior;
- West Coast USA and non-West-Coast behavior.

## Known limitations and risks

- The derivative can only select configurations returned by `util_configListGenerator.getEligibleVehicles()`.
- Changing weights cannot recover configurations excluded before that function returns.
- A future controlled catalog scan may be needed if desired vehicle types never enter the eligible pool.
- Category detection is metadata/keyword based and may misclassify poorly tagged mod vehicles.
- Quality currently means mileage/value bands, not a new independent structural-damage system.
- Physical wear depends on Mileage Wear, RLS, or another system reading mileage.
- The derivative inherits the original mod's global shopping/inspection patch approach and is not the intended final RedFox architecture.
- The original third-party `beamBook.zip` must be disabled while testing the derivative.
- Public redistribution permission for the original third-party source has not been confirmed, so the derivative binary/source was not published to the public GitHub repository.
- The research monitor is a temporary JOB-05 sidecar, not a new job or shared system.
- No runtime result should be called working, fixed, complete, or safe until David tests the exact file and returns evidence.

## Planned work after David returns

The next implementation decision depends on runtime evidence. The intended sequence is:

1. Test the research derivative and monitor first to learn what the eligible pool and classifiers actually do.
2. Fix the first proven failing layer rather than redesigning everything at once.
3. Adjust category detection and weights based on exported evidence.
4. Decide whether `getEligibleVehicles()` is sufficient or whether a controlled catalog scan is required.
5. Decide which settings are genuinely useful and stable enough to move into the canonical RedFox BeamBook.
6. Reimplement proven behavior in the isolated RedFox architecture without copying the derivative's global patch design.
7. Preserve stock/RLS purchase, money, ownership, inventory, storage, and garage authority through JOB-02's approved contract.
8. Integrate one canonical BeamBook destination into phone and PC only after JOB-01/JOB-02/JOB-11 contracts are published and JOB-00 approves integration.
9. Continue Facebook-style wall/Marketplace visual polish using the preserved screenshot/content references.
10. Keep all-map support as a required test, not an assumption.

## Exact first test after return

1. Disable or remove the original third-party `beamBook.zip`.
2. Extract `RedFox_BeamBook_Research_Test_Bundle_v0_1_0_RUNTIME_UNTESTED.zip` outside BeamNG.
3. Install both inner ZIP files in the BeamNG mods folder.
4. Start an active Career/RLS save.
5. Open Controls and look for:

```text
BeamBook Research: Open Settings
RedFox: Open BeamBook Research Monitor
```

6. Bind both actions.
7. Open the settings window. If it does not appear, press F11 once and try again.
8. Enable balanced category generation and eligible zero-population configurations.
9. Select a broad mixed category/quality setup.
10. Press Save and Regenerate Listings.
11. Open the normal vehicle-shopping screen and enter the BeamBook tile.
12. Check whether cars, pickups, SUVs, vans, buses, heavy vehicles, trailers, special vehicles, and other entries appear.
13. Check whether excellent, good, average, worn, and rough mileage/price ranges appear.
14. Open the monitor and compare its totals with the visible listings.
15. Export JSON and CSV.
16. Inspect one listing and attempt one normal purchase.
17. Confirm whether real money, ownership, inventory, storage, and garage behavior complete normally.
18. Test on West Coast USA.
19. Repeat discovery/listing/inspection essentials on at least one non-West-Coast map.

## Evidence to return

- `beamng.log` lines containing `beamBook`;
- `beamng.log` lines containing `BEAMBOOK-MONITOR`;
- exported `beamBookResearch/latest_snapshot.json`;
- exported `beamBookResearch/listings_YYYYMMDD_HHMMSS.csv`;
- screenshot showing each input action in Controls;
- screenshot of the settings window;
- screenshot of mixed BeamBook listings;
- screenshot of the monitor totals;
- screenshot of inspection;
- screenshot or description of purchase completion/failure;
- exact map name;
- whether the original `beamBook.zip` was disabled;
- BeamNG version;
- RLS/Career mod version;
- enabled-mod list;
- first exact failing checkpoint;
- whether the failure is repeatable after one clean restart.

## Files currently available only through the regular chat workspace

```text
RedFox_BeamBook_Research_Test_Bundle_v0_1_0_RUNTIME_UNTESTED.zip
beamBook_RedFoxResearch_v1_1_0_RUNTIME_UNTESTED.zip
RedFox_BeamBook_Research_Monitor_v0_1_0_RUNTIME_UNTESTED.zip
BEAMBOOK_RESEARCH_PACKAGE_GUIDE.txt
beamBook_original_vs_RedFoxResearch.diff
BEAMBOOK_RESEARCH_BUILD_MANIFEST.json
```

These derivative/research binaries are not public GitHub release assets because the original third-party code's redistribution permission is unconfirmed.

## GitHub records and commits already created

Regular-chat migration and claim continuity:

```text
c16da3c861812aad4ff991c253f992003dcb3f1a
JOB-05: record regular-chat takeover after Work-chat lockout

e5bc3e4b7af64582ae6975a387d75b7db899668d
JOB-05: transfer active claim to regular chat

f060479cee5ab2d3fed98851bb5d0adc5f89d10a
JOB-05: mark regular-chat migration complete

12dfc23accf52f0d8d265f5493e9241f79fe3b7a
JOB-05: append Work-chat migration audit trail
```

Research build record:

```text
026d4bae47018102521a43c998de112d4dbe6148
JOB-05: document BeamBook settings and monitor research build
```

Corrected research package inventory/audit:

```text
e5e449c770c828dfecfbe40518f1d92cacff1cc9
JOB-05: correct research package inventory and audit details
```

This pause checkpoint is added in a new commit and must be treated as the authoritative restart record for the camping pause.

## Exact restart point

When David returns, do not start over and do not ask him to repeat the project history.

Resume at:

```text
JOB-05 — BeamBook Marketplace
Research derivative + read-only monitor are built but runtime untested.
First action: run the exact research-bundle test, collect logs/exports/screenshots, and fix the first proven failing checkpoint.
```

The preserved canonical standalone candidate remains separate and must not be overwritten by research changes unless testing proves a specific improvement should be ported into the RedFox implementation.

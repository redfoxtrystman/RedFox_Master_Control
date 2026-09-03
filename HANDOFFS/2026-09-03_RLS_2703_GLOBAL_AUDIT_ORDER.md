# RLS Career Overhaul 2.7.0.3 Global Audit Order

Date: 2026-09-03 local user time
Project: BeamNG RedFox mods / RLS compatibility
Source coordination issue: GitHub issue #69

## Current command from David

RLS Career Overhaul 2.7.0.3 is a major internal update, not a simple drop-in replacement. It changes Career saves, inventory and parts, vehicle shopping, insurance, traffic/police, events, garages, recovery, marketplace, and UI routing.

Keep RLS 2.7.0.1 as the working baseline until each RedFox mod is updated and tested.

Full evidence is in GitHub issue #69:
https://github.com/redfoxtrystman/RedFox_Master_Control/issues/69

## Message to send to every chat

> RLS Career Overhaul has updated from 2.7.0.1 to 2.7.0.3. Read GitHub issue #69 before editing anything. Scan your mod byte-for-byte against the new RLS version, identify every overlapping or copied RLS file, and report the exact compatibility risks first. Then update only the necessary files. Preserve the current working build and make a rollback backup. Record source/output hashes, exact changed paths, static-test results, and a BeamNG runtime-test checklist. Do not claim compatibility until I test it.

## Job-specific instructions

### JOB-04 Parts/Wrecking Yard

Check `partInventory`, `partShopping`, `inventory`, `vehicleShopping`, computer registration, saves, and UI routing. Native RLS My Parts must remain authoritative. Do not restore the rejected Parts Shop deletion/recovery system.

### JOB-13 KoParts/Auctions

Check vehicle shopping, inventory, marketplace/value calculations, Career Computer registration, auction lifecycle, and native UI routing. Do not copy or replace RLS modules unnecessarily.

### Used Car Lot

Check `vehicleShopping`, `valueCalculator`, inventory delivery/storage, marketplace data, insurance fields, saves, and UI routes.

### JOB-08 Insurance

Rebase against the new native insurance code. Check inventory IDs, player attributes, vehicle policies, phone routes, and save/load behavior.

### JOB-09 Tow/Recovery

Check off-road recovery, roadside service, repo systems, traffic/police interaction, inventory custody, events, missions, phone routes, and saves.

### Phone / IceFox / FoxNet

Check all changed RLS UI/router and Career Computer paths. Do not iframe native apps or replace global RLS UI bundles.

### Garage / registration / maintenance adapters

Check inventory, garages, maintenance, computer registration, delivery/storage, save lifecycle, and vehicle ID handling.

### Persistent Catalog / Memory Guard

There is a confirmed collision with RLS 2.7.0.3's `valueCalculator.lua` and `vehicleShopping.lua`. Rebase both files before producing a compatible version.

## Mandatory process for every chat

Audit first. Show findings. Then discuss the patch plan with David before editing.

Before editing:

1. Read GitHub issue #69.
2. Preserve the current working build.
3. Make a rollback backup.
4. Compare current mod against RLS 2.7.0.1 and RLS 2.7.0.3 where available.
5. Identify exact file/path overlaps and copied RLS files.
6. Identify exact risks: save, UI route, inventory, marketplace, garage, traffic/police, recovery, insurance, events, phone/PC, career computer, and vehicle ID handling.

During patching:

1. Change only necessary files.
2. Do not replace whole RLS modules unless explicitly approved after audit.
3. Do not iframe native RLS apps.
4. Do not restore rejected systems.
5. Preserve current working RedFox behavior unless a required RLS compatibility fix needs a targeted change.

After patching:

1. Record source ZIP name, output ZIP name, source hash, output hash, and changed file list.
2. Reopen final ZIP.
3. Run static/package checks.
4. Provide a BeamNG runtime checklist.
5. State clearly: compatibility is not proven until David tests the exact ZIP.

## Note for RedFox VTOL Drive chat

RedFox VTOL Drive is mostly vehicle-side and native ImGui/GE Lua, so RLS 2.7.0.3 risk is probably lower than career apps. Still audit before any future RLS-related patch because RLS 2.7.0.3 changes traffic/police, events, recovery, vehicle shopping/garage/inventory, save lifecycle, and UI routing. VTOL's experimental NPC/traffic hover could indirectly interact with traffic/police behavior if enabled, so avoid claiming no interaction until the exact installed VTOL build and RLS 2.7.0.3 are tested together.

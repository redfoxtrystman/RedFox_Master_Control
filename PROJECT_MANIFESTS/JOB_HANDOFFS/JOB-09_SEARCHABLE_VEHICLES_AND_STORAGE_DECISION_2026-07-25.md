# JOB-09 — Searchable Vehicles and Storage Priority Decision

**Date:** 2026-07-25

## Current searchable-vehicle behavior

The periodic `Search Abandoned Vehicle` action applies only to the active target of an **Abandoned Vehicle Recovery** call.

- Player must be within 12 meters.
- Target may be searched only once.
- This is a valuables/loot roll, not a search of the installed vehicle catalog and not a yard-record search.
- Current loot modes:
  - Arcade: Nothing 20%, Common 35%, Uncommon 27%, Rare 14%, Extremely Rare 4%.
  - Balanced: Nothing 35%, Common 33%, Uncommon 22%, Rare 8.5%, Extremely Rare 1.5%.
  - Realistic: Nothing 55%, Common 27%, Uncommon 13%, Rare 4.5%, Extremely Rare 0.5%.
- Current award ranges:
  - Common: $20–$95
  - Uncommon: $100–$290
  - Rare: $300–$850
  - Extremely Rare: $900–$2,400
- The result is paid through the normal queued Career-money path.

## David’s priority decision

The next update must prioritize:

1. Company work trucks stored in RedFox tow-garage storage, not personal Career storage.
2. Company work trucks separated from abandoned/lien/police/recovered inventory.
3. Yard records categorized, searchable, sortable, and visually separated.
4. Tow history searchable, sortable, and easier to read.
5. Tow costs and rates editable and saved.
6. A controlled sale test to establish where sale money goes.
7. Invoice visual redesign may wait for the website layer.
8. Crash-scene and semi-classifier work may wait until storage/organization is proven.

This decision is implemented as the v0.2.9 candidate documented separately.

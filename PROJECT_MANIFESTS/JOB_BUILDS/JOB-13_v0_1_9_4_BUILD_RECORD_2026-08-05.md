# JOB-13 v0.1.9.4 Build Record

## Artifact

`RedFox_JOB13_FoxNet_Online_Auctions_v0_1_9_4_SINGLE_STATE_PAYMENT_RECOVERY.zip`

SHA-256: `285b741b26f30e7eb00011f695e035394d5b65af346249599f2f66251f8ccd12`

Base: v0.1.9.3 (`c132416b2f654cdce7483a83bf44b7eddccb1e5a0b03784a93990a47a97a342c`)

## Purpose

Repair the split/cloned auction timelines and duplicate settlement paths reported in v0.1.9.1–v0.1.9.3.

## Architecture lock

- one Lua-owned current/next auction state;
- one auction snapshot writer and one state-file write call;
- one low-level clock restore, reachable only through one guarded recovery gate;
- pause/resume generations prevent duplicate lifecycle restores;
- page reload, PC/phone switch, bridge reconnect, and extension unload are display-only for auction state;
- re-entrant saves are coalesced;
- 30-second active freeze snapshots remain;
- v0.1.9.3 active lots/timers/bids are not migrated.

Account profile and transaction ledger remain separate files but cannot alter active auction clocks/lots.

## Payment recovery

- Payment Pending controls added to Bought Vehicles and Invoices;
- both call the same settlement action and action lock;
- ledger can reconstruct a missing pending lot;
- an existing inventory vehicle with a pending JOB-13 delivery key is finalized in place;
- delivery claim must save before spawn;
- payment charge lock must save before deduction;
- uncertain interrupted payment returns verification-required instead of charging again;
- duplicate delivery keys and completed keys remain enforced.

## Retained behavior

- auto next-auction transition;
- pending wins survive rotation;
- next-auction reminder;
- explicit watchlist action;
- seller priority and multiple consignments;
- reserve prices;
- calmer NPC defaults and custom filters;
- bank-backed buying power;
- PC scrolling.

## Verification

Gate 1 PASS: exact base, 19 files, no duplicate/unsafe paths, protected jobs absent.

Gate 2 PASS: 11 approved JOB-13 files changed; JSON/JS/Lua syntax; mirrored HTML; one-writer/one-recovery checks; payment/delivery lock ordering.

Gate 3 PASS: fresh extraction byte-matched edited tree; ZIP integrity; 19 files; no duplicate/unsafe paths; all checks reran.

## Runtime status

UNPROVEN until the user tests the exact ZIP. First test is five page reloads plus PC/phone switching while confirming one unchanged auction timeline.

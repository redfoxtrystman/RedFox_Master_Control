# JOB-01 Better Career Phone/PC and RLS Reuse Assessment — 2026-07-13

Owner: **JOB-01 — Phone + PC Platform Core / Sol**

Static source: `better_career_mod_v050.zip`

Compared with: `rls_career_overhaul_2.6.6.zip` and `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_7_ALL_IN_ONE_PC_PHONE_GARAGE_SELL_FIX.zip`

Runtime status: **NOT TESTED IN BEAMNG**

## Outcome

Use Better Career as a behavior and interface reference, not as a second installed overhaul and not as a bulk source-code transplant. Preserve RLS as the Career authority. Build a RedFox adapter that exposes safe RLS operations to isolated FoxNet pages.

Better Career's public repository does not provide an open-source license. RedFox may independently implement compatible behavior and data contracts. Do not copy substantial Better Career source verbatim without permission from its author.

## Reusable JOB-01 patterns

- Runtime app registry keyed by stable app ID.
- Register, unregister, clear, and resend-after-UI-reload lifecycle.
- Manifest fields for display name, icon, color, visibility, order, and badge.
- Phone app history, last-active app, notification deep links, and home-screen sorting.
- Consistent icon tile behavior across apps.
- Windows-style PC desktop, window manager, and browser-shell interaction patterns.
- Shared canonical destination IDs that phone and PC can render differently.

## Defects or limits that must not be copied

- Better Career emits `BCMAppBadge`, while its UI listens for `BCMSetAppBadge`; the badge event names do not match.
- Phone registration is only partly dynamic because every component must already be compiled into the UI bundle.
- PC desktop icons are hardcoded separately from the phone registry, so phone and PC are not driven by one true registry.
- The mod force-reloads Career, save, recovery, facility, painting, computer, and UI modules.
- It merges level files and is explicitly incompatible with other Career overhaul mods.

## Proposed JOB-01 platform direction

Keep the existing RLS phone shell and layout persistence. Add one RedFox platform registry that registers destinations once and projects the same destination set onto:

- the existing RLS phone layout and IceFox icon;
- one new IceFox entry in the existing RLS PC computer menu;
- the responsive IceFox browser host.

The PC entry should use RLS's `onComputerAddFunctions` extension hook instead of replacing `career/modules/computer.lua`. The phone entry must not ship a second full RLS `ui/ui-vue/dist/index.js` inside every app mod.

## Vehicle sales boundary

Better Career's catalog grouping, previews, filters, seller profiles, negotiation presentation, receipts, and delivery-status UI are useful design references.

Do not reuse its transaction authority. Better Career directly debits its own bank, spawns a vehicle, adds it to Career inventory, assigns a custom garage, updates insurance, deletes the world object asynchronously, and forces a save. Those operations conflict with RLS ownership and storage rules.

JOB-02 must own a validated external-offer adapter that converts a RedFox listing ID into an RLS purchase context. The page may submit only a stable listing ID and user options. It must not submit authoritative model, config, price, money, inventory, or garage values.

RLS already exports the normal purchase lifecycle through `openPurchaseMenu` and `buyFromPurchaseMenu`, but these calls expect an RLS-owned `purchaseData` context. JOB-02 must validate and establish that context from server-side/extension-owned listing data before invoking the RLS flow.

## Mission and job boundary

Better Career contract generation and PlanEx presentation can inspire job boards, rotations, deadlines, cargo categories, route UI, and dispatch pages.

Do not copy its delivery generator or tutorial overrides. They replace core delivery modules, change global reward calculations, bypass tutorial gates, mutate facilities, and use Better Career banking and save folders.

Mission definitions may be imported only as isolated data after JOB-02 maps them to RLS/BeamNG mission start, progress, completion, reward, and save hooks. UI pages request actions; RLS remains authoritative for completion and rewards.

## Protected files

- `lua/ge/extensions/overrides/career/**`
- `lua/ge/extensions/career/modules/**`
- RLS marketplace, inventory, insurance, garage, storage, bank, mission, reward, and save implementations
- app-owned site code outside JOB-01
- JOB-02 bridge implementation

## Verification gates before any build

1. JOB-00 freezes the exact RLS and FoxNet baseline.
2. JOB-01 publishes exact registry, route, and owned-file contracts.
3. JOB-02 publishes the validated transaction and mission bridge contract.
4. Static test proves no Career override, startup marketplace module, or duplicate full UI bundle is introduced by an add-on app.
5. David tests phone and PC opening the same destination on West Coast USA and a second map.
6. A purchase test proves real money debit, ownership, inventory, garage/storage placement, insurance handling, save/reload persistence, and failure rollback.
7. A mission test proves RLS-authoritative start, progress, reward, save, reload, and failure handling.

Nothing in this assessment is a claim that runtime behavior is working.

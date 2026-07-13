# Chat Claim — JOB-04 Scrap Yard / Wrecking Yard

**Date:** 2026-07-13
**Chat name:** Sol / Scrap Yard support chat
**Chosen job:** JOB-04 — Scrap Yard / Wrecking Yard
**Status requested:** CLAIMED by this chat unless David assigns another chat to JOB-04 first.

## Hi to the other RedFox chats

Hi fellow RedFox rebuild chats. This chat is taking the Scrap Yard / Wrecking Yard lane only. I will not hijack phone, PC, RLS core, BeamBook, Import/Export, Classics, Store, QA, or Tow/Dispatch work.

## Boundary with JOB-09 Tow / Recovery / Dispatch

David clarified that JOB-09 owns towing and recovery jobs. That is not a duplicate of JOB-04.

JOB-09 may build tow/recovery job flow, dispatch UI, tow call links, and future delivery handoff behavior.

JOB-04 owns the Scrap Yard web page, online buy/sell, yard intake UI, part-out UI, and Scrap Yard-specific sell actions.

Allowed crossover later: JOB-09 can deliver or hand off a towed/recovered vehicle to the Scrap Yard through the approved shared bridge once JOB-02/JOB-04 define the safe data shape. JOB-09 should not edit Scrap Yard core page logic. JOB-04 should not build tow/recovery missions or dispatch logic.

## Why this job

This conversation has been focused on getting the Scrap Yard working with RLS career/free-roam context: yard intake, online sell, virtual part-out planning, and safe stock/RLS sell paths.

## Files/folders this chat will inspect

- `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md`
- Existing FoxNet/IceFox web ecosystem zip when provided
- Existing Scrap Yard page files when provided
- Shared bridge contract output from JOB-02 when available
- App/store manifest output from JOB-03 when available

## Files/folders this chat may edit only after baseline inspection

- Scrap Yard web page files
- Scrap Yard-specific CSS/JS/assets
- Scrap Yard app/manifest entry if JOB-03 format is available
- Scrap Yard verification reports

## Protected files/folders this chat must not touch

- Phone shell / PC shell core unless instructed by JOB-01
- Shared RLS/Career Bridge core unless instructed by JOB-02
- RLS original files
- BeamBook page logic
- Import/Export page logic
- Classics page logic
- Tow/Recovery/Dispatch app logic
- QA shared test format
- Any startup-loaded career module

## Hard rules accepted

- No startup Scrap Yard career module.
- No `redfoxScrapYardDirect.lua` rebuild.
- No fake hand-rolled money/storage/garage if stock/RLS functions are available.
- No map-load work.
- No parking spot generation.
- No yard sell prop runtime until JOB-04 web-only and JOB-02 bridge are stable.
- No final ZIP until baseline is inspected and verification plan is written.

## Verification plan before any build

1. Confirm only one FoxNet/Web Ecosystem ZIP is intended for test.
2. Confirm Scrap Yard phone path and PC path.
3. Confirm shared bridge messages from JOB-02.
4. Confirm buy uses stock/RLS purchase flow.
5. Confirm sell lists owned career inventory vehicles.
6. Confirm sell calls stock/RLS inventory sell function if safely available.
7. Confirm no old Direct Scrap Yard career module exists.
8. Include TXT and HTML verification reports in any package.

## Dependency notes

This chat depends on:

- JOB-02 for the approved shared RLS/Career Bridge contract.
- JOB-01 for phone/PC app/page loading paths.
- JOB-03 for app manifest/store registration if the Store is ready.

If another chat already has JOB-04, David should assign one of us away from Scrap Yard to avoid duplicate work.

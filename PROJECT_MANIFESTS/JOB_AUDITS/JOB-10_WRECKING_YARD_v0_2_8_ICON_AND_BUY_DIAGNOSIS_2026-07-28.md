# JOB-10 — Wrecking Yard v0.2.8 Icon and Buy Diagnosis

**Date:** 2026-07-28  
**Owner:** David / Captain  
**JOB-10:** Visual Design / Real Website Polish  
**Related owner jobs:** JOB-01 Phone Platform Core, JOB-04 Wrecking Yard  
**Status:** STATIC DIAGNOSIS FROM OWNER-UPLOADED v0.2.8 ZIP — NO GAMEPLAY MOD EDITED

## User-reported runtime result

David tested:

```text
zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_1051PT_v0_2_8_FILTERED_REDFOX_ONLINE_BUY_NO_FLASH_FROM_v0_2_7.zip
```

Observed:

- Wrecking Yard vehicles now display on the correct page.
- Buy Online does not complete/open correctly.
- The FoxNet Browser phone icon still shows the old fox-head tile rather than David's circular RedFox wolf logo.

## Icon diagnosis

The phone app registration inside:

```text
ui/ui-vue/dist/index.js
```

still declares:

```text
iconTile: `foxnet-browser.svg`
```

The exact active tile path in the ZIP is:

```text
ui/entrypoints/main/tiles/foxnet-browser.svg
```

That file still contains the old simplified fox-head SVG. Therefore the screenshot matches the contents of the current ZIP.

A JOB-10 visual asset pack was prepared from David's uploaded circular RedFox wolf logo:

```text
RedFox_FoxNet_Browser_Icon_Asset_Pack_v1_0.zip
SHA-256: 18b7d22fb61816e87c0adb3e62b1cba55abbd1a1a9193516506f7df03cb9cd9f
```

It contains a ready drop-in:

```text
foxnet-browser.svg
```

and transparent PNG sizes 128, 256, 512 and 1024.

### Required owner-job application

JOB-01 or JOB-04 should replace only:

```text
ui/entrypoints/main/tiles/foxnet-browser.svg
```

in the exact active phone ZIP, then record the changed file, ZIP size and hash.

A full BeamNG restart is required. Older FoxNet/Web Ecosystem ZIPs must be disabled because another ZIP containing the same tile or `ui/ui-vue/dist/index.js` can win the virtual path and keep showing the old icon.

JOB-10 did not edit or repackage the Wrecking Yard gameplay ZIP in this audit.

## Buy-path static diagnosis

The v0.2.8 Wrecking Yard page does successfully build and display temporary clones from BeamBook-backed native shop data.

In:

```text
sites/scrap_yard/assets/js/scrap.js
ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js
```

it:

1. reads native shop vehicles;
2. selects BeamBook seller entries;
3. deep-copies eligible entries;
4. changes seller identity to `redfoxWreckingYard`;
5. assigns synthetic shop IDs beginning at `5000001`;
6. returns those clones to the web page for display;
7. sends the selected synthetic ID through `RedFoxScrapYardOpenPurchaseMenu`.

The important code behavior is equivalent to:

```text
c.shopId = 5000000 + cloneIndex
...
openPurchaseMenu("instant", shopId)
```

The displayed cars therefore prove the web-page generation and image/data side works, but do not prove the synthetic shop IDs are registered in the real native vehicle-shopping lookup used by `openPurchaseMenu`.

### Most likely failure

The clones are inserted into the Lua table returned by `getVehiclesInShop()` and into the JSON result returned to the browser, but there is no separate registration/update of the native purchase system's internal ID lookup, seller map, inventory source or purchase record for those synthetic IDs.

This explains the exact runtime symptom:

```text
Listings display correctly
Buy button cannot complete the native purchase path
```

The v0.2.8 package itself labels runtime purchase as unproven.

## Correct JOB-04 repair choices

JOB-04 must choose and prove one real backend design rather than only creating display clones.

### Option A — real native shop registration

Create Wrecking Yard entries through the same native/RLS vehicle-shopping API that registers a complete purchasable shop record, including every lookup/index expected by `openPurchaseMenu`.

This is preferred if the native module exposes a supported registration/add-listing path.

### Option B — controlled temporary native entry

Before opening the purchase menu:

1. create/register one complete temporary Wrecking Yard shop entry;
2. confirm the native module can look it up by ID;
3. open the stock purchase menu;
4. let the real stock/RLS transaction handle money, ownership, delivery, garage/storage and save state;
5. remove only stale temporary entries after a safe lifecycle point.

### Option C — dedicated Wrecking Yard purchase operation

Use a dedicated JOB-04/JOB-02 operation that performs the complete real Career transaction with explicit success/failure results.

This must not be a fake browser purchase or vehicle spawn. It must prove:

```text
money deducted
vehicle ownership created
vehicle delivered/stored
inventory updated
save persistence
rollback/error handling
```

### Unsafe shortcut to avoid

Do not merely open the original BeamBook shop ID while showing a lower Wrecking Yard price unless the actual native record used for purchase is also safely changed and restored. Otherwise the player may be charged the wrong amount or purchase the wrong seller record.

## Required next runtime evidence

JOB-04 should capture:

- whether clicking Buy Online produces a toast/result;
- exact `RedFoxScrapYardPurchaseMenuResult` payload;
- beamng.log lines around `openPurchaseMenu`;
- whether synthetic shop ID exists in native vehicle-shopping state immediately before the call;
- whether a stock purchase page opens but confirmation fails, or no page opens at all;
- money, ownership, delivery, garage/storage and persistence after one cheap test purchase.

## Scope and ownership

- JOB-10 owns the wolf browser icon asset and website presentation.
- JOB-01 owns phone app registration/core tile integration.
- JOB-04 owns Wrecking Yard purchasing behavior.
- JOB-02 owns shared Career/RLS operations if a new bridge action is required.

No existing working Tow, Wrecking Yard, BeamBook, Career, RLS, phone shell or PC code was changed by JOB-10 for this diagnosis.

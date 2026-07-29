# JOB-04 — RedFox Wrecking Yard v0.2.9

## Runtime closure for v0.2.8

Owner test result: **PARTIAL PASS / REJECTED AS FINAL YARD IMPLEMENTATION**.

What worked:
- Large BeamBook-derived inventory loaded.
- RedFox Wrecking Yard page could display and click cars.
- The online native purchase page could be requested.
- PC integration improved enough to display and click listings.

What failed:
- Every listing displayed at `$500` because a zero `finalValue` was accepted before the real positive price fields.
- Vehicles were too new and too clean to resemble a Wrecking Yard.
- Refresh rebuilt from the same BeamBook pool instead of cycling the underlying cars.
- Negotiation was explicitly disabled.
- Synthetic temporary shop IDs could open the purchase UI but were not reliable through final native checkout, especially on PC.

Decision:
- Preserve the online-buy bridge and PC/phone relay research.
- Remove synthetic clone IDs and synthetic price replacement.
- Use BeamBook's original native shop IDs and native records for checkout.

## Source

- Base ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_1051PT_v0_2_8_FILTERED_REDFOX_ONLINE_BUY_NO_FLASH_FROM_v0_2_7.zip`
- Base SHA-256: `32afdc475a599f1b3b9e8c5c3ae6623b1010f46dbbdd3424ddf88e0ce470b7cf`

## Output

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_1936PT_v0_2_9_NATIVE_IDS_REAL_PRICES_CYCLE_NEGOTIATION_FROM_v0_2_8.zip`
- SHA-256: `246cf5ca47274ebc8686eab6b5cdd6edbfd7247dd7c817e6ca44e8890958beb2`
- Size: `25,396,962 bytes`
- ZIP entries: `1,423`
- ZIP integrity: **PASS**
- Runtime status: **UNPROVEN**

## Implementation

### Native listing identity

v0.2.9 no longer creates synthetic `5000000 + index` shop IDs.

For every displayed Wrecking Yard card:
- the page may deep-copy the record for presentation;
- the original BeamBook/RLS `shopId` is preserved;
- Buy / Negotiate Online opens the native checkout using that original ID;
- no browser-only native listing is inserted.

This is intended to keep the same native record available through the full phone and PC transaction.

### Real prices

Price reading now ignores zero and invalid values and selects the first positive value from:

1. `Value`
2. `askingPrice`
3. `price`
4. `marketValue`
5. `baseValue`
6. `value`
7. `finalValue`

v0.2.9 does not replace the native asking price with an artificial `$500` floor.

### Yard selection

Default visible count: `80`.

Default adjustable mix:
- 80% salvage candidates
- 10% random used
- 5% better vehicles with issues
- 5% work, tow, heavy, trailer, and special vehicles

Default selection limits:

General salvage:
- minimum price: `$900`
- maximum asking price: `$50,000`
- minimum mileage: `90,000`
- maximum year: `2016`

Random used:
- minimum mileage: `45,000`
- maximum year: `2020`

Better vehicles with issues:
- maximum asking price: `$150,000`
- minimum mileage: `130,000`
- maximum year: `2019`

Work / tow / heavy / special:
- maximum asking price: `$175,000`
- minimum mileage: `30,000`
- minimum preserved work listings: `6`

These are selection and labeling rules. This build does not yet physically remove parts or apply Barn Finder structural/mechanical damage.

### Negotiation

- v0.2.9 no longer writes `negotiationPossible = false`.
- The original native negotiation capability and seller data are preserved.
- Cards say `Buy / Negotiate Online` when the source listing supports negotiation.

### Actual inventory cycling

`Cycle to New Yard Inventory` now:
- targets the active BeamBook entries;
- marks their live generation time expired;
- calls BeamBook's normal generation/sync hook;
- rebuilds the yard selection from the new underlying pool.

Initial page load does not force expiration.

### Online purchase bridge preserved

The page sends the selected original `shopId` through the existing phone/PC IceFox message relay.

The shell opens:

```lua
career_modules_vehicleShopping.openPurchaseMenu('instant', shopId)
```

Native RLS remains responsible for money, delivery, ownership, inventory, and storage.

No manual money subtraction, spawning, ownership insertion, or storage insertion was added.

## Files changed

- `info.json`
- `sites/scrap_yard/index.html`
- `sites/scrap_yard/assets/js/scrap.js`
- `sites/scrap_yard/assets/config/wrecking_yard_mix.json`
- `ui/modModules/redfoxCareerWeb/sites/scrap_yard/index.html`
- `ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/js/scrap.js`
- `ui/modModules/redfoxCareerWeb/sites/scrap_yard/assets/config/wrecking_yard_mix.json`
- embedded verification and changed-file records
- embedded native-ID architecture notes
- preserved v0.2.8 online-buy bridge findings for Auctions and Direct Buy reuse

## Protected behavior

- IceFox welcome page remains pure UI and does not request shop data.
- No global startup shop refresh.
- No Joe's Junk storefront popup.
- No manual purchase implementation.
- No selling/scrapping implementation yet.
- No auction implementation yet.
- No shared Vue redesign.

## Static verification

PASS:
- packaged ZIP integrity
- packaged SHA and size verification
- mirrored JS identical
- mirrored HTML identical
- mirrored config identical
- JavaScript syntax with Node
- JSON parsing
- changed local HTML references
- no synthetic `5000000` IDs
- no forced `negotiationPossible = false`
- original native shop IDs preserved
- positive-price selection logic present
- initial load does not force BeamBook expiration
- refresh path does force expiration and regeneration
- `Buy / Negotiate Online` present
- embedded Lua expressions balanced

Standalone BeamNG runtime remains required.

## Required runtime test

1. Remove or disable every older JOB-04 test ZIP.
2. Keep BeamBook and the normal RLS career setup enabled.
3. Install v0.2.9.
4. Fully restart BeamNG.
5. Confirm IceFox welcome still opens without vehicle-loading lag.
6. Open Wrecking Yard and check:
   - prices vary and are not all `$500`;
   - most general listings are older, higher-mileage, and lower-priced;
   - tow/work/heavy/special vehicles are still represented;
   - cards show realistic source prices.
7. Open an eligible listing with `Buy / Negotiate Online` and confirm negotiation appears where supported.
8. Complete one inexpensive purchase on phone and verify money, delivery, ownership, inventory, and storage.
9. Repeat one purchase test from PC.
10. Click `Cycle to New Yard Inventory` and confirm the actual vehicles change rather than only reordering the same pool.

## Known limitation and next step

This version creates a more believable yard selection through real age, mileage, price, and category filtering, but it does not yet physically damage cars, remove parts, add rust, or apply Barn Finder fault profiles.

If native-ID checkout and cycling pass, the next stage is physical/mechanical salvage condition generation, followed by selling and scrapping.

## GitHub connector incident

During this checkpoint, issue #38 was accidentally created by an incorrect tool invocation and immediately closed as `not planned`. No project work is tracked there; issue #30 remains the active JOB-04 ledger.

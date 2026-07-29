# JOB-04 — RedFox Wrecking Yard v0.3.0

## Runtime closure for v0.2.9

Owner runtime result: **FAILED**.

Observed:
- all visible vehicle prices still showed `$500`
- inventory appeared unchanged
- expected v0.2.9 behavior was not visibly present

## Mandatory pre-edit verification

Exact delivered v0.2.9 archive:

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_1936PT_v0_2_9_NATIVE_IDS_REAL_PRICES_CYCLE_NEGOTIATION_FROM_v0_2_8.zip`
- SHA-256: `246cf5ca47274ebc8686eab6b5cdd6edbfd7247dd7c817e6ca44e8890958beb2`
- Size: `25,396,962 bytes`
- Entries: `1,423`
- ZIP extraction: PASS
- exactly two active Scrap Yard JavaScript copies: PASS
- mirrors byte-identical: PASS
- no active v0.2.8 synthetic `5,000,000`-series generator: PASS

Contradiction found:

- v0.2.9 source configured a `$900` minimum, not `$500`
- v0.2.9 selected positive price fields in this order: `Value`, `askingPrice`, `price`, `marketValue`, `baseValue`, `value`, `finalValue`
- BeamBook itself writes `entry.Value = askingPrice`
- BeamBook also writes `entry.marketValue = marketValue`

Because runtime still showed the old all-$500 behavior, stale or overridden browser assets were treated as a confirmed architecture risk.

## v0.3.0 output

- ZIP: `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-28_2156PT_v0_3_0_CACHE_BUST_NATIVE_PRICES_SELECTION_FROM_v0_2_9.zip`
- SHA-256: `413844fa779a221e8488d0ad26d6c635087e4b0232ba6842fa6aa6e36d633e97`
- Size: `25,409,347 bytes`
- Entries: `1,437`
- Runtime status: **UNPROVEN**

## Exact changes

- added versioned main script `scrap_v030.js`
- added versioned config `wrecking_yard_mix_v030.json`
- added cache-busting query strings
- added no-cache HTML metadata
- added visible `JOB-04 v0.3.0 ACTIVE` badge
- added expandable native-price diagnostics
- retained legacy `scrap.js` only as a compatibility loader
- returned to the exact BeamBook `getShoppingData()` path that showed varied prices in v0.2.7
- preserved original BeamBook shop IDs
- preserved original positive native asking prices
- removed every `$500` fallback from active v0.3.0 listing code
- changed cycling to a different local Wrecking Yard subset from the 100–200 BeamBook cars
- kept native online purchase bridge and negotiation availability
- did not alter BeamBook's own marketplace source list
- did not touch global Vue bundle or IceFox purchase bridge

## Price source order

1. `Value`
2. `askingPrice`
3. `price`
4. `marketValue`
5. `baseValue`
6. `value`
7. `finalValue`

Only positive numeric values are accepted. There is no `$500` fallback.

## Verification before edit

PASS:
- base archive hash and size
- exact active file count
- active mirror equality
- old synthetic-ID search
- BeamBook source inspection
- protected-file hash capture

## Verification after edit

PASS:
- Node syntax for standalone and mirrored `scrap_v030.js`
- Node syntax for compatibility loaders
- JSON parse for both versioned configs and `info.json`
- HTML mirror equality
- main JavaScript mirror equality
- loader mirror equality
- config mirror equality
- local HTML reference validation
- expected changed-file scope only
- protected global Vue hash unchanged
- protected IceFox purchase bridge hashes unchanged

## Logic regression tests

PASS:
- `Value=31400`, `finalValue=0` selects `$31,400`
- `Value=0`, `askingPrice=177800`, `finalValue=0` selects `$177,800`
- all-zero price fields return zero rather than `$500`
- cycle 1 and cycle 2 produce different shop-ID selections
- selected count never exceeds configured display count
- no selected regression vehicle resolves to `$500`

A test caught one issue before packaging: the initial quota logic selected 42 cars when configured for 40. The selection cap was fixed and the regression test was rerun successfully.

## Verification after final ZIP creation

PASS:
- ZIP integrity
- fresh extraction to a new directory
- Node syntax from extracted ZIP
- mirrored HTML from extracted ZIP
- mirrored main JavaScript from extracted ZIP
- mirrored loader from extracted ZIP
- mirrored config from extracted ZIP
- visible build badge marker
- versioned asset reference
- versioned config reference
- no active `$500` fallback marker
- no active synthetic `5,000,000` IDs
- no duplicate ZIP paths
- required verification/report entries present

One first post-ZIP command stopped because its grep expected the exact literal string `JOB-04 v0.3.0 ACTIVE` inside JavaScript, while the code constructs it as `BUILD + ' ACTIVE'`. ZIP integrity had already passed. The check was corrected to verify the actual construction and all post-ZIP tests were rerun successfully.

## Protected files unchanged

- `ui/ui-vue/dist/index.js`
- `ui/ui-vue/dist/index.css`
- `assets/js/icefox_front.js`
- `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js`

## Required runtime test

1. Remove or disable every older JOB-04 ZIP.
2. Keep BeamBook and RLS enabled.
3. Install exact v0.3.0 ZIP.
4. Fully restart BeamNG.
5. Confirm visible `JOB-04 v0.3.0 ACTIVE` badge before judging prices.
6. Confirm prices vary.
7. Open Build and native-price diagnostics and confirm positive `Value` or other selected native fields.
8. Press `Cycle Yard Selection` and confirm visible cars change.
9. Open `Buy / Negotiate Online`.
10. Complete one phone purchase and one PC purchase.
11. Verify money, delivery, ownership, inventory, and storage.

## Known limitation

v0.3.0 filters by real year, mileage, price, and work/tow/special classification. It does not fabricate rust, missing parts, physical damage, or mechanical failures. Those remain deferred until native purchase completion is proven.

## Connector incident

GitHub issue #39 was accidentally created during checkpoint logging and immediately closed as not planned. JOB-04 work remains tracked only in issue #30.

# JOB-04 v0.3.4 Designated Single-Package Base Audit

**Date:** 2026-07-31

**Designated base:** `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1430PT_v0_3_4_NATIVE_PURCHASE_FORCED_GARAGE_DELIVERY_FROM_v0_3_3.zip`

**SHA-256:** `e27c1939aa17e839a0fcab64de3fc7aa81459df0701697aa5bd2d7666a3e0e75`

**Audit mode:** Read-only. No mod source was edited or repackaged.

## Archive facts

- 1,047 files
- 25,364,755 compressed bytes
- 48,403,159 uncompressed bytes
- ZIP integrity passed
- No duplicate or unsafe paths
- `sites/**`: 371 files
- `ui/modModules/redfoxCareerWeb/sites/**`: 371 files
- Both site trees are byte-for-byte identical for all 371 relative paths
- Reports/docs/history: 195 files and 22,686,423 uncompressed bytes
- Shared main UI bundle: 2 files and 5,716,025 uncompressed bytes

## Working/current features preserved

- Styled desktop and phone IceFox welcome pages
- Phone layout registration and Vue route for `redfox-browser`
- v0.3.2 junk-focused Joe's Junk / Undesireables selection
- Native listing prices, mileage, shop IDs and negotiation
- v0.3.3 owned-vehicle dashboard
- Native vehicle sale request path
- Whole-vehicle scrap
- Strip-and-scrap shell with verified part staging before removal
- Returned-parts storage
- Used-part sale
- Catalytic-converter scrap
- Persistent request IDs and transaction states
- v0.3.4 native purchase adapter forcing `makeDelivery=true`
- No JOB-04 continuous Lua `onUpdate` loop found

## Mismatches against the current owner goal

1. **Phone icon is not complete.** The custom wolf tile exists and the compiled manifest references `foxnet-browser.svg`, but runtime still showed the old icon. Cache/load-order resolution remains open.
2. **Vehicle filtering is too restrictive.** The current owner rule allows any type of vehicle when old and beat-up, but v0.3.4 hard-excludes dump trucks, mining equipment, forklifts, cranes, aircraft, boats, fire trucks and ambulances regardless of condition.
3. **Real bad engine/transmission generation is absent.** Selection is based on seller, name, year, mileage and price. JOB-04 does not inject actual mechanical failures or missing parts.
4. **Thumbnail fallback is incomplete.** Many model SVGs exist but the active map only uses a few and defaults to the pickup image, causing Barstow/Pigeon/etc. to show the wrong generic image.
5. **Welcome routes open obsolete bundled Tow/Auction copies.** Current standalone JOB-09 and JOB-13 use different paths, so the welcome page is not opening those current systems.
6. **Large inactive/history payload remains.** Old reports, MHTML captures, old Wrecking Yard versions and unrelated sites remain mounted.
7. **Shared bridge contains unrelated legacy logic.** `redfoxCareerWeb.lua` still includes old/manual auction, insurance, quick-scrap and direct-purchase experiments not required by the current JOB-04 page.
8. **Two full site mirrors remain.** The prior split failure changed routes/cache and removed a mirror simultaneously, so it did not prove whether both complete trees are permanently required. Test one variable at a time.

## Runtime status

- Junk/high-mileage selection: owner pass
- Native varied prices/shop IDs: owner pass
- v0.3.4 garage-delivery purchase fix: code present, owner runtime unproven
- Sell/scrap/strip/returned parts/cats: code present, owner runtime unproven
- Styled welcome/Wrecking Yard: present in source and worked before the failed split
- Phone icon: failed runtime goal
- Performance cleanup: not done

## Recommended decision order

1. Freeze this exact hash as the rollback/source baseline.
2. Keep one ZIP containing the welcome page and Wrecking Yard.
3. Resolve the phone icon runtime path/cache separately.
4. Preserve both Wrecking Yard mirrors during the first cleanup build.
5. Remove only indisputable records/history first; do not change routes or runtime code in that same pass.
6. Runtime-test Career load and styling after records-only cleanup.
7. Map the welcome Tow/Auction buttons to the real standalone entry points in a separate pass.
8. Handle vehicle-type eligibility, thumbnails and real condition/damage in separate narrow passes.
9. Prove buying before destructive sale/scrap tests.

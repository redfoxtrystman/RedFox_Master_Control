# JOB-04 — Scrap Yard / Wrecking Yard

## v0.1.7 — Grey Screen Only Patch

Date/time: 2026-07-24 1725PT

Base ZIP:

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_7_ALL_IN_ONE_PC_PHONE_GARAGE_SELL_FIX.zip
```

Output ZIP:

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-24_1725PT_v0_1_7_FIX_GREY_SCREEN_ONLY_FROM_v0_10_3_7.zip
```

## User direction

David chose the v0.10.3.7 candidate as the base because it can buy cars, but it is very slow and has the grey loading/title-screen issue. David explicitly requested the first new patch fix the grey screen and only that.

## Changed files

Only the core UI bundle pair was changed:

```text
ui/ui-vue/dist/index.js
ui/ui-vue/dist/index.css
```

## Reason

The base candidate contains a custom `ui/ui-vue/dist/index.js` that is in the bad UI family associated with the grey loading/title screen. The patch replaced that file with the RLS 2.6.6-compatible RedFox phone-browser UI bundle from the prior current-RLS buy-proven line, and added its matching CSS file.

Base index.js hash:

```text
c7436c9f4ad696dba8ddc6d4b3b96a3ef810103d5dc2398de1db157c45110173
```

Replacement index.js hash:

```text
7febff530893d6b54505554649cc2e2cf7b2c4f41cc881b7ebda04e05f18cf90
```

Replacement index.css hash:

```text
957da302d3e509968ccd6cd3dea64637779ec0df745f3c1588f890aefb8d6b00
```

## Verification

Static/package checks performed:

```text
Source ZIP integrity: PASS
UI replacement source ZIP integrity: PASS
Output ZIP integrity: PASS
Output entry count: 1386
Output index.js matches replacement: PASS
Output index.css matches replacement: PASS
JavaScript syntax checks: PASS
No redfoxScrapYardDirect startup module: PASS
```

Final package SHA256:

```text
51d8e05ea2cd17e118e3b66b00b8d4302c1addb820c7204faa2a557ba68d534d
```

## Explicitly not fixed in v0.1.7

```text
Lag / slow loading
Selling cars
Scrap / strip / remove-all-parts dev test
PC access cleanup
Scrap Yard page behavior
Legacy scrapyard bridge cleanup
```

## Runtime status

Runtime is unproven until David tests this exact ZIP in BeamNG. This patch should be treated as a grey-screen-only candidate, not a final working build.

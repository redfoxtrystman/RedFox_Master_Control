# JOB-04 v0.3.5 Archive Identity and Static Verification

Date: 2026-07-30 PT

## Reason for verification

A later JOB-13 review reported that the supplied Wrecking Yard archive was still the full 1,047-file v0.3.4 package. That statement is correct for the specific archive it inspected:

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1430PT_v0_3_4_NATIVE_PURCHASE_FORCED_GARAGE_DELIVERY_FROM_v0_3_3.zip`

SHA-256:

`e27c1939aa17e839a0fcab64de3fc7aa81459df0701697aa5bd2d7666a3e0e75`

That archive is the original pre-split v0.3.4 input and must not be installed beside the split Browser Core and slim JOB-04 module.

## Correct split archives

### Browser Core v0.1.0

File:

`RedFox_FoxNet_Browser_Core_v0_1_0_COMPAT_TEST_FROM_JOB04_v0_3_4.zip`

SHA-256:

`d731f364328b1f17761117793331be85c0f6e1f7577bfcdff1eb609f57fa8fc3`

Verified contents:

- 51 files
- 1,230,641 compressed bytes inside ZIP
- 5,902,462 uncompressed bytes
- no duplicate paths
- ZIP integrity pass

### JOB-04 v0.3.5 slim module

File:

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1902PT_v0_3_5_SLIM_MODULE_REQUIRES_BROWSER_CORE_FROM_v0_3_4.zip`

SHA-256:

`358f663e2fd2ce35f8b720c1d07f5db57393135247efc6fd6cb40215e1238bd5`

Verified contents:

- 34 files
- 74 KB outer file size
- 30 retained JOB-04 files are byte-for-byte identical to their v0.3.4 versions
- new `index_v035.html`
- new `scrap_v035.js`
- updated `info.json`
- no auction site
- no tow/recovery site
- no shared main UI bundle
- no phone layout
- no browser shell
- no historical reports or MHTML captures
- no duplicate paths
- ZIP integrity pass

## Static integration verification

The Browser Core points both PC and phone browser routes to:

`sites/scrap_yard/index_v035.html`

The slim module provides:

`ui/modModules/redfoxCareerWeb/sites/scrap_yard/index_v035.html`

The merged Browser Core + slim module filesystem passed:

- JavaScript syntax checks with Node
- Lua syntax checks with Lua 5.3 compiler
- JSON parse checks
- HTML local-reference checks with zero missing local assets
- route-to-module target check
- ZIP integrity checks

The v0.3.5 page and JavaScript are the v0.3.4 working files with only the version/cache identifiers changed for the split. The native purchase adapter, selling/scrap Lua modules, junk filtering, configs, and images remain present.

## Important limitation

These checks prove archive identity, packaging, syntax, and static dependency completeness. They do not prove BeamNG runtime compatibility. Browser Core + JOB-04 v0.3.5 still requires the ordered runtime test. Do not describe v0.3.5 as runtime-passed until Career loads and the page/purchase/selling paths are tested in game.

## Required install pair

Install both:

1. `RedFox_FoxNet_Browser_Core_v0_1_0_COMPAT_TEST_FROM_JOB04_v0_3_4.zip`
2. `zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-07-30_1902PT_v0_3_5_SLIM_MODULE_REQUIRES_BROWSER_CORE_FROM_v0_3_4.zip`

Do not install the original v0.3.4 archive at the same time.

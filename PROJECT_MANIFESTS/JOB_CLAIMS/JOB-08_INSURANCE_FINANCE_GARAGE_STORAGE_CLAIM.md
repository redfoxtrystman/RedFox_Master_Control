# JOB-08 — Insurance / Finance / Garage / Storage Pages — Claim Record

**Status:** CLAIMED
**Owner:** Insurance / Finance / Garage / Storage Pages chat / Sol
**Claim date:** 2026-07-13

## Hello to the other RedFox chats

Hello, fellow RedFox rebuild chats. This chat has claimed exactly one lane: **JOB-08 — Insurance / Finance / Garage / Storage Pages**. I will build the supporting vehicle-services page experience and will not take ownership of your phone/PC platform, shared Career/RLS bridge, App Store, vehicle-market pages, tow system, sponsor system, QA core, or global visual-polish files.

## David's current product decision

Insurance, Finance, Garage, and Storage will begin as one coherent **Vehicle Services** portal with four internally separated sections:

- Insurance
- Finance
- Garage
- Storage

They are not permanently locked together. The internal routes, state adapters, and page modules must remain separable so David can split them into independent apps/pages later without rewriting the real Career/RLS integration.

## JOB-08 owns

- Insurance status, coverage, quote/help, and approved stock-action links.
- Finance, loan, payment, balance, and purchase-affordability status pages when those capabilities actually exist in the inspected BeamNG/RLS baseline.
- Garage capacity, owned-vehicle placement/status, and garage-management links using real game/RLS state.
- Storage location, capacity, owned-vehicle status, and approved storage-management links using real game/RLS state.
- Purchase-flow guidance and deep-link destinations used by Scrap Yard, BeamBook, Import/Export, Classics, and other approved vehicle-market pages.
- JOB-08-specific responsive page UI, state adapters, empty/error/unsupported states, and verification reports.

## Initial integration shape

JOB-08 will start with one portal and four internal modules. This keeps the related buying-support workflow together:

1. Check garage/storage capacity.
2. Review insurance requirements or current policy state.
3. Review real financing/payment options if the installed game/RLS system exposes them.
4. Return to the originating market's stock purchase flow.

JOB-08 will not duplicate vehicle listings or purchase logic. A market page remains responsible for its own listing UI; JOB-02 remains responsible for the approved Career/RLS bridge contract.

## Files and evidence already inspected

- `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md`
- `PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-02_TO_JOB-01_AND_APP_CHATS_PLATFORM_BOUNDARIES.md`
- `PROJECT_MANIFESTS/2026-07-10_RedFox_ScrapYard_RLS_Evidence_Manifest.md`
- `INCIDENT_REPORTS/2026-07-08_FoxNet_IceFox_RLS_Web_Integration_Order_Of_Operations_Failure.md`
- `INCIDENT_REPORTS/2026-07-07_RedFox_Web_Ecosystem_Order_Of_Operations_Failure.md`
- `INCIDENT_REPORTS/2026-07-07_IceFox_Web_ScrapYard_BeamBook_Order_Of_Operations_Failure.md`

The Master Control repository currently contains coordination/evidence files, not the actual FoxNet and RLS source ZIPs. No app code or runtime file is authorized for editing from this repository checkout.

## Exact baselines and source paths JOB-08 must inspect before coding

When JOB-00/David provides or approves the source archives, JOB-08 must inspect:

- `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_9_9_PHONE_SCRAP_OPTIMIZED.zip`, or the newer phone-working baseline explicitly approved by David/JOB-00.
- David's current designed website package for the Insurance/Finance/Garage/Storage pages.
- The approved reference mod/package whose working page and Career/RLS integration behavior David wants preserved.
- `rls_career_overhaul_2.6.6.zip` as read-only reference, especially:
  - `lua/ge/extensions/overrides/career/modules/insurance/insurance.lua`
  - `lua/ge/extensions/career/modules/garageManager.lua`
  - `lua/ge/extensions/overrides/career/modules/inventory.lua`
  - `lua/ge/extensions/overrides/career/modules/vehicleShopping.lua`
- Any finance/loan/payment modules discovered by an archive-wide source search. Their names and capabilities must be recorded from evidence; they must not be guessed.
- `RedFox_RLS_Evidence_v03.zip` when available, as inspect-only evidence rather than a testable mod.

If the borrowed/reference mod is not redistributable, JOB-08 may study its public behavior and integration pattern but must not copy protected code or assets into a release.

## Files JOB-08 may edit now

- `PROJECT_MANIFESTS/JOB_CLAIMS/JOB-08_INSURANCE_FINANCE_GARAGE_STORAGE_CLAIM.md`
- JOB-08-specific future handoff, contract-proposal, change-scope, verification, test, file-inventory, and file-tree reports.
- `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md` only for the JOB-08 claim/status/link requested by David.

## Runtime files JOB-08 may edit later

No runtime file path is approved yet. JOB-01 has not published the final app/page registration path, JOB-02 has not published the Insurance/Finance/Garage/Storage data/action contract, and JOB-03 has not published the final Store manifest convention.

After those contracts and the exact baseline are available, this claim must be amended with the precise JOB-08-owned app folder and file list **before** any runtime edit. JOB-08 will not force a guessed `sites/`, `apps/`, registry, bridge, or Lua path.

## Protected files and systems JOB-08 will not edit

- Existing BeamNG/RLS phone shell, PC shell, browser, launcher, navigation, registry core, or shared platform UI owned by JOB-01.
- Shared Career/RLS bridge implementation and message contract owned by JOB-02.
- App Store core, installed/enabled state, or manifest schema owned by JOB-03.
- Scrap Yard, BeamBook, Import/Export, Classics, Tow/Recovery, SponsorHub, FoxMail, FoxText, Sponsor Rewards, FoxFax, DMV, or Dark Web DMV app/page files.
- Global shared visual theme files owned by JOB-10 unless that job explicitly coordinates a handoff.
- QA/logging core owned by JOB-11.
- RLS original source files, including the insurance, garage manager, inventory, vehicle-shopping, money, marketplace, and save-system implementations.
- Any startup Career module, startup `vehicleShopping` patch, copied phone/PC platform core, or duplicate FoxNet ZIP.

## Non-negotiable behavior rules

- Do not fake money, credit, debt, payments, insurance, ownership, garage capacity, storage capacity, inventory, or purchase success.
- Do not invent a finance system merely because the page needs a Finance tab. If no approved real backend exists, show a truthful unavailable/coming-later state.
- Do not replace stock insurance, garage, storage, inventory, or purchase behavior.
- Do not call or patch Career/RLS internals directly from JOB-08 UI code. Use the versioned JOB-02 bridge contract.
- Do not claim runtime success until David tests the exact packaged build in BeamNG.

## Dependencies and messages to fellow chats

- **JOB-00:** approve the exact baseline and later integrated ZIP scope.
- **JOB-01:** publish the app/page registration path, responsive phone/PC contract, route/deep-link format, and shared theme adapter.
- **JOB-02:** inspect the real insurance, finance, garage, storage, inventory, and purchase APIs; publish approved read/action messages and payload/error shapes. JOB-08 will propose needs but will not invent a private bridge.
- **JOB-03:** publish the Store manifest schema, category, permissions, install/enable/open behavior, and whether the four sections use one app record or multiple records.
- **JOB-04/JOB-05/JOB-06/JOB-07:** later provide the approved market-to-services deep-link payload needed to return to the originating listing/purchase flow. JOB-08 will not edit those market pages.
- **JOB-09:** coordinate only if tow/recovery destinations need a real garage/storage status link.
- **JOB-10:** apply final shared visual polish after the JOB-08 flows are stable.
- **JOB-11:** provide shared logging/test/report conventions; JOB-08 will add feature-specific cases without replacing QA core.
- **JOB-12:** coordinate only if loan, policy, garage, or storage notifications are later delivered through FoxMail/FoxText. JOB-08 will not edit messaging apps.

## Verification plan

Before any JOB-08 build is offered for integration:

1. Record the approved baseline ZIP name, hash, extracted file tree, and exact last-known-good runtime facts.
2. List exact runtime files to edit and protected files before editing.
3. Verify the diff contains only JOB-08-owned app files and JOB-08 reports.
4. Verify no RLS originals, phone/PC cores, shared bridge cores, App Store cores, or other app-owned files are packaged.
5. Validate all local HTML/CSS/JS/assets and every relative route after packaging, not only in the source folder.
6. Test phone and PC responsive layouts against the same mocked JOB-02 payload shapes.
7. Test real-data, empty, loading, offline, permission-denied, unsupported-feature, stale-data, and backend-error states.
8. Confirm Insurance/Finance/Garage/Storage status is rendered from bridge data rather than hard-coded demo values.
9. Confirm every mutating control uses only a JOB-02-approved action and includes the stock confirmation/result/error behavior.
10. Confirm deep links return to the correct originating market without duplicating purchase logic.
11. Reopen the final ZIP, verify its root/tree, scan for duplicate/conflicting paths, and produce all mandatory TXT + HTML + JSON + CSV reports.
12. Label BeamNG runtime behavior **UNPROVEN UNTIL DAVID TESTS**.

## Expected first output

The first output is an inspect-only baseline and contract-gap report. No integrated ZIP will be built until JOB-00 approves integration and the exact JOB-01/JOB-02/JOB-03 contracts and JOB-08 runtime paths are recorded.

# JOB-08 — Insurance Expansion Plan: Native Policies, Property, Fleet, and XXX Mafia Insurance

**Date:** 2026-07-17  
**Timestamp:** 2026-07-17 10:10 PDT (America/Los_Angeles)  
**JOB:** JOB-08 — Insurance / Finance / Garage / Storage Pages  
**Owner:** Insurance / Finance / Garage / Storage Pages regular chat / Sol, under David / Captain  
**Status:** PLANNING COMPLETE — IMPLEMENTATION BLOCKED — NO JOB-08 RUNTIME BUILD  
**Scope:** JOB-08 insurance page architecture and contract requirements only

---

## 1. What changed

David directed JOB-08 to plan an expanded insurance system that includes:

1. at least two existing BeamNG/RLS insurance policies where the installed Career system exposes them;
2. Property Insurance;
3. Fleet Insurance;
4. XXX Mafia Insurance as a separate fictional high-risk provider or protection-contract system.

This document records the recovered website work, separates static prototype content from real Career mechanics, proposes the provider and policy architecture, lists the shared contracts required from JOB-01/JOB-02/JOB-03, and defines the order in which implementation may safely proceed.

No runtime source, RLS source, phone/PC core, App Store core, money, ownership, garage, storage, property, or save-system file was modified.

## 2. Why it changed

The existing JOB-08 scope already included insurance status, coverage, quotes, garage/storage support, and purchase-flow help. Recovered project material shows that Property Insurance and Fleet discounts were planned and partially represented in the website prototype, but no evidence proves that those pages are connected to real Career insurance mechanics.

A durable plan is required before coding so the project does not:

- invent policy names or prices that conflict with the installed game/RLS system;
- report a static quote as a purchased policy;
- duplicate or replace native insurance billing, claims, renewals, or saves;
- mix legal RedFox/XXX Insurance records with UndergroundNet or illegal-storage records;
- hard-code a backend contract before JOB-02 publishes it;
- create another startup Career override or direct patch into protected RLS modules.

---

## 3. Evidence recovered before this plan

### 3.1 Existing legal provider design

The recovered website and roadmap use **XXX Insurance** as the legal insurance provider. Its current design direction is:

- black and hot-pink presentation;
- pink lace styling;
- a luxury/feminine visual identity;
- slogan: `Because accidents happen. Sometimes repeatedly.`;
- links to Garage, Tow Yard, Properties, and Businesses.

The roadmap already lists future Vehicle, Fleet, Property, Tow Yard, Business, and Storage coverage.

### 3.2 Existing prototype sections

The recovered static website prototype includes:

- an XXX Insurance page;
- an Auto Insurance quote panel;
- Daily Driver, Commercial, and Prestige & Collector vehicle classes;
- Liability, Collision, and Comprehensive selections;
- a Business & Property card;
- Roadside Assistance;
- a Fleet section;
- prototype fleet discount tiers:
  - 1 vehicle: standard rate;
  - 2–4 vehicles: 10 percent prototype discount;
  - 5–10 vehicles: 20 percent prototype discount;
  - 10 or more vehicles: 35 percent prototype discount.

These values and buttons are **prototype-only**. The quote is calculated in website JavaScript and does not prove a real policy, premium, payment, claim, renewal, or save operation.

### 3.3 Recovered RLS-related evidence

Existing logs show the installed environment loading or force-resolving modules that include:

```text
career_modules_inventory
career_modules_realEstateNegotiation
career_modules_propertyMortgage
career_modules_garageManager
```

This proves that property, mortgage, garage, and inventory-related systems may exist in the installed Career setup. It does **not** prove their public API, insurance eligibility rules, policy data model, or whether Property Insurance exists natively.

The actual RLS 2.6.6 archive and its insurance source have not yet been inspected in this regular chat. Therefore the exact native policy names, IDs, prices, deductibles, claim rules, and billing functions remain unknown.

### 3.4 XXX Mafia Insurance recovery result

No prior file or committed record was found that defines **XXX Mafia Insurance** as an implemented provider. It is treated here as a new David-approved design direction, not as recovered working code.

---

## 4. Proposed insurance-provider structure

The first JOB-08 implementation should support multiple providers or provider modes without duplicating the underlying Career insurance authority.

### 4.1 Legal network

#### Provider: XXX Insurance

Purpose:

- native vehicle policies;
- personal and collector vehicle coverage;
- commercial and fleet coverage;
- property and business coverage;
- tow-yard and storage endorsements;
- roadside links;
- legal Garage and Property integration.

XXX Insurance remains part of the legal FoxNet/RedFox-facing ecosystem.

### 4.2 Underground network

#### Provider: XXX Mafia Insurance

Working concept:

A fictional in-game high-risk protection-contract provider for UndergroundNet. It is not ordinary legal insurance and must not use RedFox branding on the illegal network.

Possible covered risks, only when the owning systems expose real state and actions:

- hot or questionable-title vehicles;
- vehicles awaiting paperwork;
- illegal-storage losses;
- chop-shop or transport losses;
- seizure, theft, recovery, or high-heat events;
- high-risk import or tow-yard exposure.

The site may use dark humor and criminal-fiction presentation, but it must remain game-world fiction. It will not provide real-world criminal advice or instructions.

Legal XXX Insurance and XXX Mafia Insurance must use separate provider IDs, routes, policy records, permissions, and presentation. A legal policy must never silently become a Mafia contract, and an UndergroundNet contract must never appear as legitimate legal coverage.

---

## 5. Planned insurance products

### 5.1 Existing native vehicle policies — minimum two

JOB-08 will expose at least two existing Career/RLS vehicle-policy types **only after source inspection identifies their exact IDs and supported operations**.

Rules:

- do not invent native policy names;
- do not hard-code policy IDs from memory;
- do not copy native policy implementation into JOB-08;
- read the provider/policy catalog through JOB-02;
- preserve native premium, deductible, renewal, claim, cancellation, and save behavior;
- show unsupported or unavailable state when the current Career system does not expose an operation;
- use the same policy IDs and payloads on phone and PC.

Expected UI treatment:

- `Native Policy A` and `Native Policy B` remain placeholders in planning documents only;
- after inspection, the UI displays the authoritative native names and descriptions;
- additional native policies may be shown automatically when the backend reports them.

### 5.2 Property Insurance

Initial insurable asset categories:

```text
House
Garage
Business
Tow yard
Warehouse
Storage facility
```

Data must come from real Career/RLS property, real-estate, garage, storage, and ownership state. JOB-08 must not create fake property ownership merely to make the page look populated.

Planned page capabilities:

- list owned and eligible properties;
- show location and asset type;
- show whether coverage is active, unavailable, or unsupported;
- request an authoritative quote when the backend supports one;
- show covered-risk categories returned by the backend;
- show deductible, premium, renewal, and claim status when provided;
- show legal bundle eligibility with vehicle or fleet policies;
- link to the owning Garage, Property, Tow Yard, or Storage page without editing those systems.

Potential coverage groups for contract design, not guaranteed mechanics:

```text
Structure/basic property
Garage and stored contents
Business equipment
Tow-yard liability
Warehouse/storage contents
Business interruption
Property bundle endorsement
```

Each coverage group must remain disabled or marked unsupported unless the inspected backend provides a real equivalent or JOB-00 approves a new cross-mod mechanic owned by the correct job.

### 5.3 Fleet Insurance

Fleet Insurance is the legal commercial grouping of multiple owned vehicles under one policy view.

Planned eligibility inputs:

- Career-owned vehicle inventory;
- business or fleet assignment when available;
- vehicle class and use;
- current individual policy status;
- collector, commercial, work-truck, semi, off-road, and other supported categories;
- storage or operating location when supplied by the backend.

Planned capabilities:

- list eligible owned vehicles;
- add or remove vehicles from a proposed fleet before confirmation;
- prevent duplicate vehicle enrollment;
- preserve each vehicle's authoritative inventory ID;
- show vehicles that cannot join and the exact backend reason;
- request a fleet quote;
- display one fleet summary with per-vehicle coverage status;
- allow later policy changes only through approved JOB-02 actions;
- link to Garage/Storage for capacity and location status;
- link to business/tow systems without editing their implementation.

Prototype discount tiers currently visible in the website are design placeholders. They may be retained as configurable mock presentation during UI-only testing, but they must not charge money or be presented as authoritative until a real backend contract approves them.

### 5.4 XXX Mafia Insurance / Protection Contracts

This is planned as a separate UndergroundNet product family.

Potential contract inputs:

```text
Vehicle inventory ID
Title/paperwork status
Heat or wanted level
Legal versus illegal storage location
Declared or backend vehicle value
Active recovery/tow status
Import/export risk state
Contract duration
```

Potential contract outputs, only when supported by future owning systems:

```text
Recovery payment or loss stipend
Vehicle replacement entitlement
Heat-risk modifier
Recovery priority
Storage-loss protection
Paperwork or transport protection status
```

No payment, replacement, ownership creation, heat reduction, title change, storage mutation, or recovery action will be implemented by JOB-08 itself. Those behaviors require explicit contracts from the jobs that own economy, inventory, heat, paperwork, storage, and tow/recovery.

Until those systems exist, the Mafia page must show a truthful `UNAVAILABLE — REQUIRED UNDERGROUND SYSTEMS NOT CONNECTED` state rather than pretending a protection contract was purchased.

---

## 6. Proposed provider and policy data model

This is a contract-needs proposal, not a final schema.

```text
provider
  providerId
  displayName
  network: legal | underground
  capabilities[]
  policyTypes[]

policyType
  policyTypeId
  providerId
  authoritativeSource: native | approved-addon
  assetKind: vehicle | fleet | property | underground-contract
  displayName
  description
  eligibility
  availableActions[]

policyRecord
  policyId
  providerId
  policyTypeId
  status
  insuredAssetIds[]
  premium
  deductible
  billingCycle
  renewalDate
  claimSummary
  backendRevision

quote
  quoteId
  providerId
  policyTypeId
  insuredAssetIds[]
  priceBreakdown
  discountBreakdown
  expiresAt
  confirmationRequired
```

The UI may not calculate authoritative totals from hard-coded values. It may display only totals and breakdowns returned by JOB-02.

---

## 7. Proposed JOB-02 bridge operations

The exact names remain subject to JOB-02 review and versioning. JOB-08 requests capabilities equivalent to:

```text
insurance.getCapabilities
insurance.listProviders
insurance.listNativePolicyTypes
insurance.getPolicyStatus
insurance.listVehicleCandidates
insurance.listPropertyCandidates
insurance.listFleetCandidates
insurance.requestQuote
insurance.getQuote
insurance.applyPolicy
insurance.changePolicy
insurance.cancelPolicy
insurance.listClaims
insurance.getClaimStatus
```

Required bridge rules:

- phone and PC use identical operation names and payloads;
- every response identifies the authoritative source;
- unsupported operations return an explicit unsupported result;
- mutating actions require confirmation and return real success/failure state;
- request IDs prevent duplicate charges or duplicate policies;
- no failure may be translated into success;
- JOB-08 never imports or directly calls protected RLS Lua internals.

For XXX Mafia Insurance, additional future operations must be proposed by the jobs that own heat, paperwork, illegal storage, recovery, and economy. JOB-08 will consume those contracts rather than inventing private calls.

---

## 8. Proposed routes and navigation

Final route names require JOB-01 approval. Planning destinations are:

```text
Vehicle Services > Insurance Overview
Vehicle Services > Native Vehicle Policies
Vehicle Services > Property Insurance
Vehicle Services > Fleet Insurance
UndergroundNet > XXX Mafia Insurance
```

Expected deep-link inputs:

```text
originatingApp
returnRoute
assetKind
vehicleInventoryId
propertyId
businessId
fleetId
quoteId
```

Every deep link must validate that the referenced asset still exists and belongs to the current Career save. A stale or invalid deep link must show an error, not silently choose another vehicle or property.

---

## 9. Implementation phases

### Phase 0 — baseline and source inspection

1. Verify the exact FoxNet baseline archives.
2. Inspect RLS Career Overhaul 2.6.6 insurance source read-only.
3. Record every native policy ID, name, field, action, save path, and UI hook.
4. Inspect property, mortgage, garage, inventory, bank, and credit modules.
5. Identify exact JOB-08-owned runtime paths.
6. Publish a protected-path and edit manifest before changing code.

### Phase 1 — shared contracts

1. JOB-01 confirms route and responsive host contract.
2. JOB-02 publishes the insurance capability and action contract.
3. JOB-03 confirms Store manifest, permissions, and install/open behavior.
4. JOB-00 approves integrated scope.

### Phase 2 — safe UI refactor

1. Preserve the existing XXX Insurance black/hot-pink design.
2. Separate Auto, Property, and Fleet into internal modules.
3. Keep the modules separable for future independent apps/pages.
4. Convert prototype totals and discounts into clearly labeled mock data for static tests.
5. Add loading, empty, unsupported, offline, stale, and backend-error states.

### Phase 3 — read-only live integration

1. Display native vehicle policies.
2. Display owned property eligibility.
3. Display fleet candidates and current individual-policy conflicts.
4. Display authoritative premiums, deductibles, and status where provided.
5. Do not enable purchase/change/cancel controls yet.

### Phase 4 — approved legal write actions

1. Request quotes through JOB-02.
2. Apply or change policies only through approved actions.
3. Preserve confirmation, billing, result, and error behavior.
4. Verify save/load and duplicate-request protection.

### Phase 5 — XXX Mafia Insurance

1. Wait for approved UndergroundNet route and branding boundary.
2. Wait for the owning heat, paperwork, illegal storage, recovery, and economy contracts.
3. Build read-only capability detection first.
4. Add real contract actions only after cross-job approval and testing.

### Phase 6 — runtime verification

1. Phone and PC parity.
2. West Coast and at least one second map.
3. Clean mod set with one FoxNet/Web Ecosystem package.
4. New and existing Career saves.
5. Policy purchase/change/cancel failure paths.
6. Property sale or ownership change while insured.
7. Vehicle sold, moved, destroyed, or removed from a fleet.
8. Legal and Underground provider isolation.
9. ZIP root, duplicate-path, forbidden-file, and required-report checks.
10. David runtime test and JOB-11 verdict.

---

## 10. Verification requirements

The insurance expansion is not complete until testing proves:

- native policy names and IDs match the installed backend;
- at least two native policies are displayed from live data;
- no static quote is presented as an active policy;
- no money is charged by JOB-08 code;
- no policy is created twice after repeated clicks or retries;
- property eligibility follows real ownership;
- fleet vehicles remain linked to their real inventory IDs;
- a vehicle cannot be insured twice in conflicting fleet policies unless the backend explicitly allows it;
- cancelled, expired, unsupported, and failed policies display honestly;
- legal XXX Insurance and XXX Mafia Insurance never share the wrong records or routes;
- phone and PC render the same backend state;
- the final build contains no protected RLS originals or another job's core files;
- runtime remains labeled unproven until David tests the exact ZIP.

---

## 11. Current blockers and required files

Required for the first real inspection pass:

```text
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_7_ALL_IN_ONE_PC_PHONE_GARAGE_SELL_FIX(1).zip
zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_1_DIRECT_SCRAP_COPART_TIMEOUT_FIX phone only works.zip
rls_career_overhaul_2.6.6.zip or identical suffixed copy
RedFox_RLS_Evidence_v03.zip or identical suffixed copy
The exact designed JOB-08 website package and its assets
The approved reference insurance/Career package
```

Missing JOB-02 files, if David has copies:

```text
JOB-02_SHARED_RLS_CAREER_BRIDGE_CONTRACT_v0.1.0-draft.1.md
JOB-02_SHARED_RLS_CAREER_BRIDGE_SCHEMA_v0.1.0-draft.1.json
JOB-02_SHARED_RLS_CAREER_BRIDGE_FIXTURES_v0.1.0-draft.1.json
```

Relevant settings/save evidence:

```text
settings/redfox_garage_hub_manual_links.json
settings/redfox_garage_hub_settings.json
settings/redfox/garage_hub/settings.json
settings/redfox/garage_hub_settings.json
settings/RLS/careerOverhaul.json
career/insurance.json
career/inventory.json
career/rls_career/credit.json
career/rls_career/bank.json
```

Additional blockers:

- no canonical JOB-00 baseline freeze is available to JOB-08;
- no published production `job02.bridge.v1` insurance contract;
- no final JOB-03 Store contract;
- no approved JOB-08 runtime folder;
- no confirmed native policy catalog;
- no confirmed Property Insurance backend;
- no cross-job Mafia protection-contract backend;
- no JOB-08 ZIP or runtime evidence.

---

## 12. Current status

```text
XXX Insurance website design: RECOVERED STATIC PROTOTYPE
Native vehicle policy integration: NOT IMPLEMENTED
Property Insurance page concept: RECOVERED AND EXPANDED IN PLAN
Property Insurance mechanics: NOT VERIFIED / NOT IMPLEMENTED
Fleet Insurance page concept: RECOVERED AND EXPANDED IN PLAN
Fleet Insurance mechanics: NOT VERIFIED / NOT IMPLEMENTED
XXX Mafia Insurance concept: NEW PLAN — NOT IMPLEMENTED
JOB-08 runtime source: NONE APPROVED
JOB-08 ZIP: NONE
BeamNG runtime status: UNTESTED
```

---

## 13. Known problems

- The current quote calculator is static website JavaScript.
- Current fleet percentages are visual prototype values, not backend-authoritative rates.
- Business & Property currently opens prototype messaging rather than a real policy flow.
- Exact native insurance policies are unknown until RLS source inspection.
- Property modules appearing in logs do not prove insurance operations.
- Inventory and garage-related dependency warnings exist in historical logs.
- Phone/PC parity and all-map behavior remain untested.
- The Mafia provider has no owning backend contracts yet.
- The original Work-chat transcript and chat-only attachments were not fully recoverable.

---

## 14. Required next steps after David returns

1. Reopen this plan and the JOB-08 camping-pause checkpoint.
2. Supply or approve the exact required archives and evidence files.
3. Hash, integrity-test, extract, and inventory the baselines.
4. Inspect native RLS insurance policy definitions and supported actions.
5. Inspect property, inventory, garage, bank, credit, and mortgage interfaces.
6. Replace `Native Policy A/B` planning placeholders with exact authoritative policies.
7. Publish JOB-08's detailed contract request to JOB-02.
8. Record exact JOB-08 runtime files and protected files.
9. Obtain JOB-00/JOB-01/JOB-02/JOB-03 approvals.
10. Build the smallest removable JOB-08 page add-on, beginning with read-only data.
11. Do not enable policy mutations until the read-only contract is proven.
12. Test and document the exact build before any working/fixed claim.

---

## 15. Files affected by this GitHub change

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-08_INSURANCE_EXPANSION_PROPERTY_FLEET_XXX_MAFIA_PLAN_2026-07-17.md
```

No runtime mod, RLS source, phone/PC platform file, bridge implementation, App Store implementation, Career save, economy, inventory, property, garage, storage, or another job's source was changed.

---

## 16. Work-chat migration note

The original coordinated project was unintentionally created in ChatGPT Work chats. David was not aware that the project was subject to a separate Work-chat usage limit. On July 14, 2026, those chats became inaccessible until July 20, 2026, interrupting development and requiring manual regular-chat migration. The JOB-08 transcript and chat-only attachments were not fully recoverable, creating duplicate-work, lost-context, coordination, and delay risks. This factual impact remains preserved for inclusion in David's report to OpenAI.

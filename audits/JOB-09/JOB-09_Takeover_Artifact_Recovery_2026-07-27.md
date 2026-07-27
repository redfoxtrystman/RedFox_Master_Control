# JOB-09 Takeover Artifact Recovery Record

**Date:** 2026-07-27  
**Job:** `19 — JOB-09-RedFox_TowRecoveryDispatch`  
**Module ID:** `redfox_tow_recovery_dispatch`  
**Purpose:** Preserve the exact files supplied to the replacement chat and correct the stale v0.2.1 takeover assumption.

---

## 1. Recovered artifact inventory

### A. v0.3.0 — user-confirmed working baseline

Uploaded name:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_0_CatalogOverridesYardSearchTestStorage.zip works good`

The non-ZIP suffix is intentional so BeamNG does not load it.

- File size: 184,358 bytes
- SHA-256: `124bbf853b7c79c8b750822c6a8d29dc5353c7dc4b0d73d1c12c636af4ef391d`
- ZIP integrity: PASS
- Metadata version: 0.3.0
- User runtime label: **WORKS GOOD**
- Runtime file size: `lua/ge/extensions/redfoxTowRecoveryDispatch.lua` — 246,314 bytes

Primary v0.3.0 additions recorded inside the archive:

- exact configuration blacklist, whitelist, approval, and undo;
- saved category overrides;
- Roadside Hazard / Lost Prop handling;
- stronger target and recommended-equipment display;
- abandoned-vehicle yard search;
- Development Test Storage for Spawn Lab vehicles;
- retrieval, return, sorting/searching, and removal for development records;
- more visible Company Fleet Garage transfer control;
- removal of the generic trailer-model equals fifth-wheel assumption.

### B. v0.3.1 — newer failed property/garage experiment

Uploaded name:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_1_RLSTowShopGarageBridge(1).zip`

- File size: 218,778 bytes
- SHA-256: `662db67fc190ede9c529391c39570e93883c2c7024ebb2edb8c700837f5c4aec`
- ZIP integrity: PASS
- Metadata version: 0.3.1
- Hash match against existing GitHub build audit: EXACT
- Runtime file size: `lua/ge/extensions/redfoxTowRecoveryDispatch.lua` — 271,229 bytes

The v0.3.1 build attempted to:

- register generated `redfox_towshop_*` garage locations;
- keep company vehicles as normal owned RLS inventory records;
- move vehicles through RLS garage-location functions;
- preserve inventory ID and ownership;
- add garage capacity, undo, rollback, and legacy recovery.

Later GitHub runtime evidence records the property/garage portion as:

**FAILED — STOPPED**

Reason:

- it created a separate artificial tow-yard garage;
- the purchased property already had the real RLS garage `servicestationGarage` and its own computer;
- normal RLS My Vehicles therefore treated the vehicle as remote and offered the stock $5,000 / approximately 120-second Deliver behavior.

Owner-approved correction:

> The existing purchased property garage is the tow yard. Do not create a second garage.

---

## 2. Recovered version chain

The two supplied archives and GitHub commit history establish at least this development sequence:

| Version | Recorded direction/status |
| --- | --- |
| v0.2.1 | Rollover scenes, multiple yards, readable UI, history |
| v0.2.2 | Passenger-only fit-guard direction; rejected by David |
| v0.2.3 | Mixed roadway and roadside crash scenes |
| v0.2.4 | Cataloged Tow History Book |
| v0.2.5 | Tow Fleet Book and map-aware hazard sites |
| v0.2.6 | Vehicle selection and terrain-spawn repair |
| v0.2.7 | Spam audit and dispatch-variety hotfix |
| v0.2.8 | Temporary Vehicle Spawn Lab |
| v0.2.9 | Company Fleet Garage and yard organization |
| v0.3.0 | Catalog overrides, yard search, development test storage — David says works good |
| v0.3.1 | RLS tow-shop garage bridge — property/garage design failed runtime test |
| v0.3.2 | GitHub artifact record exists, but exact artifact and status are not yet reconciled in this chat |

This version chain must replace the prior takeover statement that v0.2.1 was the latest known build.

---

## 3. v0.3.2 unresolved record

GitHub records:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_2_PropertyTowYardComputer.zip`

- SHA-256: `c01965e54174572235a4c419c6b7557d58f6d7940435b2f43330c51f6cf8cee1`
- Size: 237,789 bytes
- Static verification: PASS
- Runtime verification at record creation: PENDING DAVID

A later handoff again proposes v0.3.2 as the next patch after documenting the v0.3.1 failure. Until the exact artifact and chronology are recovered, v0.3.2 is not approved as the current baseline.

---

## 4. Current baseline decision

### Safe user-confirmed baseline

`v0.3.0`

Use this only as the last user-confirmed working reference. Preserve it unchanged.

### Failed newer experiment

`v0.3.1`

Do not continue the artificial `redfox_towshop_*` property-garage approach.

### Next source selection

Do not edit or issue a new version until one of these is completed:

1. Recover the exact v0.3.2 artifact matching its recorded hash and inspect it; or
2. Start the focused existing-property computer correction from the preserved v0.3.1 source while retaining v0.3.0 as the rollback baseline.

No new version number should be assigned until that choice is documented.

---

## 5. Required GitHub discipline for JOB-09

For every future JOB-09 build, update GitHub before handing the ZIP to David with:

- exact filename;
- version and feature scope;
- SHA-256 and size;
- changed files;
- static verification results;
- runtime status clearly separated from static status;
- user test result;
- known failures;
- last known good baseline;
- next focused action;
- source patch or diff when practical.

After David tests a build, add the result immediately rather than leaving the build audit as `RUNTIME UNTESTED`.

---

## 6. Related incident

`INCIDENT_REPORTS/2026-07-27_JOB-09_Takeover_GitHub_Discovery_And_Version_Recovery_Failure.md`

This recovery record does not claim access to the complete inaccessible shared-chat history. It records only the evidence recovered from GitHub and the two supplied archives.

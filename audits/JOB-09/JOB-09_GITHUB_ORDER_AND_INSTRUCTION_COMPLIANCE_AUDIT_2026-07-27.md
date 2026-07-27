# JOB-09 GitHub Order and Instruction-Compliance Audit

**Date:** 2026-07-27  
**Job:** `19 — JOB-09-RedFox_TowRecoveryDispatch`  
**Module:** `redfox_tow_recovery_dispatch`  
**Primary issue:** #4  
**Audit requested by:** David / project owner

## Scope and evidence boundary

This audit covers only JOB-09 and the evidence available in:

- the current JOB-09 conversation history;
- GitHub issue #4 and its comments;
- the accessible commit history of `redfoxtrystman/RedFox_Master_Control`;
- the exact filenames, hashes, statuses, screenshots, and runtime findings recorded for JOB-09.

This document does **not** claim to have audited every other project chat. Other jobs must perform their own evidence-based audit rather than copying JOB-09's count.

## Executive finding

The repository contains a large amount of JOB-09 documentation, but the required release order was not followed consistently.

### Confirmed counts

| Category | Confirmed count | Meaning |
|---|---:|---|
| Named JOB-09 version checkpoints reviewed | 13 | v0.2.0 through v0.3.2 inclusive |
| Version/update-order incidents | 5 | Four reused version identifiers plus one contradictory canonical status |
| Repository reproducibility failures | 13 | No checkpoint was found with both a complete exact source snapshot and its exact distributable artifact preserved in GitHub as one traceable release chain |
| Direct owner-direction violations or clear requirement misreads | 4 | Listed below with evidence |
| Runtime architecture/implementation failures | 2 | v0.3.0 company-storage behavior and v0.3.1 artificial property garage/computer design |
| Other jobs/chats audited | 0 | Not enough complete evidence in this JOB-09 audit |

## Incident group 1 — Reused version identifiers

A version identifier must describe one immutable source state and one immutable artifact hash. Materially changing the build without changing the version breaks auditability and makes screenshots, hashes, logs, and bug reports ambiguous.

### Incident 1: v0.2.6 reused

The GitHub history contains materially different v0.2.6 records, including:

- police impound and emergency-scenes work;
- later selection and spawn-repair work;
- additional pause/read-first addenda.

At least two materially different build states were recorded under `v0.2.6` instead of creating a new version.

### Incident 2: v0.2.7 reused

The GitHub history contains:

- `v0.2.7` RLS progression and personal-claims work;
- a later `v0.2.7` Spam Guard / Dispatch Variety build.

These are not the same release state and should not have shared one version identifier.

### Incident 3: v0.2.8 reused

The GitHub history contains:

- `v0.2.8` Career-day clock and asset-manager work;
- a later `v0.2.8` Temporary Vehicle Spawn Lab build.

The second material build should have received a new version number.

### Incident 4: v0.2.9 reused

The GitHub history contains:

- `v0.2.9` active-call recovery work;
- a later `v0.2.9` Company Fleet Garage / Yard Organization build.

This created ambiguity about which exact v0.2.9 source and hash a report referred to.

### Corrective rule

A released or handed-off version number is immutable. Any source change after packaging requires a new version number, even when the change is small.

## Incident group 2 — Incomplete GitHub release preservation

The accessible GitHub history contains handoffs, audits, patches, hashes, test instructions, and source summaries. That documentation is useful, but it is not a complete reproducible release chain.

A compliant release chain requires all of the following to be traceable together:

1. exact full unpacked source snapshot;
2. source commit SHA;
3. exact packaged ZIP generated from that source;
4. ZIP SHA-256 and size;
5. static-verification result;
6. issue update made before the user-facing handoff;
7. later runtime result tied to that same hash.

I did not find that complete chain for any of the 13 named checkpoints. The distributable ZIPs were generally referenced as chat sandbox files, while GitHub stored documentation, summaries, or partial patches. A partial patch is not independently reconstructable when the exact base source snapshot is absent.

### Version ledger audit

| Version | GitHub evidence found | Reproducible from GitHub alone? | Audit result |
|---|---|---|---|
| v0.2.0 | Transferred build recorded in issue #4 | No | Transfer record only; exact full source/artifact chain absent |
| v0.2.1 | Transferred build recorded in issue #4 | No | Transfer record only; exact full source/artifact chain absent |
| v0.2.2 | Handoff plus a source patch from v0.2.1 | No | Patch depends on an absent exact v0.2.1 source snapshot; later rejected |
| v0.2.3 | Handoff and source-change summary | No | Full source/artifact chain absent |
| v0.2.4 | Handoff record | No | No complete source snapshot found |
| v0.2.5 | Handoff and source-change record | No | Full source/artifact chain absent |
| v0.2.6 | Multiple records under the same version | No | Version reused; no immutable release state |
| v0.2.7 | Multiple materially different records under the same version | No | Version reused; ambiguous source/hash identity |
| v0.2.8 | Multiple materially different records under the same version | No | Version reused; ambiguous source/hash identity |
| v0.2.9 | Multiple materially different records under the same version | No | Version reused; ambiguous source/hash identity |
| v0.3.0 | Audit and source summary | No | Exact full source/artifact pair not preserved in GitHub |
| v0.3.1 | Audit, source summary, and runtime-failure record | No | Exact ZIP remained a sandbox artifact; full source snapshot absent |
| v0.3.2 | Many audit/release-note commits | No | Current runtime does not contain the ZIP; later canonical handoff contradicts its claimed distribution |

## Incident group 3 — Contradictory canonical status

### Incident 5: v0.3.2 distribution contradiction

GitHub commits created on 2026-07-27 state that:

- `19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_2_PropertyTowYardComputer.zip` was verified and distributed;
- its recorded hash was `c01965e54174572235a4c419c6b7557d58f6d7940435b2f43330c51f6cf8cee1`.

A later end-of-chat handoff in the same repository states that the current distributed build was still v0.3.1 and that v0.3.2 was the next patch to build.

The current active runtime also does not contain the recorded v0.3.2 ZIP. Therefore:

> **v0.3.2 is quarantined as `PROVENANCE CONFLICT — DO NOT TREAT AS CURRENT` until the exact artifact is recovered, rehashed, source-matched, and explicitly reissued.**

The version number `v0.3.2` must not be silently reused.

## Incident group 4 — Direct owner-direction violations or requirement misreads

### Direction violation 1: v0.2.2 passenger-only accident restriction

The v0.2.2 build changed general accident scenes to passenger-only parking-space clusters. David clarified that mixed cars, semis, trailers, buses, heavy wreckers, and rotators were valid crash targets and that the real failure was the unrealistic compact parking-lot scene.

GitHub issue #4 explicitly records v0.2.2 as rejected because it contradicted the owner requirement.

### Direction violation 2: rust joke treated as a planned feature

David joked about leaving a stored vehicle until it rusted. The response converted the joke into a proposed deterioration feature. David then had to clarify that rusting was not requested.

### Direction violation 3: unnecessary legal/court process added

The discussion introduced courts, agency transfers, and detailed legal ownership paths. David explicitly rejected that level of bureaucracy and requested realistic gameplay without boring legal administration.

### Direction violation 4: player-to-player selling incorrectly stated

The discussion stated that vehicles could be sold to other players. David corrected this and required reference to actual BeamNG Career and RLS Career behavior. Research then confirmed that the supported paths are NPC Marketplace offers, NPC auction bidding, direct sale, salvage, or scrap—not multiplayer player-to-player sales.

## Incident group 5 — Runtime architecture/implementation failures

These are recorded separately from direct instruction violations because some were discovered only through runtime testing.

### Runtime failure 1: v0.3.0 company-storage ownership behavior

Observed behavior included:

- moving a vehicle to work/company storage made it disappear from normal owned access;
- moving it back could cause it to no longer be owned;
- the design used a separate company record instead of one normal RLS inventory record.

Correct rule established afterward:

- one normal owned RLS inventory record;
- same inventory ID;
- `owned=true` remains unchanged;
- company fleet is metadata and a filtered view;
- garage movement changes location only.

### Runtime failure 2: v0.3.1 artificial garage and computer

v0.3.1 created a separate artificial `Tow Yard 1` garage and Fleet Computer even though the purchased Belasco service property already had:

- the real RLS garage ID `servicestationGarage`;
- an existing property computer.

Result:

- the vehicle appeared remote from the real property computer;
- RLS offered the stock $5,000 Deliver action;
- RLS applied an approximately 120-second delivery delay;
- the generated Fleet Computer was not a usable replacement for proper property-computer integration.

Correct rule established:

> The purchased property's existing RLS garage **is** the tow yard. RedFox links business metadata and custody records to it; it does not create a second garage.

## Root causes

1. No single canonical version ledger was updated atomically.
2. Version numbers were reused after material changes.
3. GitHub often received documentation instead of a complete source-and-artifact release snapshot.
4. Multiple commits described one release without one final authoritative release manifest.
5. Chat sandbox artifacts were treated as durable even though they are not permanent repository storage.
6. Runtime findings were not always reconciled into one current-status file before later work continued.
7. Requirements were sometimes expanded from examples or jokes instead of being held to explicit owner approval.
8. Public game/RLS behavior was sometimes assumed before source verification.

## Mandatory correction before another JOB-09 patch

1. Treat v0.3.1 property integration as `FAILED — STOPPED`.
2. Treat v0.3.2 as `PROVENANCE CONFLICT — QUARANTINED`.
3. Use **v0.3.3** for the next newly built candidate.
4. Commit the full unpacked JOB-09 source snapshot before packaging.
5. Build the ZIP from that exact committed source.
6. Record the source commit SHA, ZIP hash, size, and verification result in one release manifest.
7. Update issue #4 before giving David the download.
8. After David tests, record the runtime result against the exact hash before beginning another version.
9. Never reuse a version number.
10. Do not add a feature merely because it was mentioned as a joke, example, or rejected possibility.

## Required status labels

- `DAVID-TESTED WORKING`
- `BUILT — RUNTIME UNTESTED`
- `PARTIAL`
- `BLOCKED`
- `FAILED — STOPPED`
- `PROVENANCE CONFLICT — QUARANTINED`
- `MOCKUP / PLACEHOLDER`

## Audit conclusion

JOB-09 has substantial documented work, but the repository was not being used as the complete source of truth. The immediate correction is not to erase history. It is to preserve the history, mark the contradictions, stop version reuse, and require a full source-to-artifact GitHub chain for every future version.

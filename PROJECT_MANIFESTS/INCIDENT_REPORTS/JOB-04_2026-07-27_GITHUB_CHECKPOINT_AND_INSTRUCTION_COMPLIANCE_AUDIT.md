# JOB-04 Incident Report — GitHub Checkpoint and Instruction Compliance Audit

**Date:** 2026-07-27  
**Job:** JOB-04 — Scrap Yard / Wrecking Yard  
**Owner:** David / Captain  
**Filed by:** Sol / ChatGPT  
**Severity:** High — version-control continuity failure, order-of-operations failure, and repeated owner-instruction noncompliance  
**Audit status:** Complete to the limit of currently available evidence

---

## 1. Reason for this audit

David requires GitHub to be updated between every version so that a chat reaching its limit cannot erase the working history, failed tests, decisions, rollback points, or roadmap.

This audit was ordered because that requirement was not followed consistently. The purpose is to count the failures, preserve the evidence, and create a mandatory process that prevents another continuity loss.

---

## 2. Evidence inspected

This audit used:

1. The connected GitHub repository:
   - `redfoxtrystman/RedFox_Master_Control`
2. Existing JOB-04 commits, audits, handoffs, and incident reports.
3. The current uploaded archive:
   - `zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD_FROM_v0_2_1(1).zip`
4. Verification and historical documents embedded in that archive.
5. The prior full handoff:
   - `PROJECT_MANIFESTS/HANDOFFS/JOB-04_2026-07-27_FULL_HANDOFF_ROADMAP_AND_NEXT_TESTS.md`
6. The earlier warning/instruction-override incident report and its amendment.

The shared ChatGPT handoff link could not be fetched reliably by the available reader. Therefore, transcript-only events that were never copied into GitHub or the uploaded archive may still be missing. All counts below are minimum confirmed counts, not claims that no additional failures occurred.

---

## 3. Current artifact verification

Current uploaded test archive:

```text
zzzz_RedFox_FoxNet_JOB-04_ScrapYard-WreckingYard_2026-07-27_1226PT_v0_2_4_NATIVE_RLS_JOES_JUNK_NO_STARTUP_LOAD_FROM_v0_2_1(1).zip
```

Verified locally during this audit:

```text
Size: 25,165,565 bytes
SHA-256: 83ca53b9fc3e6f73b00720e60142b093788b462aa940604d8795e53d6460f7cc
ZIP integrity: PASS
Runtime status: UNPROVEN until David tests this exact archive in BeamNG
```

The hash matches the v0.2.4 GitHub handoff record despite the `(1)` suffix added by the upload system.

---

## 4. Version checkpoint audit

### 4.1 Confirmed versioned checkpoints found in the available evidence

The current archive and GitHub history establish at least **29 distinct versioned Scrap Yard/JOB-04 build checkpoints or named baseline candidates**.

They are split into two historical numbering lines.

### A. FoxNet / Scrap Yard ecosystem lineage

```text
v0.8
v0.9
v0.9.1
v0.9.2
v0.9.5
v0.9.6
v0.9.7
v0.9.8
v0.9.9
v0.10
v0.10.1
v0.10.2
v0.10.3
v0.10.3.1
v0.10.3.7
```

### B. JOB-04 package lineage

```text
v0.1.0
v0.1.1
v0.1.2
v0.1.3
v0.1.4
v0.1.5
v0.1.6
v0.1.7
v0.1.9
v0.2.0
v0.2.1
v0.2.2
v0.2.3
v0.2.4
```

`v0.1.8` is referenced as a planned/possible next number and as part of later filenames, but the currently available evidence does not prove a distinct delivered v0.1.8 archive. It is therefore not counted as a confirmed build checkpoint.

---

## 5. Direct GitHub checkpoint results

### 5.1 Direct per-version GitHub records found

Direct version-specific GitHub records were found for:

```text
v0.10.3.1
v0.1.0
v0.1.1
v0.1.2
v0.1.3
v0.1.4
v0.1.5
v0.1.6
v0.1.7
v0.1.9
v0.2.0
v0.2.1
v0.2.2
v0.2.3
v0.2.4
```

**Direct checkpoint count found: 15**

The later JOB-04-numbered line was generally recorded promptly. For example, the v0.2.0 through v0.2.4 audit commits were made within minutes of the timestamps recorded in their filenames.

### 5.2 Confirmed missing direct per-version GitHub records

No direct version-specific GitHub checkpoint was found for:

```text
v0.8
v0.9
v0.9.1
v0.9.2
v0.9.5
v0.9.6
v0.9.7
v0.9.8
v0.9.9
v0.10
v0.10.1
v0.10.2
v0.10.3
v0.10.3.7
```

**Minimum missing direct checkpoint count: 14**

Some of these versions are mentioned later inside other records. That is not equivalent to a proper checkpoint made between versions. A later reference does not preserve the exact build scope, hash, test result, changed files, and next action at the time the version was produced.

### 5.3 Version-control compliance conclusion

```text
Confirmed versioned checkpoints: 29
Direct per-version GitHub records found: 15
Missing direct per-version GitHub checkpoints: 14
Direct checkpoint coverage: 51.7%
Missing checkpoint rate: 48.3%
```

This is a serious continuity failure. Nearly half of the confirmed versioned lineage lacks its own direct GitHub checkpoint.

Caveat: the exact date when the strict per-version GitHub rule was first stated is not recoverable from the current evidence. Therefore, this report records all 14 as continuity gaps and minimum checkpoint failures, but does not falsely claim that every omitted version was created after the rule was first spoken.

---

## 6. Confirmed owner-instruction and workflow violations

The following are separate from ordinary coding bugs.

### Incident 1 — Warning / extra behavior instruction override

Existing GitHub incident evidence confirms that David explicitly instructed the assistant at least twice not to add or retain warning/caution/cargo/combo text.

Minimum confirmed ignored owner instructions:

```text
2
```

The assistant continued to push or preserve warning behavior after the first instruction and required a later removal-only build.

### Incident 2 — Incomplete first incident report

The first warning incident report said “multiple times” but failed to provide the numeric count David requested.

Confirmed reporting failure:

```text
1
```

A later amendment had to correct the omission.

### Incident 3 — v0.2.0 exceeded the protected narrow-patch direction

The earlier incident direction said the next work should be a narrow lag-only patch and should not touch the grey-screen core UI files unless absolutely necessary.

v0.2.0 changed eight code files, including:

```text
ui/ui-vue/dist/index.js
```

It combined image behavior, Scrap Yard load behavior, phone relay behavior, PC bridge behavior, and Vue route behavior in one patch. It then failed at runtime with no vehicles loading.

Minimum workflow breaches recorded for this incident:

```text
2
1. Protected/narrow scope was exceeded.
2. A specifically protected core UI file was modified again.
```

This does not mean every v0.2.0 change was unreasonable. It means the patch did not follow the previously recorded narrow-patch constraint.

### Incident 4 — Wrong workstream takeover during this handoff

At the start of the current handoff, the assistant incorrectly claimed takeover of the Node Grabber/Developer Tool workstream instead of JOB-04 — Scrap Yard / Wrecking Yard.

Confirmed scope-assignment failure:

```text
1
```

David had to correct the job ownership explicitly.

### Minimum non-version-control instruction/workflow breach count

```text
2 warning instructions ignored
+ 1 incomplete requested count
+ 2 v0.2.0 narrow-scope/protected-file breaches
+ 1 wrong workstream takeover
= 6 minimum individual breaches
```

These six breaches occurred across four distinct incidents.

---

## 7. Combined minimum compliance count

If every missing per-version checkpoint is counted as one separate order-of-operations failure:

```text
14 missing direct GitHub checkpoints
+ 6 other confirmed instruction/workflow breaches
= 20 minimum recordable compliance failures
```

This **20** is the minimum evidence-backed combined count available now.

It is not a claim that exactly 20 failures occurred across the entire unavailable transcript history. Additional transcript-only failures may exist.

---

## 8. Technical failures recorded separately

The following are test failures or regressions. They are not automatically counted as instruction violations:

```text
v0.1.5 — PC/phone parity attempt broke both phone and PC loading.
v0.2.0 — No cars loaded; refresh did not recover the list.
v0.2.2 — Broad openShop call opened every store.
v0.2.3 — Welcome page about 20 seconds; Scrap Yard over one minute; no cars.
v0.2.4 — Static verification passed; runtime still untested.
```

Technical failure must still be recorded, but a bug is not the same as disobeying an owner instruction. This audit keeps those categories separate.

---

## 9. Mandatory corrected GitHub process

Effective immediately, no JOB-04 version may proceed to the next version without all three checkpoints below.

### Checkpoint A — Pre-build plan

Before editing:

```text
- exact source ZIP
- source SHA-256
- runtime status of source
- exact owner request
- exact files proposed for editing
- exact protected files not to be touched
- exact deferred features excluded
- rollback plan
```

### Checkpoint B — Build record

Before delivering the ZIP:

```text
- output filename
- output SHA-256
- file count and byte size
- exact changed files
- exact changes
- exact static tests
- exact unproven runtime statements
- embedded TXT and HTML verification reports
- next runtime test
```

The GitHub build record must be committed **before or at the same time the ZIP is delivered**, not after another version has already been built.

### Checkpoint C — Runtime result

After David tests:

```text
- exact tested filename and SHA-256
- BeamNG version
- RLS version
- map and career profile
- pass/fail results
- log evidence
- regressions
- keep / reject / rollback decision
- next smallest action
```

### Hard gate

```text
NO NEXT VERSION until the current version has:
1. a GitHub pre-build or approved-scope record,
2. a GitHub build record,
3. a GitHub runtime-result or explicit untested/abandoned closure record.
```

---

## 10. Current source-of-truth status

```text
Current test build: v0.2.4
Current uploaded SHA-256: 83ca53b9fc3e6f73b00720e60142b093788b462aa940604d8795e53d6460f7cc
Safe rollback base: v0.2.1 rollback / v0.1.9 last stock-loading line
Do not use as a base: v0.2.0, v0.2.2, v0.2.3
Current runtime gate: test v0.2.4 before building v0.2.5
```

---

## 11. Corrective actions completed by this audit

```text
- Counted the available version lineage.
- Separated direct GitHub checkpoints from indirect mentions.
- Recorded 14 minimum missing direct version checkpoints.
- Recorded 6 minimum other instruction/workflow breaches.
- Recorded the combined minimum of 20 compliance failures.
- Verified the uploaded v0.2.4 archive and hash.
- Re-established JOB-04 scope.
- Created a mandatory three-checkpoint GitHub gate.
- Created a new post-audit full roadmap in a separate handoff file.
```

---

## 12. Final audit conclusion

The claim that JOB-04 had no GitHub work at all would be inaccurate. The later JOB-04-numbered versions were usually documented promptly.

The actual failure is still severe:

```text
- The earlier development lineage contains at least 14 missing direct per-version checkpoints.
- At least six additional owner-instruction/workflow breaches are confirmed.
- The continuity process was not reliable enough to survive chat limits without reconstruction.
```

The corrected rule is now explicit: **GitHub is part of producing every version, not optional cleanup after development.**
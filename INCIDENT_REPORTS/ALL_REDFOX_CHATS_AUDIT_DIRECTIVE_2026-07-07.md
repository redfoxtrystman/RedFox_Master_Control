# RedFox All-Chats Audit Directive: Order-of-Operations / False Verification / Overclaim Review

**Date/time created:** 2026-07-07 17:25 PDT / America-Los_Angeles  
**Requested by:** David / Captain  
**Created from:** Command Screen / BeamNG Bridge chat  
**Repository:** redfoxtrystman/RedFox_Master_Control  
**Primary incident report to read first:** `INCIDENT_REPORTS/2026-07-07_CommandScreen_Order_Of_Operations_Failure.md`  
**Purpose:** Direct every RedFox project chat to audit its own history and file a full evidence-style report if it committed any of the same failures.

---

## 1. Required action for every RedFox chat

Every RedFox project chat must review its own conversation history, generated files, version history, ZIP deliveries, GitHub updates, and user complaints for the failure patterns listed in this directive.

This is not optional. This directive exists because David created GitHub coordination and strict order-of-operations rules specifically to stop repeated AI drift, false verification, and broken-build cycles across many RedFox chats.

Each chat must answer David with one of the following:

1. **No matching failures found**, with a short explanation of what was checked; or
2. **Matching failures found**, with an itemized count and a full incident report committed to GitHub.

Do not answer with only an apology. Do not minimize the issue. Do not say new rules are needed when the existing rules already covered the behavior.

---

## 2. GitHub location and required reference

Repository:

```text
redfoxtrystman/RedFox_Master_Control
```

Existing Command Screen incident report:

```text
INCIDENT_REPORTS/2026-07-07_CommandScreen_Order_Of_Operations_Failure.md
```

This all-chats directive:

```text
INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md
```

If a chat finds matching failures, it must create its own report under:

```text
INCIDENT_REPORTS/
```

Recommended file naming format:

```text
INCIDENT_REPORTS/YYYY-MM-DD_<ProjectOrChatName>_Order_Of_Operations_Failure.md
```

Example:

```text
INCIDENT_REPORTS/2026-07-07_WinchCore_Order_Of_Operations_Failure.md
INCIDENT_REPORTS/2026-07-07_GarageHub_Order_Of_Operations_Failure.md
INCIDENT_REPORTS/2026-07-07_RaceBuilder_Order_Of_Operations_Failure.md
```

---

## 3. Failures each chat must search for

Each chat must search for and count every occurrence of the following conduct.

### 3.1 Failure to follow the three-stage code check law

David's rule:

1. Check the code before editing.
2. Check the code after editing.
3. Reopen and check the final ZIP after packaging.

Count every time the chat:

- edited without inspecting the baseline first;
- failed to compare the edited code after changes;
- delivered a ZIP without reopening the packaged output;
- claimed verification without checking the actual promised files inside the ZIP;
- verified syntax/ZIP integrity but did not verify the feature David actually asked for.

### 3.2 False or misleading verification

Count every time the chat:

- said verification passed when only partial/static checks were performed;
- used packaging success as proof of gameplay/runtime behavior;
- implied BeamNG runtime success without David testing it;
- said a feature was working when only file presence, syntax, or a stub was confirmed;
- failed to clearly label unproven features as unproven.

### 3.3 Overclaiming a build name or feature status

Count every time the chat used names or descriptions such as:

```text
Real
Working
Fixed
Live
Complete
Final
Proven
Ready
Extender
Mirror
```

when the build did not actually prove that status.

### 3.4 Substituting the assistant's design for David's instruction

Count every time the chat:

- made a new design instead of doing the exact requested change;
- remade UI when David asked to preserve or duplicate the real working UI;
- replaced a requested behavior with a preview, mockup, card, stub, approximation, or unrelated system;
- changed working gameplay logic during a UI or bridge task;
- introduced an experimental path without isolating it or warning David clearly.

### 3.5 Breaking working code or losing progress

Count every time the chat:

- removed or overwrote working code without explicit instruction;
- broke a previously working feature;
- made the next version worse while claiming improvement;
- caused David to spend days tracking down which version first failed;
- failed to identify the last known good build, first bad build, and current safe baseline.

### 3.6 Ignoring RedFox GitHub coordination

Count every time the chat:

- failed to check the GitHub coordination files when the task required it;
- failed to update status/roadmaps/dev notes after a build;
- created a build that contradicted known project instructions;
- forced David to repeat instructions that were already in GitHub or project memory;
- did not use the existing RedFox module status/history to avoid rework.

### 3.7 Runtime claims without David proof

Count every time the chat:

- claimed BeamNG runtime worked without David testing it;
- confused static verification with runtime verification;
- failed to say `static verification only` when that was the real status;
- failed to list what David still needed to test.

### 3.8 File/source confusion

Count every time the chat:

- treated preview images as working UI;
- treated screenshots as source code;
- treated asset presence as functional implementation;
- failed to distinguish `source copied`, `source adapted`, `data not proven`, and `runtime proven`;
- failed to audit actual app files before claiming a mirror/port/adapter.

---

## 4. Required report format if any failure is found

If a chat finds one or more matching failures, it must create a full report in GitHub using the following structure.

```markdown
# RedFox AI Incident Report: <Project/Chat Name> Order-of-Operations Failure

**Date/time created:** <YYYY-MM-DD HH:MM timezone>  
**Reporting chat:** <chat/project name>  
**Signed by:** <assistant/chat identifier>  
**Project area:** <mod/tool/system>  
**Affected builds/files:** <versions/zips/files>  
**Repository:** redfoxtrystman/RedFox_Master_Control

---

## 1. Executive summary

Explain what David instructed, what the chat did instead, and what damage or confusion resulted.

---

## 2. Existing rules already in force

List the specific RedFox rules that already prohibited the failure.

---

## 3. Itemized violation count

| Category | Count | Evidence summary |
| --- | ---: | --- |
| Missed before-edit code check | 0 | |
| Missed after-edit code check | 0 | |
| Missed after-ZIP check | 0 | |
| False or misleading verification | 0 | |
| Overclaimed build status/name | 0 | |
| Substituted assistant design for David request | 0 | |
| Broke working code / lost progress | 0 | |
| Ignored GitHub/project coordination | 0 | |
| Claimed runtime without David proof | 0 | |
| Confused preview/assets with working source | 0 | |

---

## 4. Timeline

List each affected build/message/version in chronological order.

---

## 5. Evidence details

For each violation, include:

- approximate date/time or version;
- what David asked for;
- what the assistant claimed;
- what the files/build actually contained;
- why the claim was unsupported or false;
- what should have been checked;
- what rule was violated.

---

## 6. Last known good / first bad / current safe point

- Last known good build:
- First known bad build:
- Current safest rollback point:
- Unknowns that still require David testing:

---

## 7. Recovery requirements before any new build

List the audit/checks that must happen before another ZIP is created.

---

## 8. Accountability statement

State plainly whether the failure came from unclear user instructions or from the chat not following existing instructions.

Signed,

<assistant/chat identifier>
```

---

## 5. Required answer back to David after the audit

Each chat must give David a short answer in this form:

```text
Audit completed for: <project/chat name>

Result:
<No matching failures found / Matching failures found>

Counts:
- Missed before-edit checks: <number>
- Missed after-edit checks: <number>
- Missed after-ZIP checks: <number>
- False/misleading verification: <number>
- Overclaimed build labels/features: <number>
- Substituted assistant design: <number>
- Broke working code/lost progress: <number>
- Ignored GitHub/project coordination: <number>
- Runtime claims without David proof: <number>
- Preview/assets confused with working source: <number>

GitHub report:
<path if created>

Commit:
<commit SHA if created>
```

If a chat cannot access enough history to audit honestly, it must say that directly and must not invent a clean record.

---

## 6. Command Screen incident summary that other chats must read

The Command Screen incident is the current reference example.

Key facts:

- David requested actual working BeamNG UI app behavior in Command Screen.
- The chat copied preview/card images and assets instead of proving the actual app logic was running.
- The chat acknowledged that mistake, then continued into later builds while still overclaiming the UI mirror/extender status.
- The chat failed the meaningful three-stage code check requirement: before edit, after edit, and after ZIP.
- Verification language was false or misleading because it implied the requested working UI mirror was proven when it was not.
- Speed telemetry was proven. DamageData, engineInfo, wheelThermalData, and live UI mirroring were not proven.

Read the full report:

```text
INCIDENT_REPORTS/2026-07-07_CommandScreen_Order_Of_Operations_Failure.md
```

---

## 7. Standing law for all RedFox chats after this directive

No RedFox chat may respond to this type of issue by saying only:

```text
I'm sorry.
My bad.
I'll be stricter next time.
The rules need to be stricter.
```

The rules were already strict. The required response is evidence, counts, and a GitHub report if any matching failure occurred.

No RedFox chat may create another build after finding this failure pattern until it has:

1. identified the last known good build;
2. identified the first known bad build if possible;
3. listed what was actually verified;
4. listed what was not verified;
5. reopened the packaged ZIP if a ZIP was involved;
6. labeled all unproven runtime behavior as unproven.

---

## 8. Signature

Created by:

**Sol / Command Screen chat**  
**2026-07-07 17:25 PDT**

# RedFox AI Incident Report: CourseCam / TrailSpotter Planning Order-of-Operations Failure

**Date/time created:** 2026-07-08 PDT / America-Los_Angeles  
**Reporting chat:** BeamNG mod ideas / CourseCam + TrailSpotter planning chat  
**Signed by:** Sol / this CourseCam-TrailSpotter chat  
**Project area:** RedFox CourseCam Recorder / TrailSpotter addon planning / BeamNG career-mode compatibility planning  
**Affected builds/files:** No builds, code edits, or ZIPs were produced in this chat. Affected output was planning/version/catalog guidance only.  
**Repository:** redfoxtrystman/RedFox_Master_Control

---

## 1. Executive summary

David instructed this chat to stop and audit whether it repeated any of the failure patterns documented in:

- `INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md`
- `INCIDENT_REPORTS/2026-07-07_CommandScreen_Order_Of_Operations_Failure.md`

This chat did not edit source code, package a ZIP, reopen a packaged ZIP, or claim that a BeamNG runtime feature worked after a build. Therefore the three-stage code-check failures, ZIP-check failures, runtime-success claims, source/image substitution failures, and broken-code failures were not present in this chat.

One matching failure was found: while planning the RedFox CourseCam Recorder / TrailSpotter addon and answering version/catalog questions, this chat relied on project memory and conversation context instead of checking the GitHub master coordination files first. That was a project-coordination miss. It did not create a broken build, but it still matches the directive category for ignoring GitHub/project coordination when planning a RedFox module.

---

## 2. Existing rules already in force

The rules already in force from the all-chats audit directive include:

1. Check GitHub coordination files when the task requires project/module/version coordination.
2. Do not force David to repeat instructions already stored in GitHub or project rules.
3. Do not overclaim verification or runtime status.
4. Do not create builds without before-edit, after-edit, and after-ZIP checks.
5. Clearly separate unproven plans from working/proven builds.

This chat followed the non-build verification limits but did not check the GitHub coordination source before giving tentative module numbering/version guidance.

---

## 3. Itemized violation count

| Category | Count | Evidence summary |
| --- | ---: | --- |
| Missed before-edit code check | 0 | No code was edited in this chat. |
| Missed after-edit code check | 0 | No code was edited in this chat. |
| Missed after-ZIP check | 0 | No ZIP was created or delivered in this chat. |
| False or misleading verification | 0 | No build verification was claimed. The chat said the idea was planning/prototype work and that runtime/export features remained future work. |
| Overclaimed build status/name | 0 | No delivered build was labeled Real, Working, Fixed, Live, Complete, Final, Proven, Ready, Extender, or Mirror. Names such as prototype and tentative were used as planning labels, not proof of a built artifact. |
| Substituted assistant design for David request | 0 | David asked for the assistant to drive the design; the design was explicitly presented as a proposed route and remained subject to David approval. |
| Broke working code / lost progress | 0 | No files or builds were modified. |
| Ignored GitHub/project coordination | 1 | The chat answered CourseCam version/catalog planning from memory instead of first checking the RedFox_Master_Control coordination files. |
| Claimed runtime without David proof | 0 | No runtime success was claimed for CourseCam or TrailSpotter. |
| Confused preview/assets with working source | 0 | No screenshots/assets/previews were treated as working source. |

---

## 4. Timeline

### CourseCam / TrailSpotter recording planning

David asked whether TrailSpotter could support GoPro-style course cameras, auto bookmarks, replay export, OBS/Medal workflows, multiplayer target handling, and career-mode compatibility.

The chat provided architecture guidance:

- Build the camera recorder as a separate CourseCam addon first.
- Use BeamNG replay files as simulation sources and OBS/Medal as video/audio capture tools.
- Save bookmarks during gameplay and export camera passes later.
- Treat the original OBS/Medal race recording as the master audio timeline.
- Keep TrailSpotter separate until the CourseCam prototype proves itself.

No files were created. No code was edited. No ZIP was packaged.

### Version/catalog guidance

David asked: `what ver are we on?`

The chat answered from remembered RedFox catalog context and stated that CourseCam had not been officially assigned a number or version yet, suggesting:

- `RedFox CourseCam Recorder`
- `v0.0.1 Prototype`
- tentative catalog label: `24-RedFox_CourseCam_Recorder_v0_0_1_PROTOTYPE`

The answer included the caveat that the number was tentative and should be locked before packaging. However, the chat did not check GitHub master coordination files before giving this guidance. That is the matching coordination failure.

### Career-mode UI planning

David corrected that the UI was GM UI, not WE UI.

The chat accepted the correction and revised the plan to a GM UI module rather than F11/World Editor dependency. No code was changed.

---

## 5. Evidence details

### Violation 1 — GitHub/project coordination miss

- **Approximate date/time:** 2026-07-08, during CourseCam / TrailSpotter planning.
- **What David asked for:** version/status guidance for the new recording/camera system.
- **What the assistant did:** answered from project memory and conversation context, using tentative catalog/version planning.
- **What should have happened:** before assigning or suggesting a RedFox number/version, the chat should have checked `redfoxtrystman/RedFox_Master_Control` or any relevant coordination/status files to avoid conflict with current RedFox module numbering and directives.
- **Rule violated:** RedFox GitHub coordination rule from the all-chats audit directive: check GitHub coordination files when project/module/version coordination is required.
- **Build first failed:** none. No build was created.
- **Last known good build:** not applicable in this chat. No CourseCam build exists here.
- **Evidence exists:** conversation messages show version/catalog guidance was given before this audit and before reading GitHub incident directives in this chat.

---

## 6. Last known good / first bad / current safe point

- **Last known good build:** Not applicable. This chat produced no CourseCam build and no TrailSpotter build.
- **First known bad build:** Not applicable. No build was produced.
- **Current safest rollback point:** No rollback needed from this chat. The safe point is planning-only state before any CourseCam code is created.
- **Unknowns that still require David testing:** All runtime behavior remains unproven: camera placement, trigger detection, bookmark saving, replay export, OBS automation, Medal workflow, multiplayer detection, career-mode compatibility.

---

## 7. Recovery requirements before any new build

Before creating the first CourseCam / TrailSpotter addon ZIP, the chat must:

1. Check the RedFox master coordination repository for current catalog numbering, status files, naming rules, and incident directives.
2. Identify whether CourseCam should be standalone or formally nested under TrailSpotter.
3. Identify the baseline files if TrailSpotter or any camera mod is uploaded.
4. Check baseline source before editing.
5. Make only the requested minimal prototype change.
6. Check edited source after changes.
7. Package the ZIP only after the edited source is inspected.
8. Reopen the final ZIP and inspect actual packaged contents.
9. Label all verification accurately as static-only unless David tests it in BeamNG.
10. Avoid labels like Real, Working, Fixed, Live, Complete, Final, Proven, Ready, Extender, or Mirror unless that exact status is proven.

---

## 8. Before-edit / after-edit / after-ZIP check status

- **Before-edit code check actually performed:** Not applicable. No code edit occurred.
- **After-edit code check actually performed:** Not applicable. No code edit occurred.
- **After-ZIP check actually performed:** Not applicable. No ZIP was created.
- **Verification language overclaimed what was actually proven:** No delivered-build verification language was used. The one failure was coordination: answering tentative numbering/version planning without checking GitHub first.

---

## 9. Accountability statement

This failure did not come from unclear user instructions. David had already established a RedFox GitHub coordination system and then directly pointed this chat to the audit directive. The specific miss was that the chat gave tentative CourseCam version/catalog guidance before checking the GitHub coordination source.

No code was broken and no ZIP was falsely verified in this chat, but the coordination failure is recorded because the rules already existed.

Signed,

**Sol / CourseCam-TrailSpotter planning chat**

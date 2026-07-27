# Required Version and GitHub Order of Operations

**Effective:** 2026-07-27  
**Applies to:** every RedFox project job and chat

This process is mandatory. A chat must not hand a new build to David and then document it later as an afterthought.

## 1. Read before work

Before editing or building:

1. Read the job's canonical status file.
2. Read the job's latest runtime result.
3. Identify the exact current source commit and artifact hash.
4. Confirm the job number, module ID, and ownership boundaries.
5. Confirm that another chat has not already reserved the next version.

## 2. Reserve a unique version

- Use one version number for one immutable source state.
- Never reuse a released, packaged, handed-off, documented, or quarantined version number.
- Even a small code change after packaging requires another version.
- Record the reserved version in the job issue before packaging when multiple chats could overlap.

## 3. Preserve full source first

Before creating the user ZIP:

1. Commit the complete unpacked source snapshot for the new version.
2. Include every runtime file, UI file, manifest, JSON file, and owned asset required to build it.
3. Do not rely only on a prose source summary.
4. Do not rely only on a patch when the exact base source is absent.
5. Do not place stock BeamNG/RLS files into the job source unless the owner explicitly approved a coordinated override.

The source commit SHA becomes the release's source identity.

## 4. Build from committed source

- Package the ZIP only from the committed source snapshot.
- Do not make uncommitted edits between source commit and packaging.
- Record the exact build command or packaging procedure when applicable.

## 5. Verify before handoff

Required checks, as applicable:

- ZIP integrity;
- duplicate ZIP entries;
- JSON parsing;
- Lua syntax and main-chunk local limit;
- protected-path scan;
- unintended stock/RLS override scan;
- direct per-frame logging/write scan;
- file inventory;
- expected module/version strings;
- artifact size;
- SHA-256.

Static verification does not equal runtime verification.

## 6. Create one authoritative release manifest

Before giving the download to David, commit one release manifest containing:

- job number and title;
- version;
- filename;
- source commit SHA;
- ZIP SHA-256;
- size;
- exact changes;
- known limits;
- static-verification result;
- runtime status;
- focused test gate;
- rollback instructions;
- previous version/hash.

Multiple supporting documents are allowed, but one manifest must be authoritative.

## 7. Update GitHub issue before delivery

Before the user-facing download message:

1. Update the job issue with the release manifest path and commit SHA.
2. State the exact status, normally `BUILT — RUNTIME UNTESTED`.
3. State the exact focused test.
4. State which prior build is replaced, rejected, or still current.

Only after this issue update is complete may the ZIP be handed to David.

## 8. User-facing delivery

The chat response must include:

- exact version and filename;
- download link;
- SHA-256;
- status;
- focused test only;
- stop conditions;
- no claims of runtime success before David tests it.

## 9. Runtime result before next version

After David tests:

1. Record pass, partial, failure, or blocked status against the exact ZIP hash.
2. Record screenshots/log evidence and the observed behavior.
3. Update the canonical job status.
4. Mark failed paths `FAILED — STOPPED` rather than quietly replacing them.
5. Do not begin the next version until this result is in GitHub, unless David explicitly authorizes an emergency hotfix.

## 10. Required status labels

Use only clear evidence-based labels:

- `DAVID-TESTED WORKING`
- `BUILT — RUNTIME UNTESTED`
- `PARTIAL`
- `BLOCKED`
- `FAILED — STOPPED`
- `PROVENANCE CONFLICT — QUARANTINED`
- `MOCKUP / PLACEHOLDER`

## 11. Incident handling

When the process is broken:

1. Stop creating new versions.
2. Preserve the current files.
3. Create an incident report.
4. Identify affected version numbers and hashes.
5. Quarantine ambiguous artifacts.
6. Correct the canonical status.
7. Resume with a new unused version number.

Never rewrite history to hide the failure.

## 12. Requirement discipline

- Do not treat jokes as approved features.
- Do not add adjacent ideas without owner approval.
- Do not invent behavior for BeamNG or RLS; inspect current source first.
- Separate direct owner requirements from suggestions and deferred concepts.
- When a requirement changes after testing, record the old approach as a tested failure rather than calling it disobedience unless it contradicted a prior explicit instruction.

## 13. Artifact durability

Chat sandbox paths are temporary distribution paths, not durable source control.

Every release must have durable GitHub provenance through:

- full source snapshot;
- release manifest;
- artifact hash;
- issue record.

A GitHub Release asset or other approved durable artifact store should be used for exact ZIP preservation when available. Until then, the repository must at minimum preserve full source and the complete release manifest so the ZIP can be reproduced.

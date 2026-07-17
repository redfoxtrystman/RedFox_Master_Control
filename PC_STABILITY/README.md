# PC Stability / Crash Monitor Coordination

**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**GitHub issue:** https://github.com/redfoxtrystman/RedFox_Master_Control/issues/6  
**Scope:** External PC stability investigation that affects BeamNG test reliability. This is not a BeamNG feature job and does not replace JOB-00 through JOB-12.

## Why this folder exists

David is experiencing serious PC crashes and broad USB/device reset events. A diagnostic application is being developed and left running to autosave evidence so the failure can be classified as hardware, software, driver, USB, storage, power, thermal, memory or mixed.

Permanent sanitized summaries, schemas, application notes, test matrices and reviewed diagnostic findings belong here. Large raw logs, crash dumps, machine images and private data should not be blindly committed.

## Communication lane

Every chat working on the PC problem must post its current status to:

```text
https://github.com/redfoxtrystman/RedFox_Master_Control/issues/6
```

Use this block:

```text
Chat/workstream name =
Date and time =
Current application/build version =
Exact files or ZIPs inspected =
Exact files changed =
What was added or fixed =
What has been tested =
What has not been tested =
Observed crashes/errors/device resets =
Relevant timestamps =
Logs/reports produced =
Hardware/software hypothesis =
Confidence and evidence =
Known risks =
Next action =
What David must test or preserve =
```

## Permanent record paths

Suggested structure:

```text
PC_STABILITY/
├── README.md
├── STATUS/
├── APP_SOURCE_NOTES/
├── TEST_PLANS/
├── FINDINGS/
├── INCIDENT_TIMELINES/
└── TEMPLATES/
```

Chats may create subfolders as needed but must not mix BeamNG mod packages into this lane.

## File identity rules

For every monitor build, report bundle or relevant archive, record:

```text
Exact filename
Version
Archive byte size
SHA-256
ZIP integrity
Build/source baseline
Date created
David-tested status
Known limitations
```

Do not claim a build is working until David runs that exact build.

## Privacy and safety

Before committing logs or reports, remove or redact:

- passwords and authentication tokens;
- API keys;
- browser history unrelated to diagnosis;
- private documents and email contents;
- full home address or unrelated personal identifiers;
- license keys and serial numbers not required for diagnosis;
- memory dumps that may contain private data unless specifically reviewed and sanitized.

Raw Windows dumps and large binary logs should remain with David unless a reviewed excerpt or summary is necessary.

## Diagnostic evidence to correlate

The investigation should correlate exact timestamps across:

- application autosaves;
- Windows System and Application events;
- WHEA hardware errors;
- Kernel-Power events;
- USB/controller resets;
- disk/storage warnings;
- SMART/NVMe health;
- memory test results;
- CPU/GPU temperatures and power;
- driver crashes;
- display resets;
- BeamNG logs;
- device disconnect/reconnect counts;
- fresh-Windows or alternate-drive testing;
- isolated-drive and isolated-USB testing.

## Truth rules

- A full PC crash does not automatically prove a BeamNG mod is broken.
- A test interrupted by a full PC crash cannot be counted as a pass.
- Eighteen devices disappearing together suggests a shared controller, hub, power, driver or system-level event, but it does not identify the cause by itself.
- A fresh Windows test may distinguish software from hardware, but it must be performed without destroying the current diagnostic evidence.
- Hardware and software causes may coexist.
- State confidence and evidence; do not present guesses as conclusions.

## Coordinator restart action

When David returns, JOB-00 — Coordinator / Integration / Verification should:

1. read issue #6 and all new comments;
2. inventory the latest monitoring application build;
3. review autosaved reports and exact crash timestamps;
4. identify the earliest common failing layer;
5. separate confirmed evidence from hypotheses;
6. decide which controlled test should happen next;
7. record whether the PC is reliable enough for long BeamNG integration tests.

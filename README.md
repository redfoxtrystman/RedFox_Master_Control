# RedFox Master Control

This repository is the shared coordination bridge for David's RedFox/FoxNet BeamNG rebuild.

---

## One File First

Every RedFox chat must start with:

```text
RedFox_Worker_Chat_Quick_Start.md
```

For the FoxNet JOB-00 through JOB-12 rebuild, that Quick Start immediately directs the chat to the current end-to-end pipeline:

```text
PROJECT_MANIFESTS/READ_FIRST_REDFOX_END_TO_END_JOB_PIPELINE_2026-07-14.md
```

The pipeline establishes the current owner law:

```text
Backend first through WEUI/test harness
Website integration second
One shared phone/PC destination through JOB-01
Shared Career/RLS actions through JOB-02
QA through JOB-11
Final assembly through JOB-00
```

David should not have to explain the entire system to every replacement chat.

---

## Main Communication Rule

Reading the repository is not enough. Every worker chat must leave a written footprint by doing one of these:

```text
1. Update RedFox_Chat_Message_Board.md directly, or
2. Give David an exact message-board block so JOB-00 can post it.
```

If there is no message-board, claim, handoff, or audit entry, communication failed.

---

## Important Files

| File | Purpose |
|---|---|
| `RedFox_Worker_Chat_Quick_Start.md` | One-file start instructions for every chat. |
| `PROJECT_MANIFESTS/READ_FIRST_REDFOX_END_TO_END_JOB_PIPELINE_2026-07-14.md` | Current A-to-R workflow, exact job ownership, backend-first WEUI rule, website integration, QA, and final assembly. |
| `PROJECT_MANIFESTS/REDFOX_JOB_PIPELINE_MANIFEST.json` | Machine-readable JOB-00 through JOB-12 ownership and release gates. |
| `PROJECT_MANIFESTS/TEMPLATES/REDFOX_JOB_HANDOFF_TEMPLATE.json` | Required machine-readable candidate handoff template. |
| `QA_LOGGING/validate_redfox_handoffs.py` | Automated job/handoff validator. |
| `.github/workflows/redfox-handoff-validation.yml` | GitHub Actions check for the central manifest and submitted handoffs. |
| `PROJECT_MANIFESTS/REDFOX_FOXNET_REBUILD_JOB_BOARD.md` | Detailed ownership board, status, protected paths, incidents, and dependencies. |
| `RedFox_Chat_Message_Board.md` | Shared communication board. Every chat must leave something here or return a block. |
| `RedFox_Master_Build_Control_Document.md` | Broader RedFox project rules, bridge contracts, module registry, and roadmap. |
| `RedFox_File_Verification_Checklist.csv` | Before/after file-editing checklist. |
| `RedFox_Test_Results_Table.csv` | BeamNG testing result tracker. |
| `RedFox_Module_Status_Table.csv` | Module status tracker. |
| `RedFox_Communication_SignIn_Log.md` | Detailed sign-in, work-update, and finish log. |

---

## Repo Rules

No worker chat may edit real BeamNG mods until its exact JOB number/title is clear and it has inspected the relevant source.

No feature website is treated as proof of backend behavior. Each feature backend must first be testable independently through a WEUI, native test panel, console action, or equivalent harness. The final website then calls the same proven backend functions.

No fake verification. No silent renames. No silent reads. No copied platform cores. No giant overlapping ZIP piles.

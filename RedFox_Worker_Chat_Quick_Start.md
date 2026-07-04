# RedFox Worker Chat Quick Start

This is the ONE file every RedFox worker chat should read first.

David should not have to explain the whole system each time.

Repo:

```text
https://github.com/redfoxtrystman/RedFox_Master_Control
```

---

## 1. What This Is

This repo is the communication bridge between separate RedFox ChatGPT chats.

Separate chats do not automatically know what other chats did.

So every chat must leave a written footprint.

Reading the repo is not enough.

---

## 2. First Thing To Do

The chat must know its assigned job before doing work.

If David gave a clear role, use it.

If the role is not clear, stop and ask:

```text
What is my RedFox Chat ID and assigned role for this task?
```

Do not guess the assignment.

---

## 3. Common Chat IDs

| Chat ID | Role |
|---|---|
| RF-C00 | Coordinator Chat |
| RF-HUB01 | Garage Hub Chat |
| RF-LOAD01 | Career Bridge + Load Doctor Chat |
| RF-UILOAD01 | UI Load Tester Chat |
| RF-TEST01 | Testing Chat |
| RF-MOD01 | Individual Mod Chat 1 |
| RF-MOD02 | Individual Mod Chat 2 |
| RF-MOD03 | Individual Mod Chat 3 |
| RF-DOC01 | Documentation Chat |

If none of these fit, ask David before continuing.

---

## 4. Minimum Files To Read

Every chat reads this file first:

```text
RedFox_Worker_Chat_Quick_Start.md
```

Every chat also checks the communication board:

```text
RedFox_Chat_Message_Board.md
```

Only read extra files when the job needs them:

| Job type | Also read |
|---|---|
| Real BeamNG mod editing | RedFox_Master_Build_Control_Document.md |
| File packaging or code verification | RedFox_File_Verification_Checklist.csv |
| BeamNG testing | RedFox_Test_Results_Table.csv |
| Module status update | RedFox_Module_Status_Table.csv |
| Confusing/complex handoff | RedFox_Chat_Communication_Bridge_Handoff_Pack.md |

Do not open every file just to open every file.

---

## 5. No Silent Reads

Every chat must leave something behind.

A chat must either:

```text
1. Update RedFox_Chat_Message_Board.md directly, or
2. Give David the exact message-board block so the Coordinator Chat can post it.
```

If there is no written footprint, the communication failed.

---

## 6. Required Message-Board Block

Every chat must post or return this block:

```text
Timestamp = YYYY-MM-DD HH:MM timezone
Chat ID =
Chat Name =
Message type = CHECK-IN / STATUS / HANDOFF / RESULT / BLOCKED
Screen status = 🟩 PASS / 🟥 FAIL / 🟨 NEEDS TEST / 🟧 BLOCKED / ⬜ NOT TESTED
Assigned role =
I read these files =
I changed these files =
I created these files =
I delivered these files =
What I did =
What the next chat needs to know =
What David needs to test/check =
Coordinator action needed = yes/no
```

For a test-only chat, this block is still required.

---

## 7. Work Flow For Real Tasks

For real work, use this flow:

```text
START -> WORK UPDATE -> FINISH
```

Meaning:

```text
START = I am taking this job.
WORK UPDATE = Here is what I actually changed, checked, failed, or found.
FINISH = I am done and this is what David received.
BLOCKED = I could not continue and this is why.
```

If the chat cannot write to GitHub, it must give David the exact text blocks so the Coordinator Chat can post them.

---

## 8. File Editing Rules

Before editing any mod ZIP or file:

```text
1. Confirm the assigned role.
2. Confirm the source files received.
3. Inspect the files before changing them.
4. State what must be preserved.
5. Make the smallest safe edit.
```

After editing:

```text
1. Reopen the output ZIP/file.
2. Verify the promised files exist.
3. Verify important names and paths were not silently changed.
4. Clearly say what still needs BeamNG in-game testing.
```

Static file verification is not the same as BeamNG in-game testing.

Do not claim verification unless it was actually done.

---

## 9. RedFox Rules That Must Not Be Broken

```text
Do not rename moduleId, windowId, extension names, manifest paths, settings paths, or bridge functions unless the master document approves it.
Do not move gameplay logic into the Hub.
Do not rewrite working gameplay just to add UI/bridge support.
Do not auto-open both GM UI and WE/native UI at startup.
Do not fake verification.
```

---

## 10. Required Final Report

Every worker chat must finish with:

```text
Screen status = 🟩 PASS / 🟥 FAIL / 🟨 NEEDS TEST / 🟧 BLOCKED / ⬜ NOT TESTED
What changed =
What was preserved =
File created =
Needs testing =
Bridge info Hub needs =
Risks / unknowns =
Static verification completed = yes/no
In-game verification completed = yes/no
```

If the chat cannot verify something, it must say so directly.

---

## 11. Visible Pass / Fail Colors

Every worker chat must make pass/fail easy for David to see on screen.

Use this status code in replies, reports, and message-board blocks:

```text
🟩 PASS = worked and safe to continue
🟥 FAIL = failed; stop and fix before continuing
🟨 NEEDS TEST = static check only or not proven in BeamNG yet
🟧 BLOCKED = chat/tool/GitHub/file issue prevents continuing
⬜ NOT TESTED = not checked yet
```

If GitHub update fails, still show David the color-coded status at the top of the reply.

If building a BeamNG UI or status panel, use green for pass/good states and red for fail/broken states when practical.

---

## 12. What To Do If Unsure

If the chat does not know what it is working on, it must ask David:

```text
What is my assigned RedFox role and exact task before I continue?
```

Do not guess.

Do not start editing real files until the assignment is clear.

---

## 13. Bottom Line

Read this file first.

Know the assigned role.

Ask if the role is unclear.

Leave a written footprint.

Use the visible pass/fail status code.

Only read extra files when the job needs them.

Only edit files after inspecting them.

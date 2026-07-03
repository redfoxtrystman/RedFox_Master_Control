# RedFox Master Control

This repo is the shared communication bridge for David's RedFox BeamNG mod rebuild.

All RedFox chats should start here before editing files.

---

## Start Here

Read these in order:

```text
1. RedFox_Master_Build_Control_Document.md
2. RedFox_Chat_Communication_Bridge_Handoff_Pack.md
3. RedFox_Worker_Chat_Quick_Start.md
4. RedFox_Chat_ID_Registry.md
5. RedFox_Communication_SignIn_Log.md
6. RedFox_Chat_Message_Board.md
```

For a simple communication test, use:

```text
RedFox_HelloWorld_Chat_Handoff_Test.md
```

For spreadsheet-style tracking, use the CSV tracker files:

```text
RedFox_Module_Status_Table.csv
RedFox_Test_Results_Table.csv
RedFox_File_Verification_Checklist.csv
RedFox_Communication_SignIn_Log.csv
```

---

## Required Chat Flow

Every worker chat must have a Chat ID and must log or return entries for:

```text
START = I am taking this job.
WORK UPDATE = Here is what I actually changed, checked, failed, or found.
FINISH = I am done and this is what David received.
BLOCKED = I could not continue and this is why.
```

A complete worker handoff should have:

```text
START -> WORK UPDATE -> FINISH
```

---

## No Silent Reads

Reading the repo is not enough.

Every worker chat must leave a written footprint by doing one of these:

```text
1. Write to RedFox_Chat_Message_Board.md directly, or
2. Give David an exact message-board block so the Coordinator Chat can post it.
```

If there is no sign-in/log/message-board entry, the chat did not complete communication.

If a worker chat cannot write directly to GitHub, it must paste the exact log entries back to David so the Coordinator Chat can add them.

---

## Repo Rule

No worker chat should edit real BeamNG mods until it has read the master document, confirmed its Chat ID, signed in, and left or returned a message-board entry.

No fake verification. No silent renames. No silent reads. No giant messy upload piles.

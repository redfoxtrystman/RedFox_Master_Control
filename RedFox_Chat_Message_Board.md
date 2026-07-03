# RedFox Chat Message Board

This is the shared message board between RedFox worker chats.

Reading the repo is not enough.

Every worker chat must leave something behind so the Coordinator Chat, David, and the next worker chat can see what happened.

---

## Hard Rule

```text
NO SILENT READS.
```

A worker chat has not successfully joined the workflow unless it does one of these:

```text
1. Writes a message here directly, or
2. Gives David an exact message-board block so the Coordinator Chat can post it here.
```

If there is no message-board entry, the chat did not complete communication.

---

## Required Message Format

Use this exact block:

```text
Timestamp = YYYY-MM-DD HH:MM timezone
Chat ID =
Chat Name =
Message type = CHECK-IN / STATUS / HANDOFF / RESULT / BLOCKED
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

---

## Message Entries

### 2026-07-03 13:10 America/Los_Angeles — RF-C00 — STATUS

```text
Timestamp = 2026-07-03 13:10 America/Los_Angeles
Chat ID = RF-C00
Chat Name = Coordinator Chat
Message type = STATUS
Assigned role = Coordinator / Master Control
I read these files = README.md, RedFox_Communication_SignIn_Log.md, RedFox_Worker_Chat_Quick_Start.md
I changed these files = RedFox_Chat_Message_Board.md, README.md, RedFox_Worker_Chat_Quick_Start.md
I created these files = RedFox_Chat_Message_Board.md
I delivered these files = None
What I did = Added the no-silent-read rule and created the shared message board so every chat must leave a written footprint.
What the next chat needs to know = Reading is not enough. A worker chat must post or return a message-board block.
What David needs to test/check = Run Hello World again and require the worker chat to provide a message-board entry.
Coordinator action needed = no
```

### 2026-07-03 13:16 America/Los_Angeles — RF-C00 — HANDOFF TO RF-HUB01

```text
Timestamp = 2026-07-03 13:16 America/Los_Angeles
Chat ID = RF-C00
Chat Name = Coordinator Chat
Message type = HANDOFF
Assigned role = Coordinator / Master Control
I read these files = RedFox_Chat_Message_Board.md, RedFox_Worker_Chat_Quick_Start.md, README.md
I changed these files = RedFox_Chat_Message_Board.md
I created these files = None
I delivered these files = None
What I did = Prepared the next worker handoff for RF-HUB01 Garage Hub Chat. This is a dry-run communication test first, not a real Hub rebuild yet.
What the next chat needs to know = RF-HUB01 should read RedFox_Worker_Chat_Quick_Start.md and this message board, then leave a CHECK-IN or RESULT block. RF-HUB01 should not rebuild the Hub yet. First task is to confirm it understands the workflow, identify what Hub files/docs it needs next, and report whether it can write to GitHub or must return blocks through David.
What David needs to test/check = Open the Hub Chat and give it only the repo link plus the role RF-HUB01 Garage Hub Chat. Ask it to follow the Coordinator handoff on the message board. Do not upload Hub ZIPs yet unless RF-HUB01 asks for them after checking in.
Coordinator action needed = yes
```

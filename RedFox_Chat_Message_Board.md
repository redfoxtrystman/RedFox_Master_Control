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

### 2026-07-03 13:25 America/Los_Angeles — RF-HUB01 — CHECK-IN

```text
Timestamp = 2026-07-03 13:25 America/Los_Angeles
Chat ID = RF-HUB01
Chat Name = Garage Hub Chat
Message type = CHECK-IN
Assigned role = Garage Hub Chat / RedFox Garage Hub workflow owner
I read these files = RedFox_Worker_Chat_Quick_Start.md, RedFox_Chat_Message_Board.md
I changed these files = RedFox_Chat_Message_Board.md
I created these files = None
I delivered these files = None
What I did = Confirmed RF-HUB01 identity, read the required quick start and Coordinator handoff, and successfully wrote this check-in to the shared message board.
What the next chat needs to know = RF-HUB01 understands the no-silent-read workflow and can write to GitHub directly. RF-HUB01 will not rebuild the Hub yet. Next step is for David/Coordinator to provide the current Hub ZIP and the master bridge/handoff documents when real Hub work begins.
What David needs to test/check = Confirm this CHECK-IN appears in RedFox_Chat_Message_Board.md. Then provide Hub files only when ready for actual Hub inspection or rebuild planning.
Coordinator action needed = no
```

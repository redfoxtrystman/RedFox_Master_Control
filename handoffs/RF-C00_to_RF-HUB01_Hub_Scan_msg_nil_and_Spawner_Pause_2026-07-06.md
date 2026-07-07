# RF-C00 to RF-HUB01 Handoff — Hub Scan msg() nil + Spawner Pause

```text
Timestamp = 2026-07-06 19:00 America/Los_Angeles
Chat ID = RF-C00
Chat Name = Coordinator / Spawner support chat
Message type = HANDOFF
Screen status = 🟧 BLOCKED
Assigned role = Coordinator handoff for RF-HUB01 Garage Hub Chat
I read these files = RedFox_Worker_Chat_Quick_Start.md, RedFox_Chat_Message_Board.md
I changed these files = handoffs/RF-C00_to_RF-HUB01_Hub_Scan_msg_nil_and_Spawner_Pause_2026-07-06.md
I created these files = handoffs/RF-C00_to_RF-HUB01_Hub_Scan_msg_nil_and_Spawner_Pause_2026-07-06.md
I delivered these files = GitHub handoff file only; no BeamNG ZIP build delivered from this step
What I did = Captured David's current Hub failure context and the Spawner pause/recovery context so RF-HUB01 can fix Hub scan routing first before more Spawner work stacks on top.
What the next chat needs to know = Hub loads in Career after rollback, but clicking Scan causes: lua/ge/extensions/redfox/modulesHub.lua:276 attempt to call global 'msg' (a nil value). Needed fix: scanRedFoxModules must define msg(), replace msg() with the Hub-safe logger/status function, or guard it so missing msg cannot fatal. After fixing, retest Scan with RF-UILOAD01_Discoverable_Dummy_v0_1_2.zip. Do not move gameplay into the Hub. Do not rename moduleId/windowId/extension names unless approved. Do not fake BeamNG verification.
What David needs to test/check = After RF-HUB01 creates the Hub fix, install only the corrected Hub plus RF-UILOAD01_Discoverable_Dummy_v0_1_2.zip and test Hub > Scan in Career. Confirm no fatal Lua error and confirm the dummy module appears/discovery result is reported.
Coordinator action needed = yes
```

## Required starting instructions for RF-HUB01

```text
You are a RedFox worker chat.

Start with:
RedFox_Worker_Chat_Quick_Start.md

Then check:
RedFox_Chat_Message_Board.md

If you are updating module status, update:
RedFox_Module_Status_Table.csv

If you are logging test results, update:
RedFox_Test_Results_Table.csv

If you found useful research/info, update:
RedFox_Research_Findings_Log.csv

If you changed or created a build, leave a message in:
RedFox_Chat_Message_Board.md
```

## Required status format

```text
Screen status = 🟩 PASS / 🟥 FAIL / 🟨 NEEDS TEST / 🟧 BLOCKED / ⬜ NOT TESTED
Timestamp =
Chat ID =
Chat Name =
Message type =
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

## Hard rules for RF-HUB01

```text
Do not silently read.
Do not fake verification.
Do not rename moduleId/windowId/extension names unless approved.
Do not move gameplay into the Hub.
If GitHub update fails, give David the exact block so RF-C00 Coordinator can post it.
```

## Current Hub problem

```text
Current issue:
Hub loads in Career after rollback, but clicking Scan causes:

lua/ge/extensions/redfox/modulesHub.lua:276
attempt to call global 'msg' (a nil value)

Needed:
Fix scanRedFoxModules so msg() is defined, replaced, or guarded.
Then retest Scan with:
RF-UILOAD01_Discoverable_Dummy_v0_1_2.zip
```

## Spawner context — paused until Hub is stable

Spawner work is currently on hold because Hub errors can make Spawner/Hub integration testing unreliable.

Current Spawner direction after Hub is fixed:

```text
1. Do not stack more Spawner edits until Hub scan error is fixed or proven unrelated.
2. GM UI should be separated and restored, not expanded further.
3. WE/native UI should own settings.
4. GM UI should become compact: spawn buttons + catalog entry only.
5. Blocker must be restored without black-screen overlay and without giant RF logo.
6. Catalog needs repair later.
7. Random Prop must be fixed with a strict prop whitelist so buses cannot spawn as props.
```

Known recent Spawner builds/context:

```text
v0.1.25 = Theme Hub inheritance fix / installed candidate.
v0.1.26 = Local theme restore / solid GM background attempt.
v0.1.27 = opacity controls / separate settings / bigger blocker.
v0.1.28 = hard solid theme / shared GM blocker attempt.
v0.1.29 = compact GM / WE blocker restore attempt.
Current hold point = v0.1.29 paused until Hub error is verified.
```

Integration notes for Hub ↔ Spawner later:

```text
Hub should call Spawner through redfox_spawner.
Hub should treat spawner and redfox_spawner as aliases if old UI labels still use spawner.
Hub should not assume showSpawnOverlay exists.
Use openGameUI(), openWindow(), or direct action calls such as randomVehicle(), freakVehicle(), randomConfig(), freakConfig(), randomPaint(), specialPaint() when those functions exist.
Hub should not force glass/global theme onto Spawner unless Spawner explicitly allows Hub theme inheritance.
Hub should not move Spawner gameplay logic into the Hub.
```

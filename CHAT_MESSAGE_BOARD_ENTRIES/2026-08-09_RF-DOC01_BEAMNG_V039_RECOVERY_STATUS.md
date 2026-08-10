# RF-DOC01 BeamNG v0.39 Recovery Message Board Block

```text
Screen status = 🟨 NEEDS TEST
Timestamp = 2026-08-09 23:10 America/Los_Angeles
Chat ID = RF-DOC01
Chat Name = Codex Local Research Chat
Message type = STATUS / RECOVERY PLAN
Assigned role = Local BeamNG v0.39 scanner / RedFox recovery coordinator support
I read these files = AGENTS.md; PROJECT_HANDOFF.md; CHATGPT_EXPORTS/CODEX_FIRST_MESSAGE.txt; RedFox_Worker_Chat_Quick_Start.md; RedFox_Chat_Message_Board.md; RedFox_Research_Findings_Log.csv; PROJECT_MANIFESTS/00_READ_FIRST_ALL_CHATS_CORE_UI_OVERRIDE_BAN_2026-07-22.md; INCIDENT_REPORTS/ALL_REDFOX_CHATS_AUDIT_DIRECTIVE_2026-07-07.md; official BeamNG v0.39 release notes; local BeamNG v0.39 Vue mod README; current beamng.log; current mods db.json; keyboard.diff
I changed these files = RedFox_Research_Findings_Log.csv
I created these files = RESEARCH_REPORTS/BEAMNG_V039_REDFOX_RECOVERY_REPORT_2026-08-09.md; INCIDENT_REPORTS/2026-08-09_Codex_TowFoxNet_Merge_Order_Of_Operations_Failure.md; CHAT_MESSAGE_BOARD_ENTRIES/2026-08-09_RF-DOC01_BEAMNG_V039_RECOVERY_STATUS.md
I delivered these files = Local report folder D:\RedFoxMods\reports\beamng_v039_update_scan_20260809; GitHub recovery report; GitHub incident report; GitHub research-log update
What I did = Per David's new recovery goal, performed a read-only BeamNG v0.39 scan. Confirmed BeamNG is now 0.39.4.0 build 20972. Found v0.39's official Vue UI mod path /ui/ui-vue/mods. Found that current BeamNG.drive\mods no longer contains rf current mods temp--------, but current user db.json still marks 16 RedFox entries from that missing folder active. Latest log shows redfoxCareerWeb.js 404, Project 43 core_redfoxPlayerMovementLab fatal, many missing RedFox input actions, Garage Hub manifest jsonReadFile failures, and RLS 2.7.0 phone layout / legacy ui/modModules risk. Also filed an incident report for my failed broad Tow/FoxNet merge so other chats do not repeat it.
What the next chat needs to know = Do not start from scratch. Do not patch ui/ui-vue/dist/index.js. Do not install multiple versions of one RedFox mod. Do not make another broad Tow/FoxNet merge. For v0.39 web recovery, use a small /ui/ui-vue/mods/redfoxCareerWeb adapter and one shared data provider. First back up and control user cache/db/inputmaps/settings, then test one RedFox lane at a time. Start with GarageHub + RaceBuilder or the exact David-approved target.
What David needs to test/check = After backup/cache cleanup and controlled reinstall, David needs to test BeamNG with a minimal RedFox set and report whether boot, hotkeys, Hub scan, RaceBuilder UI, and web/phone routes load. Runtime remains awaiting_user_test until David tests in BeamNG.
Coordinator action needed = yes
```

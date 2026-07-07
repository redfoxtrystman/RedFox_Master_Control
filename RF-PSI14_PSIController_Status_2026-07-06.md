# RF-PSI14 — RedFox PSI Controller Status Note

```text
Screen status = 🟨 NEEDS TEST
Timestamp = 2026-07-06 20:45 America/Los_Angeles
Chat ID = RF-PSI14
Chat Name = PSI Controller / RedFox Tire Control Chat
Message type = STATUS
Assigned role = RedFox PSI Controller standalone/career-safe tire module worker chat
I read these files = RedFox_Worker_Chat_Quick_Start.md, RedFox_Chat_Message_Board.md, RedFox_Module_Status_Table.csv, RedFox_Test_Results_Table.csv
I changed these files = RedFox_Module_Status_Table.csv, RedFox_Test_Results_Table.csv
I created these files = RF-PSI14_PSIController_Status_2026-07-06.md
I delivered these files = 14-RedFox_PSIController_v0_1_7_SealKitDefaults.zip in chat only; not uploaded to repo
What I did = Checked in as the PSI/Tire Control worker chat. Current PSI build focus is standalone/career-worthy RedFox Tire Control, not Hub integration yet. v0.1.7 adds Seal Kit presets: Realistic / 1 repair, Extended / 2 repairs, Trail Kit / 3 repairs, Expedition Kit / 4 repairs, Arcade / 5 repairs, Cheat / Infinite. Rim Race Assist is OFF by default and marked experimental. The Hub UI jump was rolled back; Hub/WE bridge should wait until standalone tire behavior passes.
What the next chat needs to know = Do not move tire gameplay into the Hub. Hub or Command Center should only call exposed PSI status/command functions later. Planned external Command Center bridge should expose status like current PSI per wheel, tire state, self-sealing state, seal kit mode, and selected wheel, plus commands like setFrontPSI, setRearPSI, repairSelected, repairAllFlats, toggleSelfSealing, selectWheel. Do not require the in-game PSI UI to be visible for external control once the bridge exists.
What David needs to test/check = Disable all older RedFox PSI/Tire Control zips and test only 14-RedFox_PSIController_v0_1_7_SealKitDefaults.zip. Report: PSI works after respawn yes/no; Self-Sealing stops hiss yes/no; green sealant stops yes/no; Repair Selected works yes/no; Rim Race Assist breaks vehicle yes/no. Test Freeroam first, then Career.
Coordinator action needed = yes
```

## Current Hub-side note

Hub still has the known scanner blocker reported elsewhere: Career loads after rollback, but Scan can crash because `lua/ge/extensions/redfox/modulesHub.lua` calls missing `msg()`. RF-HUB01 should fix or guard that helper before PSI or other real modules are connected through Hub scanning.

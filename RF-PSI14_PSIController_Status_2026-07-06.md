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
What the next chat needs to know = Do not move tire gameplay into the Hub. Hub or Command Center should only call exposed PSI status/command functions later. Planned external Command Center bridge should expose status like current PSI per wheel, tire state, self-sealing state, seal kit mode, and selected wheel, plus commands like setFrontPSI, setRearPSI, repairSelected, repairAllFlats, toggleSelfSealing, selectWheel. Do not require the in-game PSI UI to be visible for external control once the bridge exists. Multi-wheel/trailer tire detection is mandatory roadmap work; see roadmap note below.
What David needs to test/check = Disable all older RedFox PSI/Tire Control zips and test only 14-RedFox_PSIController_v0_1_7_SealKitDefaults.zip. Report: PSI works after respawn yes/no; Self-Sealing stops hiss yes/no; green sealant stops yes/no; Repair Selected works yes/no; Rim Race Assist breaks vehicle yes/no. Test Freeroam first, then Career. Also test at least one vehicle with more than 4 tires and one trailer/towed vehicle when available.
Coordinator action needed = yes
```

## Current Hub-side note

Hub still has the known scanner blocker reported elsewhere: Career loads after rollback, but Scan can crash because `lua/ge/extensions/redfox/modulesHub.lua` calls missing `msg()`. RF-HUB01 should fix or guard that helper before PSI or other real modules are connected through Hub scanning.

## Roadmap note — multi-wheel / trailer tire detection

RedFox PSI Controller must support more than normal 4-wheel vehicles. David wants support for vehicles/trailers with 2, 3, 4, 6, 8, 10+ tires and trailer/towed wheel groups when BeamNG exposes them. This matters for tire-only removal, full wheel/rim removal, rim racing, dragging trailers without tires, and external Command Center tire maps.

Current code check from v0.1.7 package shows the vehicle-side tire core already contains a wheel layout scanner and labeler:

- `buildWheelLayout()` exists.
- `sendWheelLayout()` exists.
- 2-wheel labeling exists as `F / R`.
- 3-wheel labeling exists as `F / RL / RR` or `FL / FR / R`.
- 4+ wheel sorting/labeling exists.
- Dually/heavy labels such as `RRL / RRR` are supported.
- Trailer-ish names such as `T...` / `TRAILER...` and wheel1L/wheel1R/wheel2L/wheel2R patterns have partial handling.

Risk: David has only tested 4-wheel vehicles so far. Multi-wheel and trailer behavior is static-code-present but not proven in BeamNG runtime. UI needs to stay scroll-safe and button-size adaptive when many tires are detected.

Required future test cases:

1. Normal 4-wheel car/truck.
2. 3-wheeled vehicle.
3. 6x6 or dually truck.
4. Bus/dump/semi/heavy vehicle with more than 4 tires.
5. Trailer/towed vehicle with 2/4/6 tires if Beam exposes those wheels to the active vehicle/mod interface.

Required future UI behavior:

- Tire buttons must shrink or wrap cleanly when many wheels exist.
- Full list must scroll if there are too many tires.
- Button labels must remain readable: FL, FR, RL, RR, RRL, RRR, F, R, trailer labels, or safe fallback labels.
- Missing/nonexistent tire buttons must not appear.
- Selecting one tire must never retarget another wheel.
- Trailer wheels must not remove truck wheels and truck buttons must not remove trailer wheels.

Command Center/external bridge should eventually expose the full tire layout list returned by the scanner, not just front/rear PSI.

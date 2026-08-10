# RF-PSI14 v0.2.9 BeamNG 0.39 Hotfix Audit

Status: NEEDS TEST — static/package verification only

Input baseline: `14-RedFox_PSIController_v0_2_8_WorkingCode_CleanRelease.zip`
Input SHA-256: `b9175e31e4e9a0fea2c9a8bcd4a2d7815efc7744eadad14e6e12760bf987fa69`

Output ZIP: `14-RedFox_PSIController_v0_2_9_BeamNG039Hotfix.zip`
Output size: `58220` bytes
Output SHA-256: `cb1b3c97e3f6aaa48e033bbab24a5e5cfaaeda33ddab411f514f3de019edd2c3`
Final file count: `17`

## Why this patch exists

David reported the PSI mod does not work after the BeamNG v0.39 update. GitHub status said v0.2.8 was a rollback-clean package from v0.2.6. BeamNG v0.39 release notes say UI Apps were renamed to HUD Apps, the HUD Apps layout editor was ported to Vue, app hosting/hot reload changed, and Vue became the primary UI framework while legacy Angular screens remain supported through an Angular host.

## What I found in the code

1. Critical vehicle Lua bug: `setPressureGroupIdPa()` recursively called itself instead of calling BeamNG `obj:setGroupPressure(...)`. That can break PSI setting/repair when pressure change is requested.
2. Both HUD app folders were missing `app.png`. BeamNG's app creation documentation lists `app.png` as one of the three important app files and says it shows in the app selector. v0.39's new HUD Apps manager appears stricter/changed enough that missing app images are a compatibility risk.

## Changed files

- `lua/vehicle/extensions/auto/redfoxPSIController.lua`
- `ui/modules/apps/redfoxPSIController/app.json`
- `ui/modules/apps/redfoxPSIQuickControls/app.json`

## Added files

- `ui/modules/apps/redfoxPSIController/app.png`
- `ui/modules/apps/redfoxPSIQuickControls/app.png`

## Removed files

- None

## Verification results

- Final ZIP reopened/extracted: PASS
- `unzip -t`: PASS
- JSON validation: PASS
- Full GM UI JavaScript syntax: PASS
- Quick GM UI JavaScript syntax: PASS
- `setPressureGroupIdPa` recursion removed: PASS
- `obj:setGroupPressure(candidate, pa)` present: PASS
- `app.png` present for both HUD app folders: PASS
- No `mod_info/` folder added: PASS
- Lua runtime syntax not compiled because this environment has no Lua/luac. Static Lua checks only.

## Anti-spam scan

```json
{
  "setInterval": [],
  "requestAnimationFrame": [],
  "setTimeout(fetchStats)": [],
  "No wheels with pressure groups found": [],
  "pcall(function() setPressureGroupIdPa(groupId, pa) end)": []
}
```

## David test checklist

1. Disable all older PSI zips.
2. Install only v0.2.9.
3. Press F5/reload UI after enabling the mod because v0.39 has UI/HUD app changes.
4. Open Pause > System > HUD Apps and try adding RedFox Tire Control and RedFox PSI Quick Controls.
5. Click Refresh, then Set front/rear PSI on a normal vehicle.
6. Test A+ Gladiator tire PSI.
7. Test self-sealing repair and confirm hiss/green stops.
8. Let it sit idle 5–10 minutes and check console spam.

## Message board block for Coordinator

```text
Timestamp = 2026-08-10 12:11 America/Los_Angeles
Chat ID = RF-PSI14
Chat Name = PSI Controller Chat
Message type = RESULT / HANDOFF
Assigned role = PSI Controller owner
I read these files = RedFox_Module_Status_Table.csv, HANDOFFS/RF-PSI14_v0_2_8_WorkingCode_CleanRelease_Audit_2026-08-05.md, PROJECT_MANIFESTS/REDFOX_RELEASE_ZIP_CLEANUP_ROLLBACK_AMENDMENT_2026-08-05.md, BeamNG v0.39 release notes and app creation docs
I changed these files = RedFox_Module_Status_Table.csv
I created these files = HANDOFFS/RF-PSI14_v0_2_9_BeamNG039Hotfix_Audit_2026-08-10.md
I delivered these files = 14-RedFox_PSIController_v0_2_9_BeamNG039Hotfix.zip
What I did = Built v0.2.9 from David's uploaded v0.2.8 after BeamNG 0.39 broke the mod. Found and corrected a recursive pressure set bug in vehicle Lua and added app.png files to both HUD app folders for the new 0.39 HUD Apps manager. No mod_info folder added.
What the next chat needs to know = v0.2.9 is NEEDS TEST. It does not prove runtime. If HUD apps still do not appear, next step is a true v0.39 Vue Runtime UI mod route/app adapter, not another legacy Angular guess. If UI appears but PSI does not change, inspect BeamNG log for obj:setGroupPressure availability and pressure group candidates.
What David needs to test/check = Test only v0.2.9 with older PSI zips disabled. Reload UI/F5, open Pause > System > HUD Apps, add both RedFox HUD apps, click Refresh, Set PSI, test A+ Gladiator tires, self-seal, and no idle spam.
Coordinator action needed = yes
```

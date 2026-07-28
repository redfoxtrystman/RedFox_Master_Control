# RF-PSI14 — RedFox PSI Controller / RedFox Tire Control Full Handoff Roadmap

**Date/time created:** 2026-07-27 America/Los_Angeles  
**Chat ID:** RF-PSI14  
**Chat name:** PSI Controller / RedFox Tire Control Chat  
**Current working file delivered in chat:** `14-RedFox_PSIController_v0_2_3_CompactQuickUI.zip`  
**Current status:** 🟨 NEEDS TEST — static verification only  
**Primary goal:** Get 14-RedFox PSI Controller release-polished enough for David to share now, while keeping it career-safe/career-compatible first and avoiding background spam.

---

## 1. Immediate handoff summary

David is moving this workstream to a new chat because this chat is near its context limit.

The next chat should start by reading:

1. `RedFox_Worker_Chat_Quick_Start.md`
2. `RedFox_Chat_Message_Board.md`
3. `RedFox_Module_Status_Table.csv`
4. `RedFox_Test_Results_Table.csv`
5. `INCIDENT_REPORTS/2026-07-08__PSIController_Order_Of_Operations_Failure.md`
6. This handoff file: `HANDOFFS/RF-PSI14_PSIController_Full_Handoff_2026-07-27.md`

The next chat must not silently read. It must leave a message-board entry or return an exact message-board block to David.

---

## 2. Current ZIP / baseline

Current latest artifact in David's chat:

```text
14-RedFox_PSIController_v0_2_3_CompactQuickUI.zip
```

This build was made from v0.2.2 and changed only the compact quick GM UI files:

```text
ui/modules/apps/redfoxPSIQuickControls/app.js
ui/modules/apps/redfoxPSIQuickControls/app.json
```

It should preserve the v0.2.2 manual-action anti-spam throttle.

v0.2.3 static verification claimed:

```text
- Reopened v0.2.2 before editing.
- Reopened v0.2.3 after packaging.
- JSON validates.
- Full GM UI JavaScript passes syntax check.
- Quick GM UI JavaScript passes syntax check.
- No setInterval.
- No requestAnimationFrame.
- Vehicle/core file hashes match v0.2.2.
- Only quick UI files changed.
```

Runtime is NOT proven.

---

## 3. Current feature set expected in PSI Controller line

The mod currently includes or is expected to include:

### Core tire/PSI service

- Front PSI target slider in full GM UI.
- Rear PSI target slider in full GM UI.
- Front - / Front + buttons.
- Rear - / Rear + buttons.
- Reset PSI.
- Air Up speed setting.
- Air Down speed setting.
- Manual Refresh after v0.2.2 anti-spam pass.
- Manual Set/Apply behavior to avoid slider-drag spam.

### Tire service

- Tire Only mode: removes rubber tire but keeps rim/wheel attached where possible.
- Full Wheel/Rim mode: attempts to remove full wheel/rim using available BeamNG breakGroups.
- Pop Tire mode: should leave tire attached and make it flat/punctured, not act like tire-only removal.
- Apply Selected.
- Repair Selected.
- Remove All Detected.
- Repair Low/Flats.
- Selected tire readout.
- In-world selected tire marker using green sealant helper added in v0.1.8, but runtime behavior is not fully proven.

### Self-sealing tire system

- Self-Sealing Tires toggle.
- Instant Repair toggle.
- Seal Kit presets:
  - Realistic / 1 repair
  - Extended / 2 repairs
  - Trail Kit / 3 repairs
  - Expedition / 4 repairs
  - Arcade / 5 repairs
  - Cheat / Infinite
- Green sealant ooze during repair.
- Hissing/leak cleanup attempts after repair.
- Desired behavior: if self-sealing is on and a tire reaches trigger PSI, repair should refill slowly or instantly depending on setting, show green ooze while repairing, then stop hissing and stop ooze when repair pressure is reached.

### Rim race / experimental

- Rim Race Assist / drive on rims toggle.
- Must remain OFF by default.
- Marked Experimental.
- David previously saw vehicle-broken / steering fighting behavior when enabled.
- Do not make this part of career-safe release until proven.

### Multi-wheel / trailer tire handling

- Scanner code exists for 2, 3, 4, 6, 8, 10+ wheel layouts.
- Labels observed in testing:
  - 3-wheel example showed FL / FR / R.
  - 14-wheel semi showed many labels, but some labels were confusing in prior versions.
- v0.1.8 improved 7+ labels but trailer wheels still did not show for at least one semi trailer test.
- Trailer support is not fully solved. It may need a dedicated trailer/nearby vehicle bridge path if BeamNG does not expose trailer wheels through the active vehicle extension.

### UI layers

- Full GM UI app: `RedFox Tire Control`.
- Compact GM UI app: `RedFox PSI Quick Controls`.
- Optional WE/native settings panel: `redfoxPSIControllerNative.lua` from v0.1.9/v0.2.0 line.
- Hub bridge is deferred. Do not move tire gameplay into Hub.

---

## 4. Major problems already found and status

### 4.1 Background spam / lag

David found major console spam from v0.2.0:

```text
libbeamng.redfoxPSIController.veh
No wheels with pressure groups found (... total wheels)
```

v0.2.1 tried to throttle logs and classification. David then demanded a triple-check full code audit. v0.2.2 was created as the stricter manual-action throttle build.

v0.2.2 intended fixes:

```text
- Vehicle-side updateGFX returns unless explicit reason to run.
- Removed periodic GameEngine telemetry sending.
- Removed periodic wheel layout sending.
- Removed no-pressure-group warning string completely.
- Removed automatic PSI re-apply on vehicle initial report.
- Removed automatic PSI/status request on vehicle switch.
- Added explicit refreshStatus path.
- UI must click Refresh to ask for tire status.
- Self-sealing, rim assist, and blowout checks run only if user enables those modes.
```

v0.2.3 did not intentionally change the anti-spam vehicle core.

**Next test:** Run v0.2.3 alone, old PSI zips disabled, open full GM + quick GM + WE if desired, do not press buttons for 5–10 minutes, and watch console. There should be no repeated PSI spam. Then press Refresh once and verify it updates once, not constantly.

### 4.2 Compact quick UI still needs runtime test

David said the compact PSI UI was still not compact enough. v0.2.3 changed quick UI only:

```text
- Default size: 145 x 78
- Minimum size: 90 x 42
- Front row: F + slider + PSI readout + - + +
- Rear row: R + slider + PSI readout + - + +
- Bottom row: Set / Reset / Seal
- ResizeObserver-based local scaling
- Slider drag does not call engineLua; Set sends command
```

**Next test:** Resize the compact UI tiny and large. It should remain usable at roughly 1x2 inch size and should not spam Lua while resizing or dragging sliders.

### 4.3 Pop Tire vs Tire Only still needs proof

David reported earlier that Pop Tire acted like Tire Only/removal. v0.1.8 attempted to soften Pop Tire so it leaves the tire attached and makes it flat/punctured.

**Next test:** On a normal 4-wheel vehicle, choose Pop Tire, select one wheel, Apply Selected. Tire should remain on the vehicle but flat. It should not remove the tire or rim.

### 4.4 Multi-wheel/trailer gaps

David tested a 14-wheel semi and saw many buttons. Some removal/pop-all attempts did not affect every wheel. One semi trailer test did not show trailer tires.

**Next test:** Test:

1. Normal 4-wheel vehicle.
2. 3-wheel vehicle.
3. Dually/6-wheel vehicle.
4. Semi/heavy/14-wheel vehicle.
5. Semi with trailer.

Record which labels appear and whether each button targets the correct wheel. If trailer tires do not appear, do not claim trailer support. Build a diagnostic/trailer bridge pass only after core v0.2.3 passes idle-spam and compact UI tests.

### 4.5 WE/native UI status

WE/native UI exists as optional settings/status panel. It is not the core gameplay. It should not do background polling. In v0.2.0 it was adjusted to use manual Apply/Refresh behavior, but runtime should still be checked.

**Next test:** Open WE/native panel, leave idle 5–10 minutes, check console for no spam. Confirm sliders require Apply.

---

## 5. Strict order of operations for next chat

No new build should be made until David provides test results for v0.2.3 or explicitly asks for a non-runtime documentation/handoff update.

When building resumes, follow this order exactly:

1. **Identify exact baseline ZIP.** Current expected baseline: `14-RedFox_PSIController_v0_2_3_CompactQuickUI.zip`.
2. **Unzip baseline and inspect before editing.** List changed files and relevant existing functions.
3. **Make one narrow change only.** Do not combine gameplay + UI + Hub + network in one build.
4. **Compare after editing.** Produce side-by-side diff summary.
5. **Package.**
6. **Reopen final ZIP.** Verify actual packaged files, not working folder only.
7. **Search packaged files for spam paths.** Required terms:
   - `setInterval`
   - `requestAnimationFrame`
   - `updateGFX`
   - `queueGameEngineLua`
   - `obj:queueGameEngineLua`
   - `log(`
   - `print(`
   - `No wheels with pressure groups`
   - `sendWheelLayout`
   - `sendPressureStatus`
   - `refreshStatus`
8. **Label runtime truthfully.** Use NEEDS TEST unless David has tested in BeamNG.
9. **Update GitHub.** At minimum, update module status and leave message-board block or create handoff file.

---

## 6. Do-not-change / do-not-break list

Do not change these unless David explicitly asks and the baseline is checked first:

```text
lua/vehicle/extensions/auto/redfoxPSIController.lua
lua/vehicle/extensions/redfoxpartrepair.lua
lua/ge/extensions/redfoxTireSealant.lua
ui/modules/apps/redfoxPSIControl/app.js
lua/ge/extensions/redfoxPSIControllerNative.lua
```

If UI-only work is requested, do not touch vehicle tire core.

If anti-spam work is requested, do not change tire behavior except to stop background work.

If multi-wheel work is requested, build diagnostics first before changing destructive actions.

---

## 7. Current safe labels / unsafe labels

Safe labels:

```text
NEEDS TEST
static verification only
manual-action throttle line
release-polish candidate
career-safe candidate
```

Unsafe labels unless David proves runtime:

```text
Final
Fixed
Ready
Working
Proven
Complete
Live
Real
```

Do not use those in build names unless runtime is actually proven by David.

---

## 8. Current known build line summary

- `v0.1.8_MultiWheel_PopHighlightFix`: added multi-wheel label improvements, pop/highlight changes, nearby vehicle/trailer merge attempt. Runtime partly problematic/unproven.
- `v0.1.9_ReleasePolish_UIOnly`: added quick GM UI and WE/native settings; UI-only release polish.
- `v0.2.0_UIThrottleSliders`: added sliders and removed UI-side background polling, but David still saw vehicle-side spam.
- `v0.2.1_LogSpamThrottle`: throttled log/classification/telemetry but was not strict enough.
- `v0.2.2_ManualActionThrottle`: stricter anti-spam/manual-action vehicle loop; no runtime proof yet.
- `v0.2.3_CompactQuickUI`: compact quick UI patch only; preserves v0.2.2 anti-spam line; current handoff baseline.

---

## 9. Exact next test checklist for David

Test only:

```text
14-RedFox_PSIController_v0_2_3_CompactQuickUI.zip
```

Disable:

```text
all older RedFox PSI / Tire Control zips
any duplicate PSI Controller builds
```

### Test A — Idle spam / lag

1. Load a normal 4-wheel vehicle.
2. Add full GM UI: RedFox Tire Control.
3. Add compact GM UI: RedFox PSI Quick Controls.
4. Optionally open WE/native panel.
5. Do not press any PSI buttons.
6. Wait 5–10 minutes.
7. Check console.

Expected:

```text
No repeated libbeamng.redfoxPSIController.veh spam.
No repeated No wheels with pressure groups spam.
No increasing lag from PSI while idle.
```

### Test B — Compact quick UI

1. Resize compact UI very small.
2. Resize compact UI large.
3. Drag Front/Rear sliders.
4. Do not click Set yet.

Expected:

```text
UI remains usable.
Slider dragging alone does not send PSI commands.
Only Set/Reset/Seal/buttons send commands.
```

### Test C — Manual Refresh

1. Click Refresh in full GM UI.
2. Watch console.

Expected:

```text
One status refresh, not endless repeated requests.
```

### Test D — Basic PSI control

1. Set front target.
2. Click Set or Front +/-.
3. Set rear target.
4. Click Set or Rear +/-.

Expected:

```text
PSI changes only when clicked/applied.
```

### Test E — Tire service basic

1. Tire Only selected + one wheel + Apply Selected.
2. Pop Tire selected + one different wheel + Apply Selected.
3. Full Wheel/Rim selected + junk test vehicle only.

Expected:

```text
Tire Only removes tire/keeps rim when possible.
Pop Tire leaves tire attached but flat.
Full Wheel/Rim is destructive and should only happen when explicitly selected.
```

### Test F — Multi-wheel / trailer

1. Test dually/semi/heavy.
2. Check labels and correct targeting.
3. Test trailer.

Expected:

```text
Truck wheels show.
Trailer wheels may not yet show. If not, record as trailer bridge needed.
No truck button should affect the wrong wheel.
```

---

## 10. Next development roadmap after tests

### Phase 1 — Release-stable standalone PSI

Only fix issues David proves in v0.2.3. Priorities:

1. Stop any remaining spam/lag.
2. Make compact UI truly usable.
3. Make Refresh/Set/manual actions clear.
4. Keep Pop Tire distinct from Tire Only.
5. Make self-sealing behavior reliable enough for release.
6. Add README/help text for users.

### Phase 2 — Career-safe restrictions

Career compatibility is the global goal for all RedFox mods from now on.

For PSI Controller, career-safe mode should default to:

```text
Allowed:
- read wheel layout
- read PSI state on request
- set PSI manually
- limited self-sealing with Realistic / 1 repair default
- manual repair selected / repair low flats

Hidden or experimental in Career:
- Cheat / Infinite seal kit
- Rim Race Assist
- Full Wheel/Rim removal
- Pop Tire
- destructive all-wheels commands
```

Do not try to hide cheating from Career. Make it behave like a legitimate service/tool, and disable lab/cheat features by default in career mode.

### Phase 3 — Multi-wheel/trailer diagnostic

Add a non-destructive diagnostic view first:

```text
Detected vehicle ID
vehicle name if available
wheel count
wheel names
pressure groups
breakGroups
has pressure control yes/no
is trailer/extra vehicle yes/no
```

Then fix labeling/targeting. Do not fix destructive removal before labels and diagnostic are proven.

### Phase 4 — Hub bridge later

Do not connect to Garage Hub until standalone passes.

When ready, expose only bridge functions and manifest. Hub may open/close UI and request status. Hub must not own tire settings/gameplay.

### Phase 5 — Command Center / external bridge

Start read-only first:

```lua
getExternalStatus()
```

Should return:

```lua
moduleId
vehicleId
wheelCount
frontPSI
rearPSI
wheels = { label, psi, state, selected, targetVehicleId }
selfSealing
sealKitMode
selectedWheel
```

Control commands come later only after read-only telemetry is proven.

---

## 11. GitHub status at handoff

`RedFox_Module_Status_Table.csv` currently lists PSI Controller as:

```text
Current ZIP = 14-RedFox_PSIController_v0_2_3_CompactQuickUI.zip
Freeroam Status = NEEDS TEST
Career Status = NEEDS TEST
GM UI Status = COMPACT QUICK UI STATIC CHECK PASSED / FULL GM UNCHANGED
WE Native UI Status = WE NATIVE UI UNCHANGED
Hub Bridge Status = BRIDGE/COMMAND CENTER EXPORT PLANNED LATER
Known Issue = runtime size/drag behavior and anti-spam need David test
```

---

## 12. Message-board block for next chat / Coordinator

```text
Timestamp = 2026-07-27 America/Los_Angeles
Chat ID = RF-PSI14
Chat Name = PSI Controller / RedFox Tire Control Chat
Message type = HANDOFF
Assigned role = RedFox PSI Controller standalone/career-safe tire module worker chat
I read these files = RedFox_Chat_Message_Board.md, RedFox_Module_Status_Table.csv
I changed these files = RedFox_Module_Status_Table.csv only earlier; no table change needed in this handoff because v0.2.3 row already exists
I created these files = HANDOFFS/RF-PSI14_PSIController_Full_Handoff_2026-07-27.md
I delivered these files = 14-RedFox_PSIController_v0_2_3_CompactQuickUI.zip in chat; handoff roadmap in repo
What I did = Created a full handoff/roadmap for PSI Controller. Current baseline is v0.2.3 CompactQuickUI. It is static-verified only and needs David runtime testing. Main unresolved risks are idle spam/lag, compact UI resizing/usability, Pop Tire vs Tire Only behavior, self-sealing/hiss/ooze behavior, multi-wheel targeting, and trailer tire detection.
What the next chat needs to know = Do not create a new build until David reports v0.2.3 test results or explicitly asks. Do not touch vehicle tire core for UI work. Do not reconnect Hub or Command Center yet. If building resumes, inspect baseline before editing, check after editing, reopen final ZIP after packaging, include diff, and mark runtime as NEEDS TEST unless David proves it.
What David needs to test/check = Test only 14-RedFox_PSIController_v0_2_3_CompactQuickUI.zip with older PSI zips disabled. First test idle spam for 5-10 minutes, compact quick UI resize and Set behavior, then basic PSI, tire service, self-sealing, and multi-wheel/trailer detection.
Coordinator action needed = yes
```

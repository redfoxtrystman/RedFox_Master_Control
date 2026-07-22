# READ FIRST — All Chats Core UI Override Ban

**Date:** 2026-07-22  
**Owner:** David / Captain  
**Scope:** All RedFox / FoxNet / IceFox / BeamNG job chats  
**Severity:** Project-wide stop condition  
**Reason:** A JOB-04 Scrap Yard test ZIP packaged a global BeamNG UI override and caused the game title/background/UI to fail into a grey screen. David spent about 12 hours tracking down the cause. This must not happen again.

---

# What happened

The JOB-04 Scrap Yard WebUI test package included:

```text
ui/ui-vue/dist/index.js
```

That file is not a narrow Scrap Yard page file. It is a global BeamNG Vue UI bundle. Including it in a feature/job ZIP can break the whole game UI, including the title screen/background and in-game UI loading.

David reported:

```text
the game refuses to load the background screen on the title and also just grey screen when game loads
```

After inspection, the likely cause was the packaged global UI override:

```text
ui/ui-vue/dist/index.js
```

This cost David about 12 hours to isolate because it looked like a normal mod/package issue instead of one global UI file breaking the whole game.

---

# Project-wide rule

No job chat may package, replace, edit, or ship the global BeamNG Vue UI bundle:

```text
ui/ui-vue/dist/index.js
```

unless all of the following are true:

1. David explicitly approves a core UI integration task.
2. The job is specifically assigned to platform/core integration, not a feature page.
3. The baseline BeamNG UI file is inspected first.
4. The exact diff is listed before editing.
5. The package includes a rollback plan.
6. The package is clearly labeled as a high-risk core UI test.
7. The verification report explicitly says this file is included.

For normal feature jobs, this file is banned.

---

# Also high risk

This file must also be treated as high risk:

```text
lua/ge/extensions/ui/phone/layout.lua
```

A feature chat may not change it unless phone/platform integration is the actual approved scope. If a build keeps it for access/testing reasons, the verification report must label it as high-risk and explain why.

---

# Stop condition

Every job must stop packaging if its output ZIP contains:

```text
ui/ui-vue/dist/index.js
```

unless this is an approved core UI integration build.

This is now a mandatory ZIP verification item.

---

# Required verification line for every future RedFox/FoxNet/IceFox ZIP

Every verification report must include:

```text
Core UI override check:
- ui/ui-vue/dist/index.js present: YES/NO
- If YES, approved core UI build: YES/NO
- If YES without approval: FAIL, do not ship

Phone layout override check:
- lua/ge/extensions/ui/phone/layout.lua present: YES/NO
- If YES, approved phone/platform build: YES/NO
- If YES without approval: WARN/FAIL with explanation
```

---

# Plain rule for all chats

Feature mods should add their own app/page/test files. They should not overwrite BeamNG's main UI bundle.

Bad narrow-feature package behavior:

```text
Scrap Yard test panel + ui/ui-vue/dist/index.js
```

Correct narrow-feature package behavior:

```text
Scrap Yard page files
Scrap Yard WebUI test panel files
Scrap Yard-specific Lua bridge/test file
No global BeamNG Vue UI bundle
No global phone layout change unless approved or explicitly documented
```

---

# Jobs affected

This applies to every job:

```text
JOB-00 Coordinator / Integration / Verification
JOB-01 Phone + PC Platform Core
JOB-02 Shared RLS / Career Bridge
JOB-03 RedFox App Store / Play Store
JOB-04 Scrap Yard / Wrecking Yard
JOB-05 BeamBook Marketplace
JOB-06 Import / Export Yard
JOB-07 Classics / Collector Exchange
JOB-08 Insurance / Finance / Garage / Storage Pages
JOB-09 Tow / Recovery / Dispatch Integration
JOB-10 Visual Design / Real Website Polish
JOB-11 QA / Logging / Failure Triage
JOB-12 SponsorHub / FoxMail / FoxText / Sponsor Rewards
```

---

# Related incident reports

```text
INCIDENT_REPORTS/JOB-04_2026-07-22_SCRAPYARD_WEBUI_TEST_PANEL_GREY_SCREEN_CORE_UI_OVERRIDE.md
INCIDENT_REPORTS/JOB-04_2026-07-22_SCRAPYARD_GREY_SCREEN_USER_TIME_LOSS_AMENDMENT.md
```

---

# Required action for future chats

Before building or packaging, each chat must check its output ZIP for:

```text
ui/ui-vue/dist/index.js
lua/ge/extensions/ui/phone/layout.lua
```

If `ui/ui-vue/dist/index.js` is present without explicit David-approved core UI scope, the chat must remove it and rebuild before sending any ZIP.

If `lua/ge/extensions/ui/phone/layout.lua` is present, the chat must explain why it is present and mark the build as high-risk or remove it before packaging.

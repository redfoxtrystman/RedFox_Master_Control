# OWNER WEB SYSTEM RECOVERY — RETURN CHECKLIST

**Date created:** 2026-07-17  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Purpose:** This is the exact practical list for getting the RedFox/FoxNet websites connected and the web system back on track when David returns. It is not the full master order of operations.

---

## 1. Begin in JOB-00 — Coordinator / Integration / Verification

Tell JOB-00:

```text
I am back. Start the web-system recovery checklist. Give me only the next one or two actions at a time.
```

JOB-00 first checks GitHub for any new commits, issue updates, candidate changes, or blockers made while David was away.

---

## 2. Gather the exact files needed for web recovery

Create one local folder:

```text
RedFox_Web_System_Return
```

Gather these files without renaming them:

### Required shared baseline/reference files

```text
rls_career_overhaul_2.6.6.zip or the exact suffixed copy intended as the shared baseline
```

```text
The newest known working-ish FoxNet/IceFox all-in-one ZIP
```

```text
The phone-working Scrap Yard/FoxNet ZIP
```

```text
The PC-broken or newer all-in-one FoxNet ZIP used for comparison
```

### Required web/platform files

```text
The current JOB-01 — Phone + PC Platform Core source/build candidate
```

```text
The current JOB-10 — Visual Design / Real Website Polish website package
```

```text
Any older working website package that successfully opened inside BeamNG
```

### Required first feature files

```text
The newest JOB-04 — Scrap Yard / Wrecking Yard WEUI/backend candidate
```

```text
The older partly working phone Scrap Yard build
```

### Newly found references

```text
All newly found phone mods, including the one with a built-in app store
```

For every archive record:

```text
Exact filename =
Archive byte size =
SHA-256 =
ZIP integrity =
Where it came from =
Known runtime result =
```

Do not trust filenames alone.

---

## 3. Resolve the RLS baseline identity problem

Open:

```text
GitHub issue #7
Baseline blocker: reverify RLS 2.6.6 archive size and SHA-256
https://github.com/redfoxtrystman/RedFox_Master_Control/issues/7
```

JOB-01 — Phone + PC Platform Core and JOB-02 — Shared RLS / Career Bridge previously recorded two different byte sizes for the same SHA-256.

Recheck the exact archive and publish one authoritative:

- filename;
- archive byte size;
- SHA-256;
- member count;
- top-level paths;
- ZIP-integrity result.

JOB-00 — Coordinator / Integration / Verification freezes that exact archive as the shared baseline.

No new shared phone/PC/bridge build should proceed before this is corrected.

---

## 4. Compare the old working web integration against the new websites

Use the old working or partly working FoxNet/Scrap Yard package as the integration reference.

Compare it file-by-file with the current JOB-10 — Visual Design / Real Website Polish package and JOB-01 — Phone + PC Platform Core source.

Specifically identify:

- where the working page lived inside the mod;
- exact HTML entry file;
- exact app/route registration;
- whether it used `ui/modules/apps`, `ui/modModules`, an iframe, AngularJS, Vue, or another host;
- absolute versus relative asset paths;
- how phone opened the page;
- how PC opened the page;
- how JavaScript called Lua;
- whether it used `bngApi.engineLua`, messages, hooks, or a parent bridge;
- which files were shared by phone and PC;
- which files differed;
- whether the PC path loaded a different page or bridge;
- which browser-only features must be removed or replaced;
- whether `localStorage` was used only for visual state or incorrectly used as gameplay state.

The result must be a written compatibility report before mass-converting pages.

---

## 5. Prove one minimal BeamNG-hosted web page

Before connecting the full websites, build the smallest possible proof page.

The proof page must contain only:

```text
One title
One status field
One JavaScript button
One UI-to-Lua ping
One Lua-to-UI response
One close/back operation
```

It must be hosted through the actual JOB-01 — Phone + PC Platform Core path, not opened as a loose browser file.

Required result:

1. Phone opens the proof page.
2. PC opens the same canonical destination.
3. Both use the same HTML entry file or approved responsive source.
4. The button reaches Lua.
5. Lua returns a visible response.
6. Close/back works.
7. Career loads completely.
8. The same ZIP works on a second map.

If this fails, stop and fix the hosting/bridge layer before connecting any full website.

---

## 6. Stabilize JOB-01 — Phone + PC Platform Core

JOB-01 — Phone + PC Platform Core must then provide:

- one verified phone host;
- one verified PC host;
- one shared route registry;
- one canonical destination ID per app;
- one approved entry-path format;
- clear route/open/close errors;
- build/version diagnostics;
- no duplicated feature business logic;
- no separate guesswork PC bridge;
- no hard-coded fake live data presented as real.

Test `redfox.home` first, then one minimal test app.

Do not connect all websites until this host works from phone and PC.

---

## 7. Rebuild JOB-02 — Shared RLS / Career Bridge

JOB-02 — Shared RLS / Career Bridge must reconstruct and commit:

```text
Versioned bridge contract
JSON schema
Fixtures/examples
Capability handshake
Error/result format
Correlation/request IDs
Timeout behavior
```

Start with read-only operations:

```text
Get Career/session status
Get available capabilities
Get vehicle-shopping data
Get owned Career vehicles
Get garage/storage read-only information where supported
```

Phone and PC must call the exact same operation names and receive the same payload shape.

Only after read-only calls work should JOB-02 add:

```text
Open purchase menu
Confirm actual purchase result
Sell selected owned vehicle
Other approved mutations
```

Opening a menu is not purchase success. Spawning a vehicle is not purchase success.

---

## 8. Recover and prove JOB-04 — Scrap Yard / Wrecking Yard backend

JOB-04 — Scrap Yard / Wrecking Yard is the first complete feature proof.

First recover or rebuild the WEUI/backend candidate because the previous download failed.

Test the backend without the pretty website:

1. Open the development WEUI.
2. Request real vehicle-shopping data.
3. Show stock count and errors.
4. Select one listing.
5. Open the real RLS/BeamNG purchase menu.
6. List real owned Career vehicles.
7. Select one owned test vehicle only when safe.
8. Use the real inventory sell path.
9. Save the logs.
10. Repeat on a second map.

The WEUI, phone page, PC page, and final website must all call the same JOB-04 backend service.

Do not add player-owned-yard, crusher, parts, or illegal-disposal mechanics until this backend works.

---

## 9. Connect the approved Scrap Yard website

After JOB-04 — Scrap Yard / Wrecking Yard backend works:

1. JOB-10 — Visual Design / Real Website Polish hands over the approved Scrap Yard page source.
2. JOB-04 removes mock data and connects the page to the proven backend.
3. JOB-01 — Phone + PC Platform Core registers one canonical Scrap Yard destination.
4. JOB-02 — Shared RLS / Career Bridge supplies real data/actions.
5. Phone and PC open the same Scrap Yard destination.
6. Responsive layout may differ, but business logic and payloads do not.
7. Test purchase browsing, owned-vehicle listing, selected sell action, errors, close/back, and second-map behavior.

This is the first full end-to-end milestone:

```text
ONE PROVEN PHONE/PC HOST
+ ONE VERSIONED SHARED CAREER BRIDGE
+ ONE PROVEN SCRAP YARD BACKEND
+ ONE APPROVED SCRAP YARD WEBSITE
```

---

## 10. Inspect the newly found phone mods before deciding the final phone/app-store design

After the minimal JOB-01 host proof exists, inspect all newly found phone mods.

JOB-01 — Phone + PC Platform Core checks:

- phone shell;
- route registration;
- lifecycle;
- RLS conflicts;
- PC-sharing potential.

JOB-03 — RedFox App Store / Play Store checks:

- catalog format;
- install/enable/disable behavior;
- app discovery;
- update/remove behavior;
- built-in app-store UI.

JOB-02 — Shared RLS / Career Bridge checks:

- UI-to-Lua calls;
- Career permissions;
- persistence and message flow.

JOB-11 — QA / Logging / Failure Triage checks exact candidates for:

- startup overrides;
- duplicate paths;
- unsafe removal;
- packaging conflicts.

JOB-00 — Coordinator / Integration / Verification decides whether to:

```text
Extend the RLS phone
Build a RedFox-owned phone shell
Use only selected safe patterns from another mod
```

Do not replace the current phone solely because another mod has a nice app store.

---

## 11. Hand off and connect the remaining websites one at a time

Once Scrap Yard proves the full pattern, repeat it for:

```text
JOB-05 — BeamBook Marketplace
JOB-06 — Import / Export Yard
JOB-07 — Classics / Collector Exchange
JOB-08 — Insurance / Finance / Garage / Storage Pages
JOB-09 — Tow / Recovery / Dispatch
JOB-12 — SponsorHub / FoxMail / FoxText / Sponsor Rewards
```

For every page:

```text
Prove backend
→ hand off approved website source
→ remove mock data
→ connect to backend
→ register one phone/PC destination
→ test exact ZIP
→ run JOB-11 QA
→ approve through JOB-00
```

Unknown or remembered-later pages remain in the JOB-10 — Visual Design / Real Website Polish backlog and can be added later as separate destinations.

---

## 12. Exact first actions when David returns

The first practical sequence is:

```text
1. Open JOB-00 — Coordinator / Integration / Verification.
2. Gather the exact RLS, FoxNet, phone-working Scrap Yard, PC-broken FoxNet, current JOB-01, current JOB-10 and JOB-04 candidate files.
3. Resolve GitHub issue #7 and freeze the baseline.
4. Compare old working web integration against the new website structure.
5. Build and test one minimal phone/PC web-host ping page.
6. Stabilize JOB-01 — Phone + PC Platform Core.
7. Rebuild JOB-02 — Shared RLS / Career Bridge read-only contract.
8. Recover and test JOB-04 — Scrap Yard / Wrecking Yard WEUI/backend.
9. Connect the approved Scrap Yard website.
10. Test the same destination on phone, PC and a second map.
11. Only then repeat the proven pattern for the other websites.
```

---

## 13. Stop conditions

Stop and inspect before continuing when:

- Career does not finish loading;
- phone and PC open different destinations;
- Lua ping does not return;
- relative assets fail in BeamNG;
- more than one FoxNet ecosystem ZIP is installed;
- a page depends on browser-only state for gameplay;
- a purchase opens but ownership/storage does not complete;
- a ZIP identity is unknown;
- the PC suffers a full-system crash during the test;
- a job attempts to copy JOB-01 or JOB-02 into its own package.

No page is called connected, working, fixed, or finished until David tests the exact ZIP.
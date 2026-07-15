# Owner Investigation — BeamNG Web UI Compatibility and Old/New Website Comparison

**Date/time:** 2026-07-14 20:43 PDT / America/Los_Angeles  
**Issued through:** JOB-00 — Coordinator / Integration / Verification  
**Requested by:** David / Captain  
**Status:** PROVISIONAL RULES — EXACT OLD/NEW DIFF PENDING

## Why this exists

David remembers that the older working RedFox website required a BeamNG-specific adaptation and that ordinary browser HTML did not work correctly when used directly. The exact older working package has not yet been supplied to this regular chat, so this record separates confirmed BeamNG requirements, current RedFox platform requirements, and hypotheses that must be proven by comparing the old working package with the current JOB-10 website package.

## Confirmed BeamNG facts

BeamNG uses HTML/JavaScript for user-interface display and Lua for gameplay/business logic. BeamNG recommends leaving as much logic as possible in Lua and using HTML/JavaScript mainly to display results.

BeamNG's documented classic UI-app format is not a loose standalone website. A classic app is registered through BeamNG's UI system and normally includes:

```text
app.js
app.json
app.png
```

The documented classic app is an AngularJS directive in the `beamng.apps` module. A normal webpage placed somewhere on disk is therefore not automatically discoverable or callable as a BeamNG app.

Official references checked on 2026-07-14:

```text
https://documentation.beamng.com/modding/ui/app_creation/
https://documentation.beamng.com/modding/programming/languages/
```

## Current RedFox platform target

The current JOB-01 platform contract uses a RedFox-specific page-host approach rather than requiring every full website to become a small classic HUD app.

Current contract target:

```text
job01.platform.v1
```

Required page entry form:

```text
/ui/modModules/<app-owned-folder>/<entry-file>.html
```

Forbidden entry forms include:

```text
file:// URLs
parent traversal with ../
remote HTTP/HTTPS as an app entry
arbitrary Lua paths
```

Phone and PC must use:

```text
one canonical app ID
one canonical destination
one entryPath
one backend contract
```

Phone and PC may use different host shells or responsive layout, but they must not maintain separate copies of the feature logic.

Current project evidence:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/JOB-01_ROUTE_AND_DESTINATION_CONTRACT.md
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/phone/index.html
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/pc/index.html
JOB-01_PLATFORM_CORE_SOURCE/ui/modModules/redfoxPlatformCore/shared/platform.js
```

## Findings from the current JOB-10 package

Package inspected:

```text
RedFox_JOB10_Full_Websites_v0_3_0(1).zip
```

Current package purpose is visual prototyping in a normal browser, not BeamNG runtime.

Important findings:

1. `index.html` redirects to `START_HERE.html` with a meta refresh.
2. `START_HERE.html` is approximately 35.7 MB because CSS, JavaScript, and many images are embedded into one file.
3. The separate source version uses `assets/css/app.css`, `assets/js/app.js`, and relative asset paths.
4. It contains no approved BeamNG/RedFox bridge calls such as JOB-01 registry messages or JOB-02 Career/RLS messages.
5. It contains no `bngApi`, `engineLua`, or RedFox parent-message bridge implementation.
6. It uses browser-only demonstration state and `localStorage`.
7. Its displayed `https://...` addresses are visual browser labels, not registered BeamNG destinations.
8. It is correctly labeled `MOCKUP / VISUAL PROTOTYPE — NOT FUNCTIONAL IN BEAMNG`.

## Provisional conversion rule for every feature job

Until the old working package proves a different requirement, each feature job must treat the approved JOB-10 website as source material and create a BeamNG-hosted runtime entry rather than shipping `START_HERE.html` directly.

Required conversion steps:

1. Copy only the approved page's HTML structure, CSS, JavaScript, and assets into that feature job's unique `/ui/modModules/<app-folder>/` path.
2. Use a direct entry file. Do not depend on a meta-refresh launcher.
3. Prefer split HTML/CSS/JavaScript/assets for runtime. Do not use the approximately 35.7 MB self-contained prototype as the production entry unless profiling proves it safe.
4. Use absolute BeamNG UI paths for registry entry paths and any cross-app/platform assets. Keep app-owned relative assets inside the same app folder only when tested.
5. Replace demonstration arrays, fake buttons, and browser-only transactions with calls to the feature's proven backend and approved JOB-02 shared bridge operations.
6. Do not store authoritative Career, money, ownership, inventory, garage, storage, mission, or purchase state in `localStorage`.
7. Register one canonical destination through JOB-01. Phone and PC must resolve the same entry path.
8. Use host information or responsive CSS only for presentation differences.
9. Keep the WEUI/native development harness separate from the production website entry.
10. Test page loading, asset loading, bridge messages, back/close behavior, phone host, PC host, and at least one non-West-Coast map as separate checks.

## Likely cause of the old Scrap Yard phone/PC mismatch

This is not yet proven. The most likely classes of failure are:

- phone and PC loading different page files or different bridge implementations;
- phone using a working RLS route while PC used a plain/unregistered HTML path;
- relative asset or script paths resolving differently between the two hosts;
- one host having access to a parent bridge/API that the other did not;
- duplicated purchase logic instead of one shared backend contract;
- map-specific or West Coast-specific service/shop identifiers;
- browser-local state being mistaken for shared Career state.

No single cause may be marked confirmed until the old working package and the relevant broken PC package are compared.

## Required old/new comparison

When David supplies the old working package, JOB-00/JOB-01/JOB-02 and the relevant feature job must compare:

```text
ZIP root layout
mod_info and modScript files
UI folder path
entry HTML path
phone route registration
PC route registration
app or destination manifest
AngularJS/Vue/custom iframe host use
script loading order
absolute versus relative asset paths
parent frame assumptions
postMessage / bngApi / engineLua calls
Lua extension names and load order
Career/RLS event names and payloads
map/shop/facility IDs
localStorage/session state
back/close/navigation handling
Content Security or blocked URL errors in beamng.log
```

The comparison must produce:

```text
last working mechanism
exact files that made it load
exact phone/PC difference
minimum conversion template
one small proof page before converting every website
```

## Ownership

- `JOB-01` owns the page-host, registry, canonical route, phone/PC entry, and loading contract.
- `JOB-02` owns shared Career/RLS UI-to-Lua messages.
- Each feature job owns converting its approved page and connecting it to its backend.
- `JOB-10` owns the approved visual source but does not own BeamNG runtime adaptation.
- `JOB-11` verifies both host loading and backend wiring.
- `JOB-00` approves the final compatibility rule and shared conversion template after evidence.

## Current decision

Do not mass-convert all websites yet.

First prove one minimal app page using the JOB-01 host contract from both phone and PC. Then compare the old working package and use the confirmed mechanism to create one reusable conversion template for JOB-04 through JOB-09 and JOB-12.

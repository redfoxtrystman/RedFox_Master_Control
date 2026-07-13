# Owner Handoff to JOB-01 — Phone + PC First Working Milestone

**Date:** 2026-07-13  
**From:** David / Captain  
**To:** JOB-01 — Phone + PC Platform Core  
**Priority:** START NOW  
**Status:** OWNER-DIRECTED  
**Shared directive:** `PROJECT_MANIFESTS/REDFOX_FOXNET_START_ORDER_SHARED_ARCHITECTURE_DIRECTIVE_2026-07-13.md`

JOB-01 must read the shared directive, the main job board, JOB-02's platform/bridge ownership handoff, and JOB-11's verification requirements before editing.

---

# David's required outcome

David currently has:

- a working RLS phone,
- a partially working PC that does not have the desired IceFox browser experience,
- an existing working IceFox icon on the phone,
- a phone Scrap Yard page that is useful on West Coast USA,
- no equivalent working Scrap Yard path on PC,
- a purchase flow that can select a vehicle and insurance and spawn the vehicle, but does not create real ownership/storage without a developer cheat.

JOB-01's first outcome is not a redesigned phone or PC.

It is:

1. preserve the existing working phone,
2. preserve the existing partially working PC and extend it,
3. keep the existing phone IceFox entry,
4. add a real IceFox entry/icon to the existing PC,
5. make phone IceFox and PC IceFox open the same canonical functional IceFox destination,
6. publish one shared manifest/registration/route contract for every RedFox app/page,
7. make the destination system map-independent,
8. provide approved deep links/adapters to existing native RLS/in-game pages,
9. prove the route on West Coast USA and at least one non-West-Coast map supported by the current session,
10. report runtime as untested until David tests the exact build.

The phone is the portable form of the PC. The phone can be opened anywhere; the PC may remain tied to normal in-game PC access. That difference must not create separate page destinations or separate app business logic.

---

# Baseline intake instructions

David should upload the shared baseline package once to the JOB-01 chat. Do not ask David to upload identical files to every chat.

Requested baseline inputs:

- the exact currently working RLS phone files/mod ZIP,
- the exact partially working PC files/mod ZIP,
- the current FoxNet/IceFox ZIP or folder containing the phone IceFox icon,
- the current phone-working Scrap Yard build for route/host inspection only,
- any currently installed overlapping FoxNet/Web Ecosystem versions,
- any BeamNG log captured while opening phone IceFox, PC, Scrap Yard, and attempting a purchase,
- screenshots showing the current phone and PC entries if available.

JOB-01 must not edit the originals.

Before implementation, JOB-01 must publish:

- original filenames,
- sizes and hashes,
- archive integrity result,
- complete file inventories,
- overlapping/duplicate path report,
- which package is selected as the canonical platform baseline,
- which packages are reference-only,
- which packages must not be installed together,
- exact files it proposes to inspect/edit,
- exact protected files it will not edit.

If a binary ZIP is not suitable for normal repository storage, commit its inventory, hashes, origin, selected-baseline decision, and extracted source files needed for coordination. Do not create untracked competing copies across chats.

---

# Required JOB-01 contract

JOB-01 owns and must publish the final platform-facing contract for:

## App/page identity

Every app/page has one canonical ID and one canonical destination.

Phone and PC may pass host/layout information, but both hosts must resolve the same app/page identity.

## Registration

Define exactly:

- manifest path,
- required fields,
- optional fields,
- phone-enabled and PC-enabled flags,
- icon path rules,
- canonical entry/destination,
- permissions declaration,
- dependencies,
- version,
- installed/enabled state consumption,
- how a native in-game/RLS page is registered or deep-linked without copying it.

## Launch behavior

Define exactly:

- how the existing phone IceFox icon opens the IceFox destination,
- how the PC IceFox icon is registered in the existing PC,
- how both hosts invoke the same route,
- how back/home/close work on each host,
- how host-responsive presentation is communicated,
- what happens when a destination is missing or blocked,
- required logs for host, route, app ID, current map/session, success, and failure.

## Shared ownership

List every file JOB-01 owns.

List every file that belongs to:

- JOB-02 bridge,
- JOB-03 App Store,
- JOB-04 Scrap Yard,
- JOB-05 BeamBook,
- JOB-06 Import / Export,
- JOB-07 Classics,
- JOB-08 support pages,
- JOB-09 Tow / Recovery,
- JOB-10 visual design,
- JOB-11 QA,
- JOB-12 Sponsor System.

JOB-01 may expose registration slots and interfaces. It may not edit app-owned business logic.

---

# Required coordination

## With JOB-02

JOB-01 owns platform registration, host navigation, and front-end routing.

JOB-02 owns the UI-to-Lua Career/RLS bridge, current-session data, purchase actions/results, ownership/storage results, and Career/RLS errors.

JOB-01 must consume JOB-02's published bridge contract. It must not invent a second bridge.

## With JOB-11

JOB-01 must use JOB-11's test/report format.

Required tests include:

- phone IceFox opens,
- PC IceFox opens,
- both resolve the same canonical destination,
- host presentation differs only where intended,
- existing native pages can be opened through approved adapters,
- route works on West Coast USA,
- route works on a non-West-Coast map,
- no phone/PC shell replacement,
- no app business logic copied into the platform,
- no duplicate shared files,
- exact log evidence.

## With JOB-03

JOB-03 is now claimed but remains deferred for the first platform milestone.

JOB-01 must publish the registry contract JOB-03 will consume. JOB-03 must not block the first phone/PC IceFox milestone or create a competing launcher.

## With app chats

App chats receive JOB-01's versioned manifest/route contract. They must not edit JOB-01's shared platform files. Requested platform changes go through a GitHub handoff and require approval.

---

# Map-independent requirement

JOB-01 must not hard-code West Coast USA destinations, facilities, shops, dealers, parking spots, or mission paths.

The IceFox destination system must open on every map.

If an underlying RLS/Career service is unavailable on a map, navigation must still work and report the exact unavailable dependency. It must not silently load West Coast data or fake success.

The current theory that West Coast shop files caused the Scrap Yard restriction is unproven. JOB-01 must report evidence, not repeat the theory as fact.

---

# No-placeholder and truth rule

Default: do not add placeholders.

A visible control must either:

- perform the stated action, or
- be excluded from the test build.

A mockup/placeholder is permitted only after David explicitly approves it and it must be labeled:

```text
MOCKUP / PLACEHOLDER — NOT FUNCTIONAL
```

Allowed completion language:

```text
BUILT — RUNTIME UNTESTED
PARTIAL
BLOCKED
FAILED — STOPPED
DAVID-TESTED WORKING
```

Only David's BeamNG test permits `DAVID-TESTED WORKING`.

Never say “should work” as proof.

---

# Protected areas

JOB-01 must not:

- replace or hijack the RLS/BeamNG phone shell,
- replace or hijack the RLS/BeamNG PC shell,
- build a competing Career/RLS bridge,
- edit Scrap Yard purchase/business logic,
- edit BeamBook, Import / Export, Classics, support, Tow, or Sponsor business logic,
- hand-roll money, ownership, inventory, garage, storage, insurance, or purchase completion,
- create startup Career modules,
- copy West Coast-only shop behavior into the platform,
- build Snake or other games now,
- build the App Store UI unless David assigns that work to JOB-01,
- add unrequested features or leave this scope without David's permission.

---

# Required deliverables before a test ZIP

1. `JOB-01_BASELINE_INVENTORY.txt`
2. `JOB-01_BASELINE_HASHES.csv`
3. `JOB-01_DUPLICATE_PATH_REPORT.txt`
4. `JOB-01_PLATFORM_OWNED_FILES.txt`
5. `JOB-01_PROTECTED_FILES.txt`
6. `JOB-01_APP_MANIFEST_CONTRACT.md`
7. `JOB-01_ROUTE_AND_DESTINATION_CONTRACT.md`
8. `JOB-01_PHONE_PC_HOST_CONTRACT.md`
9. `JOB-01_TO_JOB-02_BRIDGE_BOUNDARY.md`
10. `JOB-01_TO_JOB-03_STORE_REGISTRY_HANDOFF.md`
11. `JOB-01_TO_ALL_APP_CHATS_REGISTRATION_HANDOFF.md`
12. Required TXT and HTML verification reports from the shared QA format.
13. Exact list of unproven runtime items.

No integrated ZIP may be produced until the baseline is inspected and these contracts identify exact edits and protected files.

---

# First acceptance gate

The first JOB-01 test package is acceptable for David to test only when static verification confirms:

- it extends rather than replaces the existing phone and PC,
- the existing phone IceFox entry remains,
- a PC IceFox entry exists,
- both entries target the same canonical functional destination,
- no app-owned business logic is included,
- no JOB-02 bridge implementation is duplicated,
- no West Coast-only route dependency is knowingly hard-coded,
- logs distinguish phone versus PC while showing the same app ID/destination,
- the package contains required TXT and HTML reports,
- runtime status is `BUILT — RUNTIME UNTESTED`.

David's test then determines whether it becomes `DAVID-TESTED WORKING`.

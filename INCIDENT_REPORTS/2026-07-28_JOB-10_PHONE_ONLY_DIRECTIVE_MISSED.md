# JOB-10 Incident Report — Phone-Only Owner Directive Missed

**Date:** 2026-07-28  
**Job:** JOB-10 — Visual Design / Real Website Polish  
**Owner:** David / Captain  
**Status:** CORRECTED IN PROJECT RECORDS — NEXT BUILD MUST BE MOBILE-ONLY

## Summary

JOB-10 published the realistic welcome-page website prototype v0.3.2 with both desktop and mobile preview/testing language even though the current owner-approved architecture had already changed to phone-only on 2026-07-23.

The controlling directive is:

```text
PROJECT_MANIFESTS/OWNER_PHONE_ONLY_ARCHITECTURE_DIRECTIVE_2026-07-23.md
```

Directive commit:

```text
43ee97781b42307f2769011c02c9afa1bfe5c723
```

The directive states:

```text
REDFOX / FOXNET PAGES RUN ON THE IN-GAME PHONE ONLY
PHONE PLATFORM CORE: ACTIVE
PC PLATFORM CORE: DEFERRED
```

It also directs JOB-10 to prioritize mobile/phone layouts. Desktop mockups may be preserved only as design references; desktop/PC runtime adaptation is deferred.

## What JOB-10 did wrong

- Relied on earlier shared phone-and-PC architecture from the old JOB-10 history.
- Did not re-check the latest JOB-00 owner directive before building and documenting v0.3.2.
- Treated desktop rendering as part of the active presentation target instead of a non-runtime visual reference.
- Described the package as a full browser website package without making the phone-only release target prominent enough.

## What remains usable

The v0.3.2 visual work is not discarded. The following remain valid as design material:

- realistic BeamNG imagery;
- BeamWire scrolling ticker;
- 100 rotating headline source items;
- mobile render;
- welcome-card visual direction;
- replaceable image folder and guide;
- verified Tow, FoxFax, UndergroundNet and XXX Insurance website references;
- separation from the working JOB-09 Tow and JOB-04 Wrecking Yard gameplay ZIPs.

The desktop preview remains a design reference only. It is not a current BeamNG runtime target, release gate or integration requirement.

## Corrective rule effective immediately

All new JOB-10 work must use this order:

```text
READ LATEST OWNER/JOB-00 DIRECTIVES
→ DESIGN PHONE-FIRST
→ TEST MOBILE WIDTHS AND PHONE HOST CONSTRAINTS
→ PRESERVE DESKTOP ONLY AS OPTIONAL REFERENCE
→ DO NOT REQUIRE PC PARITY
→ DO NOT BUILD OR PACKAGE PC-SPECIFIC INTEGRATION
```

## Mobile-only acceptance target

The next JOB-10 website revision must:

- be designed for the approved in-game phone host;
- use phone-safe dimensions, scrolling, touch targets and navigation;
- test open, close, back and page switching through the approved phone shell when integration begins;
- avoid any PC-specific route, browser shell or garage-computer dependency;
- keep the Tow and Wrecking Yard gameplay mods separate and untouched;
- label desktop screenshots as non-runtime reference only if they are included at all.

## Ownership

This failure belongs to JOB-10. It was not caused by unclear instructions. The owner directive was present in GitHub and should have been checked before the build was documented.

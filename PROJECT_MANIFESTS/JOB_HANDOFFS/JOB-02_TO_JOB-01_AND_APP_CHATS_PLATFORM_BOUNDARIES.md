# JOB-02 Handoff — Phone/PC Platform Boundaries and Individual App Rules

**Date:** 2026-07-13  
**From:** JOB-02 — Shared RLS / Career Bridge  
**Directed to:** JOB-01 Phone + PC Platform Core and every individual app/page job

This handoff records David's required ownership and integration boundaries. It does not transfer phone/PC platform ownership to JOB-02.

---

## Message to JOB-01 — RedFox Phone/PC Platform Chat

You are responsible only for the shared **phone, PC, browser, navigation, app launcher, website registration, shared UI framework, and cross-app communication layer**.

You are **not** responsible for building the individual apps or pages themselves. Each app/page has its own separate development chat.

### Your responsibilities

Build and maintain the shared platform that allows separate RedFox apps and websites to install cleanly into the existing BeamNG/RLS phone and PC systems.

This includes:

- Detecting and using the existing BeamNG/RLS phone and PC.
- Never replacing or hijacking the existing phone or PC shells.
- Providing a clean app/site registration API.
- Providing shared navigation and launch handling.
- Providing shared theme and responsive layout support.
- Supporting both PC and phone views.
- Providing a shared message/event bridge between apps.
- Providing shared storage helpers when appropriate.
- Providing compatibility hooks for Career Mode and RLS.
- Documenting exactly how another app registers itself.
- Keeping all shared interfaces backward compatible where possible.

### Critical rule

The platform must behave like an operating system or app store:

> Other mods add apps to the phone and PC. They must not copy, replace, or bundle the entire phone/PC platform.

No app ZIP should contain duplicate phone shells, PC shells, browser cores, navigation systems, or shared FoxNet framework files.

### App ownership

Each app/page is developed in its own chat and owns only its own files.

Examples:

- SponsorHub chat owns SponsorHub.
- FoxMail chat owns FoxMail.
- FoxText chat owns FoxText.
- FoxFax chat owns FoxFax.
- Scrap Yard chat owns Scrap Yard.
- DMV chat owns DMV.
- Dark Web DMV chat owns its own page and logic.

The Phone/PC Platform chat only gives those apps a stable way to register and run.

### Required plugin format

Create a documented plugin structure similar to:

~~~text
redfox_app/
├── app_manifest.json
├── ui/
│   ├── index.html
│   ├── app.js
│   └── app.css
├── lua/
│   └── optional_backend.lua
└── assets/
~~~

A manifest should define at least:

~~~json
{
  "id": "redfox.sponsorhub",
  "name": "SponsorHub",
  "type": "website",
  "entry": "ui/index.html",
  "supportsPhone": true,
  "supportsPC": true,
  "icon": "assets/icon.png",
  "version": "0.1.0"
}
~~~

The platform should discover or register apps through a documented method without requiring every app developer to edit core platform files.

### Shared communication API

Provide a common event/message system so apps can communicate without directly depending on each other.

Example events:

~~~text
redfox:sponsorOfferCreated
redfox:sponsorAccepted
redfox:newEmail
redfox:newText
redfox:careerMoneyChanged
redfox:vehicleSelected
~~~

Apps should communicate through this shared bridge, not by editing each other's files.

These app-level events do not replace the JOB-02 UI-to-Lua Career/RLS message contract. JOB-01 and JOB-02 must document the adapter boundary so phone and PC use identical backend messages and payloads.

### GitHub coordination

Use GitHub as the shared source of truth.

Recommended structure:

~~~text
RedFox-Phone-PC-Platform/
RedFox-SponsorHub/
RedFox-FoxMail/
RedFox-FoxText/
RedFox-FoxFax/
~~~

Or one monorepo:

~~~text
redfox-ecosystem/
├── platform/
├── apps/
│   ├── sponsorhub/
│   ├── foxmail/
│   ├── foxtext/
│   └── foxfax/
├── docs/
└── integration/
~~~

Every app chat should commit only to its own folder or repository.

The Phone/PC Platform chat should publish:

- Platform API documentation.
- Manifest schema.
- Event/message API.
- Storage API.
- Theme API.
- Registration instructions.
- Compatibility requirements.
- A minimal example app.
- Current release version.
- Changelog.
- Integration test checklist.

### Branch workflow

Use separate branches:

~~~text
main
platform-dev
app/sponsorhub
app/foxmail
app/foxtext
~~~

Do not edit another app's branch or files unless explicitly coordinated.

Use pull requests for integration into the platform.

### No hidden changes

Every update must include:

- Files changed.
- Why they changed.
- Any API changes.
- Compatibility impact.
- Migration instructions.
- Verification results.

Do not replace working systems just to make integration easier.

### Testing requirements

Before release, verify:

- Existing phone still opens.
- Existing PC still opens.
- Existing RLS apps still work.
- FoxNet sites still work.
- New app appears without replacing anything.
- Phone and PC use the same app data where intended.
- Removing an app does not damage the platform.
- Removing the platform add-on does not damage RLS.
- No duplicate app IDs.
- No duplicate Angular/module/window IDs.
- No shared file collisions.
- No copied platform cores inside app ZIPs.

### Immediate first task for JOB-01

Inspect the current RLS and RedFox phone/PC files and determine:

1. Which system owns the phone shell.
2. Which system owns the PC shell.
3. How existing apps/sites are registered.
4. Whether registration can be data-driven.
5. What exact files an app plugin needs.
6. What files must never be copied into app mods.
7. How phone and PC share data.
8. How Lua communicates with the UI.
9. How a new site/app can be added without modifying core files.
10. What GitHub API contract all app chats must follow.

Do not build SponsorHub, FoxMail, FoxText, or any other app in JOB-01. Build the platform and plugin interface they will use.

---

## Message to every individual app chat

> You own only your app/page. Do not copy or modify the phone shell, PC shell, browser core, shared navigation, or platform registry. Use the documented RedFox Phone/PC Platform plugin API. Commit your work to your assigned GitHub folder or branch. Communicate with other apps only through the shared event/message API.

Additional shared rule: any app that needs Career/RLS data or actions must use the versioned JOB-02 bridge contract. It must not call, patch, or copy Career/RLS internals into its own ZIP.

---

## Ownership boundary between JOB-01 and JOB-02

| Area | Owner |
|---|---|
| Phone/PC shells, browser, launcher, navigation, registry, responsive UI, theme | JOB-01 |
| UI-to-Lua Career/RLS message names, payloads, result/error contract, bridge logging | JOB-02 |
| Individual app/page UI and feature logic | Its assigned app job |
| Integration approval and combined release decision | JOB-00 |

JOB-01 and JOB-02 coordinate through published contracts. Neither job copies or takes ownership of the other's implementation.

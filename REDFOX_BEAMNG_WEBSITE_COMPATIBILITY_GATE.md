# RedFox BeamNG Website Compatibility Gate

**Status:** ACTIVE — exact old/new comparison still pending  
**Owner:** JOB-00 coordination, JOB-01 page host, JOB-02 bridge, each feature job for its own page

Before converting or wiring any JOB-10 website, read:

```text
PROJECT_MANIFESTS/JOB_HANDOFFS/OWNER_BEAMNG_WEB_UI_COMPATIBILITY_INVESTIGATION_2026-07-14.md
```

## Required rule

Do not ship the normal-browser `START_HERE.html` prototype as the BeamNG runtime page.

Each feature job must:

1. prove its backend through WEUI/test controls first;
2. create a direct BeamNG-hosted page entry under its own `/ui/modModules/<app-folder>/` path;
3. register one canonical destination through JOB-01;
4. use the same entry path and backend contract from phone and PC;
5. connect gameplay/Career/RLS actions through the feature backend and JOB-02, not browser-only demonstration state;
6. keep authoritative game state out of `localStorage`;
7. test scripts, assets, bridge messages, back/close behavior, phone, PC, and a non-West-Coast map separately;
8. preserve the old working mechanism once the supplied old/new comparison proves exactly what it was.

## Do not guess the historical fix

The current likely adapter is an absolute BeamNG UI entry such as:

```text
/ui/modModules/<app-owned-folder>/<entry-file>.html
```

But the final shared conversion template must be based on evidence from:

```text
old working website/mod package
new JOB-10 website package
phone-working Scrap Yard package
PC-broken Scrap Yard package
beamng.log from both hosts
```

No chat may mass-convert all pages until one minimal page loads from both phone and PC through the same JOB-01 destination and the old/new comparison is documented.

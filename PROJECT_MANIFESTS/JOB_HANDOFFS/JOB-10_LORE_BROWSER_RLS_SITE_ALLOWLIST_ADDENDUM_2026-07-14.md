# JOB-10 Lore Browser — RLS Site Allowlist Addendum

**Date:** 2026-07-14  
**Owner:** David / Captain  
**JOB-10:** Visual Design / Real Website Polish  
**Status:** PLAN ONLY — NOT FUNCTIONAL IN BEAMNG

## Owner direction

David clarified that the first Lore/History browser does not need unrestricted general web access, but should be able to link to approved RLS-related sites in addition to BeamNG's official documentation.

## Updated first-release browser scope

The first live-web proof should use an allowlist containing:

```text
Official BeamNG documentation and BeamNG-owned pages
Official RLS Career Overhaul pages
Official RLS documentation, guides, changelogs, support, or project pages
One owner-approved community lore/wiki source later, if desired
```

The exact RLS domains are not yet recorded in the uploaded RLS package or current GitHub manifests, and a public web search did not produce a verified official RLS site. No chat may invent or assume those URLs.

Before adding RLS domains, David or JOB-12/JOB-00 must identify the official pages and confirm they are appropriate to open from IceFox.

## Suggested presentation

The Lore/History landing page should have visibly separate source groups:

```text
Official BeamNG
RLS Career Overhaul
Community Lore
```

Possible RLS links, once exact URLs are approved:

```text
RLS home/project page
Installation and update guide
Career feature guide
Vehicle marketplace guide
Economy and progression guide
Changelog/release notes
Known issues and support
Community/Discord invite page, only if external links are approved
```

## Technical boundary

- JOB-10 designs the landing page, cards, source labels, browser toolbar, loading, blocked-page, offline, and error presentation.
- JOB-01 proves external-page loading and canonical phone/PC navigation.
- JOB-11 tests each approved RLS URL for embedding, navigation, performance, and failure behavior.
- JOB-00 approves the exact domains.
- No scraping, mirroring, or copying of RLS website content is planned.
- If an RLS page blocks embedding, IceFox should offer **Open Externally** rather than bypassing the site's security rules.

## Future option

General browsing, YouTube, and unrestricted domains remain a future experimental option. They are not required for the first Lore/RLS integration milestone.

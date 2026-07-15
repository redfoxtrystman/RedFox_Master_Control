# JOB-10 Sponsor/Messaging/Rewards + Lore & History Web Page Plan

**Date:** 2026-07-14  
**Owner:** David / Captain  
**JOB-10 owner:** Visual Design / Real Website Polish regular-chat takeover / Sol  
**Status:** VISUAL/ARCHITECTURE PLAN — NOT FUNCTIONAL IN BEAMNG

## Owner direction

David confirmed that JOB-10 must add visual website/page work for:

```text
SponsorHub
FoxMail
FoxText
Sponsor Rewards
Lore & History / Wiki Browser
```

The first four belong to the JOB-12 sponsor-system family for behavior and data. JOB-10 owns their visual design, responsive layout, icons, forms, cards, lists, message presentation, loading/empty/error states, and real-website polish.

The Lore & History page is a new IceFox page intended to let players learn about BeamNG vehicle manufacturers, vehicle history, levels, trailers, and game-world lore by browsing live real web pages rather than copying, scraping, or maintaining duplicate content.

## Lore page goal

The page should feel like a believable in-universe automotive encyclopedia or research portal while still opening authoritative live BeamNG web content.

Working names only; David has not locked the title:

```text
BeamLore
BeamPedia
MotorLore
BeamNG Lore & History
```

Suggested top-level sections:

```text
Vehicle Manufacturers
Vehicle Models
Company History
Vehicle Years and Generations
Levels and Locations
Trailers and Equipment
Motorsport and Special Configurations
Game Updates / New Content
Community Lore
```

## Live-web approach — no scraping

Preferred architecture:

1. IceFox opens a local JOB-10-designed Lore landing page.
2. The landing page contains curated categories, search, bookmarks, recent pages, and featured manufacturer/vehicle cards.
3. Clicking a result opens the real external documentation/wiki page in the IceFox content area.
4. The external page remains the source of truth; RedFox does not scrape, copy, rewrite, or periodically mirror its article content.
5. Back, Forward, Home, Reload, Stop, and Open Externally controls must be available.
6. An offline/error page must appear when internet access fails.

Primary starting source:

```text
https://documentation.beamng.com/official_content/
https://documentation.beamng.com/official_content/vehicles/
https://documentation.beamng.com/official_content/levels/
https://documentation.beamng.com/official_content/trailers/
```

The official vehicle documentation already organizes vehicles by manufacturers such as Autobello, Bruckell, Burnside, Cherrier, Civetta, ETK, Gavril, Hirochi, Ibishu, Soliad, and Wentward, and includes descriptions, years, countries, body styles, configurations, propulsion, and other history-style information.

A community wiki may be added as a second source after David chooses the exact domain and JOB-00 approves it. The UI must label official documentation separately from community-authored lore.

## Technical truth / proof still required

BeamNG's UI and apps use web technologies, and the existing IceFox prototype already renders local sites through an iframe. That makes a live-web page plausible, but external internet browsing inside the actual BeamNG WebUI is not yet proven by this project.

External pages may fail to embed because of:

```text
X-Frame-Options
Content-Security-Policy frame restrictions
cross-origin limitations
certificate/TLS incompatibility
cookie or consent screens
JavaScript/browser-version requirements
pop-up or download behavior
network/offline conditions
```

Therefore no chat may claim the live wiki works inside BeamNG until David tests an exact minimal external-page proof.

## Required proof order

Before building a full Lore browser:

1. JOB-01/JOB-10 create one isolated test route that loads one approved official BeamNG documentation page.
2. Prove the page loads inside the existing IceFox/PC content area.
3. Prove phone and PC use the same canonical route and same destination.
4. Prove Back, Home, Reload, Close, and return-to-game behavior.
5. Prove a blocked or offline page shows a controlled error instead of blank white content.
6. Prove local RedFox pages still work after visiting an external page.
7. Check beamng.log and browser console for errors.
8. Only then add category navigation, search, bookmarks, community sources, or broader web navigation.

## Safe scope recommendation

The first release should use an allowlist rather than unrestricted general web browsing.

Initial allowlist candidate:

```text
documentation.beamng.com
www.beamng.com
beamng.com
```

A selected community-wiki domain can be added later after owner approval.

The page should not initially permit arbitrary downloads, file uploads, microphone/camera access, automatic pop-ups, or unrelated general-web navigation.

## Fallback behavior

If a source prevents iframe embedding, the Lore page should not scrape it as a workaround. Approved fallbacks, in order:

1. open the same URL through an external-window/browser action if BeamNG safely supports it;
2. show a page explaining that the article cannot be embedded and provide an Open Externally button;
3. provide a local curated index with article titles/descriptions and direct links, without copying the full article.

## JOB boundaries

### JOB-10 owns

```text
Lore landing page visual design
category/navigation appearance
search/bookmark/history presentation
external-page toolbar presentation
offline/blocked/error pages
responsive phone and PC layout
SponsorHub/FoxMail/FoxText/Sponsor Rewards visual design
```

### JOB-01 owns

```text
IceFox/phone/PC browser-shell support
canonical route registration
external-page container/navigation capability
safe close/return behavior
```

### JOB-02 owns

```text
shared bridge changes only if any are actually required
```

A simple external web page should not invent a Career/RLS bridge when browser navigation alone is sufficient.

### JOB-12 owns

```text
SponsorHub behavior
FoxMail behavior
FoxText behavior
Sponsor Rewards behavior
sponsor state, offers, contracts, XP, reputation, points, rewards, persistence and payments
```

### JOB-11 owns

```text
external-page runtime tests
console/log verification
phone/PC regression testing
offline/blocked-site tests
security and navigation failure checks
```

### JOB-00 owns

```text
integration approval
source/domain approval
combined release approval
```

## Current JOB-10 page backlog

Existing browser checkpoint:

```text
RedFox_JOB10_Full_Websites_v0_3_1.zip
SHA-256 0392825fc089771e4e57056ae8c3ae17cec8f10beba50ae0cbaf821f6cee9ec8
```

New pages still to design or add:

```text
SponsorHub
FoxMail
FoxText
Sponsor Rewards
Lore & History / Wiki Browser
```

All remain browser mockups until their behavior owners provide stable handoffs and David tests the exact BeamNG integration.

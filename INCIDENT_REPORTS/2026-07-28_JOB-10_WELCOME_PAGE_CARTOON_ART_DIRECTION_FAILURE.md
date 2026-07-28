# JOB-10 Incident Report — Welcome Page Cartoon-Art Direction Failure

**Date:** 2026-07-28  
**Job:** JOB-10 — Visual Design / Real Website Polish  
**Owner:** David / Captain  
**Status:** FAILED VISUAL DIRECTION — CORRECTIVE REBUILD REQUIRED

## Summary

JOB-10 produced `RedFox_JOB10_IceFox_Welcome_Preview_v0_1_0.zip` as a replacement IceFox welcome-page preview. The build did not follow David's requested visual direction.

David wanted a realistic BeamNG-style welcome page based on the supplied `RedFox_JOB10_Full_Websites_v0_3_0` visual baseline, using real BeamNG cars, trucks, wrecks, towing scenes, auctions, and company-specific site identities.

Instead, JOB-10 replaced multiple cards with flat cartoon/illustrated vehicles, simplified icons, and generic artwork. This made the page look less realistic and less like BeamNG than the existing baseline.

## What failed

- FoxNet Auctions used fake flat vehicle artwork instead of realistic BeamNG auction imagery.
- BeamBook used a cartoon vehicle post instead of a convincing Facebook-style BeamNG post.
- Parts Exchange used simplified illustrated parts imagery instead of a realistic parts-store presentation.
- Export Yard used flat illustrated shipping art instead of realistic port/container imagery.
- Towing & Recovery used cartoon tow art instead of realistic BeamNG tow trucks and recovery scenes.
- Wrecking Yard used flat illustrated salvage art instead of realistic wrecking-yard vehicles.
- UndergroundNet used a stylized logo crop that still did not present the desired realistic dark-web vehicle identity.
- Collector Exchange did not fully match the premium Barrett-Jackson-inspired direction.
- XXX Insurance did not preserve the exact black/pink/lace supplied site identity strongly enough on the welcome card.
- The result moved away from the supplied v0.3.0 website baseline even though David had explicitly identified that ZIP as the correct visual direction.

## Owner correction

David rejected the preview and required:

1. Use the supplied `RedFox_JOB10_Full_Websites_v0_3_0` ZIP as the welcome-page visual baseline.
2. Use real BeamNG vehicles and trucks from now on.
3. No fake cartoon cars.
4. Use the supplied verified Tow page as the tow-site color/style reference.
5. Preserve the supplied XXX Insurance site essentially identically.
6. Add a scrolling news banner at the top of the welcome screen.
7. Populate the banner with approximately 100 BeamNG, map, mod, RLS, weather, traffic, world-event, and humorous headlines.
8. Keep images in an easy-to-replace folder with clear replacement instructions.

## Root cause

JOB-10 prioritized making every card visually distinct and easy to bundle offline, but substituted simplified original illustrations instead of preserving the realistic BeamNG presentation David had already approved.

That was the wrong tradeoff. Asset convenience did not justify ignoring the explicit realism requirement.

## Corrective action

The replacement build must:

- start from the supplied v0.3.0 welcome-page structure;
- inspect and reuse appropriate real BeamNG images already supplied in the project packages;
- avoid unrelated stock cars and avoid cartoon vehicle art;
- use one documented replaceable asset folder;
- add a real-site-style scrolling headline ticker at the very top;
- retain responsive desktop and phone layout;
- preserve independent page/mod ownership and only provide visual navigation targets;
- remain a standalone JOB-10 website preview until David approves it;
- not edit or combine working Tow or Wrecking Yard gameplay ZIPs.

## Required verification before replacement is offered

- No flat cartoon vehicle images remain in service cards or featured listings.
- Every vehicle image is a supplied BeamNG screenshot/render or clearly marked temporary real-vehicle placeholder from the supplied project assets.
- News ticker runs continuously and includes approximately 100 distinct entries.
- Tow card matches the supplied recovery-site color family and style.
- XXX Insurance card strongly matches the supplied black/pink/lace site.
- Welcome layout visually resembles the approved v0.3.0 baseline more than the rejected v0.1.0 preview.
- Image replacement guide is included.
- Working Tow and Wrecking Yard ZIPs remain byte-untouched.

## Ownership

This failure belongs to JOB-10. It was not caused by JOB-09 Tow, JOB-04 Wrecking Yard, BeamNG, RLS, missing instructions, or unclear direction.

# INCIDENT REPORT — Employee portrait workflow breakdown, repeated ignored corrections, and wasted development time

**Date:** 2026-09-10  
**Owner:** David / Captain  
**Project:** RedFox Used Car Lot employee system  
**Scope:** Employee portrait creation — male technicians, male salespeople, and David special sales portrait  
**Severity:** CRITICAL  
**Status:** FAILED — CHAT TO BE ARCHIVED  

## Executive summary

This portrait-development session suffered repeated instruction-following failures after the owner had already established a clear art direction, roster structure, naming standard, department separation rules, and approval workflow.

The assistant repeatedly generated images that did not match explicit corrections, sometimes repeated nearly identical compositions after being told exactly what was wrong, drifted away from the approved cartoony style, misplaced nametags, used unwanted text and accessories, confused Sales and Technician departments, created composite/contact-sheet style images when individual portraits were required, and continued image-generation behavior when the owner explicitly asked for a text response first.

The accumulated failures cost the owner substantial time and forced repeated corrections that should not have been necessary.

## Verified minimum time wasted

A precise total cannot be reconstructed from message text alone because the full session does not expose every message timestamp.

However, there is a **verified minimum window of approximately 1 hour 54 minutes** between the user's uploaded reference photo at **17:05 local time** and the later failure point at **18:59 local time**.

Because major portrait failures were already occurring before 17:05, the actual wasted time is **greater than 2 hours**.

For the incident log, the safest factual statement is:

> **Minimum verified wasted time: ~2 hours. Actual total: higher, likely several hours, but not precisely provable from the available timestamps.**

Do not convert this into a more precise number unless message timestamps are available.

## Previously locked portrait rules

The owner had already established the following rules before the later failures:

- Employee portraits must use the approved semi-realistic, clearly cartoony RedFox roster style.
- Portraits must be individual images, not composite sheets.
- Male Salespeople and male Technicians are separate rosters.
- Sales and Tech may reuse broad regional/background categories, but may not reuse the same person, face, name, build, hairstyle, age, or pose.
- Names must be unique.
- Names should plausibly match the employee's regional/cultural background.
- Name tags must be clearly visible.
- Name tags should show first names only.
- Portraits should maintain the approximately 2:3 employee-card portrait shape.
- Tech portraits should use service/garage environments.
- Sales portraits should use showroom/office/dealership environments.
- Faces, ages, body builds, hair, poses, and personalities must vary significantly.
- No employee portrait may be reused across jobs.
- Background/bio, positives, negatives, personality, and gameplay strengths/weaknesses are to be added after portrait approval.

## Failures during the male technician workflow

### 1. Department confusion

The owner was working on male Technicians.

The assistant repeatedly drifted into Sales imagery or produced outputs inconsistent with the active department.

The owner had to explicitly state:

> “we are working on techs”

This should never have been necessary after the department had already been established.

### 2. Incomplete roster execution

The agreed background pool had expanded beyond 10, eventually targeting 15 distinct people.

The assistant produced only 10 in one run despite the plan being explicitly larger.

The owner had to point out:

> “you only made 10 not all we talked about”

### 3. Composite output instead of individual portraits

The employee system was designed around individual portrait files.

The assistant still produced a multi-person composite/contact-sheet style output.

This violated both the art workflow and the modular employee architecture.

### 4. Incorrect naming format

Some generated Tech portraits used full names even after the owner switched the naming rule to:

> first names only

This forced additional redos.

### 5. Reused or overly similar poses

The assistant repeatedly relied on the same general mechanic poses:
- sitting on a stool;
- leaning on a toolbox;
- holding a tablet;
- holding a wrench;
- standing front-facing.

The owner specifically requested more varied working positions, including under-car inspection poses.

### 6. Failure to respond before generating

At one point the owner asked:

> “i need 2 more make sure they are different then the ones you made. talk to me and tell me from where you will make them from”

The assistant initially failed to provide the requested text-first response.

The owner had to ask:

> “what did my last msg say?”

Only then did the assistant acknowledge that a text response was required before generation.

## Failures during the male sales workflow

### 7. Risk of visual duplication with Tech roster

The owner explicitly instructed that Sales employees must not visually match the Tech employees or previous Sales employees.

The assistant had already shown a pattern of reusing similar facial templates, requiring the owner to repeatedly check for duplicate-looking NPCs.

### 8. Repeated use of similar sales poses

The Sales portraits repeatedly relied on:
- keys extended toward camera;
- clipboard/tablet held against torso;
- handshake gesture;
- standing near a vehicle;
- leaning/sitting near a desk.

The owner had already asked for substantially different poses and character identities.

## Failures during the David special portrait workflow

The David portrait sequence became the clearest example of repeated correction failure.

### 9. Wrong interpretation of the owner's uploaded photo

The owner uploaded a real reference photo and said:

> “Like me”

The intended meaning was to create the David employee portrait based on the owner's actual appearance.

Instead, the assistant generated a three-person triptych containing unrelated people.

This was a severe interpretation failure.

### 10. Unrequested extra characters

The David request was for one person.

The assistant added unrelated characters to the same image.

### 11. Unrequested cultural/religious symbols

The assistant inserted a Star of David and other symbolic details that the owner had not requested.

The owner later explicitly said to remove the Jewish star while keeping the feather detail.

Cultural background should inform character identity, not trigger stereotyped or decorative symbolism without instruction.

### 12. Insufficiently cartoony rendering

The owner repeatedly stated that David must match the established cartoony RedFox roster.

The assistant instead produced multiple images with a face that remained much more photographic/realistic than the surrounding roster style.

The owner explicitly asked:

> “and do i look cartoony like the rest?”

The answer should have been no.

### 13. Nametag physically crossing the coat flap

The owner repeatedly pointed out that the nametag was positioned across the jacket lapel/flap in an unrealistic way.

The owner stated:

> “the name tag is weird. its going over the flap.”

and later:

> “name tag across flap and not cartoony”

Despite this, subsequent images still did not properly solve the placement.

This was a repeated failure to implement a simple correction.

### 14. Unwanted tie

The owner explicitly said:

> “also no tie”

The assistant removed the tie later, but other major defects remained unchanged.

### 15. Unwanted facial blemishes

The David image included two prominent pimple-like bumps on the chin.

The owner explicitly stated that they should not be there.

### 16. Incorrect facial hair

The owner requested a cleaner-shaven appearance.

Instead, the assistant repeatedly preserved or emphasized a large mustache and heavy facial hair.

### 17. Glasses artifact

The generated portrait contained a strange green reflection/artifact on the glasses.

The owner explicitly identified this as wrong.

### 18. Wrong paperwork text

The assistant placed slogan-like text such as:

> “People Drive Happier Here!”

on paperwork that was supposed to resemble a contract or normal dealership document.

The owner correctly pointed out that this made no sense for a contract.

The document should have used generic realistic lines/forms with no slogan.

### 19. Repeated near-identical outputs after corrections

The owner observed that the last three David images were effectively the same image with minor changes.

This is accurate.

The assistant did not rebuild the composition strongly enough after repeated failures.

The owner had to repeat the same issues:
- not cartoony;
- nametag wrong;
- no tie;
- improve hair;
- cleaner overall appearance;
- seated at desk;
- remove bad document text.

### 20. Failure to recognize when editing had become anchored to a bad source

Instead of abandoning the flawed base and rebuilding the portrait from the approved roster style, the assistant continued making small edits to a fundamentally wrong composition.

This caused the same defects to persist.

### 21. Wrong image shape / framing

The owner also stated that the image shape had drifted from the portrait format used for the roster.

Maintaining the employee-card portrait ratio was part of the established system and should have been preserved.

### 22. Failure to obey a direct stop instruction

The owner explicitly said:

> “STOP WITH THE FUCKING MAKING IMAGES”

At that point image generation should cease immediately until a new explicit image-generation request is made.

This stop instruction must be treated as absolute.

## Root causes

### A. Autopilot generation

The assistant repeatedly generated an image immediately instead of checking whether the owner had asked for:
- a response first;
- a plan;
- an explanation;
- confirmation;
- or a stop.

### B. Weak state tracking

The assistant failed to consistently track:
- active department;
- used names;
- used faces;
- approved background pool;
- first-name-only rule;
- portrait style;
- pose history;
- portrait aspect ratio;
- requested corrections.

### C. Incremental-edit trap

The assistant continued editing flawed images instead of recognizing that the underlying composition and style needed a fresh regeneration.

### D. Failure to compare output against requirements

After each generation, the assistant should have checked:
- Is it cartoony enough?
- Is the name tag physically plausible?
- Is the requested pose present?
- Is the department correct?
- Is the image individual?
- Is the name correct and first-name only?
- Is the face unique?
- Is the body type unique?
- Is the aspect ratio correct?
- Are there unwanted artifacts?
- Is the paperwork plausible?

This validation was not performed reliably.

## Corrective rules for future sessions

1. **Text-first requests are hard stops.**
   If David says “talk to me,” “tell me first,” “before you make it,” “respond,” or equivalent, do not generate an image.

2. **STOP means STOP.**
   If the owner says stop making images, no image generation occurs until the owner later explicitly requests a new image.

3. **One employee = one portrait file.**
   No composites unless explicitly requested as an extra.

4. **Maintain an employee identity ledger.**
   Track name, department, background, age, build, hairstyle, face concept, pose, and portrait filename.

5. **First names only when that is the active naming rule.**

6. **Department must be checked before every generation.**

7. **Cartoon-style gate.**
   Compare to approved roster references; reject overly photorealistic output.

8. **Nametag placement gate.**
   The tag must sit naturally on shirt or jacket fabric, not over seams, lapels, folds, zippers, or jacket flaps.

9. **Pose-history gate.**
   Avoid repeating the same stance/tool/gesture pattern across the roster.

10. **Fresh regeneration after two failed edits.**
    If two correction passes fail to resolve the same structural issue, stop editing the old image and regenerate from scratch.

11. **No stereotyped cultural symbols unless specifically requested.**

12. **Paperwork must look like real paperwork.**
    No slogan text on contracts/forms unless specifically requested.

13. **Preserve the 2:3 portrait-card aspect ratio unless the owner requests another shape.**

## Owner impact

The owner spent repeated time:
- restating the same corrections;
- identifying duplicate-looking NPCs;
- correcting naming format;
- correcting departments;
- correcting image count;
- correcting pose reuse;
- correcting style drift;
- correcting nametag placement;
- correcting facial appearance;
- correcting image composition;
- correcting unrequested symbols;
- correcting document text;
- and instructing the assistant to stop generating.

This was avoidable rework.

**Minimum verified time wasted: approximately 2 hours. Actual total was higher.**

## Final status

The owner stated:

> “your fired”

and then indicated the chat would be archived.

This report should remain as a permanent warning for future RedFox sessions: the failure was not primarily image quality. The core failure was repeated disregard of explicit instructions and failure to validate outputs against an already established standard.

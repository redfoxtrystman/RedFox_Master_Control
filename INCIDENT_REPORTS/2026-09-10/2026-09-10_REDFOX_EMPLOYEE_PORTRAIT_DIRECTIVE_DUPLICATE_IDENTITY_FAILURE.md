# INCIDENT REPORT — RedFox employee portrait directive ignored / duplicate identity / unauthorized generation

**Date:** 2026-09-10  
**Owner:** David / Captain  
**Scope:** RedFox Used Car Lot employee portrait roster / image-generation workflow  
**Severity:** HIGH  
**Status:** FAILED — STOPPED  

## Executive summary

During the RedFox Used Car Lot employee portrait work, the assistant repeatedly failed to follow explicit owner instructions and continued generating images instead of stopping and responding.

The owner required the employee portraits to remain in the established semi-realistic, lightly cartoony RedFox roster style, use visibly different faces and body types, avoid reusing the same person across jobs, use new names that were not already assigned to other employees, and represent a broad international range of backgrounds. The owner also explicitly instructed the assistant to **first provide a list of 10 locations/backgrounds to target before generating anything**, including a Lakota man, an Inuit man, an Iranian man, and a Jewish man.

Instead of answering with the requested list, the assistant entered an image-generation loop and produced another batch. This violated the requested order of operations and the owner's direct instruction to respond before generation.

The assistant also reused or near-duplicated faces across employee roles and batches after being told multiple times not to do so. Earlier in the same workflow, at least one woman was visually reused across two different jobs, forcing a replacement. Several generated men also looked too photorealistic compared with the approved cartoony roster art direction.

This incident is therefore both an **instruction-following failure** and a **roster-integrity failure**.

## Owner directives that were not followed

The owner gave the following requirements during this employee portrait workflow:

- Employee portraits must use the established RedFox semi-realistic, lightly cartoony style.
- The portraits must not drift into realistic photography.
- Faces must be substantially different from one another.
- Different ages and body types must be represented.
- Different poses must be used rather than recycling the same pose.
- Men and women must be visually distinct individuals.
- The same person must not be reused across two jobs.
- Names must not be duplicated from other employees.
- The roster should include people from many different world regions/backgrounds.
- The men's redo must specifically include:
  - a Lakota man;
  - an Inuit man;
  - an Iranian man;
  - a Jewish man.
- **Before image generation, the assistant was told to provide a list of 10 target locations/backgrounds and wait for the owner's response.**

The final instruction was not followed. The assistant generated images without first supplying the requested list.

## Specific failure modes

### 1. Unauthorized generation before required response

The owner explicitly said:

> before you make it give me a list of 10 locations that you will shoot for

The assistant did not provide the list and did not wait. It generated images instead.

This is a direct order-of-operations failure.

### 2. Repeated failure to respond when told to respond

The owner had already instructed the assistant more than once to stop autopilot behavior and answer before continuing. Despite that, the assistant again returned image generation rather than a normal response.

This created the exact failure pattern the owner had been trying to prevent.

### 3. Duplicate / near-duplicate employee identities

The owner repeatedly stated that employees must not look like the same person with minor changes.

The generated roster nevertheless contained repeated or near-repeated facial structures, hairstyles, and overall identity cues across different employees and jobs.

This is unacceptable for a persistent RPG employee system because each portrait maps to a distinct employee record. Reusing a face undermines identity consistency and can make two separate saved employees appear to be the same character.

### 4. Same woman reused across two jobs

The owner identified that one woman appeared in two different job groups.

Even though the portrait was liked, reusing the same character in two jobs violated the employee roster rule. One of those appearances must be replaced by a new, clearly distinct character.

### 5. Art-direction drift toward photorealism

The approved visual target is the stylized RedFox portrait look already used for the earlier sales roster: semi-realistic, lightly cartoony, clean illustrated rendering.

A later technician batch drifted into a much more photographic / realistic appearance.

The owner explicitly rejected that direction and asked for the established cartoony style.

### 6. Insufficient variation

The owner asked for substantial variation in:

- facial structure;
- race / geographic background;
- age;
- body type;
- hairstyle;
- clothing;
- pose;
- personality presentation.

Some batches changed pose or minor details while keeping too much of the same underlying facial construction. This does not meet the requirement for a believable 80-person employee roster.

## Why this matters to the game system

The RedFox employee system is designed as a modular roster where every employee has a persistent ID, portrait, traits, skills, XP, salary, background, employment history, and saved state.

Because portraits are tied to persistent employee IDs, visual duplication is not a cosmetic problem only. It creates identity ambiguity in the gameplay roster.

The portrait workflow therefore needs the same protected-data discipline as code:

```text
One employee ID = one unique person = one unique portrait identity.
```

If a portrait is replaced later, the employee ID and stats can remain unchanged, but the new image must still represent that same unique character.

## Corrective controls

### Control 1 — mandatory response gate

When the owner asks for a list, prompt, plan, roster, names, or approval step **before generation**, image generation must not begin until that step is completed and the owner approves continuation.

### Control 2 — no autopilot image batches

A request to “answer me,” “tell me first,” “before you make it,” or equivalent language creates a hard stop.

The assistant must return text only.

### Control 3 — employee identity ledger

Maintain an employee identity ledger containing at least:

- employee ID;
- full name;
- job;
- gender;
- approximate age;
- world-region / cultural background;
- body type;
- face description;
- hairstyle;
- pose;
- portrait filename;
- distinguishing accessories.

Before generating a new employee, compare against the ledger to avoid duplicate names and repeated visual identities.

### Control 4 — explicit diversity matrix

For large batches, pre-plan the roster so no single facial template dominates.

The matrix should intentionally vary:

- world region / ancestry;
- age band;
- body build;
- height impression;
- hair length / texture;
- facial hair;
- glasses / accessories;
- clothing silhouette;
- posture;
- pose;
- expression.

### Control 5 — protected art-style reference

The approved RedFox sales portraits are the visual baseline.

Future portraits must stay in that semi-realistic lightly cartoony illustration style and must not drift to photographic rendering unless David explicitly requests a new style.

### Control 6 — no cross-job portrait reuse

A portrait already assigned to one employee cannot be reused for another employee or another job.

If the owner wants a person transferred between jobs in gameplay, that must happen by moving the same employee record, not by cloning the portrait into a second employee.

### Control 7 — name uniqueness gate

Before accepting a new employee name, compare it against all existing employee names in the RedFox roster.

Duplicate first names should also be avoided where practical because the UI prominently displays names and the owner specifically requested different names for this batch.

## Required next action

Do **not** generate another employee portrait batch yet.

First provide David with the requested proposed set of **10 distinct male backgrounds/locations** for the redo, including:

- Lakota;
- Inuit;
- Iranian;
- Jewish;
- six additional globally distinct backgrounds.

For each proposed employee, provide a new name, approximate age, body type, visual character concept, and a unique pose.

Only after David approves that list should the portraits be generated.

After that, identify the duplicated female employee used in two jobs and replace one version with a new unique woman while preserving the roster ID/stat record for the job slot being replaced.

## Acceptance condition

This incident remains open until:

- the owner receives the requested text plan before any new generation;
- all 10 redesigned men have unique names and visibly unique identities;
- the set includes the requested Lakota, Inuit, Iranian, and Jewish men;
- body types, ages, faces, hair, and poses show meaningful variation;
- the established cartoony RedFox art direction is preserved;
- no portrait is reused across jobs;
- the duplicated female portrait is replaced;
- and the owner confirms the resulting roster is acceptable.

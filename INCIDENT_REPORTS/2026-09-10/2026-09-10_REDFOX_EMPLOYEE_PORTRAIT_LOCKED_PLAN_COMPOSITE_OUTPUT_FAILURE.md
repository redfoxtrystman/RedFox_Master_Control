# INCIDENT REPORT — RedFox employee portrait batch ignored locked roster plan

**Date:** 2026-09-10  
**Owner:** David / Captain  
**Scope:** RedFox Used Car Lot employee portrait roster / male Sales + Technician redo  
**Severity:** HIGH  
**Status:** FAILED — STOPPED  

## Executive summary

The assistant failed to follow the locked employee portrait plan that had just been agreed with David.

The agreed plan was explicit: the male Salespeople and male Technicians were to be fully redone as new people; all names were to be unique and culturally/regionally appropriate; every portrait was to have a visible nametag; Sales and Tech could reuse broad background categories but could not reuse the same person, face, name, build, hairstyle, age, or pose; and the roster was to use an expanded pool of 15 backgrounds rather than stopping at 10.

The assistant then produced a single roster-style composite image rather than continuing the requested portrait workflow. This did not match the agreed structure and also introduced additional deviations from the locked rules.

## Locked plan that had been agreed

### Identity rules

- All names must be unique.
- Names must plausibly match the person's region/background.
- Every portrait must have a clearly visible nametag.
- Male Salespeople and Male Technicians are to be fully redone as new people.
- Sales and Techs may share the same broad background categories, but not the same:
  - person;
  - face;
  - name;
  - body build;
  - hairstyle;
  - age;
  - pose.
- Employee portraits are not to be reused across departments.

### Expanded background pool

The agreed target pool was:

1. Lakota / Native American
2. Jewish
3. Alaskan / Alaska Native
4. Native Hawaiian
5. Ukrainian
6. Iranian
7. Japanese
8. White American
9. English / UK
10. French
11. Mexican
12. Nigerian
13. Filipino
14. Italian
15. Indian

David explicitly stated that there was no requirement to remain at 10 and approved expansion beyond 10.

### Required visual variation

The assistant was to deliberately vary:

- age;
- skin tone;
- face shape;
- nose / jaw / brow structure;
- hair type and style;
- body type;
- clothing;
- posture;
- pose;
- personality / energy.

The stated purpose was to prevent the recurring “same guy with a new nametag” failure.

### Required body-type variation

The agreed body-type/personality spread included examples such as:

- lean;
- athletic;
- broad-shouldered;
- stocky;
- soft/heavyset;
- average build;
- lanky;
- older rugged;
- polished office type;
- nerdy/detail-focused type.

### Department structure

**Male Salespeople**
- more polished;
- showroom-appropriate;
- distinct sales personalities.

**Male Technicians**
- workwear / shop-ready;
- different tool and diagnostic poses;
- varied and believable mechanics.

### Post-image employee data

After the portraits are approved, each employee is to receive:

- background / short bio;
- positive traits;
- negative traits;
- personality;
- strengths / weaknesses for gameplay;
- skills/personality notes.

## Additional owner instruction immediately before the failed batch

David added that some employees should look more unconventional or “out of the box,” referencing the previously liked woman with purple hair.

He specifically requested:
- one young White American male technician in his 20s;
- visibly red hair;
- a unique person, not reused from Sales.

The assistant did create a red-haired technician, but then continued into a batch that did not preserve the agreed portrait-by-portrait workflow.

## Failure in the subsequent output

The assistant produced a single 15-person roster/composite poster.

This was not what the locked plan described.

Problems included:

- The output was a composite roster sheet rather than individual employee portrait images.
- The agreed workflow was to create new male Salespeople and new male Technicians as separate unique employees, not collapse them into one poster.
- The image combined 15 people into a single artifact, making it unsuitable for the modular employee system where each employee needs an independent portrait file.
- The roster format makes later portrait replacement impossible without editing/re-generating the entire sheet.
- It undermines the intended mapping of one employee ID to one portrait filename.
- The composite format makes facial duplication harder to inspect and easier to miss.
- It did not preserve the intended 2:3 portrait-card usage.
- It changed the deliverable structure without owner approval.

## Why the composite format is technically wrong for the employee system

The employee architecture was intentionally designed around individual portrait files, e.g.:

```text
employee_id -> portraits/EMPLOYEE_ID.png
```

This allows a face to be replaced without changing:
- stats;
- XP;
- salary;
- traits;
- employment history;
- save data.

A 15-person composite roster image breaks this modular design because multiple employee identities are baked into one image.

## Corrective controls

### Control 1 — one employee, one image file

Every employee portrait must be generated and stored independently.

No contact sheet, roster board, multi-character poster, or composite image may substitute for individual portrait assets unless David explicitly requests one as a separate supplemental image.

### Control 2 — preserve the locked roster pool

Do not silently reduce, reorder, replace, or reinterpret the 15 approved background categories.

### Control 3 — department separation

Sales and Tech sets must be developed separately, even when the same cultural/background pool is reused.

### Control 4 — identity uniqueness check before each generation

Before generating a person, verify against the existing Sales and Tech identity ledger:
- unused full name;
- unused face concept;
- unused body concept;
- unused pose concept;
- unused hairstyle combination.

### Control 5 — visible nametag gate

A candidate portrait fails if the employee name is not visibly readable on the uniform/badge.

### Control 6 — no style drift

Continue using the approved lightly cartoony / semi-realistic RedFox portrait style, not photorealism.

## Required next action

Do not create another composite roster image.

Continue with individual employee portrait images using the approved 15-background pool, preserving:
- unique names;
- region-appropriate names;
- unique faces;
- unique builds;
- unique ages;
- unique hairstyles;
- unique poses;
- visible name tags.

The young red-haired White American technician concept remains valid and may be kept as one of the technician identities if David approves the portrait.

## Acceptance condition

This incident remains open until the male Sales and male Technician redos are delivered as individual portraits and the owner confirms that:

- every employee is a unique person;
- all names are unique and region-appropriate;
- all name tags are visible;
- no Sales person is reused as a Tech;
- no Tech is reused as Sales;
- the 15-background pool is followed;
- the approved cartoony RedFox style is maintained;
- and each employee can be mapped to its own portrait file and later gameplay profile.

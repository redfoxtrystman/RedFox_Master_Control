# JOB-04 Handoff — Port JOB-09 Tow Yard Business / Location Framework to Wrecking & Scrap Yard

Date: 2026-08-16
From: JOB-09 — RedFox Tow & Recovery Dispatch
To: JOB-04 — Scrap Yard / Wrecking Yard
Status: DESIGN + SOURCE HANDOFF; DO NOT BUILD FROM AN OLD TOW VERSION

## Owner request

The complete working Tow Yard location/property/business-branch framework is to be adapted for JOB-04 so the Wrecking/Scrap Yard can have real physical yard locations as well.

JOB-04 remains its own business/job. Do not merge JOB-04 and JOB-09 business identities or storage records.

The owner will upload the current working Tow Yard build. That exact uploaded build is the required source of truth for the port. Do not copy from an older Tow archive merely because it contains similar functions.

## Framework to port from JOB-09

Port the entire functional pattern, adapted and renamed for Wrecking/Scrap Yard:

1. Multiple yard locations per map.
2. Existing custom yard marker/location records.
3. Ability to designate a purchased RLS property/garage as an additional yard using the property's real physical location.
4. Ability to link an existing custom yard to a purchased RLS property/garage without replacing the custom yard identity.
5. Persistent independent RedFox yard IDs.
6. Preserve the real RLS garage/property ID separately when linked.
7. Yard rename support.
8. Yard navigation.
9. Move custom yard marker to player position.
10. Independent per-yard storage/capacity metadata appropriate to JOB-04.
11. Duplicate-property-link prevention.
12. Save/rollback behavior on failed yard/property changes.
13. Facility transform lookup from RLS purchased garages.
14. In-place upgrade of already-created yards rather than recreating them.
15. One formal RLS-backed business identity/account with multiple yard branches.
16. First linked yard may become the primary business anchor; additional yards are branches of the same Wrecking/Scrap business.
17. Ability to change which branch is the primary anchor without recreating yards.
18. Existing purchased-property links must survive business-branch linking.
19. Existing JOB-04 inventory/scrap records must not be migrated merely by linking a branch.
20. No RLS source files are to be edited.

## Adaptation rules

Do NOT literally share JOB-09 runtime state, IDs, save keys, business type, or storage namespace with JOB-04.

JOB-04 needs its own equivalents, for example:
- Wrecking/Scrap business type and business ID
- Wrecking/Scrap yard IDs
- Wrecking/Scrap save section
- Wrecking/Scrap storage/capacity keys
- JOB-04-specific UI labels/actions

The architecture may be ported; the namespaces must remain independent.

## Physical-location goal

JOB-04 is moving toward physical Wrecking/Scrap Yard locations using the same general location pattern proven by Tow:

- purchased RLS property can become a Wrecking/Scrap Yard;
- manually chosen custom location can become a Wrecking/Scrap Yard;
- a custom yard may optionally be linked to a real purchased RLS property;
- multiple yards may coexist on one map;
- future physical business PC/toolbox/businessGarage work should attach to these existing yard records rather than create replacement yards.

## Current JOB-09 reference point

JOB-09 v0.5.0.28 introduced the first RLS business-foundation branch-link pattern on top of the existing Tow Yard system:
- formal business type: `redfoxTow`
- one business ID/account shared by multiple Tow Yard branches
- existing Tow Yards upgrade in place
- purchased-property/garage links remain intact
- no fleet migration just from linking a branch
- no RLS source-file edit

The owner is expected to provide the latest working Tow archive before JOB-04 implementation begins. If the uploaded Tow build differs from v0.5.0.28, use the uploaded working build as authoritative and re-audit the relevant functions before porting.

## Required source-first workflow

1. Inspect the uploaded current working Tow archive completely for the relevant yard/business/location code.
2. Inspect the current working JOB-04 Wrecking/Scrap archive.
3. Diff current JOB-04 against prior working baselines if needed to identify authoritative save/UI/inventory code.
4. Identify exact functions/data structures to port and exact JOB-04 equivalents.
5. Plan namespace substitutions before editing.
6. Do not copy unrelated Tow jobs, Repo, Recovery, custody, dispatch, auction, phone/PC code, or Tow-specific vehicle lifecycle into JOB-04.
7. Build the port in JOB-04 only after source review.
8. Validate Lua/JSON/ZIP integrity and changed-file scope.
9. Runtime-test one existing custom JOB-04 yard, one purchased-property designation, one custom-yard-to-property link, save/reload, and a second branch.

## Important separation rule

Wrecking Yard/Scrap Yard is JOB-04. Tow/Recovery is JOB-09. The physical-location framework should be consistent between them, but each business owns its own records, vehicles, money, storage, and yard identities.

## Deferred/future JOB-04 facility work

After the location/business branch framework proves stable, JOB-04 can add the same class of physical facility features planned for Tow:
- business PC placement/use
- toolbox placement/use where supported
- formal physical businessGarage
- fleet/yard parking
- storage zones/capacity
- map-agnostic claimed facilities
- future purchase/lease pricing and yard limits

These later pieces must attach to the existing JOB-04 yard record rather than creating a new duplicate yard.

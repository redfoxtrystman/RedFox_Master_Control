# JOB-04 Handoff — Port JOB-09 Tow Yard Business / Location Framework to Wrecking & Scrap Yard

Date: 2026-08-17
From: JOB-09 — RedFox Tow & Recovery Dispatch
To: JOB-04 — Scrap Yard / Wrecking Yard
Status: DESIGN + SOURCE HANDOFF; DO NOT BUILD FROM AN OLD TOW VERSION

## Owner request

The complete working Tow Yard location/property/business-branch framework is to be adapted for JOB-04 so the Wrecking/Scrap Yard can have real physical yard locations as well.

JOB-04 remains its own business/job. Do not merge JOB-04 and JOB-09 business identities or storage records.

The owner will upload the current working Tow Yard build. That exact uploaded build is the required source of truth for the port. Do not copy from an older Tow archive merely because it contains similar functions.

# EXACT TOW YARD SETUP WORKFLOW TO COPY

This section explains how JOB-09's yard setup actually works so JOB-04 can reproduce the same user flow and data model for Wrecking/Scrap Yards.

## 1. A RedFox yard is its own persistent object

The RedFox yard is NOT the same thing as an RLS garage/property.

Each Tow Yard has its own stable RedFox yard identity and storage identity, including concepts equivalent to:

- stable RedFox yard ID
- current map
- world position
- rotation/facing when needed
- user-visible custom yard name
- independent RedFox storage key
- independent capacities
- optional linked RLS garage/property ID
- later business-branch metadata

The important rule is that the RedFox yard remains authoritative as the branch/location record even when linked to an RLS property.

JOB-04 must do the same with a Wrecking/Scrap Yard record.

## 2. Custom yard creation — `Add Another ... Yard Location Here`

Tow lets the player stand at any usable world location and create another Tow Yard at the current position.

The equivalent JOB-04 flow should be:

`ADD ANOTHER WRECKING / SCRAP YARD LOCATION HERE`

When used:

1. Read the current map and player/world position.
2. Generate a new stable JOB-04 yard ID.
3. Generate a new independent JOB-04 storage key.
4. Save the position as that yard's physical location.
5. Create default Wrecking/Scrap capacity metadata.
6. Do NOT require the location to be an RLS purchasable property.
7. Do NOT automatically convert it into a Career garage.
8. Save it immediately and roll back if the save fails.

This allows physical Wrecking/Scrap Yards on maps/locations that have no native purchasable property.

## 3. Purchased property can become a new RedFox yard

Tow can enumerate purchased RLS garages/properties and designate one as an additional Tow Yard using the property's real physical facility location.

The JOB-04 equivalent should be:

`DESIGNATE THIS PURCHASED PROPERTY AS A WRECKING / SCRAP YARD`

When used:

1. Enumerate only legitimate purchased RLS properties/garages from RLS.
2. Resolve that facility's real world transform/location.
3. Create a NEW RedFox Wrecking/Scrap Yard record at that physical location.
4. Give it its own JOB-04 stable yard ID and storage key.
5. Store the real RLS garage/property ID separately as the link.
6. Refuse to designate the same purchased property twice for the same JOB-04 business.
7. Do not delete or replace any other Wrecking/Scrap Yard.
8. Save/rollback safely.

For Tow, if the native property already has a useful name such as `Recovery Yard`, the initial RedFox yard display name may inherit that facility name. JOB-04 can use the same pattern for relevant native facility names while still allowing the player to rename the RedFox yard later.

## 4. Existing custom yard can be linked to a purchased property WITHOUT moving or replacing it

Tow also has a separate workflow where an already-created custom Tow Yard can be linked to a purchased RLS property.

This is different from creating a new yard at the property's location.

The JOB-04 equivalent should be:

`LINK THIS EXISTING WRECKING / SCRAP YARD TO A PURCHASED PROPERTY`

When used:

- keep the existing JOB-04 yard ID;
- keep its existing physical position;
- keep its existing storage key;
- keep its current capacities;
- keep its existing stored inventory/vehicles/material records;
- add only the RLS garage/property ID relationship;
- do not teleport the custom yard to the purchased property;
- do not create a second yard;
- prevent duplicate/ambiguous property links;
- save/rollback safely.

This lets the player use a purchased property for ownership/business legitimacy while keeping the actual Wrecking/Scrap operation at a better nearby physical location.

## 5. Yard Management controls used by Tow

The Tow Yard Management screen gives each selected yard controls equivalent to:

- select yard
- rename yard
- save custom yard name
- navigate to this yard
- move this custom yard marker to my current position
- show stable RedFox yard ID
- show independent storage key
- show current position
- show linked purchased RLS garage/property when present
- business-branch state

JOB-04 should adapt the same management pattern for Wrecking/Scrap Yards rather than inventing a completely different location UI.

## 6. Existing yards are upgraded IN PLACE into business branches

JOB-09 v0.5.0.28 added the first formal RLS business-foundation link.

The user selects an already-existing Tow Yard and uses:

`LINK THIS EXISTING TOW YARD TO REDFOX TOW BUSINESS`

This does NOT create another Tow Yard.

The branch link preserves:

- stable RedFox yard ID
- independent storage key
- physical location
- custom name
- capacities
- current RLS property/garage link
- existing Tow inventory/fleet/custody data

Only business-branch metadata is added.

JOB-04 should use the same model:

`LINK THIS EXISTING WRECKING / SCRAP YARD TO WRECKING / SCRAP BUSINESS`

Do not migrate or reinterpret existing JOB-04 scrap inventory merely because the yard becomes a business branch.

## 7. One business, multiple branches

Tow uses one formal business identity and one RLS-backed business account shared by multiple Tow Yard branches.

JOB-04 must have its OWN business type/business ID/account, but use the same architecture:

ONE Wrecking/Scrap business
→ ONE business account
→ MANY Wrecking/Scrap Yard branches

Do not create a separate business/account for each yard.

The first linked yard may be the PRIMARY BUSINESS YARD/ANCHOR.

Additional existing yards become branches of the same business.

The primary anchor should later be changeable without recreating or moving yards.

## 8. Internal IDs and visible names must be separate

Tow's internal business identity remains fixed even if the player later renames the company.

JOB-04 should follow the same rule:

- fixed internal business type
- fixed internal business ID
- fixed yard IDs/storage keys
- player-editable business display name
- player-editable branch/yard names

Renaming the visible Wrecking/Scrap business or a yard must never rename IDs, storage keys, account identity or ownership references.

The visible company name should eventually be save-specific and map-wide/system-wide for that Career save, just as planned for Tow.

## 9. Physical facility features attach to the existing yard record

Future PC/toolbox/businessGarage/storage-zone work must use the already-created JOB-04 yard record as its anchor.

Do NOT solve physical facilities by creating replacement duplicate yards.

The intended future structure is:

Wrecking/Scrap Business
→ Yard Branch
   → physical yard marker/location
   → optional purchased-property link
   → business PC position/interaction
   → toolbox position/interaction where supported
   → businessGarage/parking/storage zones
   → Wrecking/Scrap inventory/storage capacities

For purchased properties that already have a normal Career/house computer, keep that existing computer untouched. A future Wrecking/Scrap BUSINESS computer may be placed/attached separately if the business system requires it.

## 10. Do not edit RLS source files

JOB-09's current direction is to integrate through public/runtime APIs and RedFox-owned bridge code rather than patching RLS files, because RLS updates frequently.

JOB-04 must follow the same update-resistant rule unless the owner explicitly approves an RLS source patch after a source audit.

# Framework to port from JOB-09

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

# Adaptation rules

Do NOT literally share JOB-09 runtime state, IDs, save keys, business type, or storage namespace with JOB-04.

JOB-04 needs its own equivalents, for example:

- Wrecking/Scrap business type and business ID
- Wrecking/Scrap yard IDs
- Wrecking/Scrap save section
- Wrecking/Scrap storage/capacity keys
- JOB-04-specific UI labels/actions

The architecture may be ported; the namespaces must remain independent.

# Physical-location goal

JOB-04 is moving toward physical Wrecking/Scrap Yard locations using the same general location pattern proven by Tow:

- purchased RLS property can become a Wrecking/Scrap Yard;
- manually chosen custom location can become a Wrecking/Scrap Yard;
- a custom yard may optionally be linked to a real purchased RLS property;
- multiple yards may coexist on one map;
- future physical business PC/toolbox/businessGarage work should attach to these existing yard records rather than create replacement yards.

# Current JOB-09 reference point

JOB-09 v0.5.0.28 introduced the first RLS business-foundation branch-link pattern on top of the existing Tow Yard system:

- formal business type: `redfoxTow`
- one business ID/account shared by multiple Tow Yard branches
- existing Tow Yards upgrade in place
- purchased-property/garage links remain intact
- no fleet migration just from linking a branch
- no RLS source-file edit

The owner has runtime-proven that the first Tow Yard can link as the primary RedFox Tow business branch and that the RedFox Tow business account is visible in the RLS bank. The RLS Business Computer route opens but its Tow business UI content is not yet populated; do not treat the blank UI as a finished pattern to copy.

The owner is expected to provide the latest working Tow archive before JOB-04 implementation begins. If the uploaded Tow build differs from v0.5.0.28, use the uploaded working build as authoritative and re-audit the relevant functions before porting.

# Required source-first workflow

1. Inspect the uploaded current working Tow archive completely for the relevant yard/business/location code.
2. Inspect the current working JOB-04 Wrecking/Scrap archive.
3. Diff current JOB-04 against prior working baselines if needed to identify authoritative save/UI/inventory code.
4. Identify exact functions/data structures to port and exact JOB-04 equivalents.
5. Plan namespace substitutions before editing.
6. Do not copy unrelated Tow jobs, Repo, Recovery, custody, dispatch, auction, phone/PC code, or Tow-specific vehicle lifecycle into JOB-04.
7. Build the port in JOB-04 only after source review.
8. Validate Lua/JSON/ZIP integrity and changed-file scope.
9. Runtime-test in this order:
   - create one custom Wrecking/Scrap Yard at player position;
   - save/reload and verify stable ID/location/storage key;
   - designate one purchased RLS property as an additional Wrecking/Scrap Yard;
   - verify no duplicate property designation;
   - link an existing custom Wrecking/Scrap Yard to a purchased property without moving/replacing it;
   - rename/navigate/move a custom yard;
   - link first existing yard to the formal Wrecking/Scrap business as primary branch;
   - verify one RLS business account;
   - link a second existing yard as another branch of that same business/account;
   - save/reload and verify all identities/links remain intact;
   - verify no existing JOB-04 scrap/inventory records changed ownership/storage just from branch linking.

# Important separation rule

Wrecking Yard/Scrap Yard is JOB-04. Tow/Recovery is JOB-09. The physical-location framework should be consistent between them, but each business owns its own records, vehicles, money, storage, and yard identities.

# Deferred/future JOB-04 facility work

After the location/business branch framework proves stable, JOB-04 can add the same class of physical facility features planned for Tow:

- business PC placement/use
- toolbox placement/use where supported
- formal physical businessGarage
- fleet/yard parking
- storage zones/capacity
- map-agnostic claimed facilities
- future purchase/lease pricing and yard limits

These later pieces must attach to the existing JOB-04 yard record rather than creating a new duplicate yard.

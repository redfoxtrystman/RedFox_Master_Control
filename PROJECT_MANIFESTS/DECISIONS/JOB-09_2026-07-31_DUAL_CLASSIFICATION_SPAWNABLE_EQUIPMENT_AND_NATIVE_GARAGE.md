# JOB-09 Decision — Spawnable Items Use Native Garage Compatibility

**Date:** 2026-07-31  
**Owner:** David / Captain  
**Applies to:** JOB-09 Tow / Recovery / Dispatch  
**Status:** FINAL OWNER DIRECTION — SUPERSEDES THE EARLIER DUAL-CLASSIFICATION PROPOSAL

## Final owner instruction

Fix the v0.4.4.6 garage-delivery block and leave props alone.

Spawnable records such as `FP Crane Chains 2 rotatable chains`, walking-character configurations, attachments, props and other equipment may be handled by BeamNG through the same Career/RLS inventory and garage pipeline used for vehicles. JOB-09 must not block those records merely because they are equipment or props.

## Required behavior

- Preserve the exact stored model/config identity.
- Allow the existing native spawn, `career_modules_inventory.addVehicle`, purchased-garage placement and final verification transaction to decide compatibility.
- Preserve pending inventory IDs, exactly-once behavior, rollback, identity-conflict protection and duplicate prevention.
- Do not add RedFox prop/equipment classification metadata to the transferred Career record.
- Do not modify third-party prop files, equipment files, JBeams, controllers, models or spawn behavior.
- Do not change stock Career/RLS inventory classes.
- Keep abandoned/lien call-selection rules separate from garage-delivery eligibility.

## v0.4.4.7 scope

1. Remove v0.4.4.6's equipment/attachment/prop garage-delivery rejection.
2. Require only complete stored model/config identity before attempting native delivery.
3. Remove real-world title-class wording from the blocking message.
4. Leave every prop/equipment file and behavior untouched.
5. Preserve v0.4.4.6 as rollback.

No broader equipment-registry or reclassification work is authorized by this decision.

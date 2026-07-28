# JOB-09 v0.3.5 — Source Summary

## Baseline

Built from v0.3.4, which preserves David-confirmed v0.3.0 dispatch behavior, the v0.3.3 top-tab WEUI/Scene Builder, and safe Fleet Book tow-yard assignment metadata.

Runtime file:

`lua/ge/extensions/redfoxTowRecoveryDispatch.lua`

## Saved target selection

Saved tow targets are interpreted as layout slots. Unless a future template explicitly sets `lockExactVehicle=true` or an exact selection policy, replay:

- preserves the saved relative position and rotation;
- preserves the scene role and vehicle class;
- rerolls an eligible model/configuration from that class;
- applies the existing recent exact-configuration and recent model block windows;
- blocks duplicate exact/model selections within the same multi-target scene when the pool allows;
- retains the original saved model/config only as a final compatible fallback.

Legacy v0.3.3/v0.3.4 templates have no selection-policy field. Missing policy intentionally means same-class reroll, so existing scene files require no destructive migration.

## Strict saved-scene roster

Saved non-target items remain exact roster records:

- police and emergency support vehicles;
- fire/EMS/support vehicles;
- cones, signs, barricades, warning markers, debris, and other saveable props.

`spawnTemplateTargets` now returns failure when any required target or scene item fails to spawn. It records expected/spawned roster counts and no longer silently omits failed support equipment.

Saved emergency-support metadata is carried in runtime scene-equipment records, preserved through re-save, and used to reactivate emergency support. When saved emergency support exists, the normal random police-support roll is skipped.

## Atomic manual replay

Scene Builder replay now stages the new target/support roster before deleting the current scene. On failure:

- staged partial objects are deleted;
- the current scene objects and editor state are preserved;
- an explicit incomplete-replay error names the missing item;
- no success message is shown.

On success, the old scene is replaced and the new target selections are added to recent dispatch variety memory.

## UI additions

The saved-template panel now shows:

- tow-target layout slots;
- required scene equipment/support count;
- same-class target replay policy;
- strict all-required roster policy.

Save and replay messages report complete roster counts.

## Preserved boundaries

- No stock BeamNG or RLS files are overwritten.
- Company garage movement and legacy retrieval remain safety-locked.
- Fleet Book yard assignment remains metadata-only.
- Purchased-property computer integration, yard color metadata, NPC driver runtime, and autonomous jobs remain deferred.

## Runtime status

**BUILT — STATIC VERIFIED — RUNTIME PENDING DAVID**
# JOB-09 — RedFox Tow & Recovery Dispatch v0.2.7

**Status:** BUILT — RUNTIME UNTESTED  
**Module:** `redfox_tow_recovery_dispatch`  
**Installable:** `19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_7_SpamGuardDispatchVariety.zip`  
**SHA-256:** `926aff0ce34615fd6aa7774ee867c08d1840e5b1ee92613a60c4f50a04921bd7`

## Trigger

David completed limited v0.2.6 Standard Tow testing and received the same very large Jerr-Dan/Jordan tow-truck target twice consecutively. A separate installed mod described as the PSA mod was also flooding the game and causing severe lag, so JOB-09 was audited for similar behavior.

## Spam audit result

- No `log()` call exists in the per-frame `M.onUpdate` body.
- No `saveState()` or `writeJson()` call exists directly in `M.onUpdate`.
- Dispatch scheduling remains behind a one-second tick gate.
- Route refresh remains approximately every eight seconds and does not log.
- Scene placement entries remove themselves after stabilization/release.
- Save writes remain tied to calls, payments, user actions, Career save hooks, or extension unload.
- The eligible installed-vehicle catalog is cached for the session.
- A one-time `[RedFox][TOW][SPAM_AUDIT]` startup diagnostic was added.

The PSA mod itself was not supplied and was not inspected.

## Selection root cause

v0.2.6 selected Standard Tow targets uniformly from a combined road-vehicle pool that included passenger, heavy, and bus configurations. A mod with many configurations could dominate that pool. There was also no recent-selection memory.

## v0.2.7 repair

- Standard Tow selection is passenger-biased: 82% passenger, 12% heavy, 4% bus, 2% semi.
- Heavy tow trucks remain possible rare targets rather than being blacklisted.
- Exact model/configuration repeats are avoided for six calls by default.
- Same-model repeats are avoided for two calls by default.
- When the preferred class contains only recently used models, another suitable class is tried before relaxing the repeat rule.
- Recent selection memory is saved per Career profile in the existing JOB-09 yard-state file.
- WE UI settings can disable the system or adjust both repeat windows.

## Preserved

All v0.2.6 police-year filtering, tractor/trailer compatibility checks, elevated spawn settling, $750 storage default, Fleet Book, yard, impound, history, scene, and save-path behavior remains.

## Focused test

1. Disable older JOB-09 ZIPs and enable only v0.2.7.
2. Verify Fleet Book, yards, records, and settings remain.
3. Leave WE UI open five minutes and inspect `redfoxTowRecoveryDispatch` log output.
4. Run five Standard Tow selections and record each target in order.
5. Continue unfinished v0.2.6 police, semi/trailer, terrain, and custom-scene tests afterward.

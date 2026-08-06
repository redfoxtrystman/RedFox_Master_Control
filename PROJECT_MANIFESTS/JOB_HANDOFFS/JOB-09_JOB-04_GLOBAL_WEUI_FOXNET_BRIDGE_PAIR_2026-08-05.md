# JOB-09 / JOB-04 Global WEUI–FoxNet Bridge Pair

**Date:** 2026-08-05 (owner local time)  
**Owner:** David / Captain  
**Status:** BUILT, STATIC/HARNESS VERIFIED, BEAMNG RUNTIME UNPROVEN

## Confirmed root cause

JOB-09 v0.4.9.4 regressed to using `extensions.redfoxTowRecoveryDispatch` as its primary website bridge lookup. Earlier runtime evidence had already proven that the live Tow WEUI uses the loaded global extension table `redfoxTowRecoveryDispatch`. This allowed the WEUI to show real yards, fleet units and stored vehicles while the FoxNet page remained disconnected or empty.

The correction is global-first everywhere:

```lua
local m = rawget(_G, "redfoxTowRecoveryDispatch")
if not m and extensions and extensions.load then
  extensions.load("redfoxTowRecoveryDispatch")
  m = rawget(_G, "redfoxTowRecoveryDispatch")
      or extensions.redfoxTowRecoveryDispatch
end
```

The global table is authoritative. The `extensions` alias remains only a compatibility fallback after an explicit load attempt.

State reads use `getWebPortalStateJson()`. Actions use `webPortalActionJsonResult(action, payloadJson)` and return a new complete state. No website-only Tow state was introduced.

## JOB-09 v0.4.9.5

Archive:

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_4_9_5_GLOBAL_WEUI_FOXNET_BRIDGE.zip`

- SHA-256: `addb9cdf006947c0d274a4bd31ec1cd00feaa730572833a6a1775563e55df787`
- Size: 4,455,140 bytes
- Files: 65
- Baseline: v0.4.9.4
- Added: 0
- Removed: 0
- Changed: 12
- Unchanged: 53

Changes are limited to version/module metadata, the lightweight loader/resolver, the Tow portal and WEUI bridge expressions, cache tokens, and read-only bridge diagnostics. Main Tow business Lua changes are limited to version text and diagnostics.

The authoritative state still includes `yards`, `yardsByLevel`, `fleet`, `yardVehicles`, `inventory`, `shopInventory`, invoices, active calls, business money and other existing Tow company data.

## JOB-04 v0.3.2.4.8 companion host

Archive:

`zzzz_RedFox_FoxNet_JOB-04_Wrecking-Yard_2026-08-05_v0_3_2_4_8_GLOBAL_TOW_BRIDGE_RECEIPT_FILTERS_FROM_v0_3_2_4_7.zip`

- SHA-256: `7283112f3def496895e1d6c2c456c241f2168f02f7de230737abf983833563c2`
- Size: 16,999,192 bytes
- Files: 689
- Baseline: v0.3.2.4.7
- Added: 6
- Removed: 0
- Changed: 27
- Unchanged: 656

JOB-04 owns the FoxNet PC host, nested phone browser and compiled BeamNG phone host, so the bridge cannot be fixed in JOB-09 alone. The companion release:

1. uses the global-first Tow resolver in the PC host;
2. forwards Tow requests through the nested phone browser;
3. uses raw `bngApi.engineLua(expression, callback)` in the compiled phone host instead of an unregistered generated `Lua_default.extensions.redfoxTowRecoveryDispatch` signature;
4. maps `ready` to `portal_ready`, `state-request` to a state read, and `action` to the JOB-09 action-plus-state API;
5. routes Tow to cache token `v=0495`;
6. carries the v0.3.2.4.7 compact expandable receipt sorting forward through a cache-proof v0.3.2.4.8 page.

All eight JOB-04 Lua files are byte-identical to v0.3.2.4.7. Sale prices, payment, vehicle removal, purchase delivery, transaction persistence, receipt storage, compact expansion, receipt sorting and Auction business logic were not changed.

## Validation

The paired build completed:

- ZIP integrity, duplicate-path and traversal checks;
- fresh extraction file-set and byte equality;
- syntax checks across 55 JSON, 49 JavaScript and 10 Lua files;
- required mirrored-file byte equality;
- JOB-04 protected-Lua hash checks;
- receipt JavaScript/CSS behavior-equivalence checks after version normalization;
- Tow state-contract assertions;
- no stale active v0.4.9.4 cache tokens;
- no `Captain David` label regression;
- no generated custom Tow Vue call remaining;
- PC, nested-phone, compiled-phone and WEUI message relay harness;
- zero overlapping file paths between JOB-04 and JOB-09.

Result: **154/154 static assertions PASS** and `TOW_RELAY_HARNESS_PASS`.

## Runtime gate

Install only the new JOB-09 v0.4.9.5 and JOB-04 v0.3.2.4.8 pair, keep current JOB-13, disable older JOB-09/JOB-04 ZIPs, clear WebUI cache and restart.

Acceptance requires:

1. Note yards, fleet and yard-vehicle counts in Tow WEUI.
2. Open FoxNet Tow on PC and confirm connected with the same records/counts.
3. Open FoxNet Tow on phone and confirm connected with the same records/counts.
4. Make one safe yard/fleet change and confirm the pages update without duplicate records.
5. Confirm Wrecking Yard badge v0.3.2.4.8, compact receipt expansion and all six receipt sort choices.
6. Confirm Auctions still open.
7. Restart and confirm no Tow or Wrecking records disappear or duplicate.

No Wrecking sale is required for this bridge test. Do not classify as a BeamNG runtime pass until David reports the result.

## Records

JOB-09 manifest SHA-256: `100f9afe60453deebe7133d785455d866d78e7030f05886f5b9411365cec165d`  
JOB-09 records-only backup SHA-256: `1cb76a381a150c4967e31ef14401794e0ebfeebabbc31493c6ceb2ab3e680e2f`

JOB-04 manifest SHA-256: `df51df449ad6b24c99c3d0e1474daa146dcdf6f051db3a37090054f38fc389c3`  
JOB-04 records-only backup SHA-256: `418a75f46db4aff5079634c31252d7a1779add50826bd40f501a0853838e7459`

The records-only backups are evidence/rollback material and must not be installed.
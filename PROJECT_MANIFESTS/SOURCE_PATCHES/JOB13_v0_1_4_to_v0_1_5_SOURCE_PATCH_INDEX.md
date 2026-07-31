# JOB-13 v0.1.4 → v0.1.5 Source Patch Index

**Patch file:** `JOB13_v0_1_4_to_v0_1_5_SOURCE_PATCH.diff`  
**Size:** 22,997 bytes  
**SHA-256:** `3067a368d8d36c5208a1d441c418f961d2c20151c0f33a54fe84e0b63a6f36ae`

## Scope

- moves the JOB-13 UI to the versioned `redfoxJob13Auctions_v015` path;
- adds JOB-13-only FoxNet Auctions route compatibility shims;
- changes persistence to `settings_v015.json` and `state_v015.json`;
- preserves the approved cached pool and summary/detail split;
- adds RLS-derived timed NPC bidding behavior;
- removes every native purchase/negotiation path from the JOB-13 auction flow;
- preserves dirty-state persistence and TEST/LIVE safety boundaries.

The complete patch is retained with the owner-delivered build artifacts. The exact resulting runtime tree is recorded in:

`PROJECT_MANIFESTS/FILE_MANIFESTS/JOB-13_v0_1_5_FILE_MANIFEST_SHA256.csv`

Build record:

`PROJECT_MANIFESTS/BUILD_AUDITS/JOB-13_v0_1_5_PHONE_ROUTE_RLS_BIDDING_PATCH_2026-07-31.md`

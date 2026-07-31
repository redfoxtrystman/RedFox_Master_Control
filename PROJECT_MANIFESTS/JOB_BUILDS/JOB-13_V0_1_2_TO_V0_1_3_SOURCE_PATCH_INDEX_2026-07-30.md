# JOB-13 v0.1.2 → v0.1.3 Source Patch Index

**Date/time:** 2026-07-30 20:38 PDT  
**Job:** JOB-13 — FoxNet Online Vehicle Auctions  
**Owner:** David / Captain

The exact external unified source patch generated during the build is:

```text
JOB13_v0_1_2_to_v0_1_3_SOURCE_PATCH.diff
SHA-256: c17d635f309885b39347fab780fb0fef4d3ce6c94597c3729a1e3f402238c648
```

Patch base:

```text
RedFox_JOB13_FoxNet_Online_Auctions_v0_1_2_STANDALONE.zip
SHA-256: 1093bda6d840d3d102cf9dc71557744d7c7fa216967a2399021f9d599362b071
```

Patch output:

```text
RedFox_JOB13_FoxNet_Online_Auctions_v0_1_3_SLIM_PATCH.zip
SHA-256: 660f6fb5eae9f54cae4173590ac08d1de7655ca3ccfc7e14b8fa7f72ed2dee1e
```

Changed runtime code paths:

```text
lua/ge/extensions/redfoxJob13Auction.lua
scripts/redfox_job13_online_auctions/modScript.lua
ui/modules/apps/redfoxJob13Auctions_v012/app.html
ui/modules/apps/redfoxJob13Auctions_v012/app.js
ui/modules/apps/redfoxJob13Auctions_v012/app.json
ui/modules/apps/redfoxJob13Auctions_v012/site/app.js
mod_info/RedFoxJOB13/info.json
```

Added runtime path:

```text
mod_info/RedFoxJOB13/RUNTIME_NOTE.txt
```

Removed runtime-only development material is listed in the v0.1.3 build record.

The runtime file manifest committed beside this index contains the exact size and SHA-256 of every file in the output ZIP. The binary ZIP and unified patch are preserved in the active chat artifacts; the repository records their exact identities without absorbing another job's code or shared UI files.

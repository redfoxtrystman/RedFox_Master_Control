# JOB-05 uploaded baseline manifest — 2026-07-14

## Exact uploaded inputs

| Input | Bytes | SHA-256 | ZIP integrity | Repository-binary decision |
|---|---:|---|---|---|
| `beamBook.zip` | 9,867 | `2b8ac94018b9ca2c0c04bba597ad4316e177c9a4fd666b408392ad6d5becccc9` | PASS | Third-party archive; hash/inventory preserved, public redistribution awaiting permission |
| `FoxFax_DROP_IN_FULL_PAGE_v1_1_DARK_LIGHT.zip` | 7,474,088 | `19e2bc379971e0583f70d5ceff85926b425cd12f1ded914b375f1e76126d334b` | PASS | User-provided layout reference; binary not duplicated in first evidence commit |
| `zzzz_RedFox_FoxNet_Web_Ecosystem_v0_10_3_7_ALL_IN_ONE_PC_PHONE_GARAGE_SELL_FIX(1).zip` | 24,510,848 | `4dac614a4b14d423c069dccc8bdb5e0e511ee208f7414d3e6ed50a86a7903597` | PASS | Current IceFox behavioral reference; binary not duplicated in first evidence commit |

## Third-party BeamBook archive inventory

```text
lua/ge/extensions/beamBookLoader.lua                              328 bytes
lua/ge/extensions/career/modules/beamBook.lua                  13,725 bytes
mod.json                                                          366 bytes
mod_info/MDVSXTFCU/icon.jpg                                     2,195 bytes
mod_info/MDVSXTFCU/info.json                                    2,546 bytes
scripts/beamBook/modScript.lua                                    146 bytes
```

## Important technical findings

- `scripts/beamBook/modScript.lua` auto-loads `beamBookLoader` at game start.
- `beamBookLoader.lua` auto-loads `career_modules_beamBook`.
- `career/modules/beamBook.lua` generates eligible private-seller vehicle listings and uses current-map parking spots.
- It persists listings to the career save and delegates travel/inspection/purchase into the game's private-seller flow.
- It patches vehicle-shopping and inspection functions globally during extension/career activation.
- It includes a West Coast-specific preview image path.

JOB-05 may adapt the proven current-map listing and inspect-before-buy order of operations, but it must not copy the startup loader or apply a shopping patch at startup. The standalone test must lazy-load only when BeamBook is opened.

## Current IceFox ecosystem findings

The current ecosystem contains a placeholder BeamBook page at:

```text
sites/beambook/
ui/modModules/redfoxCareerWeb/sites/beambook/
```

The current IceFox route points to `sites/beambook/index.html`. That placeholder has in-memory mock interactions and no proven transaction bridge. It is not the visual target and is not copied into the isolated add-on.

Protected/shared ecosystem paths include:

```text
ui/ui-vue/dist/index.js
ui/modModules/redfoxCareerWeb/
assets/js/icefox_front.js
lua/ge/extensions/redfoxCareerWeb.lua
lua/ge/extensions/ui/phone/
```

No JOB-05 ZIP may contain those paths.

## GitHub size guidance

GitHub's official documentation says:

- files above 50 MiB produce a warning;
- regular Git repositories block files above 100 MiB;
- browser uploads are limited to 25 MiB per file;
- repositories should ideally remain below 1 GB.

Reference: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github

All current JOB-05 inputs are individually below the hard 100 MiB limit. The current IceFox ecosystem is just below the browser's 25 MiB per-file limit. Binary duplication is still being minimized because every clone would carry those archives.

## Distribution note

`beamBook.zip` was identified by David as another person's mod. This manifest makes the exact inspected artifact identifiable to all chats without publicly redistributing it before permission is confirmed. If David confirms redistribution rights, JOB-05 can add the original archive to a dedicated third-party reference folder or a release asset.

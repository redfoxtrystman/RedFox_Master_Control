# RedFox Release ZIP Cleanup Law

Date: 2026-08-04
Owner: David / RedFox
Applies to: every RedFox worker chat that prepares a ZIP for public release, Patreon release, test release, handoff release, or wider user sharing.

## Purpose

Release ZIPs must be clean, inspectable, and safe to hand to another user. A release package must not contain old diff reports, stale debug notes, accidental duplicate source trees, unrelated helper scripts, hidden working directories, or misleading verification language.

Static verification is not BeamNG runtime proof. If David has not tested the exact ZIP in BeamNG, the status must say `NEEDS TEST`, `BUILT — RUNTIME UNTESTED`, or equivalent non-overclaim language.

## Mandatory release order

Every release-producing chat must perform this order before delivering the ZIP:

1. Identify the exact input ZIP/source baseline by filename, byte size, and SHA-256.
2. Unzip the input to a clean temporary folder.
3. Pre-scan every file in the input package.
4. Create a file inventory with path, byte size, SHA-256, decision `KEEP` or `REMOVE`, and reason.
5. Remove development-only artifacts unless David explicitly wants them included.
6. Preserve every runtime/source/config/UI file needed by the mod.
7. Add or verify `mod_info/info.json` when this is a public-style BeamNG mod package.
8. Add or verify `mod_info/icon.png` so BeamNG/mod managers have an icon to display.
9. Add or verify `mod_info/images/` when David wants preview images; include placeholders only unless David provides the images.
10. Replace stale/outdated README text with a release-clean README.
11. Re-scan the cleaned release tree before zipping.
12. Validate every JSON file.
13. Syntax-check JavaScript files when Node is available.
14. Lua syntax-check with Lua/luac when available; if unavailable, say so and perform text/static checks instead.
15. Search active runtime/UI files for known spam/polling hazards, including `setInterval`, `requestAnimationFrame`, `setTimeout(fetchStats)`, old repeated warning strings, accidental debug reports, and known bad loops.
16. Build the ZIP with BeamNG paths at the archive root, not inside an accidental enclosing folder.
17. Reopen the final ZIP.
18. Run `unzip -t` or equivalent archive integrity check.
19. Extract the final ZIP to a second clean folder and compare the final file list against the expected release file list.
20. Re-run JSON/JS/static anti-spam checks against the final extracted ZIP contents.
21. Record the final ZIP byte size and SHA-256.
22. Update GitHub status/handoff files and leave either a message-board entry or an exact block for Coordinator posting.
23. Deliver the ZIP and clearly state what is static-verified versus what still needs David runtime testing.

## Files normally removed from public release ZIPs

Remove these unless David explicitly says to include them:

```text
REDFOX_DIFF_REPORT_*.html
REDFOX_DIFF_SUMMARY_*.txt
REDFOX_DIFF_*.txt
old failed build reports
assistant scratch files
temporary unzip folders
prototype-only scripts
obsolete README files that contradict the current release
raw screenshots unless they belong in mod_info/images and are intentionally included
hidden OS files such as .DS_Store or Thumbs.db
```

## Files normally kept when required by the mod

Keep all runtime files that the mod needs, including but not limited to:

```text
lua/ge/extensions/**/*.lua
lua/vehicle/extensions/**/*.lua
lua/ge/extensions/core/input/actions/*.json
ui/modules/apps/**/app.js
ui/modules/apps/**/app.json
settings/**/*.json
scripts/**/modScript.lua
mod_info/info.json
mod_info/icon.png
mod_info/images/* placeholders or approved preview images
release README / audit files intentionally placed in mod_info or root
```

Do not remove a file just because it looks unfamiliar. Inspect what loads it and whether BeamNG or another preserved file references it.

## Required release audit record

Every cleaned release ZIP should include a release audit record, preferably:

```text
mod_info/RELEASE_CONTENTS_AUDIT.md
mod_info/FINAL_ZIP_VERIFICATION.txt
```

The audit should record:

```text
source baseline
output ZIP filename
status language
pre-clean inventory
keep/remove decisions
removed artifact list
final file list
JSON validation result
JavaScript syntax result
Lua syntax/static result
archive integrity result
anti-spam/static search result
final runtime-unproven warning
```

## Anti-spam release rule

No release ZIP may be handed off as clean if active runtime/UI files still contain unreviewed polling or repeated warning paths. At minimum, scan active source for:

```text
setInterval
requestAnimationFrame
setTimeout(fetchStats)
queueGameEngineLua inside uncontrolled per-frame loops
queueLuaCommand inside uncontrolled per-frame loops
repeated log/print warnings in updateGFX/onUpdate
old known spam strings from previous bug reports
```

If a loop is intentionally required, the release audit must explain why it is safe, what gates it, and what David still needs to test.

## Status language

Allowed release-clean status examples:

```text
NEEDS TEST — static verification only
BUILT — RUNTIME UNTESTED
DAVID-TESTED WORKING
PARTIAL
BLOCKED
FAILED — STOPPED
```

Do not use `final`, `fixed`, `safe`, `working`, `complete`, `proven`, or `ready` unless David tested that exact ZIP and said it works.

## GitHub requirement

For every release-clean package, update the relevant module status row and add either:

1. a message board entry in `RedFox_Chat_Message_Board.md`, or
2. an exact message-board block in the chat response for Coordinator posting.

No silent release packaging.

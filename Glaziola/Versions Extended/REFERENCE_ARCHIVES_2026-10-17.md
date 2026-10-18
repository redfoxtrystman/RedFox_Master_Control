# Versions Extended — reference archive inventory (2026-10-17)

**Source of this inventory:** three ZIP files provided by the user in the October 17, 2026 ChatGPT conversation, tested in-session.

| Original archive | Size (bytes) | ZIP entries | SHA-256 | Purpose |
|---|---:|---:|---|---|
| `Versions-Extended-1.12.2.zip` | 299731277 | 18001 | `103bba258700822395099a2246571ae77952188d7a7426794e07349c429a85a4` | Active VE 1.12.2 source, build configuration, resources, canonical changelog; archive also includes transient build/Gradle caches |
| `26.2.jar_Decompiler.com.zip` | 24371048 | 26556 | `1a8a91b6e66c4cec2cb1df7c1fe8f97fb1e306e3591021dcd7c0b7fd46cd83f5` | User-supplied decompiled 26.2 Minecraft Java, vanilla data and some bundled assets; authoritative reference for modern mechanics |
| `minecraft-assets-26.2.zip` | 430702940 | 27005 | `c629d0e2c2d1497aabe7f0ea44216d31b2db7f51fc30550bb645e28879ec48c5` | User-supplied 26.2 assets, resources, sound, models, textures and data; authoritative asset reference |

## Verification result

- All 3 input paths were readable.
- Python `zipfile.testzip()` reported **no damaged ZIP entries** in any of the three archives.
- SHA-256 was computed directly from the provided raw archive bytes.
- This is an archive-integrity inspection, **not** source-code compilation, static analysis, or gameplay validation.

## Repository storage state (important)

**All three archives are indexed here, but none of their raw ZIP bytes has been uploaded to GitHub.** The connected repository, `redfoxtrystman/RedFox_Master_Control`, is **public**. Directly committing Mojang's decompiled sources and copyrighted vanilla asset dump is inappropriate. The original project ZIP is also **299.7 MB** and the asset ZIP is **430.7 MB**; the original single files exceed GitHub's standard 100 MB per-file Git limit. The connector's text-file actions do not transfer these local binary archives.

The active VE project can eventually be uploaded independently as a **cleaned source tree** without `.gradle/`, `build/`, generated artifacts, and without republishing Mojang's complete proprietary source/asset archives. Review inclusion of bundled resources/licensing before public publication.

## Recovery and continuity

- For a future ChatGPT development session, provide access to the exact archives matching the SHA-256 values above (or to a newer, explicitly superseding VE source snapshot).
- Start with `src/versions_extended_changelog_handoff.txt` from the active project ZIP, then inspect `src/main/java/com/versionsextended/v1_14/`, datapack modules, build files and related resources.
- Follow [README.md](README.md) for project rules and the **1.14-completion-before-1.15 gate**.
- Do **not** represent this checksum inventory as storage of the actual three archives.

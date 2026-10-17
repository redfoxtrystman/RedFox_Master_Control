# Alpha 46.4 — ore harvesting and timed floor fix
Target: Minecraft 1.21.1, NeoForge 21.1.259, Cobblemon 1.8.1.

## Ores
All 9 Ruby, Sapphire and Crystal ordinary/deepslate ores and storage blocks now have the Minecraft pickaxe mining tag and iron-tier requirements. Their nine loot tables were **already present** in the Alpha 46.3.2 JAR. The missing mining tag prevented correct harvesting. All six ore tables support Silk Touch (ore block) and Fortune (gem yield); storage blocks drop themselves. No Cobblemon items or recipes were changed. No natural ore worldgen is claimed.

## Timed Fall
Alpha 46.3.2 incorrectly used `UltraFallingBlock` (a sand-like falling block) for `timed_fall`.
Pixelmon 9.4.1's actual `com.pixelmonmod.pixelmon.blocks.TimedFallBlock` implements player-specific fall-through via an incrementing/decrementing collision counter initialized to 300 collision checks. Our replacement `TimedFallBlock` uses an explicit **300 player ticks** of sustained contact (~15 seconds at 20 TPS), each player/block has an independent counter, resets after 4 ticks away, and leaves other entities supported and the block present. The registration in `ExtraPixelmonBlocks` now constructs the dedicated class.

## Verification
The delivered Alpha 46.4 JAR is a surgical Java 21 compiled-class injection, constructor method-handle modification and data repack; **not** a clean ModDevGradle build. The standalone Java collision harness passed threshold, reset, separate player, position and client/server tests. JAR 4,124 entries, 35 class files, 3,401 valid JSON files, 9 correct tool/loot IDs and all internal references resolve. Runtime Minecraft client verification remains outstanding.

The original project source includes Pixelmon-derived third-party artwork; the full ZIP and runtime JAR were delivered privately in the ChatGPT conversation, not copied into public GitHub.

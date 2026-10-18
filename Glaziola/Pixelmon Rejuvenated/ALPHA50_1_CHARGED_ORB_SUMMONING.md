# Alpha 50.1 — Right-click fully charged orbs to summon legendary birds

Temporary alternative to the shrines requested for a future update.

| Orb item | Cobblemon species |
|---|---|
| `pixelmonrejuvenated:uno_orb` | Articuno |
| `pixelmonrejuvenated:dos_orb` | Zapdos |
| `pixelmonrejuvenated:tres_orb` | Moltres |

Orbs must have **250 battle defeats** recorded on their own item stack. A right-click on a block spawns a wild, catchable bird in the neighboring empty-side cell; right-clicking in air raycasts up to 32 blocks, then falls back to 12 blocks down the player's look direction when no block is hit. Each valid orb use runs a trusted, **server-side** Cobblemon `spawnpokemonat x y z species` command with elevated permission. Nonoperators may use their charged items without having command privileges. Only the three fixed species strings can be invoked through the item.

**Successful spawn:** consume one orb, apply a 20-tick use cooldown, display feedback. **Failed spawn:** return the orb intact and show error feedback; partially charged orbs display progress and do nothing. No altar or shrine added. The grey Orb is unchanged.

This release modifies `BirdOrbItem.java` and version metadata only. The runtime JAR is an incremental **Java 21 signature-stub compilation/repack**, not a verified Gradle build. Standalone mocked tests passed for all 3 species, block targeting, air targeting, completion threshold, unsuccessful commands, and client-side nonconsumption. Archive ZIP CRC passed with **4,172 entries, 44 mod classes, and 3,435 parseable JSONs**. **Minecraft startup and real spawn behavior not tested**. Previous releases have shown that API signature stubs can still cause runtime errors.

The proprietary Pixelmon-derived assets in the user's full source ZIP and JAR are not committed to the public repository. The generated runtime and source ZIP are available privately in the ChatGPT conversation.

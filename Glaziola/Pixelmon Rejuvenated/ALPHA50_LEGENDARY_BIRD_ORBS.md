# Pixelmon Rejuvenated Alpha 50 — Legendary Bird Soul Orbs
Target Minecraft 1.21.1, NeoForge 21.1.259, Cobblemon 1.8.1.

**Added:** `orb` (grey), `uno_orb` (Frozen/Articuno), `dos_orb` (Static/Zapdos), and `tres_orb` (Fiery/Moltres), all in `pixelmonrejuvenated` namespace and Pixelmon Items creative tab.

**Recipes:** 3 shaped-free recipes exactly matching Pixelmon ingredients with Cobblemon's existing Ice Stone, Thunder Stone and Fire Stone. Plain Orb remains noncraftable, as in Pixelmon.

**Obtaining:** When a player defeats a wild Pokémon **in a Cobblemon battle**, they have a 10% chance to receive a base Orb from Dragonair, 30% from Dragonite, and 100% from Dialga, Palkia or Giratina. If inventory is full, the Orb drops nearby. This uses the battle faint event, not entity killing.

**Charging:** Colored orbs each keep an individual, persistent counter in the vanilla `DataComponents.CUSTOM_DATA` item component (key `pixelmonrejuvenated.bird_orb_defeats`) incremented by 1 for every enemy Pokémon defeated in a genuine Cobblemon battle. Counts up to **250**, not Pixelmon's current 375, per the user's request. All items carried in the player's inventory (including offhand) advance independently. Tooltip and progress bar show the charge. Allied fainting, mobs punched outside battle, and inventory contents belonging to absent players do not qualify.

**Intentionally not yet added:** Shrines, altars, and Articuno/Zapdos/Moltres summoning.

**Assets:** The four icons are Pixelmon 9.4.1 textures, copied only into the private Alpha 50 JAR and source ZIP supplied in the conversation from the user-provided Pixelmon JAR. Public GitHub contains the models and code but no proprietary texture bytes. See `docs/alpha50_orb_lang_additions.json` for translation entries merged into the private JAR's full en_us.json.

**Build limitation:** Alpha 50 is a Java 21 compiled-class integration/repack of Alpha 49. The newly compiled Java files relied on API **signature stubs** because full NeoForge/Minecraft/Cobblemon compile dependencies were unavailable here. It is **not a clean Gradle build** or an in-game runtime-tested release. Static validation includes 44 mod classes, 3,435 parseable JSON files, registration bytecode, and ZIP CRC. Prior releases built from stubs have experienced binary incompatibilities. In-game startup and charging must be verified.

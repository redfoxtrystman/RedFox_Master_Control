# Pixelmon Rejuvenated Alpha 49: Candy Eevee

The supplied user-designed `candy_vee.png` is added **unaltered** at `assets/pixelmonrejuvenated/textures/pokemon/0133_eevee/candy_eevee.png` (128×64 PNG).

- **Eevee only**: new `Candy` form/aspect `candy`, typing **Normal / Fairy**.
- `species_features/candy.json`: assignable Cobblemon flag/aspect.
- `species_feature_assignments/candy.json`: currently only `eevee`.
- `species_additions/candy_eevee.json`: adds Candy form and keeps the eight existing Eevee evolution requirements; those result species will be **ordinary** Eeveelutions until Candy equivalents are designed.
- `bedrock/pokemon/resolvers/0133_eevee/3_candy_eevee.json`: texture variation for aspect `candy` without an emissive layer (unlike Spirit Eevee).
- `SpecialPaletteKeys.java`: includes `candy` in the special-aspect set so shiny doesn't override it.
- `/spawnpokemon eevee candy` to test. No invented natural spawn rules, evolution types, or assets for the other Eeveelutions.
- Local JAR additionally contains `pixelmonrejuvenated.pokemon.form.candy` and `cobblemon.ui.pokedex.form.candy` English keys, preserving the existing complete language file.

**Build status**: the Alpha 49 runtime JAR was assembled from Alpha 48.4 by adding the new data/assets and recompiling standalone Java 21 `SpecialPaletteKeys`. All 3,428 JAR JSON files parse, 41 classes are present, all archive CRC checks pass. **Not a full NeoForge Gradle compilation, nor Minecraft runtime-tested.**

**Resource distribution**: The uploaded Candy Eevee texture is provided by the user and committed here. Existing third-party Pixelmon-derived assets remain only in the private source ZIP and JAR delivered in the ChatGPT conversation.

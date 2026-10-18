# Alpha 52 — Pixelmon-style Legendary Spawning

For Minecraft 1.21.1, NeoForge and Cobblemon 1.8.1. Pixelmon 9.4.1 legendary spawn tables were the reference; Pixelmon's proprietary mod JAR and the user's separate CCC add-on were not copied to this public repository.

## Functionality
- **69 legendary/mythical species, 70 ordinary spawn rules**, with eight unavailable special palette variants left out.
- Uses a **separate server-wide legendary spawn timer**, default interval 25,000 ticks (randomized by a 60–140% factor) with a 30% spawn chance if an eligible place was found. Player count multiplier is 0.01.
- Chooses an online player and samples up to **96 loaded terrain positions 24–96 blocks away**, restricting to compatible biome tags, times, weather, moon, heights and actual vanilla structure pieces. No forced chunk generation.
- Random weighted species selection among eligible spots, species level from the Pixelmon table, and server-side `/spawnpokemonat x y z species level=N` to create a **wild, catchable** Pokémon. Nearby players in the same dimension within 256 blocks receive a **gold notification** after a successful spawn.
- The three legendary birds remain obtainable through the previously added **250-battle-KO orbs**; this does not inject them into the ordinary spawn table. Existing orb recipes, charge progress, and right-click summoning are preserved.
- **Regigigas** is included as Level 70, Underground / Ancient City, during afternoon or dusk. The absence of its model from the user-provided compatibility pack is expected because **Cobblemon has its own Regigigas model**.

## Assets and model compatibility

The uploaded Complete Cobblemon Collection Myths and Legends compat 2.21 JAR has additional resolvers for **58/69** spawn-table species. The other 11—Latias, Latios, Mew, Rayquaza, Regice, Regidrago, Regieleki, Regigigas, Regirock, Registeel, and Zarude—were found with model/resolver/species data in the official **Cobblemon upstream repository**. A resolver absent from the optional compatibility pack should **not** be treated as proof of an unsupported Pokémon. Always check the installed exact Cobblemon version, resource packs and addons in-game. Keep the compatibility pack separately installed; it is not included in the mod.

## Configuration
A config file `config/pixelmonrejuvenated-legendary-spawns.json` is created at first server startup:
```json
{
  "enabled": true,
  "averageIntervalTicks": 25000,
  "spawnChance": 0.3,
  "playerMultiplier": 0.01,
  "searchAttempts": 96,
  "minDistance": 24,
  "maxDistance": 96,
  "announcementRadius": 256,
  "globalAnnouncements": false
}
```
Restart the game/server after editing it. Spawn checks only use already loaded chunks. For test-world verification, setting `averageIntervalTicks` to `1200` and `spawnChance` to `1.0` reduces waiting but does not bypass biome, structure or time restrictions.

## Build and testing limitations

**This is an Alpha 52 test build, not a verified full NeoForge/Gradle build.** The distributed JAR was assembled by Java 21 compilation against partial API signature stubs and repackaged from Alpha 50.1. Static JSON checks (including 27 biome tags and 70 rules), bytecode checks and ZIP CRC pass, but Minecraft startup, spawn behavior and Cobblemon binary compatibility are **not yet tested**. Prior stub-built releases have shown runtime linkage errors. Back up the world and provide a crash log if one occurs.

Compared with Pixelmon's engine this approximates its location evaluator; dynamic party-leader conditions, special palettes, held items on spawn, and flawless IV guarantees were not ported. Structure-only spawns require a candidate inside an actual vanilla structure piece. Some eligible searches can fail simply because there is no loaded appropriate terrain.

# Pixelmon Rejuvenated Alpha 48 — Natural Berry Trees and Branches

- Adds a registered NeoForge `wild_berry_tree` feature, configured/placed data, and Overworld vegetal-decoration biome modifier.
- At eligible generation positions, selects uniformly from **all 78 registered berry leaves** (not just common berries); approximately one placement attempt per 12 chunks, with terrain clearance and dirt/grass requirements.
- Newly generated trees and player-grown sprouts use the same `BerryTrees.place` routine.
- Crown logs explicitly set WallBlock north, east, south and west branch states to `LOW` **after** the canopy is placed, enabling existing branch-arm models.
- Leaves are nonpersistent and use ordinary berry harvesting/ripening. Ripening speed is unchanged; setting `randomTickSpeed` to 10 versus default 3 increases random-tick opportunities ~3.3×.
- Changes affect only **new chunks**. No modifications to Cobblemon's native apricorn recipes or tree content.
- The private Alpha 48 JAR and source ZIP were delivered separately. Full Gradle and in-game start/worldgen verification remain outstanding. Avoid distributing the private bundle of Pixelmon-derived artwork without appropriate rights.

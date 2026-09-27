from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "PKVault.Core/contract/ContractService.cs"
text = path.read_text(encoding="utf-8")

replacements = {
'''            D("easy-catch-3", ContractTier.Easy, "Quick Catch", "Catch 3 Pokémon after accepting this contract.", 2_500, ContractMetric.CatchCount, 3, [], R("poke-ball", 10)),''':
'''            D("easy-catch-3", ContractTier.Easy, "Quick Catch", "Catch 3 Pokémon after accepting this contract.", 2_500, ContractMetric.CatchCount, 3, [], R("poke-ball", 8), R("potion", 3), R("antidote", 2)),''',

'''            D("easy-catch-5", ContractTier.Easy, "Five Fresh Catches", "Catch 5 Pokémon after accepting this contract.", 4_000, ContractMetric.CatchCount, 5, [], R("great-ball", 6)),''':
'''            D("easy-catch-5", ContractTier.Easy, "Five Fresh Catches", "Catch 5 Pokémon after accepting this contract.", 4_000, ContractMetric.CatchCount, 5, [], R("great-ball", 5), R("potion", 3), R("repel", 2)),''',

'''            D("easy-species-3", ContractTier.Easy, "Three Different Species", "Catch 3 different species after accepting this contract.", 3_500, ContractMetric.DifferentSpeciesCaught, 3, [], R("great-ball", 8)),''':
'''            D("easy-species-3", ContractTier.Easy, "Three Different Species", "Catch 3 different species after accepting this contract.", 3_500, ContractMetric.DifferentSpeciesCaught, 3, [], R("great-ball", 6), R("super-potion", 2), R("full-heal", 1)),''',

'''            D("easy-level-10", ContractTier.Easy, "Training Shift", "Gain 10 total levels across your Pokémon after accepting this contract.", 3_000, ContractMetric.LevelGain, 10, [], R("super-potion", 8)),''':
'''            D("easy-level-10", ContractTier.Easy, "Training Shift", "Gain 10 total levels across your Pokémon after accepting this contract.", 3_000, ContractMetric.LevelGain, 10, [], R("super-potion", 4), R("full-heal", 2), R("x-attack", 2)),''',

'''            D("easy-evolve-1", ContractTier.Easy, "One Evolution", "Evolve 1 Pokémon after accepting this contract.", 5_000, ContractMetric.EvolutionCount, 1, [], R("rare-candy", 2)),''':
'''            D("easy-evolve-1", ContractTier.Easy, "One Evolution", "Evolve 1 Pokémon after accepting this contract.", 5_000, ContractMetric.EvolutionCount, 1, [], R("rare-candy", 1), R("fire-stone", 1), R("water-stone", 1)),''',

'''            D("easy-catch-8", ContractTier.Easy, "Busy Ball", "Catch 8 Pokémon after accepting this contract.", 6_000, ContractMetric.CatchCount, 8, [], R("great-ball", 12)),''':
'''            D("easy-catch-8", ContractTier.Easy, "Busy Ball", "Catch 8 Pokémon after accepting this contract.", 6_000, ContractMetric.CatchCount, 8, [], R("great-ball", 8), R("potion", 4), R("repel", 3)),''',

'''            D("easy-level-20", ContractTier.Easy, "Training Block", "Gain 20 total levels across your Pokémon after accepting this contract.", 6_500, ContractMetric.LevelGain, 20, [], R("rare-candy", 3)),''':
'''            D("easy-level-20", ContractTier.Easy, "Training Block", "Gain 20 total levels across your Pokémon after accepting this contract.", 6_500, ContractMetric.LevelGain, 20, [], R("rare-candy", 2), R("super-potion", 4), R("x-speed", 2)),''',

'''            D("easy-species-5", ContractTier.Easy, "Five Different Species", "Catch 5 different species after accepting this contract.", 7_000, ContractMetric.DifferentSpeciesCaught, 5, [], R("ultra-ball", 5)),''':
'''            D("easy-species-5", ContractTier.Easy, "Five Different Species", "Catch 5 different species after accepting this contract.", 7_000, ContractMetric.DifferentSpeciesCaught, 5, [], R("ultra-ball", 3), R("great-ball", 5), R("super-potion", 3)),''',

'''            D("normal-catch-15", ContractTier.Normal, "Field Sweep", "Catch 15 Pokémon after accepting this contract.", 12_000, ContractMetric.CatchCount, 15, [], R("ultra-ball", 15)),''':
'''            D("normal-catch-15", ContractTier.Normal, "Field Sweep", "Catch 15 Pokémon after accepting this contract.", 12_000, ContractMetric.CatchCount, 15, [], R("ultra-ball", 8), R("hyper-potion", 3), R("full-heal", 3), R("max-repel", 2)),''',

'''            D("normal-species-8", ContractTier.Normal, "Eight Species Run", "Catch 8 different species after accepting this contract.", 14_000, ContractMetric.DifferentSpeciesCaught, 8, [], R("rare-candy", 4)),''':
'''            D("normal-species-8", ContractTier.Normal, "Eight Species Run", "Catch 8 different species after accepting this contract.", 14_000, ContractMetric.DifferentSpeciesCaught, 8, [], R("rare-candy", 2), R("ultra-ball", 5), R("hyper-potion", 3), R("full-heal", 2)),''',

'''            D("normal-level-50", ContractTier.Normal, "Serious Training", "Gain 50 total levels across your Pokémon after accepting this contract.", 15_000, ContractMetric.LevelGain, 50, [], R("rare-candy", 5)),''':
'''            D("normal-level-50", ContractTier.Normal, "Serious Training", "Gain 50 total levels across your Pokémon after accepting this contract.", 15_000, ContractMetric.LevelGain, 50, [], R("rare-candy", 3), R("pp-up", 1), R("hyper-potion", 4), R("x-attack", 3)),''',

'''            D("normal-evolve-3", ContractTier.Normal, "Evolution Chain", "Evolve 3 Pokémon after accepting this contract.", 18_000, ContractMetric.EvolutionCount, 3, [], R("rare-candy", 6)),''':
'''            D("normal-evolve-3", ContractTier.Normal, "Evolution Chain", "Evolve 3 Pokémon after accepting this contract.", 18_000, ContractMetric.EvolutionCount, 3, [], R("rare-candy", 2), R("fire-stone", 1), R("water-stone", 1), R("thunder-stone", 1), R("leaf-stone", 1)),''',

'''            D("normal-catch-25", ContractTier.Normal, "Twenty-Five Catches", "Catch 25 Pokémon after accepting this contract.", 20_000, ContractMetric.CatchCount, 25, [], R("ultra-ball", 25)),''':
'''            D("normal-catch-25", ContractTier.Normal, "Twenty-Five Catches", "Catch 25 Pokémon after accepting this contract.", 20_000, ContractMetric.CatchCount, 25, [], R("ultra-ball", 12), R("hyper-potion", 4), R("max-repel", 4), R("revive", 2)),''',

'''            D("normal-species-12", ContractTier.Normal, "Twelve Species Run", "Catch 12 different species after accepting this contract.", 22_000, ContractMetric.DifferentSpeciesCaught, 12, [], R("max-revive", 5)),''':
'''            D("normal-species-12", ContractTier.Normal, "Twelve Species Run", "Catch 12 different species after accepting this contract.", 22_000, ContractMetric.DifferentSpeciesCaught, 12, [], R("max-revive", 2), R("ultra-ball", 8), R("full-heal", 4), R("pp-up", 1)),''',

'''            D("normal-level-75", ContractTier.Normal, "Training Marathon", "Gain 75 total levels across your Pokémon after accepting this contract.", 25_000, ContractMetric.LevelGain, 75, [], R("rare-candy", 8)),''':
'''            D("normal-level-75", ContractTier.Normal, "Training Marathon", "Gain 75 total levels across your Pokémon after accepting this contract.", 25_000, ContractMetric.LevelGain, 75, [], R("rare-candy", 4), R("pp-up", 1), R("protein", 1), R("iron", 1), R("hyper-potion", 4)),''',

'''            D("normal-evolve-5", ContractTier.Normal, "Evolution Workshop", "Evolve 5 Pokémon after accepting this contract.", 28_000, ContractMetric.EvolutionCount, 5, [], R("rare-candy", 10)),''':
'''            D("normal-evolve-5", ContractTier.Normal, "Evolution Workshop", "Evolve 5 Pokémon after accepting this contract.", 28_000, ContractMetric.EvolutionCount, 5, [], R("rare-candy", 3), R("moon-stone", 1), R("sun-stone", 1), R("dusk-stone", 1), R("dawn-stone", 1), R("shiny-stone", 1), R("revive", 3)),''',

'''            D("hard-catch-40", ContractTier.Hard, "Forty Catches", "Catch 40 Pokémon after accepting this contract.", 35_000, ContractMetric.CatchCount, 40, [], R("ultra-ball", 50), R("rare-candy", 5)),''':
'''            D("hard-catch-40", ContractTier.Hard, "Forty Catches", "Catch 40 Pokémon after accepting this contract.", 35_000, ContractMetric.CatchCount, 40, [], R("ultra-ball", 20), R("hyper-potion", 5), R("max-repel", 5), R("pp-up", 2), R("rare-candy", 2)),''',

'''            D("hard-species-20", ContractTier.Hard, "Twenty Species Hunt", "Catch 20 different species after accepting this contract.", 40_000, ContractMetric.DifferentSpeciesCaught, 20, [], R("rare-candy", 10)),''':
'''            D("hard-species-20", ContractTier.Hard, "Twenty Species Hunt", "Catch 20 different species after accepting this contract.", 40_000, ContractMetric.DifferentSpeciesCaught, 20, [], R("rare-candy", 4), R("ultra-ball", 15), R("full-restore", 3), R("pp-up", 2), R("max-repel", 5)),''',

'''            D("hard-level-150", ContractTier.Hard, "Elite Training", "Gain 150 total levels across your Pokémon after accepting this contract.", 45_000, ContractMetric.LevelGain, 150, [], R("rare-candy", 15)),''':
'''            D("hard-level-150", ContractTier.Hard, "Elite Training", "Gain 150 total levels across your Pokémon after accepting this contract.", 45_000, ContractMetric.LevelGain, 150, [], R("rare-candy", 6), R("pp-up", 3), R("protein", 2), R("iron", 2), R("calcium", 2), R("carbos", 2)),''',

'''            D("hard-evolve-10", ContractTier.Hard, "Ten Evolutions", "Evolve 10 Pokémon after accepting this contract.", 50_000, ContractMetric.EvolutionCount, 10, [], R("rare-candy", 15), R("max-revive", 5)),''':
'''            D("hard-evolve-10", ContractTier.Hard, "Ten Evolutions", "Evolve 10 Pokémon after accepting this contract.", 50_000, ContractMetric.EvolutionCount, 10, [], R("rare-candy", 5), R("fire-stone", 1), R("water-stone", 1), R("thunder-stone", 1), R("leaf-stone", 1), R("moon-stone", 1), R("sun-stone", 1), R("dusk-stone", 1), R("dawn-stone", 1), R("shiny-stone", 1), R("ice-stone", 1), R("max-revive", 3)),''',

'''            D("hard-shiny-1", ContractTier.Hard, "Shiny Hunt", "Catch 1 shiny Pokémon after accepting this contract.", 55_000, ContractMetric.ShinyCatchCount, 1, [], R("rare-candy", 20), R("max-revive", 10)),''':
'''            D("hard-shiny-1", ContractTier.Hard, "Shiny Hunt", "Catch 1 shiny Pokémon after accepting this contract.", 55_000, ContractMetric.ShinyCatchCount, 1, [], R("rare-candy", 5), R("luxury-ball", 10), R("pp-up", 2), R("max-revive", 3), R("shiny-stone", 1)),''',

'''            D("hard-catch-75", ContractTier.Hard, "Seventy-Five Catches", "Catch 75 Pokémon after accepting this contract.", 60_000, ContractMetric.CatchCount, 75, [], R("ultra-ball", 75)),''':
'''            D("hard-catch-75", ContractTier.Hard, "Seventy-Five Catches", "Catch 75 Pokémon after accepting this contract.", 60_000, ContractMetric.CatchCount, 75, [], R("ultra-ball", 30), R("full-restore", 5), R("max-repel", 10), R("pp-up", 2), R("max-revive", 2)),''',

'''            D("hard-species-30", ContractTier.Hard, "Thirty Species Hunt", "Catch 30 different species after accepting this contract.", 65_000, ContractMetric.DifferentSpeciesCaught, 30, [], R("rare-candy", 20)),''':
'''            D("hard-species-30", ContractTier.Hard, "Thirty Species Hunt", "Catch 30 different species after accepting this contract.", 65_000, ContractMetric.DifferentSpeciesCaught, 30, [], R("rare-candy", 5), R("ultra-ball", 20), R("full-restore", 5), R("pp-up", 2), R("max-repel", 5), R("fire-stone", 1), R("water-stone", 1)),''',

'''            D("hard-shiny-2", ContractTier.Hard, "Double Shiny Hunt", "Catch 2 shiny Pokémon after accepting this contract.", 75_000, ContractMetric.ShinyCatchCount, 2, [], R("master-ball", 1)),''':
'''            D("hard-shiny-2", ContractTier.Hard, "Double Shiny Hunt", "Catch 2 shiny Pokémon after accepting this contract.", 75_000, ContractMetric.ShinyCatchCount, 2, [], R("rare-candy", 8), R("luxury-ball", 15), R("pp-up", 3), R("max-revive", 5), R("full-restore", 5)),''',

'''            D("legendary-any", ContractTier.Legendary, "Legendary Acquisition", "Catch any 1 Legendary Pokémon after accepting this contract.", 80_000, ContractMetric.SpeciesSetCatchCount, 1, LegendaryPool, R("ultra-ball", 50), R("rare-candy", 10)),''':
'''            D("legendary-any", ContractTier.Legendary, "Legendary Acquisition", "Catch any 1 Legendary Pokémon after accepting this contract.", 80_000, ContractMetric.SpeciesSetCatchCount, 1, LegendaryPool, R("ultra-ball", 25), R("full-restore", 5), R("max-revive", 3), R("pp-up", 3), R("rare-candy", 4)),''',

'''            SpeciesBounty("legendary-lugia", ContractTier.Legendary, 249, 95_000, R("ultra-ball", 75), R("rare-candy", 15)),''':
'''            SpeciesBounty("legendary-lugia", ContractTier.Legendary, 249, 95_000, R("ultra-ball", 30), R("rare-candy", 5), R("full-restore", 4), R("pp-up", 3), R("max-revive", 3)),''',

'''            SpeciesBounty("legendary-ho-oh", ContractTier.Legendary, 250, 95_000, R("ultra-ball", 75), R("rare-candy", 15)),''':
'''            SpeciesBounty("legendary-ho-oh", ContractTier.Legendary, 250, 95_000, R("ultra-ball", 30), R("rare-candy", 5), R("full-restore", 4), R("pp-up", 3), R("max-revive", 3)),''',

'''            SpeciesBounty("legendary-rayquaza", ContractTier.Legendary, 384, 110_000, R("ultra-ball", 75), R("rare-candy", 20)),''':
'''            SpeciesBounty("legendary-rayquaza", ContractTier.Legendary, 384, 110_000, R("ultra-ball", 35), R("rare-candy", 6), R("full-restore", 5), R("pp-up", 3), R("max-revive", 4)),''',

'''            SpeciesBounty("legendary-dialga", ContractTier.Legendary, 483, 110_000, R("ultra-ball", 75), R("rare-candy", 20)),''':
'''            SpeciesBounty("legendary-dialga", ContractTier.Legendary, 483, 110_000, R("ultra-ball", 35), R("rare-candy", 6), R("full-restore", 5), R("pp-up", 3), R("max-revive", 4)),''',

'''            SpeciesBounty("legendary-palkia", ContractTier.Legendary, 484, 110_000, R("ultra-ball", 75), R("rare-candy", 20)),''':
'''            SpeciesBounty("legendary-palkia", ContractTier.Legendary, 484, 110_000, R("ultra-ball", 35), R("rare-candy", 6), R("full-restore", 5), R("pp-up", 3), R("max-revive", 4)),''',

'''            SpeciesBounty("legendary-giratina", ContractTier.Legendary, 487, 125_000, R("ultra-ball", 100), R("rare-candy", 20)),''':
'''            SpeciesBounty("legendary-giratina", ContractTier.Legendary, 487, 125_000, R("ultra-ball", 40), R("rare-candy", 7), R("full-restore", 5), R("pp-up", 4), R("max-revive", 5), R("dusk-stone", 1)),''',

'''            SpeciesBounty("legendary-reshiram", ContractTier.Legendary, 643, 125_000, R("ultra-ball", 100), R("rare-candy", 20)),''':
'''            SpeciesBounty("legendary-reshiram", ContractTier.Legendary, 643, 125_000, R("ultra-ball", 40), R("rare-candy", 7), R("full-restore", 5), R("pp-up", 4), R("max-revive", 5), R("fire-stone", 1)),''',

'''            SpeciesBounty("legendary-zekrom", ContractTier.Legendary, 644, 125_000, R("ultra-ball", 100), R("rare-candy", 20)),''':
'''            SpeciesBounty("legendary-zekrom", ContractTier.Legendary, 644, 125_000, R("ultra-ball", 40), R("rare-candy", 7), R("full-restore", 5), R("pp-up", 4), R("max-revive", 5), R("thunder-stone", 1)),''',

'''            SpeciesBounty("legendary-xerneas", ContractTier.Legendary, 716, 135_000, R("ultra-ball", 100), R("rare-candy", 25)),''':
'''            SpeciesBounty("legendary-xerneas", ContractTier.Legendary, 716, 135_000, R("ultra-ball", 40), R("rare-candy", 8), R("full-restore", 6), R("pp-up", 4), R("max-revive", 5), R("shiny-stone", 1)),''',

'''            SpeciesBounty("legendary-yveltal", ContractTier.Legendary, 717, 135_000, R("ultra-ball", 100), R("rare-candy", 25)),''':
'''            SpeciesBounty("legendary-yveltal", ContractTier.Legendary, 717, 135_000, R("ultra-ball", 40), R("rare-candy", 8), R("full-restore", 6), R("pp-up", 4), R("max-revive", 5), R("dusk-stone", 1)),''',

'''            D("mythical-two-legendaries", ContractTier.Mythical, "Double Legendary Contract", "Catch any 2 Legendary Pokémon after accepting this contract.", 200_000, ContractMetric.SpeciesSetCatchCount, 2, LegendaryPool, R("master-ball", 1), R("rare-candy", 20)),''':
'''            D("mythical-two-legendaries", ContractTier.Mythical, "Double Legendary Contract", "Catch any 2 Legendary Pokémon after accepting this contract.", 200_000, ContractMetric.SpeciesSetCatchCount, 2, LegendaryPool, R("master-ball", 1), R("rare-candy", 8), R("full-restore", 10), R("pp-up", 5), R("max-revive", 5)),''',

'''            D("mythical-any", ContractTier.Mythical, "Mythical Acquisition", "Catch any 1 Mythical Pokémon after accepting this contract.", 225_000, ContractMetric.SpeciesSetCatchCount, 1, MythicalPool, R("master-ball", 1), R("rare-candy", 25)),''':
'''            D("mythical-any", ContractTier.Mythical, "Mythical Acquisition", "Catch any 1 Mythical Pokémon after accepting this contract.", 225_000, ContractMetric.SpeciesSetCatchCount, 1, MythicalPool, R("master-ball", 1), R("rare-candy", 10), R("pp-up", 5), R("max-revive", 5), R("full-restore", 10)),''',

'''            SpeciesBounty("mythical-mewtwo", ContractTier.Mythical, 150, 300_000, R("master-ball", 1), R("rare-candy", 25), R("max-revive", 10)),''':
'''            SpeciesBounty("mythical-mewtwo", ContractTier.Mythical, 150, 300_000, R("master-ball", 1), R("rare-candy", 10), R("pp-up", 5), R("max-revive", 5), R("full-restore", 10)),''',

'''            SpeciesBounty("mythical-mew", ContractTier.Mythical, 151, 350_000, R("master-ball", 1), R("rare-candy", 30)),''':
'''            SpeciesBounty("mythical-mew", ContractTier.Mythical, 151, 350_000, R("master-ball", 1), R("rare-candy", 10), R("pp-up", 5), R("full-restore", 10), R("max-elixir", 3)),''',

'''            SpeciesBounty("mythical-celebi", ContractTier.Mythical, 251, 325_000, R("master-ball", 1), R("rare-candy", 30)),''':
'''            SpeciesBounty("mythical-celebi", ContractTier.Mythical, 251, 325_000, R("master-ball", 1), R("rare-candy", 10), R("pp-up", 5), R("full-restore", 8), R("leaf-stone", 2), R("sun-stone", 2)),''',

'''            SpeciesBounty("mythical-jirachi", ContractTier.Mythical, 385, 350_000, R("master-ball", 1), R("rare-candy", 35)),''':
'''            SpeciesBounty("mythical-jirachi", ContractTier.Mythical, 385, 350_000, R("master-ball", 1), R("rare-candy", 12), R("pp-up", 6), R("max-elixir", 4), R("shiny-stone", 2)),''',

'''            SpeciesBounty("mythical-darkrai", ContractTier.Mythical, 491, 375_000, R("master-ball", 1), R("rare-candy", 35)),''':
'''            SpeciesBounty("mythical-darkrai", ContractTier.Mythical, 491, 375_000, R("master-ball", 1), R("rare-candy", 12), R("pp-up", 6), R("full-restore", 10), R("dusk-stone", 2)),''',

'''            SpeciesBounty("mythical-arceus", ContractTier.Mythical, 493, 500_000, R("master-ball", 2), R("rare-candy", 50)),''':
'''            SpeciesBounty("mythical-arceus", ContractTier.Mythical, 493, 500_000, R("master-ball", 2), R("rare-candy", 15), R("pp-up", 10), R("full-restore", 15), R("max-revive", 10)),''',

'''            SpeciesBounty("mythical-victini", ContractTier.Mythical, 494, 350_000, R("master-ball", 1), R("rare-candy", 35)),''':
'''            SpeciesBounty("mythical-victini", ContractTier.Mythical, 494, 350_000, R("master-ball", 1), R("rare-candy", 12), R("pp-up", 5), R("full-restore", 8), R("fire-stone", 2), R("max-elixir", 3)),''',

'''            SpeciesBounty("mythical-magearna", ContractTier.Mythical, 801, 400_000, R("master-ball", 1), R("rare-candy", 40)),''':
'''            SpeciesBounty("mythical-magearna", ContractTier.Mythical, 801, 400_000, R("master-ball", 1), R("rare-candy", 12), R("pp-up", 6), R("full-restore", 10), R("shiny-stone", 2), R("max-revive", 5)),''',

'''            SpeciesBounty("mythical-zeraora", ContractTier.Mythical, 807, 400_000, R("master-ball", 1), R("rare-candy", 40)),''':
'''            SpeciesBounty("mythical-zeraora", ContractTier.Mythical, 807, 400_000, R("master-ball", 1), R("rare-candy", 12), R("pp-up", 6), R("full-restore", 10), R("thunder-stone", 2), R("max-revive", 5)),''',

'''            SpeciesBounty("mythical-pecharunt", ContractTier.Mythical, 1025, 450_000, R("master-ball", 2), R("rare-candy", 40)),''':
'''            SpeciesBounty("mythical-pecharunt", ContractTier.Mythical, 1025, 450_000, R("master-ball", 1), R("rare-candy", 15), R("pp-up", 8), R("full-restore", 10), R("max-revive", 5), R("dusk-stone", 2)),'''
}

for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"alpha52d reward rebalance anchor not found: {old[:90]}")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print(f"PKVault V8 alpha52d mixed contract rewards applied ({len(replacements)} definitions rebalanced)")

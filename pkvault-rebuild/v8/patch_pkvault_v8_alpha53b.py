from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / 'PKVault.Core/contract/ContractService.cs'
t = path.read_text(encoding='utf-8')

def rep(old, new, label):
    global t
    if old not in t:
        raise RuntimeError(f'alpha53b anchor not found: {label}')
    t = t.replace(old, new, 1)

rep(
'''    RequiredSpeciesCaughtDistinct,
}
''',
'''    RequiredSpeciesCaughtDistinct,
    TrainerBattles,
}
''',
'metric enum')

rep(
'''        public long ShinyCatchCount { get; set; }
        public Dictionary<ushort, long> SpeciesCatchCounts { get; } = [];
''',
'''        public long ShinyCatchCount { get; set; }
        public long TrainerBattleCount { get; set; }
        public Dictionary<string, long> TrainerBattleCounts { get; } = new(StringComparer.Ordinal);
        public Dictionary<ushort, long> SpeciesCatchCounts { get; } = [];
''',
'tracker fields')

rep('var offers = await BuildOffers(store);', 'var offers = await BuildOffers(store, tracker);', 'purchase offers')
rep('var offers = await BuildOffers(store);', 'var offers = await BuildOffers(store, tracker);', 'state offers')
rep(
'''    private async Task<List<BuiltOffer>> BuildOffers(StoreState store)
''',
'''    private async Task<List<BuiltOffer>> BuildOffers(StoreState store, TrackerState tracker)
''',
'BuildOffers signature')
rep(
'''            var pool = Definitions.Where(x => x.Tier == tier).ToArray();
''',
'''            var pool = Definitions
                .Where(x => x.Tier == tier)
                .Where(x => x.Metric != ContractMetric.TrainerBattles || tracker.TrainerBattleCounts.Count > 0)
                .ToArray();
''',
'trainer-support pool filter')

rep(
'''    private async Task UpdateTracker(TrackerState state)
    {
        var current = new Dictionary<string, PokemonSnapshot>(StringComparer.Ordinal);
        foreach (var loader in GetRealLoaders())
''',
'''    private async Task UpdateTracker(TrackerState state)
    {
        UpdateTrainerBattleTracker(state);

        var current = new Dictionary<string, PokemonSnapshot>(StringComparer.Ordinal);
        foreach (var loader in GetRealLoaders())
''',
'UpdateTracker hook')

rep(
'''            ContractMetric.RequiredSpeciesCaughtDistinct => tracker.EventSequence,
            _ => 0,
''',
'''            ContractMetric.RequiredSpeciesCaughtDistinct => tracker.EventSequence,
            ContractMetric.TrainerBattles => tracker.TrainerBattleCount,
            _ => 0,
''',
'trainer baseline')

rep(
'''            ContractMetric.RequiredSpeciesCaughtDistinct => definition.Species.LongCount(x => tracker.SpeciesLastCatchSequence.GetValueOrDefault(x) > startMetric),
            _ => 0,
''',
'''            ContractMetric.RequiredSpeciesCaughtDistinct => definition.Species.LongCount(x => tracker.SpeciesLastCatchSequence.GetValueOrDefault(x) > startMetric),
            ContractMetric.TrainerBattles => Math.Max(0, tracker.TrainerBattleCount - startMetric),
            _ => 0,
''',
'trainer progress')

anchor = '''    private async Task RememberVaultPokemon(TrackerState state)
'''
helpers = '''    private void UpdateTrainerBattleTracker(TrackerState state)
    {
        var observed = GetRealLoaders()
            .Select(loader => (Key: GetContractGameKey(loader.Save), Count: GetTrainerBattleCount(loader.Save)))
            .Where(x => x.Count >= 0)
            .GroupBy(x => x.Key, StringComparer.Ordinal)
            .Select(group => (Key: group.Key, Count: group.Max(x => x.Count)));

        foreach (var entry in observed)
        {
            var previous = state.TrainerBattleCounts.GetValueOrDefault(entry.Key);
            if (entry.Count <= previous)
                continue;

            state.TrainerBattleCount += entry.Count - previous;
            state.TrainerBattleCounts[entry.Key] = entry.Count;
        }
    }

    private static int GetTrainerBattleCount(SaveWrapper save)
    {
        var raw = save.GetSave();
        return raw switch
        {
            SAV3 gen3 => checked((int)Math.Min(gen3.GetRecord(9), int.MaxValue)),
            SAV4HGSS hgss => checked((int)Math.Min(hgss.Records.GetRecord32((int)Record4.Record4HGSSIndex.TrainerBattles), int.MaxValue)),
            SAV5 gen5 => checked((int)Math.Min(gen5.Records.GetRecord32(6), int.MaxValue)),
            SAV6 gen6 => Math.Max(0, gen6.GetRecord(6)),
            SAV7 gen7 => Math.Max(0, gen7.GetRecord(5)),
            SAV8BS bdsp => CountBdspDefeatedTrainers(bdsp),
            _ => -1,
        };
    }

    private static int CountBdspDefeatedTrainers(SAV8BS save)
    {
        var count = 0;
        for (var trainer = 0; trainer < 707; trainer++)
        {
            if (save.BattleTrainer.GetIsWin(trainer))
                count++;
        }
        return count;
    }

    private static string GetContractGameKey(SaveWrapper save) => save.GetSave() switch
    {
        EssentialsLegacySaveFile essentials => $"ess-{essentials.ProfileId}",
        SAV3 { DirectSpeciesIDs: true } => "romhack-too-many-types",
        _ => $"version-{(byte)save.Version}",
    };

'''
if anchor not in t:
    raise RuntimeError('alpha53b helper anchor')
t = t.replace(anchor, helpers + anchor, 1)

rep(
'''            else if (key == "shiny" && long.TryParse(raw, NumberStyles.Integer, CultureInfo.InvariantCulture, out var shinies)) state.ShinyCatchCount = Math.Max(0, shinies);
            else if (key.StartsWith("species.", StringComparison.Ordinal) && ushort.TryParse(key[8..], out var species))
''',
'''            else if (key == "shiny" && long.TryParse(raw, NumberStyles.Integer, CultureInfo.InvariantCulture, out var shinies)) state.ShinyCatchCount = Math.Max(0, shinies);
            else if (key == "trainer" && long.TryParse(raw, NumberStyles.Integer, CultureInfo.InvariantCulture, out var trainerBattles)) state.TrainerBattleCount = Math.Max(0, trainerBattles);
            else if (key.StartsWith("trainer.", StringComparison.Ordinal) && long.TryParse(raw, NumberStyles.Integer, CultureInfo.InvariantCulture, out var gameTrainerBattles))
                state.TrainerBattleCounts[key[8..]] = Math.Max(0, gameTrainerBattles);
            else if (key.StartsWith("species.", StringComparison.Ordinal) && ushort.TryParse(key[8..], out var species))
''',
'tracker load')

rep(
'''            $"shiny={state.ShinyCatchCount.ToString(CultureInfo.InvariantCulture)}",
        };
        lines.AddRange(state.SpeciesCatchCounts.OrderBy(x => x.Key).Select(x =>
''',
'''            $"shiny={state.ShinyCatchCount.ToString(CultureInfo.InvariantCulture)}",
            $"trainer={state.TrainerBattleCount.ToString(CultureInfo.InvariantCulture)}",
        };
        lines.AddRange(state.TrainerBattleCounts.OrderBy(x => x.Key, StringComparer.Ordinal).Select(x =>
            $"trainer.{x.Key}={x.Value.ToString(CultureInfo.InvariantCulture)}"));
        lines.AddRange(state.SpeciesCatchCounts.OrderBy(x => x.Key).Select(x =>
''',
'tracker save')

# Add battle contracts into each ordinary difficulty band.
rep(
'''            D("easy-species-5", ContractTier.Easy, "Five Different Species", "Catch 5 different species after accepting this contract.", 7_000, ContractMetric.DifferentSpeciesCaught, 5, [], R("ultra-ball", 5), R("great-ball", 5), R("super-potion", 4), R("full-heal", 2)),

            D("normal-catch-15",''',
'''            D("easy-species-5", ContractTier.Easy, "Five Different Species", "Catch 5 different species after accepting this contract.", 7_000, ContractMetric.DifferentSpeciesCaught, 5, [], R("ultra-ball", 5), R("great-ball", 5), R("super-potion", 4), R("full-heal", 2)),
            D("easy-trainer-battles-5", ContractTier.Easy, "Local Challenger", "Win 5 trainer battles after accepting this contract. Only games with a reliable saved trainer-battle counter contribute.", 4_500, ContractMetric.TrainerBattles, 5, [], R("great-ball", 8), R("super-potion", 5), R("revive", 2)),

            D("normal-catch-15",''',
'easy trainer contract')

rep(
'''            D("normal-evolve-5", ContractTier.Normal, "Evolution Workshop", "Evolve 5 Pokémon after accepting this contract.", 12_000, ContractMetric.EvolutionCount, 5, [], R("rare-candy", 3), R("moon-stone", 1), R("sun-stone", 1), R("dusk-stone", 1), R("dawn-stone", 1), R("shiny-stone", 1), R("revive", 3)),

            D("hard-catch-40",''',
'''            D("normal-evolve-5", ContractTier.Normal, "Evolution Workshop", "Evolve 5 Pokémon after accepting this contract.", 12_000, ContractMetric.EvolutionCount, 5, [], R("rare-candy", 3), R("moon-stone", 1), R("sun-stone", 1), R("dusk-stone", 1), R("dawn-stone", 1), R("shiny-stone", 1), R("revive", 3)),
            D("normal-trainer-battles-15", ContractTier.Normal, "Route Circuit", "Win 15 trainer battles after accepting this contract. Only games with a reliable saved trainer-battle counter contribute.", 10_000, ContractMetric.TrainerBattles, 15, [], R("ultra-ball", 12), R("hyper-potion", 5), R("revive", 4), R("rare-candy", 2), R("full-heal", 4)),

            D("hard-catch-40",''',
'normal trainer contract')

rep(
'''            D("hard-shiny-2", ContractTier.Hard, "Double Shiny Hunt", "Catch 2 shiny Pokémon after accepting this contract.", 75_000, ContractMetric.ShinyCatchCount, 2, [], R("rare-candy", 20), R("luxury-ball", 30), R("pp-up", 8), R("pp-max", 3), R("max-revive", 10), R("full-restore", 15), R("bottle-cap", 3), R("gold-bottle-cap", 1)),
            D("legendary-any",''',
'''            D("hard-shiny-2", ContractTier.Hard, "Double Shiny Hunt", "Catch 2 shiny Pokémon after accepting this contract.", 75_000, ContractMetric.ShinyCatchCount, 2, [], R("rare-candy", 20), R("luxury-ball", 30), R("pp-up", 8), R("pp-max", 3), R("max-revive", 10), R("full-restore", 15), R("bottle-cap", 3), R("gold-bottle-cap", 1)),
            D("hard-trainer-battles-30", ContractTier.Hard, "Trainer Circuit", "Win 30 trainer battles after accepting this contract. Only games with a reliable saved trainer-battle counter contribute.", 35_000, ContractMetric.TrainerBattles, 30, [], R("ultra-ball", 25), R("rare-candy", 5), R("full-restore", 8), R("max-revive", 5), R("pp-up", 2)),
            D("hard-trainer-battles-50", ContractTier.Hard, "Trainer Gauntlet", "Win 50 trainer battles after accepting this contract. Only games with a reliable saved trainer-battle counter contribute.", 55_000, ContractMetric.TrainerBattles, 50, [], R("ultra-ball", 40), R("rare-candy", 10), R("full-restore", 10), R("max-revive", 6), R("pp-up", 4), R("bottle-cap", 1)),
            D("legendary-any",''',
'hard trainer contracts')

path.write_text(t, encoding='utf-8')

check = path.read_text(encoding='utf-8')
assert 'ContractMetric.TrainerBattles' in check
assert 'easy-trainer-battles-5' in check
assert 'normal-trainer-battles-15' in check
assert 'hard-trainer-battles-30' in check
assert 'hard-trainer-battles-50' in check
assert 'tracker.TrainerBattleCount - startMetric' in check
assert 'tracker.TrainerBattleCounts.Count > 0' in check
print('PASS alpha53b trainer-battle contracts')

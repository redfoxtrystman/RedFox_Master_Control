from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve()
q=root/'PKVault.Core/quest/QuestService.cs'
t=q.read_text(encoding='utf-8')

def rep(old,new,label):
    global t
    if old not in t: raise RuntimeError(f'alpha53a1 anchor not found: {label}')
    t=t.replace(old,new,1)

rep('''    private sealed record GameQuestSnapshot(
        string Key,
        string Name,
        int PlaySeconds,
        int DexCaught,
        int DexTarget
    );
''','''    private sealed record GameQuestSnapshot(
        string Key,
        string Name,
        int PlaySeconds,
        int DexCaught,
        int DexTarget,
        int TrainerBattles
    );

    private sealed record GymGameDefinition(string Key, string Name, string[] Badges);
    private sealed record GymProgressSnapshot(string Key, ulong BadgeMask);
    private sealed record GymRewardPlan(QuestRewardDTO Display, string? ItemKey, IReadOnlyList<(string ItemKey, long Count)>? Bundle);

    private static readonly GymGameDefinition[] GymDefinitions =
    [
        new("gen1-kanto", "Pokémon Red / Blue / Yellow", ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Soul Badge", "Marsh Badge", "Volcano Badge", "Earth Badge"]),
        new("gen2-johto-kanto", "Pokémon Gold / Silver / Crystal", ["Zephyr Badge", "Hive Badge", "Plain Badge", "Fog Badge", "Storm Badge", "Mineral Badge", "Glacier Badge", "Rising Badge", "Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Soul Badge", "Marsh Badge", "Volcano Badge", "Earth Badge"]),
        new("gen3-hoenn", "Pokémon Ruby / Sapphire / Emerald", ["Stone Badge", "Knuckle Badge", "Dynamo Badge", "Heat Badge", "Balance Badge", "Feather Badge", "Mind Badge", "Rain Badge"]),
        new("gen3-kanto", "Pokémon FireRed / LeafGreen", ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Soul Badge", "Marsh Badge", "Volcano Badge", "Earth Badge"]),
        new("romhack-tmt-hoenn", "Pokémon Emerald — Too Many Types", ["Stone Badge", "Knuckle Badge", "Dynamo Badge", "Heat Badge", "Balance Badge", "Feather Badge", "Mind Badge", "Rain Badge"]),
        new("gen4-sinnoh", "Pokémon Diamond / Pearl / Platinum", ["Coal Badge", "Forest Badge", "Cobble Badge", "Fen Badge", "Relic Badge", "Mine Badge", "Icicle Badge", "Beacon Badge"]),
        new("gen4-johto-kanto", "Pokémon HeartGold / SoulSilver", ["Zephyr Badge", "Hive Badge", "Plain Badge", "Fog Badge", "Storm Badge", "Mineral Badge", "Glacier Badge", "Rising Badge", "Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Soul Badge", "Marsh Badge", "Volcano Badge", "Earth Badge"]),
        new("gen5-unova-bw", "Pokémon Black / White", ["Trio Badge", "Basic Badge", "Insect Badge", "Bolt Badge", "Quake Badge", "Jet Badge", "Freeze Badge", "Legend Badge"]),
        new("gen5-unova-b2w2", "Pokémon Black 2 / White 2", ["Basic Badge", "Toxic Badge", "Insect Badge", "Bolt Badge", "Quake Badge", "Jet Badge", "Legend Badge", "Wave Badge"]),
        new("gen6-kalos", "Pokémon X / Y", ["Bug Badge", "Cliff Badge", "Rumble Badge", "Plant Badge", "Voltage Badge", "Fairy Badge", "Psychic Badge", "Iceberg Badge"]),
        new("gen6-hoenn", "Pokémon Omega Ruby / Alpha Sapphire", ["Stone Badge", "Knuckle Badge", "Dynamo Badge", "Heat Badge", "Balance Badge", "Feather Badge", "Mind Badge", "Rain Badge"]),
        new("gen8-sinnoh", "Pokémon Brilliant Diamond / Shining Pearl", ["Coal Badge", "Forest Badge", "Cobble Badge", "Fen Badge", "Relic Badge", "Mine Badge", "Icicle Badge", "Beacon Badge"]),
        new("gen9-paldea", "Pokémon Scarlet / Violet", ["Bug Badge", "Grass Badge", "Electric Badge", "Water Badge", "Normal Badge", "Ghost Badge", "Psychic Badge", "Ice Badge"]),
    ];
''','records')

rep('''        var playtimeSnapshots = await LoadIntMap(MetaKey.QUEST_PLAYTIME_SNAPSHOTS);
        var knownIdentities = await LoadStringSet(MetaKey.QUEST_PKM_IDENTITIES);
''','''        var playtimeSnapshots = await LoadIntMap(MetaKey.QUEST_PLAYTIME_SNAPSHOTS);
        var trainerBattleSnapshots = await LoadIntMap(MetaKey.QUEST_TRAINER_BATTLE_SNAPSHOTS);
        var gymBadgeHistory = await LoadStringSet(MetaKey.QUEST_GYM_BADGE_HISTORY);
        var gymGamesSeen = await LoadStringSet(MetaKey.QUEST_GYM_GAMES_SEEN);
        var knownIdentities = await LoadStringSet(MetaKey.QUEST_PKM_IDENTITIES);
''','loads')

rep('''        var playtimeChanged = false;
        var vaultCaughtSpecies = new HashSet<ushort>();

        var realLoaders = GetRealLoaders();
''','''        var playtimeChanged = false;
        var trainerBattleSnapshotsChanged = false;
        var gymBadgeHistoryChanged = false;
        var gymGamesSeenChanged = false;
        var vaultCaughtSpecies = new HashSet<ushort>();

        var realLoaders = GetRealLoaders();
        var gameSnapshotsForProgress = BuildGameSnapshots(realLoaders);
        foreach (var game in gameSnapshotsForProgress.Where(x => x.TrainerBattles >= 0))
        {
            if (!trainerBattleSnapshots.TryGetValue(game.Key, out var storedTrainerBattles) || game.TrainerBattles > storedTrainerBattles)
            {
                trainerBattleSnapshots[game.Key] = game.TrainerBattles;
                trainerBattleSnapshotsChanged = true;
            }
        }

        foreach (var gym in BuildGymProgress(realLoaders))
        {
            if (gymGamesSeen.Add(gym.Key)) gymGamesSeenChanged = true;
            if (!TryGetGymDefinition(gym.Key, out var definition)) continue;
            for (var badge = 0; badge < definition.Badges.Length; badge++)
            {
                if ((gym.BadgeMask & (1UL << badge)) == 0) continue;
                if (gymBadgeHistory.Add(GymBadgeHistoryKey(gym.Key, badge))) gymBadgeHistoryChanged = true;
            }
        }
''','tracking')

rep('''        if (playtimeChanged)
            await SaveIntMap(MetaKey.QUEST_PLAYTIME_SNAPSHOTS, playtimeSnapshots);
        if (historyChanged || currentCaught.Count > 0)
''','''        if (playtimeChanged)
            await SaveIntMap(MetaKey.QUEST_PLAYTIME_SNAPSHOTS, playtimeSnapshots);
        if (trainerBattleSnapshotsChanged)
            await SaveIntMap(MetaKey.QUEST_TRAINER_BATTLE_SNAPSHOTS, trainerBattleSnapshots);
        if (gymBadgeHistoryChanged)
            await SaveStringSet(MetaKey.QUEST_GYM_BADGE_HISTORY, gymBadgeHistory);
        if (gymGamesSeenChanged)
            await SaveStringSet(MetaKey.QUEST_GYM_GAMES_SEEN, gymGamesSeen);
        if (historyChanged || currentCaught.Count > 0)
''','saves')

rep('''        var legendaryCaughtCount = caughtHistory.Count(LegendarySpecies.ContainsKey);
        var mythicalCaughtCount = caughtHistory.Count(MythicalSpecies.ContainsKey);
        var gameSnapshots = BuildGameSnapshots(realLoaders);
        var itemInventory = await itemBankService.GetState();
''','''        var legendaryCaughtCount = caughtHistory.Count(LegendarySpecies.ContainsKey);
        var mythicalCaughtCount = caughtHistory.Count(MythicalSpecies.ContainsKey);
        var gameSnapshots = gameSnapshotsForProgress;
        var trainerBattleProgress = trainerBattleSnapshots.Values.Sum(x => (long)x);
        var itemInventory = await itemBankService.GetState();
''','snapshot reuse')

q.write_text(t,encoding='utf-8')
meta=root/'PKVault.Core/db/entity/MetaEntity.cs'
m=meta.read_text(encoding='utf-8')
old='''    ITEM_BANK_PAGE_NAMES = 24,
}'''
new='''    ITEM_BANK_PAGE_NAMES = 24,
    QUEST_TRAINER_BATTLE_SNAPSHOTS = 25,
    QUEST_GYM_BADGE_HISTORY = 26,
    QUEST_GYM_GAMES_SEEN = 27,
}'''
if old not in m: raise RuntimeError('alpha53a1 MetaKey anchor')
meta.write_text(m.replace(old,new,1),encoding='utf-8')
print('PASS alpha53a1 battle/gym persistence scaffolding')

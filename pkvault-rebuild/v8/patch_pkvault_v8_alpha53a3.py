from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
q=root/'PKVault.Core/quest/QuestService.cs'
t=q.read_text(encoding='utf-8')
old='''    private static List<GameQuestSnapshot> BuildGameSnapshots(IEnumerable<SaveLoadersRecord> loaders)
    {
        return loaders
            .Select(loader =>
            {
                var save = loader.Save;
                return new GameQuestSnapshot(
                    Key: GetGameKey(save),
                    Name: GetGameName(save),
                    PlaySeconds: Math.Max(0, save.PlayTimeInSeconds),
                    DexCaught: GetDexCaughtCount(save),
                    DexTarget: GetDexTarget(save)
                );
            })
            .GroupBy(x => x.Key, StringComparer.Ordinal)
            .Select(group =>
            {
                var bestDex = group.OrderByDescending(x => x.DexCaught).First();
                return bestDex with
                {
                    PlaySeconds = group.Max(x => x.PlaySeconds),
                    DexCaught = group.Max(x => x.DexCaught),
                    DexTarget = group.Max(x => x.DexTarget),
                };
            })
            .OrderBy(x => x.Name, StringComparer.Ordinal)
            .ToList();
    }

'''
new='''    private static List<GameQuestSnapshot> BuildGameSnapshots(IEnumerable<SaveLoadersRecord> loaders)
    {
        return loaders
            .Select(loader =>
            {
                var save = loader.Save;
                return new GameQuestSnapshot(
                    Key: GetGameKey(save),
                    Name: GetGameName(save),
                    PlaySeconds: Math.Max(0, save.PlayTimeInSeconds),
                    DexCaught: GetDexCaughtCount(save),
                    DexTarget: GetDexTarget(save),
                    TrainerBattles: GetTrainerBattleCount(save)
                );
            })
            .GroupBy(x => x.Key, StringComparer.Ordinal)
            .Select(group =>
            {
                var bestDex = group.OrderByDescending(x => x.DexCaught).First();
                return bestDex with
                {
                    PlaySeconds = group.Max(x => x.PlaySeconds),
                    DexCaught = group.Max(x => x.DexCaught),
                    DexTarget = group.Max(x => x.DexTarget),
                    TrainerBattles = group.Max(x => x.TrainerBattles),
                };
            })
            .OrderBy(x => x.Name, StringComparer.Ordinal)
            .ToList();
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
            if (save.BattleTrainer.GetIsWin(trainer)) count++;
        }
        return count;
    }

    private static List<GymProgressSnapshot> BuildGymProgress(IEnumerable<SaveLoadersRecord> loaders)
        => loaders.Select(loader => GetGymProgress(loader.Save))
            .Where(x => x is not null).Select(x => x!)
            .GroupBy(x => x.Key, StringComparer.Ordinal)
            .Select(group => new GymProgressSnapshot(group.Key, group.Aggregate(0UL, (mask, item) => mask | item.BadgeMask)))
            .ToList();

    private static GymProgressSnapshot? GetGymProgress(SaveWrapper save)
    {
        var raw = save.GetSave();
        var definition = GetGymDefinition(save);
        if (definition is null) return null;

        ulong mask = raw switch
        {
            SAV1 gen1 => (uint)gen1.Badges & 0xFFu,
            SAV2 gen2 => (uint)gen2.Badges & 0xFFFFu,
            SAV3 gen3 => (uint)gen3.Badges & 0xFFu,
            SAV4HGSS hgss => ((uint)hgss.Badges & 0xFFu) | (((ulong)hgss.Badges16 & 0xFFu) << 8),
            SAV4 gen4 => (uint)gen4.Badges & 0xFFu,
            SAV5 gen5 => (uint)gen5.Misc.Badges & 0xFFu,
            SAV6 gen6 => (uint)gen6.Badges & 0xFFu,
            SAV8BS bdsp => GetBdspGymBadgeMask(bdsp),
            SAV9SV sv => GetPaldeaGymBadgeMask(sv),
            _ => 0,
        };
        var allowed = (1UL << definition.Badges.Length) - 1;
        return new(definition.Key, mask & allowed);
    }

    private static GymGameDefinition? GetGymDefinition(SaveWrapper save)
    {
        if (save.GetSave() is SAV3 { DirectSpeciesIDs: true })
            return GymDefinitions.First(x => x.Key == "romhack-tmt-hoenn");
        var key = save.Version switch
        {
            GameVersion.RD or GameVersion.GN or GameVersion.BU or GameVersion.YW => "gen1-kanto",
            GameVersion.GD or GameVersion.SI or GameVersion.C => "gen2-johto-kanto",
            GameVersion.R or GameVersion.S or GameVersion.E => "gen3-hoenn",
            GameVersion.FR or GameVersion.LG => "gen3-kanto",
            GameVersion.D or GameVersion.P or GameVersion.Pt => "gen4-sinnoh",
            GameVersion.HG or GameVersion.SS => "gen4-johto-kanto",
            GameVersion.B or GameVersion.W => "gen5-unova-bw",
            GameVersion.B2 or GameVersion.W2 => "gen5-unova-b2w2",
            GameVersion.X or GameVersion.Y => "gen6-kalos",
            GameVersion.OR or GameVersion.AS => "gen6-hoenn",
            GameVersion.BD or GameVersion.SP => "gen8-sinnoh",
            GameVersion.SL or GameVersion.VL => "gen9-paldea",
            _ => null,
        };
        return key is null ? null : GymDefinitions.First(x => x.Key == key);
    }

    private static bool TryGetGymDefinition(string key, out GymGameDefinition definition)
    {
        definition = GymDefinitions.FirstOrDefault(x => string.Equals(x.Key, key, StringComparison.Ordinal))!;
        return definition is not null;
    }

    private static ulong GetBdspGymBadgeMask(SAV8BS save)
    {
        ulong result = 0;
        for (var badge = 0; badge < 8; badge++)
            if (save.FlagWork.GetSystemFlag(124 + badge)) result |= 1UL << badge;
        return result;
    }

    private static ulong GetPaldeaGymBadgeMask(SAV9SV save)
    {
        ReadOnlySpan<uint> badgeKeys = [
            0x89306FE6u, 0xB4C3AFE6u, 0x8205ECADu, 0xA803FAADu,
            0xF90EFD79u, 0xCDA61DEDu, 0x3B819021u, 0x46B6CB30u,
        ];
        ulong result = 0;
        for (var badge = 0; badge < badgeKeys.Length; badge++)
            if (save.Blocks.TryGetBlock(badgeKeys[badge], out var block) && block.Type == SCTypeCode.Bool2) result |= 1UL << badge;
        return result;
    }

    private static string GymBadgeHistoryKey(string gymKey, int badge) => $"{gymKey}:{badge}";

    private static GymRewardPlan GetGymBadgeReward(int badgeIndex) => badgeIndex switch
    {
        0 => new(new("Great Ball", 5), "great-ball", null),
        1 => new(new("Super Potion", 5), "super-potion", null),
        2 => new(new("5 Great Balls + 2 Revives", 1), null, [("great-ball", 5L), ("revive", 2L)]),
        3 => new(new("Ultra Ball", 5), "ultra-ball", null),
        4 => new(new("5 Hyper Potions + 3 Full Heals", 1), null, [("hyper-potion", 5L), ("full-heal", 3L)]),
        5 => new(new("Rare Candy", 3), "rare-candy", null),
        6 => new(new("5 Ultra Balls + 2 Max Revives", 1), null, [("ultra-ball", 5L), ("max-revive", 2L)]),
        7 => new(new("5 Rare Candies + 5 Full Restores", 1), null, [("rare-candy", 5L), ("full-restore", 5L)]),
        8 => new(new("5 Ultra Balls + 2 Rare Candies", 1), null, [("ultra-ball", 5L), ("rare-candy", 2L)]),
        9 => new(new("5 Ultra Balls + 3 Full Restores", 1), null, [("ultra-ball", 5L), ("full-restore", 3L)]),
        10 => new(new("3 Rare Candies + 2 Max Revives", 1), null, [("rare-candy", 3L), ("max-revive", 2L)]),
        11 => new(new("Ultra Ball", 10), "ultra-ball", null),
        12 => new(new("Rare Candy", 5), "rare-candy", null),
        13 => new(new("PP Up + 5 Full Restores", 1), null, [("pp-up", 1L), ("full-restore", 5L)]),
        14 => new(new("2 PP Ups + 3 Max Revives", 1), null, [("pp-up", 2L), ("max-revive", 3L)]),
        _ => new(new("Bottle Cap + PP Max + 10 Ultra Balls", 1), null, [("bottle-cap", 1L), ("pp-max", 1L), ("ultra-ball", 10L)]),
    };

    private static GymRewardPlan GetGymCircuitReward(int badgeCount)
        => badgeCount > 8
            ? new(new("Gold Bottle Cap + 2 PP Max + 10 Rare Candies + 20 Ultra Balls", 1), null, [("gold-bottle-cap", 1L), ("pp-max", 2L), ("rare-candy", 10L), ("ultra-ball", 20L)])
            : new(new("Bottle Cap + 5 Rare Candies + 10 Ultra Balls + 5 Max Revives", 1), null, [("bottle-cap", 1L), ("rare-candy", 5L), ("ultra-ball", 10L), ("max-revive", 5L)]);

'''
if old not in t: raise RuntimeError('alpha53a3 BuildGameSnapshots anchor')
q.write_text(t.replace(old,new,1),encoding='utf-8')
print('PASS alpha53a3 trainer/badge save readers')

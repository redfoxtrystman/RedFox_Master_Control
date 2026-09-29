from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()

def rep(path, old, new, label):
    t=path.read_text(encoding='utf-8')
    if old not in t:
        raise RuntimeError(f'anchor not found: {label}')
    path.write_text(t.replace(old,new,1),encoding='utf-8')

cs=root/'PKVault.Core/contract/ContractService.cs'
t=cs.read_text(encoding='utf-8')

t=t.replace('''internal enum ContractTier\n{\n    Easy,\n    Normal,\n    Hard,\n    Legendary,\n    Mythical,\n}\n''','''internal enum ContractTier\n{\n    Easy,\n    Normal,\n    Hard,\n    Legendary,\n    Mythical,\n    Apex,\n}\n''',1)
t=t.replace('''    SpeciesCatchCount,\n    SpeciesSetCatchCount,\n}\n''','''    SpeciesCatchCount,\n    SpeciesSetCatchCount,\n    RequiredSpeciesCaughtDistinct,\n}\n''',1)
t=t.replace('private sealed record HistoryState(string InstanceId, string DefinitionId, long CompletedAtUnix);','private sealed record HistoryState(string InstanceId, string DefinitionId, string OfferId, long CompletedAtUnix);',1)

# Reward completion + history seed
old='''            foreach (var reward in definition.Rewards)\n            {\n                var rewardId = $"contract:{active.InstanceId}:{reward.ItemKey}";\n                if (reward.IsMoney)\n                    await itemBankService.GrantQuestMoneyReward(rewardId, reward.Count);\n                else\n                    await itemBankService.GrantQuestReward(rewardId, reward.ItemKey, reward.Count);\n            }\n\n            store.Active.Remove(active);\n            store.History.Insert(0, new(active.InstanceId, active.DefinitionId, DateTimeOffset.Now.ToUnixTimeSeconds()));\n'''
new='''            foreach (var reward in RewardsFor(definition, active.OfferId))\n            {\n                var rewardId = $"contract:{active.InstanceId}:{reward.ItemKey}";\n                if (reward.IsMoney)\n                    await itemBankService.GrantQuestMoneyReward(rewardId, reward.Count);\n                else\n                    await itemBankService.GrantQuestReward(rewardId, reward.ItemKey, reward.Count);\n            }\n\n            store.Active.Remove(active);\n            store.History.Insert(0, new(active.InstanceId, active.DefinitionId, active.OfferId, DateTimeOffset.Now.ToUnixTimeSeconds()));\n'''
if old not in t: raise RuntimeError('complete rewards anchor')
t=t.replace(old,new,1)

t=t.replace('Rewards: RewardDtos(definition)\n                );','Rewards: RewardDtos(definition, active.OfferId)\n                );',1)
t=t.replace('Rewards: RewardDtos(definition)\n                );','Rewards: RewardDtos(definition, entry.OfferId)\n                );',1)

old='''        var usedDefinitions = new HashSet<string>(StringComparer.Ordinal);\n        var result = new List<BuiltOffer>(4);\n\n        for (var slot = 0; slot < 4; slot++)\n        {\n            var daily = slot < 2;\n            var cadence = daily ? "Daily" : "Weekly";\n            var periodKey = daily ? $"D:{dailyKey}" : $"W:{weeklyKey}";\n            var random = DeterministicRandom($"{userId}|{periodKey}|slot:{slot}");\n            var tier = RollTier(random, daily);\n            var pool = Definitions.Where(x => x.Tier == tier).ToArray();\n'''
new='''        var usedDefinitions = new HashSet<string>(StringComparer.Ordinal);\n        var result = new List<BuiltOffer>(6);\n\n        for (var slot = 0; slot < 6; slot++)\n        {\n            var daily = slot < 4;\n            var cadence = daily ? "Daily" : "Weekly";\n            var periodKey = daily ? $"D:{dailyKey}" : $"W:{weeklyKey}";\n            var random = DeterministicRandom($"{userId}|{periodKey}|slot:{slot}");\n            var tier = daily\n                ? slot switch\n                {\n                    0 => ContractTier.Easy,\n                    1 => ContractTier.Normal,\n                    2 => ContractTier.Hard,\n                    _ => RollDailyWildcardTier(random),\n                }\n                : RollWeeklyTier(random);\n            var pool = Definitions.Where(x => x.Tier == tier).ToArray();\n'''
if old not in t: raise RuntimeError('BuildOffers anchor')
t=t.replace(old,new,1)

t=t.replace('Rewards: RewardDtos(definition),','Rewards: RewardDtos(definition, offerId),',1)

old='''    private static ContractTier RollTier(Random random, bool daily)\n    {\n        var roll = random.Next(100);\n        if (daily)\n        {\n            if (roll < 40) return ContractTier.Easy;\n            if (roll < 80) return ContractTier.Normal;\n            return ContractTier.Hard;\n        }\n\n        if (roll < 30) return ContractTier.Normal;\n        if (roll < 60) return ContractTier.Hard;\n        if (roll < 85) return ContractTier.Legendary;\n        return ContractTier.Mythical;\n    }\n'''
new='''    private static ContractTier RollDailyWildcardTier(Random random)\n    {\n        var roll = random.Next(100);\n        if (roll < 35) return ContractTier.Easy;\n        if (roll < 75) return ContractTier.Normal;\n        return ContractTier.Hard;\n    }\n\n    private static ContractTier RollWeeklyTier(Random random)\n    {\n        // Normal -> Mythical is the ordinary weekly band. Apex is a deliberately\n        // tiny jackpot override so it remains a genuine event when it appears.\n        var roll = random.Next(100);\n        if (roll < 30) return ContractTier.Normal;\n        if (roll < 60) return ContractTier.Hard;\n        if (roll < 85) return ContractTier.Legendary;\n        if (roll < 98) return ContractTier.Mythical;\n        return ContractTier.Apex;\n    }\n'''
if old not in t: raise RuntimeError('RollTier anchor')
t=t.replace(old,new,1)

# exact required species metric
old='''            ContractMetric.SpeciesCatchCount => definition.Species.Sum(x => tracker.SpeciesCatchCounts.GetValueOrDefault(x)),\n            ContractMetric.SpeciesSetCatchCount => definition.Species.Sum(x => tracker.SpeciesCatchCounts.GetValueOrDefault(x)),\n            _ => 0,\n'''
new='''            ContractMetric.SpeciesCatchCount => definition.Species.Sum(x => tracker.SpeciesCatchCounts.GetValueOrDefault(x)),\n            ContractMetric.SpeciesSetCatchCount => definition.Species.Sum(x => tracker.SpeciesCatchCounts.GetValueOrDefault(x)),\n            ContractMetric.RequiredSpeciesCaughtDistinct => tracker.EventSequence,\n            _ => 0,\n'''
if old not in t: raise RuntimeError('baseline metric anchor')
t=t.replace(old,new,1)
old='''            ContractMetric.SpeciesCatchCount => Math.Max(0, definition.Species.Sum(x => tracker.SpeciesCatchCounts.GetValueOrDefault(x)) - startMetric),\n            ContractMetric.SpeciesSetCatchCount => Math.Max(0, definition.Species.Sum(x => tracker.SpeciesCatchCounts.GetValueOrDefault(x)) - startMetric),\n            _ => 0,\n'''
new='''            ContractMetric.SpeciesCatchCount => Math.Max(0, definition.Species.Sum(x => tracker.SpeciesCatchCounts.GetValueOrDefault(x)) - startMetric),\n            ContractMetric.SpeciesSetCatchCount => Math.Max(0, definition.Species.Sum(x => tracker.SpeciesCatchCounts.GetValueOrDefault(x)) - startMetric),\n            ContractMetric.RequiredSpeciesCaughtDistinct => definition.Species.LongCount(x => tracker.SpeciesLastCatchSequence.GetValueOrDefault(x) > startMetric),\n            _ => 0,\n'''
if old not in t: raise RuntimeError('progress metric anchor')
t=t.replace(old,new,1)

# backward compatible history persistence
old='''            else if (line.StartsWith("history=", StringComparison.Ordinal))\n            {\n                var p = line[8..].Split('|');\n                if (p.Length == 3 && long.TryParse(p[2], out var when))\n                    state.History.Add(new(p[0], p[1], when));\n            }\n'''
new='''            else if (line.StartsWith("history=", StringComparison.Ordinal))\n            {\n                var p = line[8..].Split('|');\n                if (p.Length == 4 && long.TryParse(p[3], out var when))\n                    state.History.Add(new(p[0], p[1], p[2], when));\n                else if (p.Length == 3 && long.TryParse(p[2], out when))\n                    state.History.Add(new(p[0], p[1], p[0], when));\n            }\n'''
if old not in t: raise RuntimeError('history load anchor')
t=t.replace(old,new,1)
t=t.replace('lines.AddRange(state.History.Select(x => $"history={x.InstanceId}|{x.DefinitionId}|{x.CompletedAtUnix}"));','lines.AddRange(state.History.Select(x => $"history={x.InstanceId}|{x.DefinitionId}|{x.OfferId}|{x.CompletedAtUnix}"));',1)

old='''    private static List<ContractRewardLineDTO> RewardDtos(ContractDefinition definition)\n        => definition.Rewards.Select(x => new ContractRewardLineDTO(\n            x.ItemKey,\n            Humanize(x.ItemKey),\n            x.Count,\n            x.IsMoney\n        )).ToList();\n'''
new='''    private static ContractReward[] RewardsFor(ContractDefinition definition, string rewardSeed)\n        => definition.Tier == ContractTier.Apex ? BuildApexRewards(rewardSeed) : definition.Rewards;\n\n    private static ContractReward[] BuildApexRewards(string rewardSeed)\n    {\n        var random = DeterministicRandom($"apex-rewards|{rewardSeed}");\n        var rewards = new List<ContractReward>\n        {\n            R("master-ball", 1),\n            R("ultra-ball", 20),\n        };\n        var pool = new (string Key, int Min, int Max)[]\n        {\n            ("rare-candy", 8, 20), ("pp-up", 4, 10), ("pp-max", 1, 4),\n            ("full-restore", 10, 30), ("max-revive", 5, 15), ("max-elixir", 3, 8),\n            ("max-ether", 5, 12), ("luxury-ball", 10, 30), ("quick-ball", 15, 30),\n            ("dusk-ball", 15, 30), ("timer-ball", 15, 30), ("bottle-cap", 2, 5),\n            ("gold-bottle-cap", 1, 3), ("ability-capsule", 1, 3), ("big-nugget", 3, 8),\n            ("hp-up", 3, 8), ("protein", 3, 8), ("iron", 3, 8),\n            ("calcium", 3, 8), ("carbos", 3, 8),\n        };\n\n        var wanted = random.Next(10, 16);\n        foreach (var entry in pool.OrderBy(_ => random.Next()).Take(wanted - rewards.Count))\n            rewards.Add(R(entry.Key, random.Next(entry.Min, entry.Max + 1)));\n        return [.. rewards];\n    }\n\n    private static List<ContractRewardLineDTO> RewardDtos(ContractDefinition definition, string rewardSeed)\n        => RewardsFor(definition, rewardSeed).Select(x => new ContractRewardLineDTO(\n            x.ItemKey,\n            Humanize(x.ItemKey),\n            x.Count,\n            x.IsMoney\n        )).ToList();\n'''
if old not in t: raise RuntimeError('RewardDtos anchor')
t=t.replace(old,new,1)

# Normal band prices
prices={
'normal-catch-15':'6_000','normal-species-8':'7_000','normal-level-50':'7_500','normal-evolve-3':'8_500',
'normal-catch-25':'9_000','normal-species-12':'10_000','normal-level-75':'11_000','normal-evolve-5':'12_000'}
for id,newprice in prices.items():
    import re
    pat=rf'(D\("{re.escape(id)}", ContractTier\.Normal,.*?, )([0-9_]+)(, ContractMetric\.)'
    nt,n=re.subn(pat,rf'\g<1>{newprice}\g<3>',t,count=1)
    if n!=1: raise RuntimeError(f'price anchor {id}')
    t=nt

# Apex contracts appended after mythical definitions
anchor='''            SpeciesBounty("mythical-pecharunt", ContractTier.Mythical, 1025, 450_000, R("master-ball", 1), R("rare-candy", 15), R("pp-up", 8), R("full-restore", 10), R("max-revive", 5), R("dusk-stone", 2)),\n'''
insert=anchor+'''\n            D("apex-kanto-gauntlet", ContractTier.Apex, "Kanto Gauntlet", "Catch Mewtwo, Articuno, Zapdos, and Moltres after accepting this contract. Every one of the four is required.", 1_500_000, ContractMetric.RequiredSpeciesCaughtDistinct, 4, [150, 144, 145, 146]),\n            D("apex-johto-sovereigns", ContractTier.Apex, "Johto Sovereigns", "Catch Raikou, Entei, Suicune, Lugia, and Ho-Oh after accepting this contract. Every one of the five is required.", 1_750_000, ContractMetric.RequiredSpeciesCaughtDistinct, 5, [243, 244, 245, 249, 250]),\n            D("apex-weather-trinity", ContractTier.Apex, "Weather Trinity", "Catch Kyogre, Groudon, and Rayquaza after accepting this contract. Every member of the trio is required.", 1_650_000, ContractMetric.RequiredSpeciesCaughtDistinct, 3, [382, 383, 384]),\n            D("apex-creation-crisis", ContractTier.Apex, "Creation Crisis", "Catch Dialga, Palkia, Giratina, and Arceus after accepting this contract. Every one of the four is required.", 2_250_000, ContractMetric.RequiredSpeciesCaughtDistinct, 4, [483, 484, 487, 493]),\n'''
if anchor not in t: raise RuntimeError('apex insertion anchor')
t=t.replace(anchor,insert,1)
cs.write_text(t,encoding='utf-8')

# Frontend contract tier type and colors/text
api=root/'frontend/src/contracts/contract-api.ts'
t=api.read_text(encoding='utf-8')
t=t.replace("tier: 'Easy' | 'Normal' | 'Hard' | 'Legendary' | 'Mythical';","tier: 'Easy' | 'Normal' | 'Hard' | 'Legendary' | 'Mythical' | 'Apex';",1)
api.write_text(t,encoding='utf-8')

shop=root/'frontend/src/shop/shop-page.tsx'
t=shop.read_text(encoding='utf-8')
t=t.replace("        case 'Mythical': return 'pink';\n", "        case 'Mythical': return 'pink';\n        case 'Apex': return 'red';\n",1)
t=t.replace('Four offers are stocked at a time. Purchased contracts stay active until completed or abandoned.','Six offers are stocked at a time: four daily and two weekly. Purchased contracts stay active until completed or abandoned.',1)
t=t.replace('2 slots · Easy / Normal / Hard','4 slots · guaranteed Easy / Normal / Hard + 1 wildcard',1)
t=t.replace('2 slots · Normal / Hard / Legendary / Mythical','2 slots · Normal / Hard / Legendary / Mythical · rare Apex',1)
t=t.replace('Weekly rolls are indepent: both slots can roll the same tier. A board can have two Mythicals, two Legendaries, neither, or lower-tier weekly contracts. Abandoning an active contract does not refund its purchase price.','Weekly rolls are independent from Normal through Mythical. Each weekly slot also has a 2% chance to become an Apex contract costing ₽1.5M–₽2.25M with exact multi-Legendary requirements and a 10–15-line premium reward bundle. Abandoning an active contract does not refund its purchase price.',1)
shop.write_text(t,encoding='utf-8')

qp=root/'frontend/src/quests/quest-page.tsx'
t=qp.read_text(encoding='utf-8')
t=t.replace("    case 'Mythical': return 'pink';\n", "    case 'Mythical': return 'pink';\n    case 'Apex': return 'red';\n",1)
qp.write_text(t,encoding='utf-8')

# sanity
ct=cs.read_text(encoding='utf-8')
assert 'Apex,' in ct
assert 'new List<BuiltOffer>(6)' in ct
assert 'var daily = slot < 4;' in ct
assert 'if (roll < 98) return ContractTier.Mythical;' in ct
assert 'return ContractTier.Apex;' in ct
assert 'normal-species-12' in ct and '10_000, ContractMetric.DifferentSpeciesCaught' in ct
assert 'RequiredSpeciesCaughtDistinct' in ct
assert 'BuildApexRewards' in ct
assert 'apex-kanto-gauntlet' in ct
assert '1_500_000' in ct and '2_250_000' in ct
print('PASS alpha52y contract economy + 4 daily / 2 weekly + Apex contracts')

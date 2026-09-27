from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52k1 anchor not found: {label}")
    return text.replace(old, new, 1)

quest_path = root / "PKVault.Core/quest/QuestService.cs"
text = quest_path.read_text(encoding="utf-8")

text = rep(text,
"""    long Target,
    bool Completed,
    QuestRewardDTO Reward
);
""",
"""    long Target,
    bool Completed,
    bool Claimable,
    QuestRewardDTO Reward
);
""",
"QuestEntryDTO")

text = rep(text,
"""public record QuestRerollRequest(string QuestId);
public record QuestStateDTO(
""",
"""public record QuestRerollRequest(string QuestId);
public record QuestClaimRequest(string QuestId);
public record QuestStateDTO(
""",
"QuestClaimRequest")

text = rep(text,
"""    private sealed record RewardPlan(QuestRewardDTO Display, string? ItemKey, IReadOnlyList<(string ItemKey, long Count)>? Bundle = null);

    private sealed class DailyState(string date)
""",
"""    private sealed record RewardPlan(QuestRewardDTO Display, string? ItemKey, IReadOnlyList<(string ItemKey, long Count)>? Bundle = null);
    private sealed record QuestClaimPlan(
        string CompletionId,
        string Title,
        string Description,
        QuestRewardDTO Reward,
        string? RewardItemKey,
        IReadOnlyList<(string ItemKey, long Count)>? ItemRewards,
        long BonusMoney
    );

    private readonly Dictionary<string, QuestClaimPlan> claimPlans = new(StringComparer.Ordinal);

    private sealed class DailyState(string date)
""",
"claim plan")

text = rep(text,
"""    public async Task<QuestStateDTO> RerollDailyQuest(string questId)
    {
""",
"""    public async Task<QuestStateDTO> ClaimQuest(string questId)
    {
        await QuestGate.WaitAsync();
        try
        {
            var current = await EvaluateCore();
            if (!claimPlans.TryGetValue(questId, out var plan))
            {
                var existing = current.DailyQuests
                    .Concat(current.Quests)
                    .Concat(current.Achievements)
                    .FirstOrDefault(x => string.Equals(x.Id, questId, StringComparison.Ordinal));

                if (existing?.Completed == true)
                    return current;

                throw new InvalidOperationException("That quest is not ready to claim.");
            }

            var completed = await LoadStringSet(MetaKey.QUEST_COMPLETED);
            if (completed.Contains(plan.CompletionId))
                return current;

            if (plan.Reward.IsMoney)
                await itemBankService.GrantQuestMoneyReward(plan.CompletionId, plan.Reward.Count);
            else if (plan.ItemRewards is not null)
            {
                foreach (var grant in plan.ItemRewards)
                    await itemBankService.GrantQuestReward(plan.CompletionId, grant.ItemKey, grant.Count);
            }
            else if (!string.IsNullOrWhiteSpace(plan.RewardItemKey))
                await itemBankService.GrantQuestReward(plan.CompletionId, plan.RewardItemKey, plan.Reward.Count);

            if (plan.BonusMoney > 0 && !plan.Reward.IsMoney)
                await itemBankService.GrantQuestMoneyReward(plan.CompletionId, plan.BonusMoney);

            completed.Add(plan.CompletionId);
            await SaveStringSet(MetaKey.QUEST_COMPLETED, completed);

            var refreshed = await EvaluateCore();
            var claimed = refreshed.NewlyCompleted.ToList();
            claimed.Add(new(
                Id: plan.CompletionId,
                Title: plan.Title,
                Message: $"Reward claimed: {plan.Description}",
                Reward: plan.Reward
            ));
            return refreshed with { NewlyCompleted = claimed };
        }
        finally
        {
            QuestGate.Release();
        }
    }

    public async Task<QuestStateDTO> RerollDailyQuest(string questId)
    {
""",
"ClaimQuest")

text = rep(text,
"""            if (completed.Contains(DailyCompletionId(today, questId)))
                throw new InvalidOperationException("Completed daily quests cannot be rerolled.");

            var blocked = daily.ActiveQuestIds.ToHashSet(StringComparer.Ordinal);
""",
"""            if (completed.Contains(DailyCompletionId(today, questId)))
                throw new InvalidOperationException("Claimed daily quests cannot be rerolled.");

            if (definitions.TryGetValue(questId, out var activeDefinition)
                && activeDefinition.Progress(daily) >= activeDefinition.Target)
                throw new InvalidOperationException("Ready-to-claim daily quests cannot be rerolled.");

            var blocked = daily.ActiveQuestIds.ToHashSet(StringComparer.Ordinal);
""",
"reroll guard")

text = rep(text,
"""    private async Task<QuestStateDTO> EvaluateCore()
    {
        var completed = await LoadStringSet(MetaKey.QUEST_COMPLETED);
""",
"""    private async Task<QuestStateDTO> EvaluateCore()
    {
        claimPlans.Clear();
        var completed = await LoadStringSet(MetaKey.QUEST_COMPLETED);
""",
"claim clear")

old_correction = """        // Alpha44 could shrink an Essentials Dex target to the highest species
        // still occupying a save slot. If that falsely completed a full-Dex
        // achievement, clear only that bad completion now that the profile target
        // is stable. Item/money provenance remains idempotent, so a later genuine
        // completion cannot duplicate the already-granted bugged reward.
        var correctedCompletionHistory = false;
        foreach (var game in gameSnapshots.Where(game => game.Key.StartsWith("ess-", StringComparison.Ordinal)))
        {
            var completionId = $"dex-{game.Key}-complete";
            if (game.DexCaught < game.DexTarget && completed.Remove(completionId))
                correctedCompletionHistory = true;
        }

"""
if old_correction not in text:
    raise RuntimeError("alpha52k1 correction block missing")
text = text.replace(old_correction, "", 1)

old_game_dex = """            if (game.DexTarget >= 25)
                quests.Add(await EvaluateQuest($"dex-{game.Key}-25", $"dex-{game.Key}-25", "Pokédex", $"{game.Name}: 25 Caught", $"Catch/register 25 species in {game.Name}.", game.DexCaught, 25, new("5 Poké Balls + 2 Potions", 1), null, completed, newlyCompleted, [("poke-ball", 5L), ("potion", 2L)]));
            if (game.DexTarget >= 50)
                quests.Add(await EvaluateQuest($"dex-{game.Key}-50", $"dex-{game.Key}-50", "Pokédex", $"{game.Name}: 50 Caught", $"Catch/register 50 species in {game.Name}.", game.DexCaught, 50, MoneyReward(1_500), null, completed, newlyCompleted));
            if (game.DexTarget >= 100)
                quests.Add(await EvaluateQuest($"dex-{game.Key}-100", $"dex-{game.Key}-100", "Pokédex", $"{game.Name}: 100 Caught", $"Catch/register 100 species in {game.Name}.", game.DexCaught, 100, new("5 Great Balls + 3 Super Potions", 1), null, completed, newlyCompleted, [("great-ball", 5L), ("super-potion", 3L)]));

            foreach (var percent in Enumerable.Range(1, 9).Select(x => x * 10))
            {
                var target = Math.Max(1, (int)Math.Ceiling(game.DexTarget * (percent / 100d)));
                var reward = GetDexProgressReward(percent);
                quests.Add(await EvaluateQuest(
                    $"dex-{game.Key}-{percent}pct", $"dex-{game.Key}-{percent}pct", "Pokédex",
                    $"{game.Name}: {percent}% Complete",
                    $"Complete {percent}% of {game.Name}'s applicable Pokédex ({target}/{game.DexTarget}).",
                    game.DexCaught, target, reward.Display, reward.ItemKey, completed, newlyCompleted, reward.Bundle));
            }
"""
if old_game_dex not in text:
    raise RuntimeError("alpha52k1 game dex block missing")
text = text.replace(old_game_dex, "", 1)

old_game_ach = """        // 100% game Pokédex completion is an Achievement. The 10%-90% ladder remains
        // in Quests so normal progression is rewarding without handing out premium loot.
        foreach (var game in gameSnapshots)
        {
            achievements.Add(await EvaluateQuest(
                $"dex-{game.Key}-complete", $"dex-{game.Key}-complete", "Full Pokédex",
                $"{game.Name}: Pokédex Complete",
                $"Complete {game.Name}'s full applicable Pokédex ({game.DexTarget}/{game.DexTarget}).",
                game.DexCaught, game.DexTarget,
                new("Master Ball + Gold Bottle Cap + 5 PP Max + 20 Full Restores + ₽50,000", 1), null,
                completed, newlyCompleted,
                [("master-ball", 1L), ("gold-bottle-cap", 1L), ("pp-max", 5L), ("full-restore", 20L)],
                bonusMoney: 50_000));
        }

"""
if old_game_ach not in text:
    raise RuntimeError("alpha52k1 game achievement block missing")
text = text.replace(old_game_ach, "", 1)

old_species_auto = """        foreach (var species in caughtHistory.Where(LegendarySpecies.ContainsKey).Order())
        {
            var id = LegendaryQuestId(species);
            if (!completed.Add(id))
                continue;

            var name = LegendarySpecies[species];
            var reward = GetLegendaryReward(species);
            await GrantRewardPlan(id, reward);
            newlyCompleted.Add(new(id, $"Legendary Catch: {name}", $"Caught {name} for the first time across PKVault. This completion is now permanent.", reward.Display));
        }

        foreach (var species in caughtHistory.Where(MythicalSpecies.ContainsKey).Order())
        {
            var id = MythicalQuestId(species);
            if (!completed.Add(id))
                continue;

            var name = MythicalSpecies[species];
            var reward = new RewardPlan(new("Master Ball", 1), "master-ball");
            await GrantRewardPlan(id, reward);
            newlyCompleted.Add(new(id, $"Mythical Catch: {name}", $"Caught {name} for the first time across PKVault. Mythical first-catch rewards are Master Balls.", reward.Display));
        }

"""
if old_species_auto not in text:
    raise RuntimeError("alpha52k1 species auto block missing")
text = text.replace(old_species_auto, "", 1)

old_species_cards = """        achievements.AddRange(LegendarySpecies
            .OrderBy(x => x.Key)
            .Select(x =>
            {
                var reward = GetLegendaryReward(x.Key);
                return new QuestEntryDTO(
                    Id: LegendaryQuestId(x.Key),
                    Category: "Legendary",
                    Title: $"Catch {x.Value}",
                    Description: "Catch this Legendary in any supported real save. Most Legendary rewards are Nuggets or 25–50 Ultra Balls; each species can reward only once.",
                    Progress: completed.Contains(LegendaryQuestId(x.Key)) ? 1 : 0,
                    Target: 1,
                    Completed: completed.Contains(LegendaryQuestId(x.Key)),
                    Reward: reward.Display);
            })
            .Concat(MythicalSpecies.OrderBy(x => x.Key).Select(x => new QuestEntryDTO(
                Id: MythicalQuestId(x.Key),
                Category: "Mythical",
                Title: $"Catch {x.Value}",
                Description: "Catch this Mythical in any supported real save. Each unique Mythical awards one Master Ball exactly once across PKVault.",
                Progress: completed.Contains(MythicalQuestId(x.Key)) ? 1 : 0,
                Target: 1,
                Completed: completed.Contains(MythicalQuestId(x.Key)),
                Reward: new("Master Ball", 1)))));
"""
new_species_cards = """        foreach (var species in LegendarySpecies.OrderBy(x => x.Key))
        {
            var id = LegendaryQuestId(species.Key);
            var reward = GetLegendaryReward(species.Key);
            achievements.Add(await EvaluateQuest(
                id, id, "Legendary", $"Catch {species.Value}",
                "Register this Legendary across PKVault, then claim its one-time reward.",
                caughtHistory.Contains(species.Key) ? 1 : 0, 1,
                reward.Display, reward.ItemKey, completed, newlyCompleted, reward.Bundle));
        }

        foreach (var species in MythicalSpecies.OrderBy(x => x.Key))
        {
            var id = MythicalQuestId(species.Key);
            achievements.Add(await EvaluateQuest(
                id, id, "Mythical", $"Catch {species.Value}",
                "Register this Mythical across PKVault, then claim its one-time Master Ball reward.",
                caughtHistory.Contains(species.Key) ? 1 : 0, 1,
                new("Master Ball", 1), "master-ball", completed, newlyCompleted));
        }
"""
text = rep(text, old_species_cards, new_species_cards, "species claim cards")

old_eval = """        var isComplete = completed.Contains(completionId);
        if (!isComplete && progress >= target)
        {
            completed.Add(completionId);

            if (reward.IsMoney)
            {
                await itemBankService.GrantQuestMoneyReward(completionId, reward.Count);
            }
            else if (itemRewards is not null)
            {
                foreach (var grant in itemRewards)
                    await itemBankService.GrantQuestReward(completionId, grant.ItemKey, grant.Count);
            }
            else if (!string.IsNullOrWhiteSpace(rewardItemKey))
            {
                await itemBankService.GrantQuestReward(completionId, rewardItemKey, reward.Count);
            }

            if (bonusMoney > 0 && !reward.IsMoney)
                await itemBankService.GrantQuestMoneyReward(completionId, bonusMoney);

            newlyCompleted.Add(new(
                Id: completionId,
                Title: title,
                Message: description,
                Reward: reward
            ));
            isComplete = true;
        }

        return new(
            Id: displayId,
            Category: category,
            Title: title,
            Description: description,
            Progress: Math.Min(progress, target),
            Target: target,
            Completed: isComplete,
            Reward: reward
        );
"""
new_eval = """        var isClaimed = completed.Contains(completionId);
        var isClaimable = !isClaimed && progress >= target;

        if (isClaimable)
        {
            claimPlans[displayId] = new(
                CompletionId: completionId,
                Title: title,
                Description: description,
                Reward: reward,
                RewardItemKey: rewardItemKey,
                ItemRewards: itemRewards,
                BonusMoney: bonusMoney
            );
        }

        return new(
            Id: displayId,
            Category: category,
            Title: title,
            Description: description,
            Progress: Math.Min(progress, target),
            Target: target,
            Completed: isClaimed,
            Claimable: isClaimable,
            Reward: reward
        );
"""
text = rep(text, old_eval, new_eval, "EvaluateQuest")

text = text.replace(
    "if (newlyCompleted.Count > 0 || correctedCompletionHistory || archivistPokemonRewardChanged)",
    "if (archivistPokemonRewardChanged)",
    1,
)

text = rep(text,
"""        dailyQuests = dailyQuests.Select(x => x with { Completed = completed.Contains(DailyCompletionId(today, x.Id)) }).ToList();
        quests = quests.Select(x => x with { Completed = completed.Contains(x.Id) }).ToList();
        achievements = achievements.Select(x => x with { Completed = completed.Contains(x.Id) }).ToList();
""",
"""        dailyQuests = dailyQuests.Select(x =>
        {
            var claimed = completed.Contains(DailyCompletionId(today, x.Id));
            return x with { Completed = claimed, Claimable = !claimed && x.Progress >= x.Target };
        }).ToList();
        quests = quests.Select(x =>
        {
            var claimed = completed.Contains(x.Id);
            return x with { Completed = claimed, Claimable = !claimed && x.Progress >= x.Target };
        }).ToList();
        achievements = achievements.Select(x =>
        {
            var claimed = completed.Contains(x.Id);
            return x with { Completed = claimed, Claimable = !claimed && x.Progress >= x.Target };
        }).ToList();
""",
"claimable rebuild")

quest_path.write_text(text, encoding="utf-8")

route_path = root / "PKVault.Core/quest/routes/QuestRoute.cs"
route = route_path.read_text(encoding="utf-8")
route = rep(route,
"""    [HttpPost("reroll")]
    public async Task<QuestStateDTO> Reroll(QuestRerollRequest request)
        => await questService.RerollDailyQuest(request.QuestId);
""",
"""    [HttpPost("reroll")]
    public async Task<QuestStateDTO> Reroll(QuestRerollRequest request)
        => await questService.RerollDailyQuest(request.QuestId);

    [HttpPost("claim")]
    public async Task<QuestStateDTO> Claim(QuestClaimRequest request)
        => await questService.ClaimQuest(request.QuestId);
""",
"claim route")
route_path.write_text(route, encoding="utf-8")

json_path = root / "PKVault.Core/router/RouteJsonContext.cs"
json = json_path.read_text(encoding="utf-8")
json = rep(json,
"""[JsonSerializable(typeof(QuestRerollRequest))]
""",
"""[JsonSerializable(typeof(QuestRerollRequest))]
[JsonSerializable(typeof(QuestClaimRequest))]
""",
"json claim request")
json_path.write_text(json, encoding="utf-8")

print("alpha52k1 backend manual claim + regional-only Dex applied")

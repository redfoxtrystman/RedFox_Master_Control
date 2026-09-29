from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve()
q=root/'PKVault.Core/quest/QuestService.cs'
t=q.read_text(encoding='utf-8')

def rep(old,new,label):
    global t
    if old not in t: raise RuntimeError(f'alpha53a2 anchor not found: {label}')
    t=t.replace(old,new,1)

anchor='''        };

        foreach (var game in gameSnapshots)
        {
            var minutes = game.PlaySeconds / 60L;
'''
insert='''        };

        quests.Add(await EvaluateQuest("quest-trainer-battles-10", "quest-trainer-battles-10", "Battles", "Trainer Warm-Up", "Record 10 trainer battles in supported game saves. PKVault keeps the highest observed saved total per game so backup copies do not double-count.", trainerBattleProgress, 10, new("10 Great Balls + 5 Super Potions", 1), null, completed, newlyCompleted, [("great-ball", 10L), ("super-potion", 5L)]));
        quests.Add(await EvaluateQuest("quest-trainer-battles-25", "quest-trainer-battles-25", "Battles", "Route Challenger", "Record 25 trainer battles in supported game saves.", trainerBattleProgress, 25, new("10 Great Balls + 5 Revives + ₽2,500", 1), null, completed, newlyCompleted, [("great-ball", 10L), ("revive", 5L)], bonusMoney: 2_500));
        quests.Add(await EvaluateQuest("quest-trainer-battles-50", "quest-trainer-battles-50", "Battles", "Seasoned Trainer", "Record 50 trainer battles in supported game saves.", trainerBattleProgress, 50, new("15 Ultra Balls + 3 Rare Candies + 5 Full Heals", 1), null, completed, newlyCompleted, [("ultra-ball", 15L), ("rare-candy", 3L), ("full-heal", 5L)]));
        quests.Add(await EvaluateQuest("quest-trainer-battles-100", "quest-trainer-battles-100", "Battles", "Hundred Battles", "Record 100 trainer battles in supported game saves.", trainerBattleProgress, 100, new("25 Ultra Balls + 5 Rare Candies + 5 Full Restores + ₽7,500", 1), null, completed, newlyCompleted, [("ultra-ball", 25L), ("rare-candy", 5L), ("full-restore", 5L)], bonusMoney: 7_500));
        quests.Add(await EvaluateQuest("quest-trainer-battles-250", "quest-trainer-battles-250", "Battles", "Veteran Circuit", "Record 250 trainer battles in supported game saves.", trainerBattleProgress, 250, new("Bottle Cap + 10 Rare Candies + 10 Max Revives + ₽15,000", 1), null, completed, newlyCompleted, [("bottle-cap", 1L), ("rare-candy", 10L), ("max-revive", 10L)], bonusMoney: 15_000));
        quests.Add(await EvaluateQuest("quest-trainer-battles-500", "quest-trainer-battles-500", "Battles", "Battle-Hardened", "Record 500 trainer battles in supported game saves.", trainerBattleProgress, 500, new("Gold Bottle Cap + PP Max + 15 Rare Candies + 10 Full Restores + ₽30,000", 1), null, completed, newlyCompleted, [("gold-bottle-cap", 1L), ("pp-max", 1L), ("rare-candy", 15L), ("full-restore", 10L)], bonusMoney: 30_000));
        quests.Add(await EvaluateQuest("quest-trainer-battles-1000", "quest-trainer-battles-1000", "Battles", "Trainer Battle Legend", "Record 1,000 trainer battles in supported game saves.", trainerBattleProgress, 1000, new("Ability Capsule + Gold Bottle Cap + 3 PP Max + 20 Rare Candies + ₽50,000", 1), null, completed, newlyCompleted, [("ability-capsule", 1L), ("gold-bottle-cap", 1L), ("pp-max", 3L), ("rare-candy", 20L)], bonusMoney: 50_000));

        foreach (var game in gameSnapshots)
        {
            var minutes = game.PlaySeconds / 60L;
'''
rep(anchor,insert,'trainer quest chain')

anchor='''        achievements.Add(await EvaluateQuest("quest-legendary-3", "quest-legendary-3", "Legendary", "Legend Hunter I",'''
insert='''        foreach (var gymKey in gymGamesSeen.Order(StringComparer.Ordinal))
        {
            if (!TryGetGymDefinition(gymKey, out var gym))
                continue;

            var earned = 0;
            for (var badge = 0; badge < gym.Badges.Length; badge++)
            {
                var hasBadge = gymBadgeHistory.Contains(GymBadgeHistoryKey(gym.Key, badge));
                if (hasBadge) earned++;

                var reward = GetGymBadgeReward(badge);
                achievements.Add(await EvaluateQuest(
                    $"gym-{gym.Key}-{badge + 1}", $"gym-{gym.Key}-{badge + 1}", "Gym",
                    $"{gym.Badges[badge]} — {gym.Name}",
                    $"Earn the {gym.Badges[badge]} in {gym.Name}. Badge progress is read from the game save and retained by PKVault once observed.",
                    hasBadge ? 1 : 0, 1,
                    reward.Display, reward.ItemKey, completed, newlyCompleted, reward.Bundle));
            }

            var circuitReward = GetGymCircuitReward(gym.Badges.Length);
            achievements.Add(await EvaluateQuest(
                $"gym-{gym.Key}-circuit", $"gym-{gym.Key}-circuit", "Gym",
                gym.Badges.Length > 8 ? $"{gym.Name} — All 16 Badges" : $"{gym.Name} — Gym Circuit Complete",
                gym.Badges.Length > 8
                    ? $"Earn all {gym.Badges.Length} badges across the full Johto + Kanto circuit in {gym.Name}."
                    : $"Earn all {gym.Badges.Length} Gym Badges in {gym.Name}.",
                earned, gym.Badges.Length,
                circuitReward.Display, circuitReward.ItemKey, completed, newlyCompleted, circuitReward.Bundle));
        }

        achievements.Add(await EvaluateQuest("quest-legendary-3", "quest-legendary-3", "Legendary", "Legend Hunter I",'''
rep(anchor,insert,'gym achievements')
q.write_text(t,encoding='utf-8')
assert 'quest-trainer-battles-1000' in t
assert 'Gym Circuit Complete' in t
print('PASS alpha53a2 trainer battle quests + gym achievement cards')

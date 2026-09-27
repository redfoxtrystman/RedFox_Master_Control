from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52l anchor not found: {label}")
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# Backend: one request claims every requested ready reward under one quest gate.
# The backend rebuilds claim plans from live state and ignores stale IDs.
# ---------------------------------------------------------------------------
quest_path = root / "PKVault.Core/quest/QuestService.cs"
text = quest_path.read_text(encoding="utf-8")

text = rep(
    text,
    """public record QuestRerollRequest(string QuestId);
public record QuestClaimRequest(string QuestId);
public record QuestStateDTO(
""",
    """public record QuestRerollRequest(string QuestId);
public record QuestClaimRequest(string QuestId);
public record QuestClaimAllRequest(IReadOnlyList<string> QuestIds);
public record QuestStateDTO(
""",
    "QuestClaimAllRequest DTO",
)

old_claim = """    public async Task<QuestStateDTO> ClaimQuest(string questId)
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
"""
new_claim = """    public async Task<QuestStateDTO> ClaimQuest(string questId)
        => await ClaimQuests([questId]);

    public async Task<QuestStateDTO> ClaimQuests(IReadOnlyList<string> questIds)
    {
        await QuestGate.WaitAsync();
        try
        {
            var current = await EvaluateCore();
            if (questIds.Count == 0)
                return current;

            var requested = questIds
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .Distinct(StringComparer.Ordinal)
                .ToList();

            if (requested.Count == 0)
                return current;

            var completed = await LoadStringSet(MetaKey.QUEST_COMPLETED);
            var claimedNotifications = new List<QuestCompletionDTO>();

            foreach (var questId in requested)
            {
                if (!claimPlans.TryGetValue(questId, out var plan))
                    continue;
                if (completed.Contains(plan.CompletionId))
                    continue;

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
                claimedNotifications.Add(new(
                    Id: plan.CompletionId,
                    Title: plan.Title,
                    Message: $"Reward claimed: {plan.Description}",
                    Reward: plan.Reward
                ));
            }

            if (claimedNotifications.Count == 0)
                return current;

            // Persist all claimed completion IDs together after rewards are issued.
            // Reward provenance is already idempotent per completion ID, so a crash
            // cannot duplicate item or money rewards on a later retry.
            await SaveStringSet(MetaKey.QUEST_COMPLETED, completed);

            var refreshed = await EvaluateCore();
            return refreshed with
            {
                NewlyCompleted = refreshed.NewlyCompleted
                    .Concat(claimedNotifications)
                    .ToList()
            };
        }
        finally
        {
            QuestGate.Release();
        }
    }
"""
text = rep(text, old_claim, new_claim, "ClaimQuests backend")
quest_path.write_text(text, encoding="utf-8")

route_path = root / "PKVault.Core/quest/routes/QuestRoute.cs"
route = route_path.read_text(encoding="utf-8")
route = rep(
    route,
    """    [HttpPost("claim")]
    public async Task<QuestStateDTO> Claim(QuestClaimRequest request)
        => await questService.ClaimQuest(request.QuestId);
""",
    """    [HttpPost("claim")]
    public async Task<QuestStateDTO> Claim(QuestClaimRequest request)
        => await questService.ClaimQuest(request.QuestId);

    [HttpPost("claim-all")]
    public async Task<QuestStateDTO> ClaimAll(QuestClaimAllRequest request)
        => await questService.ClaimQuests(request.QuestIds);
""",
    "claim-all route",
)
route_path.write_text(route, encoding="utf-8")

json_path = root / "PKVault.Core/router/RouteJsonContext.cs"
json = json_path.read_text(encoding="utf-8")
json = rep(
    json,
    """[JsonSerializable(typeof(QuestClaimRequest))]
""",
    """[JsonSerializable(typeof(QuestClaimRequest))]
[JsonSerializable(typeof(QuestClaimAllRequest))]
""",
    "claim-all JSON context",
)
json_path.write_text(json, encoding="utf-8")

# ---------------------------------------------------------------------------
# Frontend API + UI.
# ---------------------------------------------------------------------------
api_path = root / "frontend/src/quests/quest-api.ts"
api = api_path.read_text(encoding="utf-8")
api += """

export const claimAllQuests = async (questIds: string[]) =>
  (await customInstance<{ data: QuestState; status: number; headers: Headers }>(
    '/api/quest/claim-all',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ questIds }),
    }
  )).data;
"""
api_path.write_text(api, encoding="utf-8")

page_path = root / "frontend/src/quests/quest-page.tsx"
page = page_path.read_text(encoding="utf-8")

page = rep(
    page,
    """import { claimQuest, loadQuestState, rerollDailyQuest, type DailyReroll, type QuestEntry, type QuestReward } from './quest-api';
""",
    """import { claimAllQuests, claimQuest, loadQuestState, rerollDailyQuest, type DailyReroll, type QuestEntry, type QuestReward } from './quest-api';
""",
    "claimAll import",
)

page = rep(
    page,
    """  const claimMutation = useMutation({
    mutationFn: claimQuest,
    onSuccess: data => queryClient.setQueryData(['quest-state'], data),
  });

  const contractQuery = useQuery({
""",
    """  const claimMutation = useMutation({
    mutationFn: claimQuest,
    onSuccess: data => queryClient.setQueryData(['quest-state'], data),
  });
  const claimAllMutation = useMutation({
    mutationFn: claimAllQuests,
    onSuccess: data => queryClient.setQueryData(['quest-state'], data),
  });

  const contractQuery = useQuery({
""",
    "claimAll mutation",
)

page = rep(
    page,
    """  const filteredDailyQuests = dailyQuests;
  const filteredQuests = filterQuests(quests);
  const filteredAchievements = filterQuests(achievements);
""",
    """  const filteredDailyQuests = dailyQuests;
  const filteredQuests = filterQuests(quests);
  const filteredAchievements = filterQuests(achievements);
  const dailyClaimableIds = dailyQuests.filter(quest => quest.claimable).map(quest => quest.id);
  const questClaimableIds = quests.filter(quest => quest.claimable).map(quest => quest.id);
  const achievementClaimableIds = achievements.filter(quest => quest.claimable).map(quest => quest.id);
""",
    "claimable ID lists",
)

page = rep(
    page,
    """  const clearFilters = () => {
    setSearch('');
    setCategory('all');
    setStatus('all');
  };

  const renderFilters = () => <Card withBorder p='sm' style={{ flexShrink: 0 }}>
""",
    """  const clearFilters = () => {
    setSearch('');
    setCategory('all');
    setStatus('all');
  };

  const renderClaimAll = (questIds: string[]) => <Group justify='flex-end'>
    <Button
      color='green'
      disabled={questIds.length === 0}
      loading={claimAllMutation.isPending}
      onClick={() => claimAllMutation.mutate(questIds)}
    >
      Claim All ({questIds.length})
    </Button>
  </Group>;

  const renderFilters = () => <Card withBorder p='sm' style={{ flexShrink: 0 }}>
""",
    "renderClaimAll helper",
)

page = rep(
    page,
    """    {activeTab === 'daily' && <Stack gap='sm'>
      <Text size='sm' c='dimmed'>A save is baselined the first time PKVault sees it, so preloaded Pokémon and existing playtime do not count as activity made today.</Text>
""",
    """    {activeTab === 'daily' && <Stack gap='sm'>
      <Group justify='space-between' align='center'>
        <Text size='sm' c='dimmed'>A save is baselined the first time PKVault sees it, so preloaded Pokémon and existing playtime do not count as activity made today.</Text>
        {renderClaimAll(dailyClaimableIds)}
      </Group>
""",
    "daily claim all",
)

page = rep(
    page,
    """    {activeTab === 'quests' && <Stack gap='sm'>
      {renderFilters()}
      <Text size='sm' c='dimmed'>Permanent progress stays recorded even if the save that originally proved it is removed later. Playtime rewards are deposited into the shared PKVault Pokédollar Bank.</Text>
""",
    """    {activeTab === 'quests' && <Stack gap='sm'>
      <Group justify='space-between' align='center'>
        <Text size='sm' c='dimmed'>Permanent progress stays recorded even if the save that originally proved it is removed later. Playtime rewards are deposited into the shared PKVault Pokédollar Bank.</Text>
        {renderClaimAll(questClaimableIds)}
      </Group>
      {renderFilters()}
""",
    "quests claim all",
)

page = rep(
    page,
    """    {activeTab === 'achievements' && <Stack gap='sm'>
      {renderFilters()}
      <Text fw={700}>Major achievements</Text>
      <Text size='sm' c='dimmed'>Full Pokédex completions, full regional collections, Legendary/Mythical accomplishments, and other major milestones live here. Mythicals award Master Balls; Legendary rewards remain premium one-time rewards.</Text>
""",
    """    {activeTab === 'achievements' && <Stack gap='sm'>
      <Group justify='space-between' align='center'>
        <div>
          <Text fw={700}>Major achievements</Text>
          <Text size='sm' c='dimmed'>Full regional Pokédex collections, Legendary/Mythical accomplishments, and other major milestones live here. Mythicals award Master Balls; Legendary rewards remain premium one-time rewards.</Text>
        </div>
        {renderClaimAll(achievementClaimableIds)}
      </Group>
      {renderFilters()}
""",
    "achievements claim all",
)

page_path.write_text(page, encoding="utf-8")

print("PKVault V8 alpha52l Claim All buttons for Daily / Quests / Achievements applied")

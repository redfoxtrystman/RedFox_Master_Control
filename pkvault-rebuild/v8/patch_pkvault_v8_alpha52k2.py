from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52k2 anchor not found: {label}")
    return text.replace(old, new, 1)

api_path = root / "frontend/src/quests/quest-api.ts"
api = api_path.read_text(encoding="utf-8")
api = rep(api,
"""  completed: boolean;
  reward: QuestReward;
};
""",
"""  completed: boolean;
  claimable: boolean;
  reward: QuestReward;
};
""",
"claimable type")

api += """

export const claimQuest = async (questId: string) =>
  (await customInstance<{ data: QuestState; status: number; headers: Headers }>(
    '/api/quest/claim',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ questId }),
    }
  )).data;
"""
api_path.write_text(api, encoding="utf-8")

page_path = root / "frontend/src/quests/quest-page.tsx"
page = page_path.read_text(encoding="utf-8")

page = rep(page,
"""import { loadQuestState, rerollDailyQuest, type DailyReroll, type QuestEntry, type QuestReward } from './quest-api';
""",
"""import { claimQuest, loadQuestState, rerollDailyQuest, type DailyReroll, type QuestEntry, type QuestReward } from './quest-api';
""",
"claim import")

page = rep(page,
"""  onReroll?: (questId: string) => void;
  rerolling?: boolean;
}> = ({ quest, reroll, onReroll, rerolling }) => <Card
  withBorder
  style={quest.completed ? {
    borderColor: 'var(--mantine-color-green-6)',
    background: 'var(--mantine-color-green-light)',
  } : undefined}
>
""",
"""  onReroll?: (questId: string) => void;
  rerolling?: boolean;
  onClaim?: (questId: string) => void;
  claiming?: boolean;
}> = ({ quest, reroll, onReroll, rerolling, onClaim, claiming }) => <Card
  withBorder
  style={quest.completed ? {
    borderColor: 'var(--mantine-color-green-6)',
    background: 'var(--mantine-color-green-light)',
  } : quest.claimable ? {
    borderColor: 'var(--mantine-color-yellow-6)',
    background: 'var(--mantine-color-yellow-light)',
  } : undefined}
>
""",
"QuestCard props")

page = rep(page,
"""      {quest.completed
        ? <CheckCircle2Icon size={18} color='var(--mantine-color-green-6)' />
        : <CircleIcon size={18} />}
""",
"""      {quest.completed
        ? <CheckCircle2Icon size={18} color='var(--mantine-color-green-6)' />
        : quest.claimable
          ? <Badge color='yellow' variant='filled'>READY TO CLAIM</Badge>
          : <CircleIcon size={18} />}
""",
"claim indicator")

pattern = re.compile(r"\{reroll && onReroll && !quest\.completed && <Button.*?</Button>\}", re.S)
replacement = """<Group gap='xs'>
        {quest.claimable && onClaim && <Button
          size='xs'
          color='green'
          loading={claiming}
          onClick={() => onClaim(quest.id)}
        >
          Claim Reward
        </Button>}
        {reroll && onReroll && !quest.completed && !quest.claimable && <Button
          size='xs'
          variant='light'
          leftSection={<RefreshCwIcon size={14} />}
          loading={rerolling}
          onClick={() => onReroll(quest.id)}
        >
          {reroll.freeRerollAvailable ? 'Reroll — FREE' : 'Reroll — ' + formatMoney(reroll.nextRerollCost)}
        </Button>}
      </Group>"""
page, count = pattern.subn(replacement, page, count=1)
if count != 1:
    raise RuntimeError("alpha52k2 reroll/claim button block not found")

page = rep(page,
"""  onReroll?: (questId: string) => void;
  rerolling?: boolean;
}> = ({ quests, empty, reroll, onReroll, rerolling }) => {
""",
"""  onReroll?: (questId: string) => void;
  rerolling?: boolean;
  onClaim?: (questId: string) => void;
  claiming?: boolean;
}> = ({ quests, empty, reroll, onReroll, rerolling, onClaim, claiming }) => {
""",
"QuestGrid props")

page = rep(page,
"""      onReroll={onReroll}
      rerolling={rerolling}
    />)}
""",
"""      onReroll={onReroll}
      rerolling={rerolling}
      onClaim={onClaim}
      claiming={claiming}
    />)}
""",
"QuestGrid pass claim")

page = rep(page,
"""  const rerollMutation = useMutation({
    mutationFn: rerollDailyQuest,
    onSuccess: data => queryClient.setQueryData(['quest-state'], data),
  });

  const contractQuery = useQuery({
""",
"""  const rerollMutation = useMutation({
    mutationFn: rerollDailyQuest,
    onSuccess: data => queryClient.setQueryData(['quest-state'], data),
  });
  const claimMutation = useMutation({
    mutationFn: claimQuest,
    onSuccess: data => queryClient.setQueryData(['quest-state'], data),
  });

  const contractQuery = useQuery({
""",
"claim mutation")

page = rep(page,
"""    const matchesStatus = status === 'all'
      || (status === 'completed' && quest.completed)
      || (status === 'incomplete' && !quest.completed);
""",
"""    const matchesStatus = status === 'all'
      || (status === 'completed' && quest.completed)
      || (status === 'claimable' && quest.claimable)
      || (status === 'incomplete' && !quest.completed && !quest.claimable);
""",
"claimable status filter")

page = rep(page,
"""            ['all', 'All'],
            ['incomplete', 'Incomplete'],
            ['completed', 'Completed'],
""",
"""            ['all', 'All'],
            ['incomplete', 'Incomplete'],
            ['claimable', 'Ready to Claim'],
            ['completed', 'Claimed'],
""",
"status buttons")

page = rep(page,
"""        onReroll={questId => rerollMutation.mutate(questId)}
        rerolling={rerollMutation.isPending}
      />
""",
"""        onReroll={questId => rerollMutation.mutate(questId)}
        rerolling={rerollMutation.isPending}
        onClaim={questId => claimMutation.mutate(questId)}
        claiming={claimMutation.isPending}
      />
""",
"daily claim wiring")

page = rep(page,
"""      <QuestGrid quests={filteredQuests} empty={filtersActive ? 'No quests match the current filters.' : 'No permanent quests are available.'} />
""",
"""      <QuestGrid
        quests={filteredQuests}
        empty={filtersActive ? 'No quests match the current filters.' : 'No permanent quests are available.'}
        onClaim={questId => claimMutation.mutate(questId)}
        claiming={claimMutation.isPending}
      />
""",
"quest claim wiring")

page = rep(page,
"""      <QuestGrid quests={filteredAchievements} empty={filtersActive ? 'No achievements match the current filters.' : 'No achievements are available.'} />
""",
"""      <QuestGrid
        quests={filteredAchievements}
        empty={filtersActive ? 'No achievements match the current filters.' : 'No achievements are available.'}
        onClaim={questId => claimMutation.mutate(questId)}
        claiming={claimMutation.isPending}
      />
""",
"achievement claim wiring")

page_path.write_text(page, encoding="utf-8")
print("alpha52k2 frontend quest claim UI applied")

from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
route = root / "frontend/src/routes/quests.tsx"
route.parent.mkdir(parents=True, exist_ok=True)
route.write_text("""import { createFileRoute } from '@tanstack/react-router';
import { QuestPage } from '../quests/quest-page';

export const Route = createFileRoute('/quests')({
    component: QuestPage,
});
""", encoding="utf-8")

print("PKVault V8 alpha40b quest route registered")

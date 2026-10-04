from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()


def rep(path: str, old: str, new: str, label: str):
    p = root / path
    text = p.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            print(f"ALREADY {path}: {label}")
            return
        raise RuntimeError(f"alpha53n anchor not found: {label} in {path}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"PATCHED {path}: {label}")


def insert_before(path: str, marker: str, insertion: str, label: str):
    p = root / path
    text = p.read_text(encoding="utf-8")
    if insertion in text:
        print(f"ALREADY {path}: {label}")
        return
    if marker not in text:
        raise RuntimeError(f"alpha53n marker not found: {label} in {path}")
    p.write_text(text.replace(marker, insertion + marker, 1), encoding="utf-8")
    print(f"PATCHED {path}: {label}")

# ---------------------------------------------------------------------------
# Permanent per-game shiny history.  This is appended as a new MetaKey so no
# persisted numeric IDs move for existing users.
# ---------------------------------------------------------------------------
rep(
    "PKVault.Core/db/entity/MetaEntity.cs",
    '''    QUEST_GYM_GAMES_SEEN = 27,\n}''',
    '''    QUEST_GYM_GAMES_SEEN = 27,\n    QUEST_SHINY_GAME_IDENTITIES = 28,\n}''',
    "per-game shiny history meta key",
)

quest = "PKVault.Core/quest/QuestService.cs"

rep(
    quest,
    '''    private const string ApricornUnlockProgressionKey = "shop.apricorn.unlocked";\n''',
    '''    private const string ApricornUnlockProgressionKey = "shop.apricorn.unlocked";\n\n    private sealed record PrestigePokemonRewardDefinition(\n        string CompletionId,\n        string MarkerId,\n        string VariantId,\n        ushort Species,\n        string Name\n    );\n\n    private static readonly PrestigePokemonRewardDefinition[] PrestigePokemonRewards =\n    [\n        new("region-kanto-complete", "reward-prestige-celebi", "9be20a53-f28b-4c0c-8c49-801000000002", (ushort)Species.Celebi, "Lv. 50 Celebi"),\n        new("prestige-lgpe-meltan", "reward-prestige-meltan", "9be20a53-f28b-4c0c-8c49-801000000003", (ushort)Species.Meltan, "Shiny Meltan Lv. 50"),\n        new("region-sinnoh-complete", "reward-prestige-manaphy", "9be20a53-f28b-4c0c-8c49-801000000004", (ushort)Species.Manaphy, "Shiny Manaphy Lv. 50"),\n        new("region-unova-complete", "reward-prestige-keldeo", "9be20a53-f28b-4c0c-8c49-801000000005", (ushort)Species.Keldeo, "Shiny Keldeo Lv. 50"),\n        new("prestige-unova-meloetta", "reward-prestige-meloetta", "9be20a53-f28b-4c0c-8c49-801000000006", (ushort)Species.Meloetta, "Shiny Meloetta Lv. 50"),\n        new("prestige-kalos-volcanion", "reward-prestige-volcanion", "9be20a53-f28b-4c0c-8c49-801000000007", (ushort)Species.Volcanion, "Shiny Volcanion Lv. 50"),\n        new("prestige-hisui-enamorus", "reward-prestige-enamorus", "9be20a53-f28b-4c0c-8c49-801000000008", (ushort)Species.Enamorus, "Shiny Enamorus Lv. 50"),\n    ];\n''',
    "prestige reward definitions",
)

rep(
    quest,
    '''    private sealed record RewardPlan(QuestRewardDTO Display, string? ItemKey, IReadOnlyList<(string ItemKey, long Count)>? Bundle = null);\n''',
    '''    private sealed record RewardPlan(QuestRewardDTO Display, string? ItemKey, IReadOnlyList<(string ItemKey, long Count)>? Bundle = null);\n    private sealed record GameDexProgress(int Caught, int Target);\n''',
    "game dex progress record",
)

rep(
    quest,
    '''        var shinySpeciesHistory = await LoadSpeciesSet(MetaKey.QUEST_SHINY_SPECIES);\n        var unownForms = await LoadStringSet(MetaKey.QUEST_UNOWN_FORMS);\n''',
    '''        var shinySpeciesHistory = await LoadSpeciesSet(MetaKey.QUEST_SHINY_SPECIES);\n        var shinyGameIdentities = await LoadStringSet(MetaKey.QUEST_SHINY_GAME_IDENTITIES);\n        var unownForms = await LoadStringSet(MetaKey.QUEST_UNOWN_FORMS);\n''',
    "load per-game shiny history",
)

rep(
    quest,
    '''        var shinySpeciesChanged = false;\n        var unownFormsChanged = false;\n''',
    '''        var shinySpeciesChanged = false;\n        var shinyGameIdentitiesChanged = false;\n        var unownFormsChanged = false;\n''',
    "per-game shiny change flag",
)

rep(
    quest,
    '''        foreach (var loader in realLoaders)\n        {\n            var saveKey = GetSaveStateKey(loader.Save);\n            var dtos = loader.Pkms.GetAllDtos();\n''',
    '''        foreach (var loader in realLoaders)\n        {\n            var saveKey = GetSaveStateKey(loader.Save);\n            var prestigeShinyGameKey = GetPrestigeShinyGameKey(loader.Save);\n            var dtos = loader.Pkms.GetAllDtos();\n''',
    "resolve shiny game key per save",
)

rep(
    quest,
    '''                else if (dto.IsShiny && species > 0 && shinySpeciesHistory.Add(species))\n                {\n                    shinySpeciesChanged = true;\n                }\n            }\n''',
    '''                else if (dto.IsShiny && species > 0 && shinySpeciesHistory.Add(species))\n                {\n                    shinySpeciesChanged = true;\n                }\n\n                // Prestige shiny challenges count only Pokémon that originate in\n                // the relevant game family and match the trainer identity of the\n                // save proving the catch. Imported shinies therefore cannot pad a\n                // Let's Go / Unova / Kalos / Hisui challenge. Progress is permanent.\n                if (dto.IsShiny\n                    && prestigeShinyGameKey is not null\n                    && IsNativePrestigeShiny(dto, loader.Save, prestigeShinyGameKey)\n                    && shinyGameIdentities.Add($"{prestigeShinyGameKey}|{identity}"))\n                {\n                    shinyGameIdentitiesChanged = true;\n                }\n            }\n''',
    "record native per-game shinies",
)

rep(
    quest,
    '''        if (shinySpeciesChanged)\n            await SaveSpeciesSet(MetaKey.QUEST_SHINY_SPECIES, shinySpeciesHistory);\n        if (unownFormsChanged)\n''',
    '''        if (shinySpeciesChanged)\n            await SaveSpeciesSet(MetaKey.QUEST_SHINY_SPECIES, shinySpeciesHistory);\n        if (shinyGameIdentitiesChanged)\n            await SaveStringSet(MetaKey.QUEST_SHINY_GAME_IDENTITIES, shinyGameIdentities);\n        if (unownFormsChanged)\n''',
    "persist per-game shiny history",
)

# Regional-origin dexes are collection achievements, not event distributions.
# Mythicals are excluded from both totals and progress so the reward itself can
# never be a circular requirement.
rep(
    quest,
    '''            var regionTotal = region.EndSpecies - region.StartSpecies + 1;\n            var regionCaught = CountCaughtInRange(caughtHistory, region.StartSpecies, region.EndSpecies);\n''',
    '''            var regionTotal = CountRequiredSpeciesInRange(region.StartSpecies, region.EndSpecies);\n            var regionCaught = CountCaughtInRange(caughtHistory, region.StartSpecies, region.EndSpecies);\n''',
    "exclude mythicals from regional totals",
)

rep(
    quest,
    '''                    $"Register {percent}% of the species originally introduced in {region.Name} ({target}/{regionTotal}).",\n''',
    '''                    $"Register {percent}% of the non-Mythical species originally introduced in {region.Name} ({target}/{regionTotal}).",\n''',
    "regional progress description",
)

# Replace the regional completion block so Kanto is explicitly global and the
# first-debut prestige rewards are visible on the completion cards.
rep(
    quest,
    '''        foreach (var entry in regionProgress)\n        {\n            achievements.Add(await EvaluateQuest(\n                $"region-{entry.Region.Key}-complete", $"region-{entry.Region.Key}-complete", "Regional Dex",\n                $"{entry.Region.Name} Origin Dex Complete",\n                $"Register every official species originally introduced in {entry.Region.Name} ({entry.Total}/{entry.Total}).",\n                entry.Caught, entry.Total,\n                new("Master Ball + Gold Bottle Cap + 10 Max Revives + ₽30,000", 1), null,\n                completed, newlyCompleted,\n                [("master-ball", 1L), ("gold-bottle-cap", 1L), ("max-revive", 10L)],\n                bonusMoney: 30_000));\n        }\n''',
    '''        foreach (var entry in regionProgress)\n        {\n            var completionId = $"region-{entry.Region.Key}-complete";\n            var title = entry.Region.Key == "kanto"\n                ? "Global Kanto Dex Complete"\n                : $"{entry.Region.Name} Origin Dex Complete";\n            var description = entry.Region.Key == "kanto"\n                ? $"Register every non-Mythical Kanto species across PKVault ({entry.Total}/{entry.Total}). Any supported game can contribute."\n                : $"Register every non-Mythical species originally introduced in {entry.Region.Name} ({entry.Tota
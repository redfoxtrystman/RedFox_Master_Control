from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52f anti-reuse anchor not found: {label}")
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# Contracts: remember every local PKVault Pokémon identity as already-owned.
# Save Pokémon are processed FIRST so a genuinely new catch can still count on
# the same evaluation where PKVault mirrors it. Vault identities are then added
# silently to permanent history, so moving an old vault Pokémon into a save can
# never become a fake catch later.
# ---------------------------------------------------------------------------
contract_path = root / "PKVault.Core/contract/ContractService.cs"
contract = contract_path.read_text(encoding="utf-8")

contract = replace_once(
    contract,
    """public class ContractService(
    ISavesLoadersService savesLoadersService,
    IMetaLoader metaLoader,
    ItemBankService itemBankService
)
""",
    """public class ContractService(
    ISavesLoadersService savesLoadersService,
    IMetaLoader metaLoader,
    ItemBankService itemBankService,
    IPkmVariantLoader pkmVariantLoader
)
""",
    "ContractService pkmVariantLoader dependency",
)

contract = replace_once(
    contract,
    """        if (!state.Ready)
        {
            foreach (var pair in current)
                state.Pokemon[pair.Key] = pair.Value;
            state.Ready = true;
            return;
        }
""",
    """        if (!state.Ready)
        {
            foreach (var pair in current)
                state.Pokemon[pair.Key] = pair.Value;
            await RememberVaultPokemon(state);
            state.Ready = true;
            return;
        }
""",
    "contract first-run vault baseline",
)

contract = replace_once(
    contract,
    """            state.Pokemon[id] = snapshot;
        }
    }

    private long GetMetricBaseline""",
    """            state.Pokemon[id] = snapshot;
        }

        // Do this after save-event detection. An old Pokémon that already lives in
        // PKVault becomes permanently known without earning catch credit. A real new
        // catch seen in a save first still earns exactly one event.
        await RememberVaultPokemon(state);
    }

    private async Task RememberVaultPokemon(TrackerState state)
    {
        foreach (var dto in await pkmVariantLoader.GetAllDtos())
        {
            if (dto.IsExternal || !dto.IsEnabled)
                continue;

            var identity = StableId(GetPkmIdentity(dto), 32);
            if (state.Pokemon.ContainsKey(identity))
                continue;

            state.Pokemon[identity] = new(
                GetOfficialSpecies(dto),
                Math.Max(1, (int)dto.Level),
                dto.IsShiny
            );
        }
    }

    private long GetMetricBaseline""",
    "contract persistent vault identity memory",
)

contract = replace_once(
    contract,
    "private static string GetPkmIdentity(PkmSaveDTO dto)",
    "private static string GetPkmIdentity(PkmBaseDTO dto)",
    "contract common identity DTO",
)
contract = replace_once(
    contract,
    "private static ushort GetOfficialSpecies(PkmSaveDTO dto)",
    "private static ushort GetOfficialSpecies(PkmBaseDTO dto)",
    "contract common species DTO",
)

contract_path.write_text(contract, encoding="utf-8")

# ---------------------------------------------------------------------------
# Quests: same protection for the existing daily/achievement catch tracker.
# Seed local PKVault identities silently AFTER live-save event detection. Also
# store their level/species/shiny baseline so moving them into a save cannot
# create fake training/evolution/shiny progress either.
# ---------------------------------------------------------------------------
quest_path = root / "PKVault.Core/quest/QuestService.cs"
quest = quest_path.read_text(encoding="utf-8")

quest = replace_once(
    quest,
    """        if (!identityReady)
            await SaveMetaValue(MetaKey.QUEST_PKM_IDENTITIES_READY, "1");
""",
    """        // Treat Pokémon already stored in local PKVault as previously owned.
        // This is intentionally after save scanning: a genuine new in-game catch can
        // still be detected first, while an old vault Pokémon can never be recycled
        // into a save to satisfy Catch/Shiny/Training/Evolution objectives.
        foreach (var dto in await pkmVariantLoader.GetAllDtos())
        {
            if (dto.IsExternal || !dto.IsEnabled)
                continue;

            var identity = GetPkmIdentity(dto);
            var species = GetOfficialSpecies(dto);
            var level = Math.Max(1, (int)dto.Level);

            if (knownIdentities.Add(identity))
                identitiesChanged = true;

            if (!pkmLevels.TryGetValue(identity, out var vaultLevel) || vaultLevel != level)
            {
                pkmLevels[identity] = level;
                levelsChanged = true;
            }

            if (species > 0 && (!pkmSpecies.TryGetValue(identity, out var vaultSpecies) || vaultSpecies != species))
            {
                pkmSpecies[identity] = species;
                pkmSpeciesChanged = true;
            }

            if (dto.IsShiny && shinyIdentities.Add(identity))
                shinyIdentitiesChanged = true;
            if (dto.IsShiny && species > 0 && shinySpeciesHistory.Add(species))
                shinySpeciesChanged = true;
        }

        if (!identityReady)
            await SaveMetaValue(MetaKey.QUEST_PKM_IDENTITIES_READY, "1");
""",
    "quest vault anti-reuse baseline",
)

quest = replace_once(
    quest,
    "private static string GetPkmIdentity(PkmSaveDTO dto)",
    "private static string GetPkmIdentity(PkmBaseDTO dto)",
    "quest common identity DTO",
)
quest = replace_once(
    quest,
    "private static ushort GetOfficialSpecies(PkmSaveDTO dto)",
    "private static ushort GetOfficialSpecies(PkmBaseDTO dto)",
    "quest common species DTO",
)

quest_path.write_text(quest, encoding="utf-8")

print("PKVault V8 alpha52f permanent Pokémon identity anti-reuse protection applied to Quests + Contracts")

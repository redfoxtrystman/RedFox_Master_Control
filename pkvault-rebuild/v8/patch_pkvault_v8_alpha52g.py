from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52g identity/history anchor not found: {label}")
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# Quests: permanent collection progress and repeatable-event progress are
# intentionally separate.
#
# - Vault species/forms/shinies DO count toward permanent collection history.
# - Vault identities are silently remembered so moving an old vault Pokemon
#   into a save never creates a fake daily/repeatable catch.
# - Only first-seen identities discovered in a real save increment daily events.
# ---------------------------------------------------------------------------
quest_path = root / "PKVault.Core/quest/QuestService.cs"
quest = quest_path.read_text(encoding="utf-8")

quest = replace_once(
    quest,
    """        var playtimeChanged = false;

        var realLoaders = GetRealLoaders();
""",
    """        var playtimeChanged = false;
        var vaultCaughtSpecies = new HashSet<ushort>();

        var realLoaders = GetRealLoaders();
""",
    "quest vault species staging set",
)

quest = replace_once(
    quest,
    """            var identity = GetPkmIdentity(dto);
            var species = GetOfficialSpecies(dto);
            var level = Math.Max(1, (int)dto.Level);

            if (knownIdentities.Add(identity))
""",
    """            var identity = GetPkmIdentity(dto);
            var species = GetOfficialSpecies(dto);
            var level = Math.Max(1, (int)dto.Level);

            // Permanent unlock/collection progress is ownership/history based.
            // Existing Pokemon in PKVault count even if they predate this build.
            if (species > 0)
                vaultCaughtSpecies.Add(species);
            if (species == 201 && dto.Form <= 27 && unownForms.Add(dto.Form.ToString(CultureInfo.InvariantCulture)))
                unownFormsChanged = true;

            // Repeatable event progress is identity based. Merely owning/moving
            // this Pokemon does not award a new catch.
            if (knownIdentities.Add(identity))
""",
    "quest split permanent history from repeatable identity",
)

quest = replace_once(
    quest,
    """        var currentCaught = GetCurrentlyCaughtSpecies(realLoaders);
        var historyChanged = false;
        foreach (var species in currentCaught)
        {
            if (caughtHistory.Add(species))
                historyChanged = true;
        }
""",
    """        var currentCaught = GetCurrentlyCaughtSpecies(realLoaders);
        var historyChanged = false;

        // Permanent progress is the union of species registered by real saves and
        // species physically owned in PKVault storage. This lets an existing Gen-1
        // collection satisfy permanent Kanto/collection unlocks immediately.
        foreach (var species in currentCaught.Concat(vaultCaughtSpecies))
        {
            if (caughtHistory.Add(species))
                historyChanged = true;
        }
""",
    "quest permanent storage species history union",
)

quest = replace_once(
    quest,
    """    private static string GetPkmIdentity(PkmBaseDTO dto)
    {
        var pkm = dto.Pkm.GetMutablePkm();
        if (pkm is GBPKM gb)
        {
            return string.Join('|', "gb-id", dto.TID, dto.OriginTrainerName, gb.DV16.ToString("X4", CultureInfo.InvariantCulture));
        }

        if (pkm is PKEssentials essentials)
        {
            return string.Join('|', "ess-id", essentials.ProfileId, dto.TID, dto.SID ?? 0, dto.OriginTrainerName, dto.PID.ToString("X8", CultureInfo.InvariantCulture));
        }

        return string.Join('|', "pk-id", dto.TID, dto.SID ?? 0, dto.OriginTrainerName, dto.PID.ToString("X8", CultureInfo.InvariantCulture));
    }
""",
    """    private static string GetPkmIdentity(PkmBaseDTO dto)
    {
        var pkm = dto.Pkm.GetMutablePkm();

        // Essentials local species IDs can change on evolution, so keep its
        // species-independent personal identity. For normal formats use PKVault's
        // own IdBase, which is designed to survive box moves and evolutions.
        if (pkm is PKEssentials essentials)
            return string.Join('|', "ess-id", essentials.ProfileId, dto.TID, dto.SID ?? 0, dto.OriginTrainerName, dto.PID.ToString("X8", CultureInfo.InvariantCulture));

        return dto.IdBase;
    }
""",
    "quest use PKVault stable identity",
)

quest_path.write_text(quest, encoding="utf-8")

# Contracts use the same stable identity rule. Their metric baseline at purchase
# still decides which genuinely new post-purchase events count toward progress.
contract_path = root / "PKVault.Core/contract/ContractService.cs"
contract = contract_path.read_text(encoding="utf-8")

contract = replace_once(
    contract,
    """    private static string GetPkmIdentity(PkmBaseDTO dto)
    {
        var pkm = dto.Pkm.GetMutablePkm();
        if (pkm is GBPKM gb)
            return string.Join('|', "gb-id", dto.TID, dto.OriginTrainerName, gb.DV16.ToString("X4", CultureInfo.InvariantCulture));
        if (pkm is PKEssentials essentials)
            return string.Join('|', "ess-id", essentials.ProfileId, dto.TID, dto.SID ?? 0, dto.OriginTrainerName, dto.PID.ToString("X8", CultureInfo.InvariantCulture));
        return string.Join('|', "pk-id", dto.TID, dto.SID ?? 0, dto.OriginTrainerName, dto.PID.ToString("X8", CultureInfo.InvariantCulture));
    }
""",
    """    private static string GetPkmIdentity(PkmBaseDTO dto)
    {
        var pkm = dto.Pkm.GetMutablePkm();
        if (pkm is PKEssentials essentials)
            return string.Join('|', "ess-id", essentials.ProfileId, dto.TID, dto.SID ?? 0, dto.OriginTrainerName, dto.PID.ToString("X8", CultureInfo.InvariantCulture));

        return dto.IdBase;
    }
""",
    "contract use PKVault stable identity",
)

contract_path.write_text(contract, encoding="utf-8")

print("PKVault V8 alpha52g split permanent collection history from repeatable fresh-catch identity tracking")

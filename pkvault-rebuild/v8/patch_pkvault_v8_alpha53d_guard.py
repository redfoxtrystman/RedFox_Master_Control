from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

replacement = '''    private static string GetPkmIdentity(PkmBaseDTO dto)
    {
        var pkm = dto.Pkm.GetMutablePkm();
        if (pkm is PKEssentials essentials)
            return string.Join('|', "ess-id", essentials.ProfileId, dto.TID, dto.SID ?? 0, dto.OriginTrainerName, dto.PID.ToString("X8", CultureInfo.InvariantCulture));

        return dto.IdBase;
    }
'''

for rel in (
    "PKVault.Core/quest/QuestService.cs",
    "PKVault.Core/contract/ContractService.cs",
):
    path = root / rel
    text = path.read_text(encoding="utf-8")
    old = "    private static string GetPkmIdentity(PkmBaseDTO dto) => ProgressionPkmIdentity.Get(dto);\n"
    if old not in text:
        if replacement in text:
            continue
        raise RuntimeError(f"alpha53d identity guard anchor missing: {rel}")
    path.write_text(text.replace(old, replacement, 1), encoding="utf-8")

print("PASS alpha53d progression identity guard compatibility")

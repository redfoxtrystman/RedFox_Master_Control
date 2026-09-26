from pathlib import Path
import csv
import json
import re
import unicodedata
import sys

root = Path(sys.argv[1]).resolve()
source = Path(__file__).with_name("data") / "uranium-items-pinned.txt"
target = root / "PKVault.Core/romhacks/essentials/EssentialsItemProfile.Generated.cs"

def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower().replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")

rows = []
with source.open("r", encoding="utf-8-sig", newline="") as fh:
    for row in csv.reader(fh):
        if not row or row[0].lstrip().startswith("#"):
            continue
        try:
            item_id = int(row[0])
        except (ValueError, IndexError):
            continue
        if item_id <= 0 or len(row) < 5:
            continue
        name = row[2].strip() or row[1].strip() or f"Item #{item_id}"
        try:
            pocket = int(row[4])
        except ValueError:
            pocket = 1
        rows.append((item_id, name, pocket, slug(name)))

if len(rows) < 500:
    raise SystemExit(f"Expected a full Uranium item database, parsed only {len(rows)} rows")

entries = "\n".join(
    f"        [{item_id}] = new({item_id}, {json.dumps(name, ensure_ascii=False)}, {pocket}, {json.dumps(key, ensure_ascii=False)}),"
    for item_id, name, pocket, key in rows
)

target.write_text(f"""namespace PKVault.Core;

public sealed record EssentialsItemDefinition(
    int Id,
    string Name,
    int Pocket,
    string KeyHint
);

public static class EssentialsItemProfile
{{
    public const int InsurgenceSharedBaseMaxId = 525;

    private static readonly IReadOnlyDictionary<int, EssentialsItemDefinition> Uranium =
        new Dictionary<int, EssentialsItemDefinition>
    {{
{entries}
    }};

    public static EssentialsItemDefinition? Get(string profileId, int itemId)
    {{
        if (string.Equals(profileId, "pokemon-uranium", StringComparison.Ordinal))
            return Uranium.GetValueOrDefault(itemId);

        if (string.Equals(profileId, "pokemon-insurgence", StringComparison.Ordinal)
            && itemId <= InsurgenceSharedBaseMaxId)
            return Uranium.GetValueOrDefault(itemId);

        return null;
    }}

    public static IEnumerable<EssentialsItemDefinition> GetAll(string profileId)
    {{
        if (string.Equals(profileId, "pokemon-uranium", StringComparison.Ordinal))
            return Uranium.Values;

        if (string.Equals(profileId, "pokemon-insurgence", StringComparison.Ordinal))
            return Uranium.Values.Where(x => x.Id <= InsurgenceSharedBaseMaxId);

        return [];
    }}
}}
""", encoding="utf-8")

print(f"Generated {len(rows)} Uranium item definitions -> {target}")

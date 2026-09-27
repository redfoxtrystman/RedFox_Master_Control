from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52j anchor not found: {label}")
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# 1) Main-db lock fix
#
# Direct SQLite connections to pkvault.db must not use pooling. A disposed
# pooled Microsoft.Data.Sqlite connection can keep the Windows file handle
# alive, which breaks BackupService.ReadBytes when Save creates its backup.
# ---------------------------------------------------------------------------
for rel in [
    "PKVault.Core/quest/QuestService.cs",
    "PKVault.Core/contract/ContractService.cs",
    "PKVault.Core/storage/services/ItemBankService.cs",
]:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '$"Data Source={sessionService.MainDbPath};Mode=ReadOnly"',
        '$"Data Source={sessionService.MainDbPath};Mode=ReadOnly;Pooling=False"'
    )
    text = text.replace(
        '$"Data Source={sessionService.MainDbPath}"',
        '$"Data Source={sessionService.MainDbPath};Pooling=False"'
    )
    path.write_text(text, encoding="utf-8")

backup_path = root / "PKVault.Core/backup/services/BackupService.cs"
backup = backup_path.read_text(encoding="utf-8")
if "using Microsoft.Data.Sqlite;" not in backup:
    backup = rep(
        backup,
        "using System.Text.Json;\n",
        "using System.Text.Json;\nusing Microsoft.Data.Sqlite;\n",
        "BackupService Sqlite import",
    )

backup = rep(
    backup,
    """        var rawDbFilepath = sessionService.MainDbRelativePath;
        var dbFilepath = sessionService.MainDbPath;
        if (fileIOService.Exists(dbFilepath))
        {
""",
    """        var rawDbFilepath = sessionService.MainDbRelativePath;
        var dbFilepath = sessionService.MainDbPath;
        if (fileIOService.Exists(dbFilepath))
        {
            // Alpha52j: our Shop/Quest/Contract services directly access the
            // committed DB. Clear any idle SQLite pools before reading the raw
            // database for a backup so Windows cannot report pkvault.db in-use.
            SqliteConnection.ClearAllPools();
""",
    "BackupService pool clear",
)
backup_path.write_text(backup, encoding="utf-8")

# ---------------------------------------------------------------------------
# 2) Valuable/treasure items
#
# These are intentionally SELL ONLY. They are the classic Pokémon money items;
# buying them back from PKVault would turn the Shop into a pointless money loop.
# Values use their normal Poké Mart sell values rather than special NPC/maniac
# bonus prices.
# ---------------------------------------------------------------------------
shop_path = root / "PKVault.Core/shop/ShopService.cs"
shop = shop_path.read_text(encoding="utf-8")
shop = rep(
    shop,
    """        new("pp-up", "Utilities", 9800, 4900),

        new("fire-stone", "Evolution Items", 3000, 1500),
""",
    """        new("pp-up", "Utilities", 9800, 4900),

        // Classic sell-for-cash treasure items. Sell-only by design.
        new("nugget", "Valuables", 0, 5000, false, true),
        new("big-nugget", "Valuables", 0, 20000, false, true),
        new("tiny-mushroom", "Valuables", 0, 250, false, true),
        new("big-mushroom", "Valuables", 0, 2500, false, true),
        new("balm-mushroom", "Valuables", 0, 7500, false, true),
        new("pearl", "Valuables", 0, 1000, false, true),
        new("big-pearl", "Valuables", 0, 4000, false, true),
        new("pearl-string", "Valuables", 0, 10000, false, true),
        new("stardust", "Valuables", 0, 1500, false, true),
        new("star-piece", "Valuables", 0, 6000, false, true),
        new("comet-shard", "Valuables", 0, 12500, false, true),
        new("rare-bone", "Valuables", 0, 2500, false, true),
        new("pretty-wing", "Valuables", 0, 500, false, true, "pretty feather"),
        new("slowpoke-tail", "Valuables", 0, 4900, false, true),
        new("gold-leaf", "Valuables", 0, 500, false, true),
        new("silver-leaf", "Valuables", 0, 500, false, true),

        new("fire-stone", "Evolution Items", 3000, 1500),
""",
    "valuable item catalog",
)
shop_path.write_text(shop, encoding="utf-8")

page_path = root / "frontend/src/shop/shop-page.tsx"
page = page_path.read_text(encoding="utf-8")
page = rep(
    page,
    """    'Utilities': 'escape-rope',
    'Key Items': 'coin-case',
""",
    """    'Utilities': 'escape-rope',
    'Valuables': 'nugget',
    'Key Items': 'coin-case',
""",
    "Valuables category icon",
)
page = rep(
    page,
    """        'Stones', 'TMs', 'Utilities', 'Key Items', 'Evolution Items',
""",
    """        'Stones', 'TMs', 'Utilities', 'Valuables', 'Key Items', 'Evolution Items',
""",
    "Valuables category ordering",
)
page_path.write_text(page, encoding="utf-8")

print("PKVault V8 alpha52j main DB lock fix + sell-only valuables applied")

from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

controller = root / "PKVault.Core" / "shop" / "ShopController.cs"
text = controller.read_text(encoding="utf-8")
old = "[FromBody] "
if old not in text:
    raise RuntimeError("alpha51b expected ShopController FromBody markers were not found")
controller.write_text(text.replace(old, ""), encoding="utf-8")

bank = root / "PKVault.Core" / "storage" / "services" / "ItemBankService.cs"
text = bank.read_text(encoding="utf-8")
old = "await using var transaction = await connection.BeginTransactionAsync();"
new = "await using var transaction = connection.BeginTransaction();"
if old not in text:
    raise RuntimeError("alpha51b expected async SQLite transaction marker was not found")
bank.write_text(text.replace(old, new, 1), encoding="utf-8")

print("PKVault V8 alpha51b Shop compile fixes applied")

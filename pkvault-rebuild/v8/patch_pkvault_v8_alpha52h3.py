from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
q = root / "PKVault.Core/storage/services/ItemBankService.cs"
text = q.read_text(encoding="utf-8")

old = """    public async Task<long> ApplyContractMoneyDelta(long moneyDelta)
    {
"""
new = """    public Task<long> ApplyContractMoneyDelta(long moneyDelta)
        => ApplyProgressionMoneyDelta(moneyDelta);

    public async Task<long> ApplyProgressionMoneyDelta(long moneyDelta)
    {
"""

if old not in text:
    raise RuntimeError("alpha52h3 progression money anchor not found")

q.write_text(text.replace(old, new, 1), encoding="utf-8")
print("alpha52h3 progression money persistence applied")

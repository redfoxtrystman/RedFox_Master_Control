from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "PKVault.Core/Program.cs"
text = path.read_text(encoding="utf-8")

old = """        services.AddScoped<QuestController>();
        services.AddScoped<ShopController>();
"""
new = """        services.AddScoped<QuestController>();
        services.AddScoped<ShopController>();
        services.AddScoped<ContractController>();
"""

if old not in text:
    raise RuntimeError("alpha52c ContractController DI anchor not found")

path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("PKVault V8 alpha52c ContractController DI registration applied")

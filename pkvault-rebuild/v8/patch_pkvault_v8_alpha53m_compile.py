from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "PKVault.Core/shop/EvolutionItemShopService.cs"
text = path.read_text(encoding="utf-8")

if "using PKHeX.Core;" not in text:
    text = "using PKHeX.Core;\n\n" + text

old = ".Select(version => (int)version.Generation)"
new = ".Select(version => (int)((GameVersion)version).Generation)"
if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise RuntimeError("alpha53m compile fix generation anchor missing")

path.write_text(text, encoding="utf-8")
print("PASS alpha53m compile fix: evolution item version bytes -> GameVersion generation")


# Compatibility wrapper for older internal harnesses/callers. The supplied scope
# is deliberately ignored so no request-owned SessionDbContext participates in
# the SQLite snapshot lifecycle.
session = root / "PKVault.Core/db/services/SessionService.cs"
s = session.read_text(encoding="utf-8")
iface_old = "    public Task PersistSession();\n"
iface_new = "    public Task PersistSession();\n    public Task PersistSession(IServiceScope scope);\n"
if "public Task PersistSession(IServiceScope scope);" not in s:
    if iface_old not in s:
        raise RuntimeError("alpha53m PersistSession interface anchor missing")
    s = s.replace(iface_old, iface_new, 1)

class_anchor = "    public async Task PersistSession()\n"
wrapper = """    public Task PersistSession(IServiceScope scope)
    {
        // Legacy callers used to hand an active DB-backed scope into PersistSession.
        // Dispose it before taking the SQLite snapshot or that writer can block the
        // backup indefinitely. Current production callers use PersistSession().
        scope.Dispose();
        return PersistSession();
    }

    public async Task PersistSession()
"""
if "public Task PersistSession(IServiceScope scope) => PersistSession();" not in s:
    if class_anchor not in s:
        raise RuntimeError("alpha53m PersistSession class anchor missing")
    s = s.replace(class_anchor, wrapper, 1)

session.write_text(s, encoding="utf-8")
print("PASS alpha53m compatibility: legacy PersistSession(scope) delegates to safe snapshot path")

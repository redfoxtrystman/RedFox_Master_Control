#!/usr/bin/env python3
"""Rebuild FalloutCraft v0.3.5 freeze-guard test from the exact v0.3.4 binary baseline."""
from pathlib import Path
import zipfile, hashlib, struct, json, tempfile, sys

EXPECTED_DLL = "0ffbb676912c80ffdb3da676d7c677d254168cb0425fbdc23707e91e822a51f7"
EXPECTED_JAR = "9e59639f2c81b986204ed9131ef693cd47e2e07fec98af36689eaad8a8438075"
THUNK_RVA = 0x5300
GETTICK_PTR_RVA = 0x84A0
LASTSET_RVA = 0x8678
CALL_RVA = 0x4CCB
THUNK = bytearray.fromhex(
    "4883ec38488944242048894c24284889542430ff15000000004c8b1500000000"
    "4989c34d29d34983fb32721f48890500000000488b442420488b4c2428488b54"
    "243041b0014883c438ffe0488b442420488b4c2428488b5424304883c438c3"
)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def patch_dll(src, dst):
    b = bytearray(Path(src).read_bytes())
    if hashlib.sha256(b).hexdigest() != EXPECTED_DLL:
        raise SystemExit("Wrong v0.3.4 FalloutCraft.dll")
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    n = struct.unpack_from("<H", b, pe + 6)[0]
    osz = struct.unpack_from("<H", b, pe + 20)[0]
    sh = pe + 24 + osz
    secs = {}
    for i in range(n):
        o = sh + i * 40
        name = bytes(b[o:o+8]).rstrip(b"\0").decode()
        vs, va, rs, rp = struct.unpack_from("<IIII", b, o + 8)
        secs[name] = (o, vs, va, rs, rp)

    def off(rva):
        for _, vs, va, rs, rp in secs.values():
            if va <= rva < va + max(vs, rs):
                return rp + rva - va
        raise ValueError(hex(rva))

    t = bytearray(THUNK)
    for disp_off, next_off, target in [
        (0x15, 0x19, GETTICK_PTR_RVA),
        (0x1C, 0x20, LASTSET_RVA),
        (0x2F, 0x33, LASTSET_RVA),
    ]:
        struct.pack_into("<i", t, disp_off, target - (THUNK_RVA + next_off))

    call_off = off(CALL_RVA)
    if bytes(b[call_off:call_off+5]) != bytes.fromhex("41b001ffd0"):
        raise SystemExit("Unexpected v0.3.4 SetPosition callsite")
    b[call_off:call_off+5] = b"\xE8" + struct.pack("<i", THUNK_RVA - (CALL_RVA + 5))
    thunk_off = off(THUNK_RVA)
    b[thunk_off:thunk_off+len(t)] = t
    struct.pack_into("<I", b, secs[".text"][0] + 8, 0x4360)
    struct.pack_into("<I", b, secs[".data"][0] + 8, 0x680)
    b = b.replace(b"FalloutCraft 0.3.4", b"FalloutCraft 0.3.5")
    Path(dst).write_bytes(b)

def patch_jar(src, dst):
    if sha(src) != EXPECTED_JAR:
        raise SystemExit("Wrong v0.3.4 Fabric jar")
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "fabric.mod.json":
                obj = json.loads(data)
                obj["version"] = "0.3.5"
                obj["description"] = (
                    "FalloutCraft 0.3.5 safety hotfix: throttled Fallout puppet relocation, "
                    "retained SkyCraft-style visual interpolation, mirror-world takeover, "
                    "and HUD/hand export."
                )
                data = (json.dumps(obj, indent=2) + "\n").encode()
            elif info.filename.endswith(".class"):
                data = data.replace(b"0.3.3", b"0.3.5")
            zout.writestr(info, data)

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_v035_hotfix.py INPUT_v0.3.4.zip OUTPUT_v0.3.5.zip")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        zipfile.ZipFile(sys.argv[1]).extractall(td)
        dll = td / "Data/F4SE/Plugins/FalloutCraft.dll"
        jar = td / "mods/FalloutCraft-fabric-0.1.0.jar"
        patch_dll(dll, dll)
        new_jar = td / "mods/new.jar"
        patch_jar(jar, new_jar)
        new_jar.replace(jar)
        with zipfile.ZipFile(sys.argv[2], "w", zipfile.ZIP_DEFLATED) as z:
            for p in td.rglob("*"):
                if p.is_file():
                    z.write(p, p.relative_to(td))

if __name__ == "__main__":
    main()

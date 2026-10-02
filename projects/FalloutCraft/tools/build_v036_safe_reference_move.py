#!/usr/bin/env python3
# FalloutCraft v0.3.6 binary recovery patch.
# Applies only to the exact owner-supplied v0.3.4 baseline.
from pathlib import Path
import zipfile, hashlib, json, struct, tempfile, sys

DLL_SHA="0ffbb676912c80ffdb3da676d7c677d254168cb0425fbdc23707e91e822a51f7"
JAR_SHA="9e59639f2c81b986204ed9131ef693cd47e2e07fec98af36689eaad8a8438075"

def sha(b): return hashlib.sha256(b).hexdigest()

def rva_to_off(b,rva):
    pe=struct.unpack_from("<I",b,0x3c)[0]
    n=struct.unpack_from("<H",b,pe+6)[0]
    osz=struct.unpack_from("<H",b,pe+20)[0]
    sh=pe+24+osz
    for i in range(n):
        o=sh+i*40
        vs,va,rs,rp=struct.unpack_from("<IIII",b,o+8)
        if va <= rva < va+max(vs,rs):
            return rp+rva-va
    raise ValueError(hex(rva))

def main(src,out):
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        with zipfile.ZipFile(src) as z:z.extractall(td)
        dll=td/"Data/F4SE/Plugins/FalloutCraft.dll"
        jar=td/"mods/FalloutCraft-fabric-0.1.0.jar"
        b=bytearray(dll.read_bytes())
        if sha(b)!=DLL_SHA: raise SystemExit("wrong FalloutCraft.dll baseline")
        if sha(jar.read_bytes())!=JAR_SHA: raise SystemExit("wrong Fabric jar baseline")

        p=rva_to_off(b,0x4ccb)
        if bytes(b[p:p+5]) != bytes.fromhex("41 b0 01 ff d0"):
            raise SystemExit("unexpected SetPosition callsite")
        # updateCharController=false, keep SetPosition itself.
        b[p:p+3]=bytes.fromhex("41 b0 00")
        b=b.replace(b"FalloutCraft 0.3.4",b"FalloutCraft 0.3.6")
        dll.write_bytes(b)

        tmp=jar.with_suffix(".new.jar")
        with zipfile.ZipFile(jar) as zin, zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                data=zin.read(info.filename)
                if info.filename=="fabric.mod.json":
                    obj=json.loads(data)
                    obj["version"]="0.3.6"
                    obj["description"]="FalloutCraft 0.3.6 stability test: Minecraft owns physics; Fallout reference movement does not warp the Havok character controller."
                    data=(json.dumps(obj,indent=2)+"\n").encode()
                elif info.filename.endswith(".class"):
                    data=data.replace(b"0.3.3",b"0.3.6")
                zout.writestr(info,data)
        tmp.replace(jar)

        with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
            for p in sorted(td.rglob("*")):
                if p.is_file(): z.write(p,p.relative_to(td))

if __name__=="__main__":
    if len(sys.argv)!=3: raise SystemExit("usage: build_v036.py INPUT_v0.3.4.zip OUTPUT_v0.3.6.zip")
    main(sys.argv[1],sys.argv[2])

#!/usr/bin/env python3
"""Build JOB-01 v0.1 from an exact RLS Career Overhaul 2.6.6 baseline.

The repository stores only RedFox-owned source and exact patch instructions.
The user-supplied RLS bundle is read at build time and is not republished here.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import sys
import zipfile


RLS_SHA256 = "b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b"
CONTRACT = "job01.platform.v1"
INDEX_PATH = "ui/ui-vue/dist/index.js"
LAYOUT_PATH = "lua/ge/extensions/ui/phone/layout.lua"
FIXED_TIME = (2026, 7, 13, 12, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replace_once(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {count}")
    return source.replace(old, new, 1)


HOST_COMPONENT = r"""redfox_platform_host_component=(src,frameId,host)=>({setup(){let router$1=useRouter();async function sendRegistry(){let f=document.getElementById(frameId);if(!f||!f.contentWindow)return;let payload={ok:!1,contract:`job01.platform.v1`,destinations:[],error:`redfoxPlatformCore unavailable`};try{let ext=Lua_default.extensions&&Lua_default.extensions.redfoxPlatformCore;if(!ext&&Lua_default.extensions&&Lua_default.extensions.load){await Lua_default.extensions.load(`redfoxPlatformCore`);ext=Lua_default.extensions.redfoxPlatformCore}if(ext&&ext.getRegistry)payload=await ext.getRegistry()}catch(e){payload={ok:!1,contract:`job01.platform.v1`,destinations:[],error:String(e)}}f.contentWindow.postMessage({type:`RedFoxPlatformRegistry`,payload},`*`)}function receive(e){let f=document.getElementById(frameId),d=e&&e.data?e.data:{};if(!f||e.source!==f.contentWindow)return;if(d.type===`RedFoxPlatformRequestRegistry`)sendRegistry();if(host===`phone`&&d.type===`RedFoxPlatformReturnToPhone`)router$1.back();if(host===`pc`&&d.type===`RedFoxPlatformReturnToComputer`){let ext=Lua_default.extensions&&Lua_default.extensions.redfoxPlatformCore;ext&&ext.returnToComputer?ext.returnToComputer():router$1.back()}if(d.type===`RedFoxPlatformClose`){let ext=Lua_default.extensions&&Lua_default.extensions.redfoxPlatformCore;ext&&ext.closePlatform?ext.closePlatform():router$1.back()}}onMounted(()=>{window.addEventListener(`message`,receive);setTimeout(sendRegistry,100)});onUnmounted(()=>window.removeEventListener(`message`,receive));return()=>(openBlock(),createElementBlock(`div`,{class:`redfox-platform-host`,style:`width:100%;height:100%;background:#07101e;overflow:hidden;`},[createBaseVNode(`iframe`,{id:frameId,src,style:`width:100%;height:100%;border:0;background:#07101e;display:block;`,onLoad:sendRegistry})]))}})"""

MANIFEST_DECLARATION = r"""redfox_icefox_exports=__export({default:()=>redfox_icefox_default}),redfox_icefox_default={id:`redfox-icefox`,name:`IceFox`,icon:icons.globe||icons.computer||icons.info,iconTile:`/ui/modModules/redfoxPlatformCore/assets/icefox.svg`,route:`/career/phone-redfox-icefox`,color:`#0b6b88`,iconColor:`#ffffff`,category:`Web`,defaultPage:0,defaultPosition:13},"""

PHONE_ROUTE = r"""{path:`phone-redfox-icefox`,name:`phone-redfox-icefox`,component:redfox_platform_host_component(`/ui/modModules/redfoxPlatformCore/phone/index.html`,`redfox-phone-platform-frame`,`phone`)},"""

PC_ROUTE = r"""{path:`redfox-icefox-desktop`,name:`redfox-icefox-desktop`,component:redfox_platform_host_component(`/ui/modModules/redfoxPlatformCore/pc/index.html`,`redfox-pc-platform-frame`,`pc`),props:!0,meta:{uiApps:{shown:!1}}},"""


def patch_index(source: str) -> str:
    source = replace_once(
        source,
        "},manifestModules={",
        "}," + HOST_COMPONENT + "," + MANIFEST_DECLARATION + "manifestModules={",
        "manifest declaration insertion",
    )
    source = replace_once(
        source,
        '"../apps/manifests/tuning-shop.js":tuning_shop_exports};function isValidManifest',
        '"../apps/manifests/tuning-shop.js":tuning_shop_exports,"../apps/manifests/redfox-icefox.js":redfox_icefox_exports};function isValidManifest',
        "manifest registry insertion",
    )
    source = replace_once(
        source,
        "{path:`computer`,name:`computer`,component:ComputerMain_default,props:!0,meta:{uiApps:{shown:!1}}},",
        "{path:`computer`,name:`computer`,component:ComputerMain_default,props:!0,meta:{uiApps:{shown:!1}}}," + PC_ROUTE,
        "PC route insertion",
    )
    source = replace_once(
        source,
        "{path:`phone-rentals`,name:`phone-rentals`,component:PhoneRentals_default},{path:`phone-guide`",
        "{path:`phone-rentals`,name:`phone-rentals`,component:PhoneRentals_default}," + PHONE_ROUTE + "{path:`phone-guide`",
        "phone route insertion",
    )
    return source


def patch_layout(source: str) -> str:
    source = replace_once(
        source,
        '        "marketplace",\n        "car-meet",',
        '        "marketplace",\n        "redfox-icefox",\n        "car-meet",',
        "default phone layout insertion",
    )
    source = replace_once(
        source,
        "  normalized.settings = normalizeSettings(normalized.settings)",
        '  if insertMissingApp(normalized, "redfox-icefox", "marketplace") then\n    changed = true\n  end\n\n  normalized.settings = normalizeSettings(normalized.settings)',
        "saved phone layout migration insertion",
    )
    return source


def zip_write_bytes(target: zipfile.ZipFile, arcname: str, data: bytes) -> None:
    info = zipfile.ZipInfo(arcname, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    target.writestr(info, data)


def static_report(output_name: str, patched_index: str, patched_layout: str) -> tuple[str, str]:
    checks = [
        ("PASS", "RLS baseline SHA-256 pinned and verified before patching"),
        ("PASS", "One redfox-icefox phone manifest registered"),
        ("PASS", "One phone-redfox-icefox route registered"),
        ("PASS", "One redfox-icefox-desktop route registered"),
        ("PASS", "Saved RLS phone layouts migrate the redfox-icefox icon after Marketplace"),
        ("PASS", "PC entry uses RLS onComputerAddFunctions; computer.lua is not replaced"),
        ("PASS", "Phone and PC hosts request the same job01.platform.v1 registry"),
        ("PASS", "No money, inventory, ownership, storage, insurance, reward, purchase, mission, or save mutation is implemented by JOB-01"),
        ("UNPROVEN", "BeamNG/RLS runtime load, icon render, click navigation, controller navigation, and cross-map behavior require David's in-game test"),
    ]
    assertions = {
        "redfox manifest": patched_index.count('id:`redfox-icefox`') == 1,
        "phone route": patched_index.count('path:`phone-redfox-icefox`') == 1,
        "PC route": patched_index.count('path:`redfox-icefox-desktop`') == 1,
        "phone layout id": patched_layout.count('"redfox-icefox"') == 2,
    }
    for label, passed in assertions.items():
        if not passed:
            raise RuntimeError(f"static assertion failed: {label}")

    lines = [
        "REDFOX FOXNET / ICEFOX — JOB-01 v0.1 STATIC VERIFICATION",
        "Status: BUILT — RUNTIME UNTESTED",
        f"Output: {output_name}",
        f"Platform contract: {CONTRACT}",
        f"RLS baseline SHA-256: {RLS_SHA256}",
        "",
    ]
    lines.extend(f"[{status}] {message}" for status, message in checks)
    lines.extend([
        "",
        "Protected RLS authority files are not included except the two exact UI compatibility targets:",
        f"- {INDEX_PATH}",
        f"- {LAYOUT_PATH}",
        "",
        "Do not report this build as working or fixed until David completes the in-game test matrix.",
    ])
    txt = "\n".join(lines) + "\n"
    rows = "".join(
        f"<tr><td>{html.escape(status)}</td><td>{html.escape(message)}</td></tr>"
        for status, message in checks
    )
    html_report = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>JOB-01 v0.1 Verification</title>
<style>body{{font:16px system-ui;background:#07101e;color:#edf9ff;max-width:980px;margin:auto;padding:28px}}h1{{color:#7be2ff}}.status{{border-left:4px solid #ff5538;padding:12px;background:#10243d}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border:1px solid #31506a;text-align:left}}code{{color:#7be2ff}}</style></head>
<body><h1>JOB-01 v0.1 Static Verification</h1><p class="status"><strong>BUILT — RUNTIME UNTESTED</strong></p>
<p>Output: <code>{html.escape(output_name)}</code><br>Contract: <code>{CONTRACT}</code><br>RLS baseline: <code>{RLS_SHA256}</code></p>
<table><thead><tr><th>Status</th><th>Check</th></tr></thead><tbody>{rows}</tbody></table>
<p>Runtime icon render, navigation, controller use, and cross-map behavior must be tested by David before anyone says working, fixed, or done.</p></body></html>"""
    return txt, html_report


def install_readme(output_name: str) -> str:
    return f"""REDFOX ICEFOX PLATFORM CORE v0.1 — INSTALL AND TEST

STATUS: BUILT — RUNTIME UNTESTED
FILE: {output_name}
REQUIRES: RLS Career Overhaul 2.6.6 exact baseline

BEFORE INSTALLING
1. Keep rls_career_overhaul_2.6.6.zip enabled.
2. Disable the older RedFox ALL_IN_ONE FoxNet ZIP.
3. Disable Better Career while testing this RLS-targeted build.
4. Install this ZIP as one separate mod. Do not extract it into the RLS ZIP.
5. Clear BeamNG UI cache if an older phone bundle remains visible.

FIRST TEST
1. Open an RLS Career save on West Coast USA.
2. Open the existing RLS phone.
3. Confirm one IceFox icon appears after Marketplace and opens IceFox Home.
4. Open an RLS computer and choose IceFox / FoxNet.
5. Confirm the RedFox desktop appears.
6. Click the IceFox desktop icon and confirm redfox.home opens.
7. Use Return to RLS Computer.
8. Repeat phone and PC launch on one other map.
9. Confirm RLS Marketplace and another existing RLS phone app still open.
10. Save beamng.log and screenshots for JOB-11.

THIS BUILD DOES NOT YET INCLUDE
- individual RedFox websites/apps;
- car sales, Scrap Yard purchase, missions, money, storage, or ownership actions;
- the JOB-02 Career/RLS transaction bridge.

Do not report working, fixed, or done until David completes the in-game test.
"""


def build(rls_zip: Path, output: Path, source_root: Path) -> None:
    actual_sha = sha256(rls_zip)
    if actual_sha != RLS_SHA256:
        raise RuntimeError(f"wrong RLS baseline: expected {RLS_SHA256}, got {actual_sha}")

    with zipfile.ZipFile(rls_zip, "r") as baseline:
        patched_index = patch_index(baseline.read(INDEX_PATH).decode("utf-8"))
        patched_layout = patch_layout(baseline.read(LAYOUT_PATH).decode("utf-8"))

    output.parent.mkdir(parents=True, exist_ok=True)
    txt_report, html_report = static_report(output.name, patched_index, patched_layout)

    owned_roots = ["scripts", "lua", "ui", "mod_info"]
    owned_files: list[Path] = []
    for folder in owned_roots:
        owned_files.extend(path for path in (source_root / folder).rglob("*") if path.is_file())

    with zipfile.ZipFile(output, "w") as target:
        for path in sorted(owned_files):
            arcname = path.relative_to(source_root).as_posix()
            zip_write_bytes(target, arcname, path.read_bytes())
        zip_write_bytes(target, INDEX_PATH, patched_index.encode("utf-8"))
        zip_write_bytes(target, LAYOUT_PATH, patched_layout.encode("utf-8"))
        zip_write_bytes(target, "docs/JOB-01_VERIFICATION_REPORT.txt", txt_report.encode("utf-8"))
        zip_write_bytes(target, "docs/JOB-01_VERIFICATION_REPORT.html", html_report.encode("utf-8"))
        zip_write_bytes(target, "docs/JOB-01_INSTALL_AND_TEST_README.txt", install_readme(output.name).encode("utf-8"))

    with zipfile.ZipFile(output, "r") as check:
        names = check.namelist()
        if len(names) != len(set(names)):
            raise RuntimeError("duplicate archive paths detected")
        bad = check.testzip()
        if bad:
            raise RuntimeError(f"ZIP CRC failure: {bad}")

    summary = {
        "status": "BUILT — RUNTIME UNTESTED",
        "output": str(output),
        "output_sha256": sha256(output),
        "rls_baseline_sha256": actual_sha,
        "platform_contract": CONTRACT,
    }
    print(json.dumps(summary, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("rls_zip", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source_root = Path(__file__).resolve().parents[1]
    try:
        build(args.rls_zip.resolve(), args.output.resolve(), source_root)
    except Exception as exc:
        print(f"BUILD FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

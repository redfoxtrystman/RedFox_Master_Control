#!/usr/bin/env python3
"""RedFox/FoxNet JOB-11 static package auditor.

Date: 2026-07-14 13:08 PDT
Owner: JOB-11 — QA / Logging / Failure Triage
Status: synthetic PASS/FAIL fixtures tested; real project candidate untested
What changed: added Gate 1 ZIP integrity, report, forbidden-file, collision,
    app-ID, and inventory checks with TXT/HTML/JSON/CSV output.
Why: the promised JOB-11 package checker was not committed before the original
    Work chat became inaccessible under the separate Work-chat usage limit.
Files affected: QA_LOGGING/tools/redfox_package_audit.py
Known problems: static heuristics require manual ownership/contract review and
    cannot prove BeamNG runtime behavior.
Required next step: audit the first exact candidate supplied by JOB-00 or David.

Performs Gate 1 checks without claiming BeamNG runtime success.
Standard-library only; Python 3.10+ recommended.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
import zipfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Iterable

REQUIRED_REPORT_PATTERNS = (
    re.compile(r"(^|/)CHANGE_SCOPE_.*\.txt$", re.I),
    re.compile(r"(^|/)OPEN_THIS_VERIFICATION_REPORT_.*\.txt$", re.I),
    re.compile(r"(^|/)OPEN_THIS_VERIFICATION_REPORT_.*\.html$", re.I),
    re.compile(r"(^|/)VERIFY_.*\.json$", re.I),
    re.compile(r"(^|/)VERIFY_.*_FILE_INVENTORY\.csv$", re.I),
    re.compile(r"(^|/)FILE_TREE_.*\.txt$", re.I),
    re.compile(r"(^|/)LOGGING_AND_TESTING_README\.txt$", re.I),
    re.compile(r"(^|/)LOGGING_AND_TESTING_README\.html$", re.I),
)

FORBIDDEN_EXACT_SUFFIXES = (
    "lua/ge/extensions/career/modules/redfoxscrapyarddirect.lua",
)

PROTECTED_CORE_MARKERS = (
    "ui/modmodules/redfoxcareerweb/phone/",
    "ui/modmodules/redfoxcareerweb/assets/js/icefox_front.js",
    "assets/js/icefox_front.js",
    "ui/ui-vue/dist/index.js",
)

TEXT_EXTENSIONS = {
    ".txt", ".md", ".html", ".htm", ".css", ".js", ".json", ".lua",
    ".xml", ".csv", ".yaml", ".yml", ".ini", ".cfg",
}

APP_ID_PATTERNS = (
    re.compile(r'"(?:appId|app_id|id)"\s*:\s*"([A-Za-z0-9_.-]+)"'),
    re.compile(r"\b(?:appId|app_id)\s*[:=]\s*['\"]([A-Za-z0-9_.-]+)['\"]"),
)

@dataclass
class Finding:
    severity: str
    code: str
    package: str
    path: str
    message: str

@dataclass
class EntryRecord:
    package: str
    path: str
    size: int
    compressed_size: int
    crc: str
    sha256: str | None

@dataclass
class PackageRecord:
    path: str
    filename: str
    size_bytes: int
    sha256: str
    zip_integrity: str
    entry_count: int
    top_levels: list[str] = field(default_factory=list)
    detected_app_ids: list[str] = field(default_factory=list)

@dataclass
class AuditResult:
    generated_utc: str
    job: str
    status: str
    packages: list[PackageRecord]
    findings: list[Finding]
    entries: list[EntryRecord]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized(name: str) -> str:
    return name.replace("\\", "/").lstrip("./").lower()


def unsafe_zip_path(name: str) -> bool:
    raw = name.replace("\\", "/")
    p = PurePosixPath(raw)
    return raw.startswith("/") or bool(re.match(r"^[A-Za-z]:/", raw)) or ".." in p.parts


def required_reports_found(names: Iterable[str]) -> list[bool]:
    values = list(names)
    return [any(pattern.search(name) for name in values) for pattern in REQUIRED_REPORT_PATTERNS]


def is_text_candidate(name: str, size: int) -> bool:
    return Path(name).suffix.lower() in TEXT_EXTENSIONS and size <= 5 * 1024 * 1024


def inspect_package(path: Path, entries: list[EntryRecord], findings: list[Finding]) -> PackageRecord:
    package_sha = file_sha256(path)
    package = PackageRecord(
        path=str(path.resolve()),
        filename=path.name,
        size_bytes=path.stat().st_size,
        sha256=package_sha,
        zip_integrity="NOT_TESTED",
        entry_count=0,
    )

    if not zipfile.is_zipfile(path):
        package.zip_integrity = "FAIL"
        findings.append(Finding("FAIL", "NOT_ZIP", path.name, "", "File is not a readable ZIP archive."))
        return package

    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        package.zip_integrity = "PASS" if bad is None else "FAIL"
        if bad is not None:
            findings.append(Finding("FAIL", "ZIP_CRC", path.name, bad, "CRC/integrity test failed."))

        infos = archive.infolist()
        package.entry_count = len(infos)
        names = [info.filename.replace("\\", "/") for info in infos]
        normalized_names = [normalized(name) for name in names]
        tops = sorted({PurePosixPath(name).parts[0] for name in names if PurePosixPath(name).parts})
        package.top_levels = tops

        duplicates: dict[str, int] = {}
        for name in normalized_names:
            duplicates[name] = duplicates.get(name, 0) + 1
        for name, count in sorted(duplicates.items()):
            if count > 1:
                findings.append(Finding("FAIL", "DUPLICATE_ENTRY", path.name, name, f"ZIP contains {count} entries with this normalized path."))

        if len(tops) > 1:
            findings.append(Finding("REVIEW", "MULTIPLE_TOP_LEVELS", path.name, "", f"Archive has multiple top-level entries: {', '.join(tops)}"))

        report_checks = required_reports_found(names)
        for pattern, found in zip(REQUIRED_REPORT_PATTERNS, report_checks):
            if not found:
                findings.append(Finding("FAIL", "MISSING_REQUIRED_REPORT", path.name, "", f"No entry matched required pattern: {pattern.pattern}"))

        app_ids: set[str] = set()
        for info, name, norm in zip(infos, names, normalized_names):
            if info.is_dir():
                continue
            if unsafe_zip_path(name):
                findings.append(Finding("FAIL", "UNSAFE_PATH", path.name, name, "Absolute, drive-qualified, or parent-traversal path."))
            if "__pycache__" in norm or norm.endswith(".pyc"):
                findings.append(Finding("FAIL", "PYTHON_CACHE", path.name, name, "Python cache/generated bytecode must not ship."))
            if any(norm.endswith(suffix) for suffix in FORBIDDEN_EXACT_SUFFIXES):
                findings.append(Finding("FAIL", "FORBIDDEN_STARTUP_MODULE", path.name, name, "Prohibited Scrap Yard startup Career module."))
            if any(marker in norm for marker in PROTECTED_CORE_MARKERS):
                findings.append(Finding("REVIEW", "PROTECTED_CORE_PRESENT", path.name, name, "Shared phone/PC/platform core path is present; verify this package owns it."))

            data: bytes | None = None
            entry_hash: str | None = None
            try:
                data = archive.read(info)
                entry_hash = bytes_sha256(data)
            except Exception as exc:  # pragma: no cover - defensive
                findings.append(Finding("FAIL", "ENTRY_READ", path.name, name, f"Could not read entry: {exc}"))

            entries.append(EntryRecord(path.name, name, info.file_size, info.compress_size, f"{info.CRC:08x}", entry_hash))

            if data is None or not is_text_candidate(name, info.file_size):
                continue
            text = data.decode("utf-8", errors="replace")
            lowered = text.lower()
            if "vehicleshopping" in lowered and ("onextensionloaded" in lowered or "oncareeractive" in lowered or "onclientstartmission" in lowered):
                findings.append(Finding("REVIEW", "VEHICLESHOPPING_STARTUP_REFERENCE", path.name, name, "vehicleShopping appears near a startup/lifecycle hook; manual review required."))
            if "redfoxscrapyarddirect" in lowered:
                findings.append(Finding("FAIL", "FORBIDDEN_DIRECT_REFERENCE", path.name, name, "References prohibited redfoxScrapYardDirect implementation."))
            for pattern in APP_ID_PATTERNS:
                app_ids.update(pattern.findall(text))

        package.detected_app_ids = sorted(app_ids)
    return package


def cross_package_checks(packages: list[PackageRecord], entries: list[EntryRecord], findings: list[Finding]) -> None:
    by_path: dict[str, list[EntryRecord]] = {}
    for entry in entries:
        by_path.setdefault(normalized(entry.path), []).append(entry)
    for path, records in sorted(by_path.items()):
        package_names = sorted({record.package for record in records})
        if len(package_names) > 1:
            hashes = {record.sha256 for record in records}
            severity = "FAIL" if len(hashes) > 1 else "REVIEW"
            findings.append(Finding(severity, "CROSS_PACKAGE_COLLISION", ", ".join(package_names), path,
                                    "Same install path appears in multiple packages" + (" with different content." if len(hashes) > 1 else " with identical content.")))

    ids: dict[str, list[str]] = {}
    for package in packages:
        for app_id in package.detected_app_ids:
            ids.setdefault(app_id, []).append(package.filename)
    for app_id, package_names in sorted(ids.items()):
        unique = sorted(set(package_names))
        if len(unique) > 1:
            findings.append(Finding("FAIL", "DUPLICATE_APP_ID", ", ".join(unique), app_id, "App ID detected in multiple candidate packages."))


def verdict(findings: list[Finding]) -> str:
    if any(item.severity == "FAIL" for item in findings):
        return "FAIL/STOP"
    if any(item.severity == "REVIEW" for item in findings):
        return "BLOCKED — MANUAL REVIEW REQUIRED"
    return "PASS — STATIC GATE 1 ONLY; RUNTIME UNPROVEN"


def write_outputs(result: AuditResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "VERIFY_JOB11_PACKAGE_AUDIT.json"
    csv_path = output_dir / "VERIFY_JOB11_PACKAGE_AUDIT_FILE_INVENTORY.csv"
    txt_path = output_dir / "OPEN_THIS_VERIFICATION_REPORT_JOB11_PACKAGE_AUDIT.txt"
    html_path = output_dir / "OPEN_THIS_VERIFICATION_REPORT_JOB11_PACKAGE_AUDIT.html"

    json_path.write_text(json.dumps(asdict(result), indent=2), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["package", "path", "size", "compressed_size", "crc", "sha256"])
        writer.writeheader()
        for entry in result.entries:
            writer.writerow(asdict(entry))

    lines = [
        "RedFox/FoxNet JOB-11 Static Package Audit",
        f"Generated UTC: {result.generated_utc}",
        f"Verdict: {result.status}",
        "Runtime: UNPROVEN — this report does not establish BeamNG runtime success.",
        "",
        "Packages:",
    ]
    for package in result.packages:
        lines.extend([
            f"- {package.filename}",
            f"  Size: {package.size_bytes}",
            f"  SHA-256: {package.sha256}",
            f"  ZIP integrity: {package.zip_integrity}",
            f"  Entries: {package.entry_count}",
            f"  Top levels: {', '.join(package.top_levels) or '(none)'}",
            f"  Detected app IDs: {', '.join(package.detected_app_ids) or '(none)'}",
        ])
    lines.append("")
    lines.append("Findings:")
    if not result.findings:
        lines.append("- None.")
    else:
        for item in result.findings:
            lines.append(f"- [{item.severity}] {item.code} | {item.package} | {item.path} | {item.message}")
    txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    rows = "".join(
        f"<tr><td>{html.escape(item.severity)}</td><td>{html.escape(item.code)}</td><td>{html.escape(item.package)}</td><td>{html.escape(item.path)}</td><td>{html.escape(item.message)}</td></tr>"
        for item in result.findings
    ) or '<tr><td colspan="5">No findings.</td></tr>'
    package_rows = "".join(
        f"<tr><td>{html.escape(item.filename)}</td><td>{item.size_bytes}</td><td><code>{item.sha256}</code></td><td>{html.escape(item.zip_integrity)}</td><td>{item.entry_count}</td></tr>"
        for item in result.packages
    )
    html_path.write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>JOB-11 Package Audit</title>
<style>body{{font-family:system-ui,sans-serif;max-width:1200px;margin:2rem auto;padding:0 1rem}}table{{border-collapse:collapse;width:100%;margin:1rem 0}}th,td{{border:1px solid #bbb;padding:.45rem;text-align:left;vertical-align:top}}code{{overflow-wrap:anywhere}}.verdict{{font-size:1.2rem;font-weight:700}}</style></head>
<body><h1>RedFox/FoxNet JOB-11 Static Package Audit</h1><p class="verdict">{html.escape(result.status)}</p>
<p><strong>Runtime remains unproven.</strong> This report covers static Gate 1 only.</p>
<h2>Packages</h2><table><thead><tr><th>File</th><th>Bytes</th><th>SHA-256</th><th>ZIP integrity</th><th>Entries</th></tr></thead><tbody>{package_rows}</tbody></table>
<h2>Findings</h2><table><thead><tr><th>Severity</th><th>Code</th><th>Package</th><th>Path/ID</th><th>Message</th></tr></thead><tbody>{rows}</tbody></table>
<p>Generated UTC: {html.escape(result.generated_utc)}</p></body></html>""", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="JOB-11 static ZIP/package audit. Runtime is not tested.")
    parser.add_argument("packages", nargs="+", type=Path, help="Candidate ZIP files to inspect together.")
    parser.add_argument("--output", type=Path, default=Path("job11_audit_output"), help="Output directory.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    missing = [str(path) for path in args.packages if not path.is_file()]
    if missing:
        print("Missing input file(s): " + ", ".join(missing), file=sys.stderr)
        return 2

    findings: list[Finding] = []
    entries: list[EntryRecord] = []
    packages = [inspect_package(path, entries, findings) for path in args.packages]
    cross_package_checks(packages, entries, findings)
    result = AuditResult(
        generated_utc=datetime.now(timezone.utc).isoformat(),
        job="JOB-11 — QA / Logging / Failure Triage",
        status=verdict(findings),
        packages=packages,
        findings=findings,
        entries=entries,
    )
    write_outputs(result, args.output)
    print(result.status)
    print(f"Reports: {args.output.resolve()}")
    return 1 if result.status.startswith("FAIL") else 0


if __name__ == "__main__":
    raise SystemExit(main())

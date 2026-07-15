#!/usr/bin/env python3
"""Validate RedFox job ownership, pipeline manifest, and candidate handoffs.

Standard-library only so it can run locally or in GitHub Actions.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "PROJECT_MANIFESTS" / "REDFOX_JOB_PIPELINE_MANIFEST.json"
HANDOFF_NAME = "REDFOX_JOB_HANDOFF.json"
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
JOB_RE = re.compile(r"^JOB-(0[0-9]|1[0-2])$")


class ValidationError(Exception):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise ValidationError(f"missing file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(
            f"invalid JSON in {path.relative_to(ROOT)}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(data, dict):
        raise ValidationError(f"top-level JSON must be an object: {path.relative_to(ROOT)}")
    return data


def require(data: dict[str, Any], dotted: str, errors: list[str]) -> Any:
    value: Any = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            errors.append(f"missing required field: {dotted}")
            return None
        value = value[part]
    if value is None or value == "" or value == []:
        errors.append(f"empty required field: {dotted}")
    return value


def validate_manifest() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    manifest = load_json(MANIFEST_PATH)

    jobs = manifest.get("jobs")
    if not isinstance(jobs, dict):
        errors.append("manifest.jobs must be an object")
        return manifest, errors

    expected = {f"JOB-{number:02d}" for number in range(13)}
    actual = set(jobs)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"manifest missing jobs: {', '.join(missing)}")
    if extra:
        errors.append(f"manifest has unexpected jobs: {', '.join(extra)}")

    for job_id, job in jobs.items():
        if not JOB_RE.match(job_id):
            errors.append(f"invalid job ID in manifest: {job_id}")
        if not isinstance(job, dict):
            errors.append(f"manifest job entry must be an object: {job_id}")
            continue
        if not job.get("title"):
            errors.append(f"manifest job missing title: {job_id}")
        if not isinstance(job.get("owns"), list) or not job["owns"]:
            errors.append(f"manifest job missing owns list: {job_id}")
        if not isinstance(job.get("must_not"), list) or not job["must_not"]:
            errors.append(f"manifest job missing must_not list: {job_id}")

    phases = manifest.get("required_phases")
    if not isinstance(phases, list) or "test_harness" not in phases or "backend_proof" not in phases:
        errors.append("manifest must require test_harness and backend_proof phases")

    statuses = manifest.get("allowed_statuses")
    if not isinstance(statuses, list) or not statuses:
        errors.append("manifest.allowed_statuses must be a non-empty list")

    return manifest, errors


def handoff_paths() -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.rglob(HANDOFF_NAME):
        rel_parts = path.relative_to(ROOT).parts
        if ".git" in rel_parts or "TEMPLATES" in rel_parts:
            continue
        paths.append(path)
    return sorted(paths)


def validate_handoff(path: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    data = load_json(path)
    rel = path.relative_to(ROOT)

    required = [
        "schema_version",
        "job_id",
        "job_title",
        "owner_chat",
        "candidate.name",
        "candidate.version",
        "candidate.status",
        "candidate.baseline",
        "candidate.git_commit_or_pr",
        "candidate.zip_name",
        "candidate.zip_size_bytes",
        "candidate.sha256",
        "ownership.files_added",
        "ownership.files_changed",
        "ownership.files_removed",
        "ownership.protected_files_confirmed_untouched",
        "ownership.dependencies",
        "backend.entry_points",
        "backend.service_functions",
        "backend.test_harness_type",
        "backend.test_harness_entry",
        "backend.test_harness_release_disposition",
        "backend.backend_test_steps",
        "backend.backend_expected_results",
        "backend.backend_actual_results",
        "website.app_or_site_id",
        "website.canonical_destination",
        "website.page_entry",
        "website.phone_expected_result",
        "website.pc_expected_result",
        "contracts.job01_platform_version",
        "contracts.job02_bridge_version",
        "contracts.permissions",
        "contracts.expected_log_prefixes",
        "verification.static_checks_passed",
        "verification.zip_reopened_and_checked",
        "verification.duplicate_paths_checked",
        "verification.forbidden_paths_checked",
        "verification.david_runtime_tested",
        "verification.runtime_result",
        "reports.change_scope_txt",
        "reports.verification_txt",
        "reports.verification_html",
        "reports.verify_json",
        "reports.file_inventory_csv",
        "reports.file_tree_txt",
        "reports.logging_readme_txt",
        "reports.logging_readme_html",
        "next_action",
    ]
    values = {field: require(data, field, errors) for field in required}

    job_id = values.get("job_id")
    jobs = manifest.get("jobs", {})
    if not isinstance(job_id, str) or not JOB_RE.match(job_id):
        errors.append(f"invalid job_id: {job_id!r}")
    elif job_id not in jobs:
        errors.append(f"job_id is not in central manifest: {job_id}")
    else:
        expected_title = jobs[job_id].get("title")
        if values.get("job_title") != expected_title:
            errors.append(
                f"job_title mismatch for {job_id}: expected {expected_title!r}, got {values.get('job_title')!r}"
            )

    allowed_statuses = manifest.get("allowed_statuses", [])
    status = values.get("candidate.status")
    if status not in allowed_statuses:
        errors.append(f"candidate.status is not allowed: {status!r}")

    size = values.get("candidate.zip_size_bytes")
    if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
        errors.append("candidate.zip_size_bytes must be a positive integer")

    sha256 = values.get("candidate.sha256")
    if not isinstance(sha256, str) or not SHA256_RE.match(sha256):
        errors.append("candidate.sha256 must be exactly 64 hexadecimal characters")

    for field in (
        "verification.static_checks_passed",
        "verification.zip_reopened_and_checked",
        "verification.duplicate_paths_checked",
        "verification.forbidden_paths_checked",
    ):
        if values.get(field) is not True:
            errors.append(f"{field} must be true before QA intake")

    disposition = values.get("backend.test_harness_release_disposition")
    allowed_dispositions = {
        "retained developer-only",
        "hidden",
        "disabled",
        "separate test package",
        "removed",
    }
    if disposition not in allowed_dispositions:
        errors.append(
            "backend.test_harness_release_disposition must be one of: "
            + ", ".join(sorted(allowed_dispositions))
        )

    runtime_tested = values.get("verification.david_runtime_tested")
    if not isinstance(runtime_tested, bool):
        errors.append("verification.david_runtime_tested must be boolean")
    if status == "DAVID-TESTED WORKING":
        if runtime_tested is not True:
            errors.append("DAVID-TESTED WORKING requires verification.david_runtime_tested=true")
        for field in (
            "verification.runtime_test_maps",
            "verification.runtime_test_timestamp",
            "verification.log_files",
        ):
            require(data, field, errors)
    elif runtime_tested is True and status == "BUILT — RUNTIME UNTESTED":
        errors.append("runtime-tested candidate cannot remain labeled BUILT — RUNTIME UNTESTED")

    if errors:
        return [f"{rel}: {message}" for message in errors]
    return []


def main() -> int:
    all_errors: list[str] = []
    try:
        manifest, manifest_errors = validate_manifest()
        all_errors.extend(f"{MANIFEST_PATH.relative_to(ROOT)}: {error}" for error in manifest_errors)
    except ValidationError as exc:
        print(f"REDFOX VALIDATION FAILED\n- {exc}")
        return 1

    paths = handoff_paths()
    for path in paths:
        try:
            all_errors.extend(validate_handoff(path, manifest))
        except ValidationError as exc:
            all_errors.append(str(exc))

    if all_errors:
        print("REDFOX VALIDATION FAILED")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print("REDFOX VALIDATION PASSED")
    print(f"- central jobs validated: {len(manifest.get('jobs', {}))}")
    print(f"- candidate handoffs validated: {len(paths)}")
    if not paths:
        print("- note: no non-template REDFOX_JOB_HANDOFF.json files are present yet")
    return 0


if __name__ == "__main__":
    sys.exit(main())

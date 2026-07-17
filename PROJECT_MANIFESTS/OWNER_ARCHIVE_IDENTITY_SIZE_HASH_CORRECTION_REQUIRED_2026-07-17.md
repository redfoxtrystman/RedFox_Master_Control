# OWNER ALERT — Archive Identity, Size and SHA-256 Correction Required

**Date:** 2026-07-17  
**Owner:** David / Captain  
**Coordinator:** JOB-00 — Coordinator / Integration / Verification  
**Status:** STOP CONDITION FOR SHARED-BASELINE FREEZE

## Problem

Two project lanes recorded the same SHA-256 for an `rls_career_overhaul_2.6.6` archive but recorded different byte sizes:

```text
SHA-256:
b3cd053dafaef96ebe283bb5f39d2b7187430ad99f4b9f94d0aa825d5c1f155b

JOB-01 — Phone + PC Platform Core recorded archive size:
43,066,347 bytes

JOB-02 — Shared RLS / Career Bridge recorded archive size:
40,035,328 bytes
```

A byte-for-byte file with one SHA-256 cannot have two different byte sizes. At least one record is incorrect, describes a different measurement, or was copied from a different file.

## Jobs required to recheck

- JOB-00 — Coordinator / Integration / Verification.
- JOB-01 — Phone + PC Platform Core.
- JOB-02 — Shared RLS / Career Bridge.
- JOB-11 — QA / Logging / Failure Triage when activated for baseline verification.
- Any feature job that copied either size into its own audit.

## Mandatory verification method

Use the exact archive file intended as the shared input. Record:

```text
Exact filename, including suffix such as (1) or (2)
Absolute/local location used for verification
Archive byte size from the file itself
SHA-256 calculated from the file itself
ZIP integrity result
Archive member count
Top-level paths
Date/time verified
Tool/command used
Verifier job and chat title
```

The record must clearly distinguish:

- archive file byte size;
- extracted folder total size;
- sum of uncompressed member sizes;
- operating-system rounded display size;
- download/card display size.

Only the archive file byte size may be paired with the archive SHA-256 as its identity.

## Recommended commands

PowerShell:

```powershell
$file = "C:\path\to\rls_career_overhaul_2.6.6.zip"
(Get-Item $file).Length
Get-FileHash $file -Algorithm SHA256
```

Python:

```python
from pathlib import Path
import hashlib

path = Path(r"C:\path\to\rls_career_overhaul_2.6.6.zip")
print(path.stat().st_size)
print(hashlib.sha256(path.read_bytes()).hexdigest())
```

Do not use extracted-size totals as the archive size.

## Required correction output

After verification, publish one current authoritative record:

```text
Canonical filename =
Archive byte size =
SHA-256 =
ZIP integrity =
Member count =
Verified by =
Verified at =
Supersedes current copied size notes = yes
Explanation of discrepancy =
```

Historical audits must not be silently rewritten to pretend the mistake never happened. Add a correction note that identifies which old measurement was wrong and why.

## Stop rule

Until this is resolved:

- JOB-00 — Coordinator / Integration / Verification must not freeze the shared RLS baseline.
- JOB-01 — Phone + PC Platform Core must not claim its builder input was independently reverified from the currently available file.
- JOB-02 — Shared RLS / Career Bridge must not claim the currently available archive matches its old size note.
- Other chats must not copy either size as authoritative.

Filename similarity is not identity. A suffixed copy can be identical, modified, recompressed or corrupt; verify every exact file used.

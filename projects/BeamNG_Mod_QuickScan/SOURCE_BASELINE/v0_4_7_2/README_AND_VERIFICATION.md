# QuickScan v0.4.7.2 Source Baseline and Verification

## Baseline

- Parent: exact verified v0.4.7.1 source.
- Change boundary: filename-only rename storage and cleanup UI only.
- Source SHA-256: `4dd5224ee6fdc633e01b18095285fb560036bfa643e2ce9c5dd4086c99815c7f`.
- Package SHA-256: `a6def9ddd2a4f39a6708cb614825d923298a309862edb1855ebf2ec866e425e2`.

## Storage behavior

`Manifest only (recommended)` is the default for filename-only renames. It records original/new paths, SHA-256, timestamp, warning, Undo database row, and JSONL history. It does not duplicate the ZIP.

`Full ZIP copy` is optional and clearly warns that it can consume substantial disk space.

Operations that rewrite files inside a ZIP remain outside this exception and must create complete backups.

## Tests

```text
PASS Python compilation
PASS inherited full self-test chain
PASS v0.4.7.2 storage self-test
PASS final ZIP CRC and reopen
PASS extracted package compile/self-test
PASS extracted Storage-window GUI smoke
PASS filename-only rename without a backup ZIP
PASS SHA-256 unchanged by rename
PASS Undo restored the original filename and hash
```

## Windows test still required

- Open Storage and confirm it reports the old `backups/renames` size.
- Clean old filename-only backups after confirming renamed files are present.
- Rename a small copied batch using Manifest-only mode.
- Confirm the data folder grows only by a small amount.

# QuickScan v0.4.7.3 — Baseline and Verification

## Exact hashes

```text
Source SHA-256
4e7c7d6a66327de5b76a23d257bf1677bd12315f540b9339fde7a979c859e98a

Package SHA-256
470811b9819e9a9edceffa6d1a0c2520c0e1c6058d86141bad651dcd7b064a57
```

## Strict rename policy

Filename-only renames are manifest-only. The application may not create a second ZIP, image copy, or report copy for rename safety. Undo uses the same current file and refuses safely if that file is missing or changed.

## Tests performed from the final extracted package

- Python compile: PASS
- Complete inherited self-test chain: PASS
- v0.4.7.3 strict storage self-test: PASS
- Live scanner-created mod rename: PASS
- No `backups/renames` directory after rename: PASS
- JSONL manifest `backup_created=false`: PASS
- Empty database backup path: PASS
- Hash-verified Undo using same file: PASS
- Storage GUI fixed-policy text: PASS
- No backup-mode selector: PASS
- Package contains no uploaded user ZIPs/images: PASS

## Windows test still required

David should rename and undo a small copied set on the real D-drive installation, confirm the data folder grows only by small manifest/database records, and remove legacy rename backups after confirming the renamed ZIPs remain present.

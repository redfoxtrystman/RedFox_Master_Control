# JOB-04 Parts Manager v0.1.1 — vaulted working baseline

This vault preserves the exact user-supplied archive that was known to work by itself but conflicted with JOB-13 KoParts when both were loaded.

## Preserved archive

- Original user file: `JOB04_PartsManager_v0.1.1_UI_BOOT_FIX.zip CONFLICT WITH KOPARTS`
- Exact archive SHA-256: `e10cd85b6f05646bef4b1939263337038bb06d44692fbe49d06a196c822f876a`
- Exact archive size: `13,570 bytes`
- GitHub storage file: `JOB04_PartsManager_v0.1.1_UI_BOOT_FIX.zip.base64`

The GitHub connector available in this chat cannot write arbitrary binary bytes directly, so the exact ZIP bytes are stored losslessly as Base64 text. To restore the original ZIP, Base64-decode that file and save the result as `JOB04_PartsManager_v0.1.1_UI_BOOT_FIX.zip`. Verify the SHA-256 above before using it.

## Runtime status

- Known useful/working Parts Manager baseline when used by itself.
- Known conflict with JOB-13 KoParts when both were loaded together.
- Later delayed-loader experiments reduced startup contention but eventually stopped showing parts reliably, so v0.1.1 is the preferred functional baseline for any future revival.

## Future direction — do not implement yet

Owner suggested that the separate Parts Manager may eventually be better absorbed into the RedFox Used Car Lot / Service Shop instead of remaining a separate standalone module. That future design could reuse the dealership's planned repair/service workflow and potentially avoid the JOB-04 Parts Manager ↔ JOB-13 KoParts lifecycle conflict.

Possible future structure:

`Used Car Lot -> Service Shop -> Parts / Repair / Maintenance`

If revived, inspect the current RLS Part Inventory/repair APIs first, then decide whether to port the known-good v0.1.1 parts logic into the Service Shop rather than restarting the standalone Parts Manager.

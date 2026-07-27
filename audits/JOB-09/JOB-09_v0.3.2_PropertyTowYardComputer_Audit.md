# JOB-09 v0.3.2 — Property Tow-Yard Computer Audit

**Catalog job:** 19 — JOB-09-RedFox_TowRecoveryDispatch  
**Module:** `redfox_tow_recovery_dispatch`  
**Status:** BUILT — RUNTIME UNTESTED

## Reason for patch

David's v0.3.1 runtime test showed that the generated `Tow Yard 1` garage and generated Fleet Computer were not the correct architecture. A vehicle assigned to the artificial yard could be offered the normal RLS $5,000 delivery action from the actual Belasco service property computer, including the stock 120-second delivery delay.

## v0.3.2 correction

- Existing purchased/rented RLS property garage becomes the tow yard.
- Existing RLS property computer gains RedFox management actions through `onComputerAddFunctions`.
- No second artificial garage or Fleet Computer is registered by the active property bridge.
- A saved unlinked yard can be connected from the current property computer.
- A new tow-yard designation can be created from an eligible property computer.
- Old `redfox_towshop_*` owned-vehicle locations are migrated to the real property garage ID when linked.
- Same-property company assignment changes RedFox metadata without invoking RLS paid delivery or delay.
- Company-slot counts only include vehicles with `redfoxCompanyVehicle == true`, not every personal vehicle at the property.
- Tow-yard display names can be edited and persist.
- Five company slots and ten separate custody slots remain the defaults.

## Runtime boundary

No stock BeamNG Career or RLS files are included or modified. The patch changes only JOB-09's extension and documentation.

## Static verification

- Lua syntax/main-chunk local limit: PASS
- JSON parse: PASS
- Required property-computer hooks/markers: PASS
- Active artificial-garage registration disabled: PASS
- Protected path scan: PASS
- Direct per-frame log/write scan: PASS
- ZIP integrity: PASS

## Artifact

`19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_2_PropertyTowYardComputer.zip`

SHA-256: `c01965e54174572235a4c419c6b7557d58f6d7940435b2f43330c51f6cf8cee1`

Size: 237,789 bytes

## Focused runtime proof

1. Use the normal Belasco property computer.
2. Connect the saved tow yard to that property.
3. Reopen the computer and confirm Tow Yard Management appears.
4. Confirm the vehicle location is the real property garage ID, such as `servicestationGarage`.
5. Confirm no $5,000 same-property delivery or 120-second delay.
6. Rename the tow yard and confirm persistence after reload.

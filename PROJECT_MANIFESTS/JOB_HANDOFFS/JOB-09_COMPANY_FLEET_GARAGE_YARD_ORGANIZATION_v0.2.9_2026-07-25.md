# JOB-09 v0.2.9 — Company Fleet Garage and Yard Organization

**Date:** 2026-07-25  
**Module:** `redfox_tow_recovery_dispatch`  
**Status:** **BUILT — RUNTIME UNTESTED**

## Installable candidate

- File: `19-JOB-09-RedFox_TowRecoveryDispatch_v0_2_9_CompanyFleetGarageYardOrganization.zip`
- SHA-256: `6929f51ee22bf0d81d7e39cc69582ce38dbc6a7710c1a6db4642163072881bdc`
- Size: 159,875 bytes
- ZIP entries: 61
- Uncompressed bytes: 534,873
- Binary is not committed to GitHub; David receives it through the active ChatGPT artifact.

## Scope completed

### Company Fleet Garage

- Adds RedFox company work-truck storage separate from personal Career inventory and separate from recovered/impound inventory.
- Requires the current truck to match the selected Fleet Book model and exact stored configuration.
- Requires the truck to have a personal Career inventory ID.
- Saves a RedFox company record before attempting Career inventory removal.
- Calls the public Career inventory removal function and verifies the inventory record is gone.
- Blocks physical company retrieval when removal cannot be confirmed, reducing duplicate risk.
- Saves Fleet Book unit ID, name, RF call sign, role, model/configuration, paint, available Career configuration data, approximate part conditions, assigned map, and assigned tow yard.
- Retrieves a confirmed company truck physically at its assigned RedFox yard.
- Returns a retrieved truck to virtual company storage and refreshes available configuration, paint, and part-condition information.
- Adds event-level diagnostics:
  - `[RedFox][TOW][COMPANY_TRANSFER_AUDIT]`
  - `[RedFox][TOW][COMPANY_RETRIEVE]`
  - `[RedFox][TOW][COMPANY_RETURN]`

### Fleet Book organization

- Replaces the giant full-fleet scroll with a selected-unit previous/next view.
- Keeps technical details behind an open/close section.
- Adds a persistent next RF call-sign number, preventing future `count + 1` call-sign reuse after deletion.
- Company-stored units cannot have their Fleet Book identity record deleted while attached to a company asset.

### Recovered / Impound Yard organization

- Adds saved category filters:
  - All Yard Vehicles
  - Abandoned Vehicles
  - Lien / Unpaid
  - Police Impound
  - Disposition Eligible
  - Physically Retrieved
- Categories can overlap. For example, an abandoned vehicle can also be lien/unpaid and later disposition eligible.
- Adds text search across record ID, vehicle name/model/configuration, map, source, payer, yard, note, and categories.
- Adds sort modes for date, vehicle name, estimated value, and current lien.
- Adds compact rows with open/close details.
- Adds larger accent separators to distinguish records.
- Displays assigned yard, source, estimated value, stored time, billing days, storage rate, accrued storage, tow lien, current balance, physical/virtual state, and hold end.

### Tow History organization

- Adds text search and sort modes.
- Adds compact summaries with open/close detailed records.
- Adds stronger record separators.
- Existing history entries are preserved.

### Editable pricing and cost settings

Saved Settings now expose:

- abandoned recovery base charge;
- standard tow base charge;
- rolled-car recovery base charge;
- semi recovery base charge;
- multi-vehicle accident base charge;
- standard response and tow distance rates;
- heavy response and tow distance rates;
- additional-vehicle charge;
- storage daily rate;
- impound hold length;
- recovered-yard capacity;
- company-garage capacity;
- development direct-sale percentage.

### Development direct-sale payment test

- A disposition-eligible recovered vehicle can be prepared and confirmed for a direct development sale.
- Sale amount is a saved percentage of estimated vehicle value with a minimum floor.
- The payment is queued to the normal Career money path.
- The recovered-yard record is removed and a linked sale-history entry is created.
- Adds `[RedFox][TOW][YARD_SALE_AUDIT]`.
- This is only a payment/storage test. It is not marketplace, West Coast auction, or Copart integration.

## Static verification

- ZIP integrity: PASS
- Lua `loadfile` syntax and local-variable limit: PASS
- JSON parsing: PASS
- Protected Career/shared override path scan: PASS
- Per-frame log/save/UI-message spam scan: PASS
- Required feature scan: PASS

## Required first runtime test

1. Disable every older JOB-09 ZIP and enable only v0.2.9.
2. Back up the Career save and the BeamNG user-folder `settings/redfox/` directory.
3. Use a noncritical registered tow truck.
4. Select the matching Fleet Book unit and enter that exact truck.
5. Transfer it to Company Fleet Garage.
6. Verify it disappears from personal Career inventory and appears exactly once in Company Fleet Garage.
7. Save/reload and confirm there is no duplicate.
8. Retrieve it at its assigned tow yard, drive it, return it, save/reload, and retrieve it again.
9. Test yard filters/search/sorts and history search/sorts.
10. Change pricing settings and verify persistence.
11. Record Career money before/after one development direct sale and return the audit line.

## Runtime risks

- Exact Career inventory removal behavior can vary with the installed RLS build.
- Some custom truck configurations or part-condition tables may not reconstruct perfectly.
- An interruption between the separate RedFox save and Career save must be tested.
- WE UI text buffers and sort/search performance need testing with David’s large records.

## Deferred intentionally

- Invoice/receipt visual redesign.
- Shared Career-clock storage billing and old $75/day record migration.
- Marketplace, West Coast auction, Copart, public auction, salvage, or owner-release contracts.
- Cross-map company fleet relocation and port transfer.
- Semi-trailer classifier/coupling repair.
- New crash scenes and additional call categories.
- Website and phone registration.

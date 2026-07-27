# JOB-09 v0.3.2 Source Summary

## Runtime file changed

- `lua/ge/extensions/redfoxTowRecoveryDispatch.lua`

## Property-computer bridge

The extension now listens for RLS computer-menu construction through `M.onComputerAddFunctions(menuData, computerFunctions)`.

At an eligible property computer it adds one of:

- `Connect <saved yard name> to This Property`
- `Designate This Property as a Tow Yard`
- `<custom yard name> Management`
- `<custom yard name> Custody Inventory`

The callback closes the stock computer menu and opens JOB-09 management while retaining the real RLS computer and garage IDs.

## Saved yard fields

- `id`: permanent RedFox yard/business identity
- `name`: editable display name
- `rlsGarageId`: existing RLS property garage ID
- `rlsComputerId`: existing RLS property computer ID
- `rlsGarageName`: property display name
- `legacyGarageId`: previous v0.3.1 artificial `redfox_towshop_*` ID, retained only for migration
- `companyCapacity`: default 5
- `custodyCapacity`: default 10

## Vehicle behavior

- Normal owned vehicles remain in RLS inventory.
- Company identity is determined by `redfoxCompanyVehicle == true`, not merely by being located at a tow-yard property.
- A same-location assignment skips `moveVehicleToGarage`, avoiding stock paid delivery and the stock delivery timer.
- Old artificial locations migrate directly to the linked real property ID and save immediately.
- Custody vehicles remain separate JOB-09 records and do not become owned inventory vehicles.

## Deferred

- Business bank-account screen
- Business insurance
- Paid capacity expansions
- Dedicated boat/trailer/heavy storage routing
- Property liquidation
- Cross-map loaded transport
- Emergency-scene expansion

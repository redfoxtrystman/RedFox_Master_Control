# JOB-09 v0.3.1 — Source Summary

## User-confirmed design correction

Every RedFox tow yard is a garage location for **company-owned** trucks. Company vehicles remain normal owned RLS Career inventory vehicles. Abandoned, impound, lien, and customer-storage vehicles remain separate RedFox custody records.

## Main implementation

Runtime file:

`lua/ge/extensions/redfoxTowRecoveryDispatch.lua`

### Tow-shop garage registration

- Stable garage code: `redfox_towshop_<level>_<yard>`
- Stable matching computer code
- Per-Career generated `.sites.json` under `settings/redfox/`
- Heavy-sized parking spots
- Garage storage zone for normal RLS store/retrieve behavior
- Runtime injection into current-map `freeroam_facilities` garage and computer tables
- RLS `addPurchasedGarage` and `buildGarageSizes`
- Verification that RLS exposes purchased status and capacity data

### Company vehicle movement

- Uses the current RLS inventory ID
- Requires `owned ~= false`
- Calls RLS `moveVehicleToGarage`
- Re-reads and verifies destination and ownership
- Rolls back location and RedFox metadata when verification fails
- Adds Fleet Book ID, RF call sign, role, and assigned tow-shop code to the same RLS vehicle record
- Uses RLS `removeVehicleObject` only to store the physical object after the inventory move verifies
- Requests immediate Career save and My Vehicles refresh

### Reverse and undo

- Move back to recorded previous personal garage
- Current-map tow-shop-to-tow-shop movement
- One-step undo to the prior verified garage location
- Capacity checks before movement

### v0.3.0 recovery

- Old separate-company records are marked legacy
- Explicit recovery only
- Backup before recovery
- Reconnect original inventory record when present
- Otherwise reconstruct one owned RLS vehicle from saved model/config/paint/condition
- Verify the new owned record and destination before removing the obsolete RedFox record

## Capacity defaults

- Company garage slots: 5 per tow shop
- Universal RedFox custody slots: 10 per tow yard
- Untouched old 50/20 defaults migrate to 5/10
- Paid expansion and dedicated storage upgrades remain future work

## Deferred

- Cross-map relocation
- Shop sale/liquidation blocking
- Dedicated boat/trailer/heavy storage routing
- Lien claim conversion
- RLS Marketplace and used-car auction handoff
- Full paid Development Call Builder
- Invoice redesign
- Colored dispatch route arrows
- Additional crash scenes

## Runtime status

**BUILT — RUNTIME UNTESTED**
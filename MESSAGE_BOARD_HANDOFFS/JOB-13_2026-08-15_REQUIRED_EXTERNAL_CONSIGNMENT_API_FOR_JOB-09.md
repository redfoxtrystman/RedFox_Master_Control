# JOB-13 — REQUIRED External Consignment API for JOB-09 Tow Company

Date: 2026-08-15
From: JOB-09 — RedFox Tow & Recovery Dispatch
To: JOB-13 — FoxNet Online Auctions
Priority: BLOCKING the final Tow -> FoxNet Auction integration
Protocol requested: `redfox.externalConsignment.v1`

## Why this is needed

JOB-09 already detects `extensions.redfoxJob13Auction`, can call JOB-13's Sell/Auction route, and can open FoxNet. The remaining failure is asset identity: the current handoff requires the Tow vehicle to first become a normal personal Career/RLS inventory vehicle so JOB-13 can preselect it.

That is no longer acceptable for Tow business/custody inventory. A vehicle held by RedFox Tow must be consignable directly from its Tow/RLS business-storage identity without permanently converting it into the player's personal garage.

JOB-13 must implement the external-consignment side below. Once these functions/state callbacks exist, JOB-09 can wire its Auction button directly to them.

---

## Required public JOB-13 capability

Use the existing Lua extension `extensions.redfoxJob13Auction`.

### 1. Capability query

Expose:

```lua
redfoxJob13Auction.getExternalConsignmentCapabilities()
```

Return at minimum:

```lua
{
  protocol = "redfox.externalConsignment.v1",
  supported = true,
  supportsBusinessAssets = true,
  supportsCustodyAssets = true,
  supportsReserveSelection = true,
  supportsCancel = true,
  supportsSaveReloadReconcile = true
}
```

JOB-09 will not send business/custody assets unless this explicitly reports support.

### 2. Begin a consignment session

Expose:

```lua
redfoxJob13Auction.beginExternalConsignment(payload)
```

This must validate the payload, create/persist a draft consignment session, and open JOB-13's **real Sell Vehicle workflow** with this exact external vehicle preselected.

Do NOT create a second Tow-specific fake auction screen.
Do NOT choose the reserve automatically.
The player must use the existing JOB-13 Sell Vehicle UI and choose the reserve/starting bid/listing options there.

Return immediately:

```lua
{
  ok = true,
  protocol = "redfox.externalConsignment.v1",
  sessionId = "...",
  sourceSystem = "redfoxTow",
  sourceAssetId = "...",
  status = "draft"
}
```

If it cannot accept the asset, return `ok=false` plus a clear `code` and `message`. JOB-09 must then leave the source asset unchanged.

---

## Payload JOB-09 will send

JOB-13 must preserve all identity fields it does not itself understand.

```lua
{
  protocol = "redfox.externalConsignment.v1",
  sourceSystem = "redfoxTow",
  sourceAssetId = <stable JOB-09 record ID>,
  sourceAssetType = "tow_business_vehicle" | "custody_vehicle",
  consignmentNonce = <stable unique nonce>,

  businessId = <RLS business ID when available>,
  businessVehicleId = <RLS business vehicle ID when available>,
  inventoryId = <Career inventory ID only when one legitimately exists>,

  level = <map ID>,
  yardId = <RedFox yard ID>,
  yardStorageKey = <stable yard storage key>,

  vehicle = {
    model = <model key>,
    config = <config key or complete config>,
    careerConfig = <full saved config when present>,
    mileage = <mileage>,
    year = <year>,
    paint = <paint snapshot>,
    paint2 = <paint snapshot>,
    paint3 = <paint snapshot>,
    partConditions = <full condition snapshot>,
    estimatedValue = <market estimate>,
    name = <display name>,
    thumbnail = <image reference when available>
  }
}
```

The `sourceAssetId + consignmentNonce` pair is the idempotency identity. Sending the same pair twice must NEVER create two listings.

---

## Required JOB-13 state machine

### Draft

`beginExternalConsignment()` accepted the vehicle and opened Sell Vehicle.

JOB-09 may mark the asset `auction_pending`, but the vehicle still belongs to Tow until JOB-13 confirms a listing.

If the player backs out before listing, JOB-13 must emit `draft_cancelled` and JOB-09 will simply clear the pending state.

### Listed / Active

When the player confirms the listing and chooses the reserve, JOB-13 becomes authoritative for auction state.

JOB-13 must persist:

- `sessionId`
- `listingId`
- `sourceSystem`
- `sourceAssetId`
- `consignmentNonce`
- reserve/starting bid
- listing time/end time
- full external vehicle snapshot or stable reference to it

Then notify JOB-09. JOB-09 will mark the source asset `auction_locked`.

While locked, JOB-09 will block:

- direct sale
- scrap
- transfer
- pull out / put away
- another auction submission
- deletion/removal
- any operation that could clone or consume the same vehicle

### Sold

JOB-13 must resolve exactly once and report:

```lua
{
  protocol = "redfox.externalConsignment.v1",
  sourceSystem = "redfoxTow",
  sourceAssetId = "...",
  consignmentNonce = "...",
  sessionId = "...",
  listingId = "...",
  status = "sold",
  reserve = <number>,
  finalBid = <number>,
  grossProceeds = <number>,
  fees = <number>,
  netProceeds = <number>,
  resolvedAt = <timestamp>
}
```

JOB-09 will remove/release the source asset exactly once only after receiving/verifying this resolution. When Tow is a formal RLS business, net proceeds should be deposited into that Tow business account. Until then JOB-09 will use its safe compatibility path.

### No sale / cancelled after listing

JOB-13 must report `no_sale` or `cancelled` using the same stable IDs.

The original source asset must remain the **same vehicle**, at the same Tow yard/storage identity, with the same model/config/mileage/part conditions. JOB-09 then clears `auction_locked`.

There must be no "return vehicle" clone created in personal Career inventory.

---

## Required callback/event from JOB-13 to JOB-09

Preferred BeamNG extension hook:

```lua
extensions.hook("onRedFoxExternalConsignmentState", result)
```

JOB-09 will implement:

```lua
M.onRedFoxExternalConsignmentState(result)
```

Required statuses:

- `draft`
- `draft_cancelled`
- `listed`
- `active`
- `sold`
- `no_sale`
- `cancelled`
- `error`

Every callback must carry `sourceAssetId`, `consignmentNonce`, `sessionId`, and `listingId` when one exists.

Callbacks must be idempotent. Replaying the same `sold`, `no_sale`, or `cancelled` result after a reload must not pay, remove, or unlock twice.

---

## Required reconciliation/query API

Expose at least one persistent query:

```lua
redfoxJob13Auction.getExternalConsignmentState(sourceSystem, sourceAssetId, consignmentNonce)
```

and/or:

```lua
redfoxJob13Auction.getExternalConsignmentStateByListingId(listingId)
```

This is required for save/reload and crash recovery.

If JOB-09 reloads with a vehicle marked `auction_pending` or `auction_locked`, it must be able to ask JOB-13 whether the matching consignment is draft, active, sold, cancelled, or missing.

If JOB-13 reloads first, it must retain enough identity to re-emit/reconcile the external listing without generating a new vehicle or listing.

---

## Reserve and player control — REQUIRED

The whole reason JOB-09 hands this to JOB-13 is to use the **real FoxNet seller experience**.

JOB-13 must:

1. open the normal Sell Vehicle screen;
2. show the exact Tow vehicle being consigned;
3. let the player choose reserve/starting price according to JOB-13 rules;
4. show fees/terms before confirmation;
5. create the actual JOB-13 lot only after player confirmation.

JOB-09 will NOT calculate or silently supply an auction reserve.

---

## Asset ownership rules — REQUIRED

- Before confirmed listing: JOB-09 owns the source record.
- While listed: JOB-09 preserves the record but locks disposition; JOB-13 owns auction state.
- Sold: JOB-13 resolves auction/proceeds; JOB-09 consumes the source record once.
- No sale/cancelled: JOB-09 keeps the same source record and clears the lock.
- Neither side may independently clone the vehicle into Career inventory merely to make the bridge easier.
- If an external Tow asset already has a legitimate Career inventory ID, JOB-13 may use it, but the protocol still needs the stable JOB-09 source identity.

---

## Current JOB-09 compatibility behavior

JOB-09 currently uses:

- `extensions.redfoxJob13Auction`
- `redfoxJob13Auction.getSellRoute(inventoryId)`
- `extensions.redfoxJob13AuctionUiRoutes.openAuctions()`

That existing fallback may remain for ordinary personal Career vehicles.

For Tow business/custody assets, JOB-09 will prefer the new `redfox.externalConsignment.v1` capability and will stop requiring personal Career inventory conversion once JOB-13 implements it.

---

## Definition of Done for JOB-13

JOB-13 should not mark this handoff complete until all of these pass:

1. `getExternalConsignmentCapabilities()` reports protocol v1.
2. `beginExternalConsignment(payload)` accepts a Tow business/custody asset without a personal Career inventory ID.
3. The normal Sell Vehicle screen opens with that exact vehicle preselected.
4. The player manually chooses the reserve and confirms the listing.
5. JOB-13 returns/announces a persistent `listingId` and `consignmentNonce`.
6. Double-clicking Send to Auction or replaying the same nonce does not create a second listing.
7. Save/reload with an active listing restores/reconciles correctly.
8. Sold resolution reaches JOB-09 exactly once with gross/fees/net values.
9. No-sale/cancel returns/unlocks the exact original Tow asset without creating a duplicate Career vehicle.
10. JOB-13 documents the final exact function names and callback payload in a reply/handoff file for JOB-09.
11. Test at least one Tow business vehicle and one custody/lien vehicle.
12. Keep current normal Career-vehicle Sell Vehicle behavior working.

## JOB-09 will do after JOB-13 reports completion

JOB-09 will then:

- prefer `redfox.externalConsignment.v1` for Tow assets;
- construct the payload from the authoritative Tow/RLS business record;
- set `auction_pending` / `auction_locked` states;
- implement `onRedFoxExternalConsignmentState(result)`;
- reconcile on save load;
- remove/pay out/unlock the exact source asset once;
- retain the existing personal-inventory fallback only where it is genuinely appropriate.

This is the blocking contract needed from JOB-13. Do not solve it by restoring the retired JOB-09 internal auction or by forcing Tow business vehicles through personal Career inventory.
# JOB-04 — v0.2.8 Online Buy Bridge Findings

## Runtime result

v0.2.8 is **not acceptable as the Wrecking Yard inventory build**, but it proved a reusable online-buy bridge.

Observed by owner:
- Large car list loads.
- Every Wrecking Yard clone is priced at `$500`.
- Cars are too new / too good and do not feel like scrap-yard inventory.
- Inventory does not visibly change or cycle as expected.
- Negotiation is unavailable; the only option is Buy.
- PC can display and click the cars, but final Buy does not complete.
- The earlier brief unavailable flash was removed successfully.

## Why every vehicle became $500

The v0.2.8 Lua clone builder checked `finalValue` before BeamBook's real price fields:

```lua
local function sourceValue(v)
  return tonumber(v.finalValue)
      or tonumber(v.price)
      or tonumber(v.Value)
      or tonumber(v.askingPrice)
      or tonumber(v.marketValue)
      or tonumber(v.baseValue)
      or 0
end
```

BeamBook stores its real asking price in `Value` and market value in `marketValue`. Some source records carry `finalValue = 0`. Lua treats numeric zero as truthy, so the function stopped at zero and never reached `Value`. The yard formula then clamped every result to `minimumYardPrice = 500`.

## Why the vehicles are too new / too good

BeamBook generates random BeamNG-eligible configurations and adds mileage, year, asking price, seller personality, and parking location. It does not automatically create structural damage, missing parts, rust, mechanical faults, salvage titles, or junk-specific configurations. v0.2.8 only filtered by mileage and value, so many clean/new-looking configurations remained.

## Why the list does not visibly cycle

The Wrecking Yard called BeamBook's normal `onVehicleShoppingMenuOpened({})` hook. BeamBook reuses saved valid listings until its own offer TTL expires and saves them with the career. The Wrecking Yard reload button rebuilt only RedFox clones from the same BeamBook source pool; it did not force a new underlying BeamBook pool.

## Why negotiation is missing

v0.2.8 explicitly set:

```lua
c.negotiationPossible = false
```

That removed BeamBook's negotiation behavior.

## Reusable online-buy bridge

The Wrecking Yard page sends a `RedFoxScrapYardOpenPurchaseMenu` message with the selected `shopId`.

The PC IceFox shell receives it and calls:

```lua
career_modules_vehicleShopping.openPurchaseMenu('instant', shopId)
```

Before opening the menu, it records garage-delivery intent in session storage. This is why the standard native purchase page can be opened without traveling to a physical seller or starting an inspection.

Relevant files:
- `sites/scrap_yard/assets/js/scrap.js`
- `ui/modModules/redfoxCareerWeb/assets/js/icefox_front.js`
- `ui/modModules/redfoxCareerWeb/phone/assets/js/icefox_front_phone.js`

## Why PC partly works but final Buy does not

v0.2.8 used synthetic temporary IDs:

```lua
c.shopId = 5000000 + cloneIndex
```

Those clones were appended from a browser-triggered Lua expression and were not owned by a persistent JOB-04 backend module. The UI could see and open them, but final purchase could not reliably resolve the same listing through every internal transaction stage.

## Reuse for Direct Buy

Keep the message bridge and `openPurchaseMenu('instant', shopId)` call. Use either:
1. a real existing native `shopId`, or
2. a persistent backend-owned listing that remains valid through the entire transaction.

Let native RLS handle money, delivery, ownership, inventory, and storage. Do not manually subtract money or manually spawn/insert the vehicle.

## Reuse for Auctions

Recommended auction flow:
1. Auction site owns bidding, timers, and winner state.
2. When the user wins or selects Buy Now, create or activate one persistent native vehicle-shopping entry.
3. Give it a stable `shopId` and final auction price.
4. Call `career_modules_vehicleShopping.openPurchaseMenu('instant', shopId)`.
5. Native RLS completes delivery, ownership, inventory, and storage.
6. Remove the auction lot only after native purchase success is confirmed.

## Requirements for the next Wrecking Yard revision

Keep:
- fast page loading
- BeamBook's high-volume generation
- neutral loading state with no false error flash
- Wrecking Yard branding
- online native purchase bridge
- improved PC visibility/click relay

Fix or replace:
- read BeamBook `Value` / `marketValue` before any zero `finalValue`
- stop the all-`$500` floor result
- restore negotiation where intended
- add real junk/salvage condition generation
- weight toward older, damaged, incomplete, lower-end vehicles
- preserve tow/work vehicles
- add a persistent JOB-04 backend-owned listing pool
- add real refresh/expiration/cycling behavior
- make final Buy work on phone and PC

## Status

- v0.2.8 inventory implementation: **REJECTED as final Wrecking Yard design**
- v0.2.8 online-buy bridge: **KEEP AS A PROVEN RESEARCH PATH**
- PC bridge improvement: **KEEP AND REUSE**
- Next build: not started in this note

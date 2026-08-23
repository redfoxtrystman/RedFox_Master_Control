# JOB-13 Handoff — Auction Expansion into Working Car Lot / Dealership

Date: 2026-08-23
From: JOB-09 — RedFox Tow & Recovery Dispatch
To: JOB-13 — FoxNet Online Auctions / Car Lot expansion
Status: OWNER-DIRECTED EXPANSION HANDOFF

## Owner direction

The existing Auction work is being expanded into a working used-car lot / dealership. The Auction chat should own and design that expansion while preserving the existing FoxNet Auction work.

Do not merge JOB-09 Tow runtime/state into JOB-13. Tow should provide vehicles to the dealer through a stable handoff/API. The car lot should own its own inventory, business state, sales, financing, customers, storage capacity, and repo-default state.

## Existing required Tow -> Auction contract

Keep and build on the existing handoff:

`MESSAGE_BOARD_HANDOFFS/JOB-13_2026-08-15_REQUIRED_EXTERNAL_CONSIGNMENT_API_FOR_JOB-09.md`

Protocol requested there: `redfox.externalConsignment.v1`

That contract remains important for direct Tow/custody vehicle auctioning without forcing the vehicle through the player's personal garage.

## Critical storage lesson from JOB-09

Do NOT implement dealer inventory as ordinary personal Career garage storage.

JOB-09 just proved why this is wrong: tagging/moving normal Career inventory vehicles to a Tow Yard still causes them to appear in normal personal garages and consume personal garage capacity.

The car lot needs its own authoritative dealer/business inventory and its own logical capacity. Vehicles may retain a legitimate Career inventory ID where useful, but they must not consume personal garage slots merely because they are dealer stock.

Dealer stock needs to behave like a real business-owned asset:

- visible in the dealer/car-lot UI;
- not counted against personal garage capacity;
- can be physically retrieved/spawned when needed;
- can be edited/repaired/painted/configured through normal garage/tuning workflows where supported;
- can be listed for sale;
- sale proceeds go to the dealer/business account;
- save/reload preserves exact vehicle identity/configuration/condition;
- no clone-on-transfer shortcuts.

## Car lot core concept

Start with a dealer inventory capacity of **10 vehicles**.

Allow paid expansion over time up to **100 vehicles**.

Capacity should be dealer/business capacity, not personal garage space.

The dealer may eventually have a physical lot/garage, but the authoritative vehicle record should be backend business inventory so physical rendering can be proximity-budgeted later.

## Vehicle acquisition sources

The car lot should be able to receive vehicles from multiple sources:

1. **Tow Yard / JOB-09**
   - disposition-eligible abandoned vehicles;
   - unpaid tow vehicles after legal disposition;
   - other Tow-owned vehicles the player elects to transfer/sell to the dealer;
   - direct transfer must preserve exact vehicle identity and condition.

2. **FoxNet Auction / JOB-13**
   - player buys a vehicle at auction and chooses the car lot/dealer as the destination;
   - external auction purchases should be able to land directly in dealer stock without consuming personal garage capacity.

3. **Personal ownership**
   - player may contribute/transfer a personally owned vehicle into dealer inventory with no automatic purchase/sale payment;
   - if the dealer later sells it, the dealer/business gets the proceeds;
   - if transferred back to personal ownership before sale, it becomes a personal asset again.

4. **Future dealer sourcing**
   - trade-ins;
   - wholesale purchases;
   - fleet liquidations;
   - repo returns;
   - possible direct NPC seller acquisitions.

## Sale model

Vehicles should sell **slowly over time**, not instantly.

The owner wants the car lot to feel like an actual dealership/business. Suggested factors for sale chance/time:

- asking price relative to market value;
- vehicle condition;
- mileage;
- desirability / vehicle class;
- age;
- dealer reputation / upgrades later;
- inventory age / days on lot;
- optional advertising/promotions later.

The player should be able to set/list a price. The system may suggest a market-based price, but the player should retain control.

When sold:

- remove exactly the dealer-owned vehicle once;
- pay dealer/business bank account once;
- write a sales/receipt/ledger record;
- preserve price, buyer/finance status, fees, and profit information for history.

## Dealer business bank

The dealership should use a real RLS-backed business bank/account if practical, following the same principle as JOB-09's RedFox Tow business account.

Needed behavior:

- car-lot sales deposit to dealer business account;
- auction purchases paid from the appropriate player/business source selected by design;
- player can transfer money between personal and business account through the native RLS Bank where supported;
- no fake parallel money balance if the real RLS bank can be used.

## Customer financing / loans

The owner wants the dealer to offer vehicle financing.

A customer may buy a car using a dealer-originated loan/payment plan.

Track at minimum:

- vehicle sold;
- sale price;
- down payment;
- financed principal;
- payment amount/cadence;
- balance remaining;
- payment history;
- missed payments;
- delinquency/default state;
- stable customer/loan ID;
- original vehicle identity for repo linkage/history.

Dealer receives payments over time according to the finance model.

## Repo integration from dealer defaults

If a financed buyer stops paying, the dealer can generate a **Repo job**.

Preferred architecture:

Dealer/JOB-13 creates a stable repo request -> RedFox integration/Tow provider accepts it -> JOB-09 runs the actual repo/recovery gameplay -> recovered vehicle returns to dealer inventory or designated Tow/holding destination according to the contract.

Do not make the dealer secretly duplicate/spawn a replacement vehicle after repo. Preserve one asset lifecycle.

Repo request should include enough data for JOB-09 to identify/reconstruct the actual financed vehicle and destination:

- loan ID;
- dealer business ID;
- dealer asset/vehicle ID;
- vehicle snapshot/reference;
- debtor/customer ID;
- pickup map/location or procedural target information;
- return destination;
- repo fee/reward rules;
- idempotency nonce.

On successful repo:

- loan becomes repossessed/default-resolved;
- recovered vehicle becomes dealer stock again;
- dealer may relist/resell it;
- Tow gets the agreed repo service payout through its own business system;
- no duplicate vehicle is created.

## Car lot UI / garage expectations

The car lot should have a real inventory browser similar to normal BeamNG/RLS garage views:

- vehicle preview image;
- year / make / model / config;
- mileage;
- condition/value;
- acquisition source and cost;
- asking price;
- days/time on lot;
- financed/sold/reserved status where relevant.

Needed actions over time:

- retrieve/spawn;
- repair;
- paint;
- parts/configuration upgrades;
- rename / plate where appropriate;
- set sale price;
- list/unlist;
- send to auction;
- transfer to/from personal or another business where supported;
- view profit/cost basis.

The same exact business asset must remain authoritative across these actions.

## Physical lot later

The owner wants a **big garage/lot** capable of scaling to 100 stored vehicles.

Do not keep 100 fully simulated BeamNG vehicles alive.

Use backend inventory as authoritative. Later physical display should use a budgeted approach:

- only nearby/selected vehicles become full simulated vehicles;
- other stock remains records or lightweight/static/parked representations;
- approaching the lot can hydrate selected nearby inventory;
- leaving the area can dehydrate/despawn while retaining exact saved state.

This is the same memory-safety principle JOB-09 plans for physical impound lots.

## Tow -> Car Lot transfer requirement

JOB-09 will eventually need a clean direct action such as:

`Send to Car Lot`

for eligible Tow-owned/disposition vehicles.

The transfer should be transactional:

1. JOB-09 presents exact source asset identity/snapshot.
2. JOB-13 validates capacity and acceptance.
3. JOB-13 creates/persists dealer asset.
4. JOB-13 returns success with stable dealer asset ID.
5. Only then JOB-09 removes/releases the Tow source record.
6. If any step fails, original Tow asset remains unchanged.

Idempotency is mandatory. Repeating the same transfer request after lag/reload must not create duplicate dealer stock.

Suggested future protocol:

`redfox.externalDealerTransfer.v1`

Do not finalize exact function names until JOB-13 reviews its current source and existing auction architecture.

## Interaction with Auction

Auction and Car Lot should complement each other:

- Tow vehicle -> Auction directly via `redfox.externalConsignment.v1`;
- Tow vehicle -> Car Lot inventory;
- Car Lot vehicle -> FoxNet Auction;
- Auction purchase -> Car Lot inventory;
- no personal-garage conversion required for business assets.

The auction remains the fast/competitive sale channel; the car lot is the slower retail channel with potentially higher margins and financing risk.

## Ownership/accounting rule

Who owns the vehicle at the moment of sale determines who gets the money.

Examples:

- personal vehicle transferred to dealer, then dealer sells -> dealer business account gets proceeds;
- dealer vehicle transferred back to personal, then personally sold -> personal account gets proceeds;
- Tow disposition vehicle transferred to dealer -> dealer owns it after confirmed transfer; subsequent retail/auction sale belongs to dealer;
- direct Tow auction consignment -> proceeds follow the existing Tow/Auction consignment contract and should go to Tow business account.

Transfers between player and owned businesses do **not** automatically create purchase/sale income unless the player explicitly performs a sale transaction.

## Current JOB-09 state relevant to dealer work

Current Tow development baseline at this handoff: v0.5.0.35.

Important current findings:

- RedFox Tow now has a real RLS-backed business bank/account.
- Tow Company Computer is now RedFox-owned and can display Fleet Book/Career records plus custody/impound and bank state.
- JOB-09 is actively replacing the incorrect personal-garage-backed company storage with true business/Tow Yard storage so company vehicles stop consuming personal garage capacity.
- Tow custody categories include abandoned/hold, unpaid tow, police impound, recovered/other, and disposition eligibility concepts.
- Tow intends automatic abandoned-vehicle custody/hold and direct business disposition paths.
- Any future Tow->Dealer transfer must use the authoritative Tow business/custody record after this storage work stabilizes; do not build against the temporary personal-garage workaround.

## Source-first requirement for JOB-13

Before implementing the dealer:

1. inspect the current working JOB-13 Auction archive/source;
2. inspect the existing `redfox.externalConsignment.v1` handoff;
3. inspect exact paid RLS 2.7.0.1 businessInventory/businessManager/bank/garage APIs relevant to independent business storage;
4. determine whether an existing RLS business type can be safely extended or whether JOB-13 needs its own dealer business module;
5. preserve Auction behavior while adding dealer capability;
6. do not edit RLS source files unless the owner explicitly approves it;
7. keep dealer inventory independent of personal garage capacity;
8. validate save/reload, duplicate protection, business-account payout, and vehicle identity before broad migration.

## Definition of first usable Car Lot build

A first meaningful version should prove this vertical slice:

1. Car Lot business exists with its own account/state.
2. Capacity starts at 10.
3. Player can add one personally owned vehicle to dealer inventory without money changing hands and without consuming a personal garage slot afterward.
4. Player can add one auction-acquired vehicle directly to dealer inventory.
5. Player can receive one Tow-transferred vehicle through a safe test adapter or mocked handoff if JOB-09's final storage API is not ready yet.
6. Dealer UI shows vehicle card/image/details.
7. Vehicle can be retrieved and edited/repaired/painted/configured through supported garage workflow.
8. Vehicle can be listed at a player-selected price.
9. Simulated buyer can purchase it after a non-instant delay.
10. Sale proceeds go to dealer business account exactly once.
11. Save/reload preserves dealer inventory and listings.
12. Capacity upgrade can increase beyond 10 without touching personal garage capacity.

Financing/repo can follow after this dealer-inventory/sales vertical slice is stable, but its IDs/data model should be planned from the beginning so sold financed vehicles can later generate repo work cleanly.

## Separation rule

JOB-13 owns Auction + Car Lot/Dealer functionality.
JOB-09 owns Tow/Recovery/Impound gameplay.

They should communicate through stable transfer/consignment/repo contracts rather than sharing save tables or directly mutating each other's internal state.

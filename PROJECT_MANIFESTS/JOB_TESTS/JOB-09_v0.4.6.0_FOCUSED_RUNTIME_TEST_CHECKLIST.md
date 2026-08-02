# JOB-09 v0.4.6.0 Focused Runtime Test

## Install

1. Close BeamNG completely.
2. Disable/remove every older JOB-09 ZIP.
3. Install only v0.4.6.0.
4. Use West Coast USA and the disposable test save.
5. Confirm the RedFox tow yard is linked to an owned RLS garage with at least one free slot.

## Public website

1. Open the RedFox Tow website.
2. Confirm the public front page appears first.
3. Press **Request Tow** and choose a service tile.
4. Press **Dispatch Selected Service**.
5. Confirm the Company Portal opens to Dispatch and a real JOB-09 call/offer is requested.
6. Separately test **Tow My Current Vehicle** on an owned Career vehicle.

## Company portal

Confirm these sections open and use live state rather than the old demo values:

- Overview
- Dispatch Center
- Scene Manager
- Records & History
- Tow Yard Inventory / Company Assets
- Company Fleet
- Tow Yard Management
- Invoices
- Settings & Tools

## Immediate native claim—the critical test

Use a new disposition-eligible custody vehicle.

1. Open **Tow Yard Inventory**.
2. Confirm the claim button reads **Claim & Create Career Vehicle**.
3. Open it and confirm the modal shows the exact linked owned RLS garage.
4. Press **Create Career Vehicle** once.
5. Do not press it again, change maps, buy/sell another car, or open a dealership during native registration.

Expected result:

- one Career inventory ID is created;
- native parts/originalParts/changedSlots complete;
- insurance recognizes the vehicle, including a valid uninsured state;
- the vehicle is stored in the exact linked RLS garage;
- the custody record disappears only after verification;
- the Tow Company Assets list keeps one record with the same Career inventory ID;
- the acquisition cost is charged once, after successful native verification;
- save/reload preserves both Career inventory and RedFox company metadata;
- no separate **Deliver to Linked RLS Garage** step is required for the new claim.

## Failure gate

At the first failure:

1. Do not repeat the button.
2. Close BeamNG normally if possible.
3. Preserve the newest `beamng.log`.
4. Record the custody ID, shop ID, and Career inventory ID shown.
5. Confirm whether money was charged and whether the custody record remained.

Expected safe failure: no acquisition charge, custody remains, and no duplicate native vehicle. If a native ID remains, both records should lock for review rather than creating another vehicle.

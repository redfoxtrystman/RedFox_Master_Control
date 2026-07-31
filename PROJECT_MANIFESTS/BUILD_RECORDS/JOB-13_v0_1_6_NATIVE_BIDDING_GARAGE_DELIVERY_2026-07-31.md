# JOB-13 v0.1.6 — Native bidding and Career garage delivery

Owner order: use existing RLS/West Coast auction bidding and the game's existing delivery-to-garage purchase path. Do not invent another transaction or garage system.

Artifact: `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_6_NATIVE_BIDDING_GARAGE_DELIVERY.zip`

SHA-256: `8fa86d6fa09287bd07ba97dd4281362e8c05950b31bfd57da5dfc0f2cc39cce4`

Branch records: `JOB13_SOURCE/v0_1_6/`

Result:

- v0.1.5 rejected and replaced;
- unauthorized LIVE lock removed;
- fake TEST wallet/invoice/transit/garage system removed;
- fixed pool built before page entry;
- three RLS-confirmed native configurations cycled across 12 lots;
- player/NPC timed proxy bidding enabled;
- winner submitted through silent `vehicleShopping` instant purchase;
- `makeDelivery=true` delegates payment, inventory, spawn, delay, garage selection and move-to-garage to RLS/BeamNG;
- no other website or shared core paths included beyond the two Auction page mirrors;
- fresh-ZIP static and behavior harnesses passed;
- BeamNG runtime remains unproven.

No next build until David records the exact v0.1.6 runtime result.

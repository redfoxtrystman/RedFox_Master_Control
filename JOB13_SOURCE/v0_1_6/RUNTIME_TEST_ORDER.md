# JOB-13 v0.1.6 runtime test order

1. Remove every older JOB-13 ZIP, especially rejected v0.1.5.
2. Install only `RedFox_JOB13_FoxNet_Online_Auctions_v0_1_6_NATIVE_BIDDING_GARAGE_DELIVERY.zip`.
3. Clear BeamNG WebUI cache and fully restart BeamNG.
4. Enter Career mode with at least one owned garage slot available.
5. Open FoxNet Auctions and time the first 12-lot display.
6. Confirm the page does not remain on LOADING and does not show zero lots.
7. Activate Standard membership and confirm Career cash decreases by the configured fee.
8. Open one lot, place a bid or confidential maximum, and confirm NPC bidding/history.
9. Use WEUI Auction Clock controls only if needed to close the lot quickly.
10. If the player wins, confirm the exact auction total is deducted and the game delivers the vehicle to an owned garage.
11. Record the first failure and preserve `beamng.log`; do not build v0.1.7 before this result.

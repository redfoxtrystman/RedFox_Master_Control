# PKVault Shop — Development Checklist

## 1. Navigation and shell
- [x] Add SHOP to the existing top-level PKVault navigation.
- [x] Add native BUY / SELL mode control matching the locked screenshots.
- [ ] Verify route restoration after Reload all data & saves.
- [ ] Verify scaling at PKVault's supported UI zoom values.

## 2. PKVault-only economy boundary
- [x] BUY uses only the PKVault Pokédollar Bank.
- [x] BUY deposits only into the central PKVault Item Bank.
- [x] SELL removes only from the central PKVault Item Bank.
- [x] SELL proceeds go only to the PKVault Pokédollar Bank.
- [x] No direct save/game source, destination, or wallet controls.
- [ ] Prove Shop persistence cannot commit unrelated Pokémon save edits.

## 3. Catalog and pricing
- [x] Server-authoritative Shop service/controller.
- [x] Initial canonical price table.
- [ ] Expand canonical prices to every safely supported official item.
- [ ] Add reviewed canonical prices for fangame-only items where needed.
- [x] Distinct BUY and SELL values.
- [ ] Backend-enforce protected/non-sellable items.
- [ ] Add price-table regression tests.

## 4. Assets and item identity
- [x] Reuse PKVault/PKHeX item sprite pipeline.
- [ ] Do not generate duplicate artwork for official items.
- [ ] Generate art only for genuinely missing custom/fangame items.
- [x] Use Pokédollar text/symbol rather than a generic coin asset.
- [x] Normalize known equivalent item keys.
- [x] Alias-aware search.
- [ ] Expand alias table as compatibility profiles grow.

## 5. Filters and discovery
- [x] Search.
- [x] Category filtering.
- [x] Sort controls.
- [x] Single lower-left Compatible only toggle.
- [x] Compact compatibility badges/tooltips.
- [x] Show In PKVault ownership.
- [x] Show Total ownership across loaded sources for information only.

## 6. Quantity controls
- [x] Minus button.
- [x] Editable numeric field.
- [x] Plus button.
- [ ] Clamp BUY quantities to available funds / valid transaction limits.
- [ ] Clamp SELL quantities to owned sellable count.
- [ ] Reject invalid negative, zero, overflow, and stale quantities server-side.

## 7. BUY basket
- [x] Add/remove lines.
- [x] Editable basket quantities.
- [x] Independently scrollable basket.
- [x] Total cost.
- [x] Current / remaining bank balance.
- [x] Remember BUY basket and UI state.
- [ ] Final transaction confirmation pass.
- [ ] Atomic persistence + rollback verification.

## 8. SELL basket
- [x] Add/remove lines.
- [x] Editable basket quantities.
- [x] Independently scrollable sale basket.
- [x] Total proceeds.
- [x] Current / after-sale bank balance.
- [x] Remember SELL basket and UI state.
- [x] No duplicate-selling helper.
- [ ] Final transaction confirmation pass.
- [ ] Atomic persistence + rollback verification.

## 9. Transaction isolation
- [x] Shop transaction gate.
- [x] Apply Shop item/money delta to committed Shop state.
- [x] Attempt rollback if persistence fails.
- [ ] Regression test with unrelated pending Pokémon/storage edits present.
- [ ] Regression test crash/restart immediately after BUY.
- [ ] Regression test crash/restart immediately after SELL.
- [ ] Verify repeated reload cannot double-apply a completed transaction.

## 10. Alpha51 Shop test build
- [x] Apply first Shop prototype patch over alpha50.
- [x] Dedicated SHOP-TEST packaging planned separately from CLEAN.
- [x] Seed PKVault Pokédollar Bank to approximately ₽50,000 (exactly ₽50,000 in test seed).
- [x] Fill Storage / Item Bank Box 1 with 30 varied random-ish official item stacks.
- [x] Keep CLEAN artifact completely unseeded.
- [x] CI compile/frontend checks pass.
- [x] Download and package-smoke-test generated alpha51 SHOP-TEST artifact (seed files and executable present).
- [ ] Verify BUY, SELL, scrolling, remembered baskets, aliases, and persistence in the packaged Windows build.


## Alpha51 package verification
- [x] Successful GitHub Actions build completed for the alpha51 Shop line.
- [x] SHOP-TEST artifact contains the Windows executable.
- [x] Package verification: ₽50,000 seed file is present and exact.
- [x] Package verification: 30 item stacks are present in Item Bank / Storage Box 1, slots 0–29.
- [x] All 30 seeded item records identify Box 1.
- [ ] Launch the Windows executable and perform hands-on BUY/SELL transaction testing.


## Alpha51c route fix
- [x] Register ShopController in CoreRouter's static controller registry.
- [x] CI asserts CoreRouter contains typeof(ShopController).
- [x] Successful alpha51c CI rebuild after route registration fix.
- [ ] Hands-on verify GET /api/shop and BUY/SELL requests in the Windows test build.


## Alpha51d desktop JSON bridge fix
- [x] Diagnose GET /api/shop reaching CoreRouter successfully but failing in HybridWebView response serialization.
- [x] Register ShopStateDTO / ShopItemDTO in RouteJsonContext for desktop response serialization.
- [x] Register ShopTransactionRequestDTO / ShopTransactionLineDTO for BUY/SELL body binding.
- [x] Add a CI runtime smoke test that serializes ShopStateDTO and deserializes a Shop transaction payload through RouteJsonContext.
- [x] Alpha51d CI completed successfully with the Shop JSON bridge smoke test passing.
- [ ] Hands-on verify the corrected Windows Shop page loads without the red query error.

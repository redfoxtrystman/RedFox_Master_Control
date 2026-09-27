# PKVault Shop — Locked Visual Reference

These screenshots are the approved visual baseline for the real PKVault Shop.

- `PKVault_SHOP_BUY_LOCKED_REFERENCE.jpg` — **this is how BUY mode should look.**
- `PKVault_SHOP_SELL_LOCKED_REFERENCE.jpg` — **this is how SELL mode should look.**

The images are design references, not bitmap UI assets. Implement the interface with PKVault's existing components, layout system, item sprites, and icon pipeline.

## Locked design decisions

- Shop is PKVault-only: BUY deposits into the central PKVault Item Bank and spends the PKVault Pokédollar Bank; SELL removes only from the central PKVault Item Bank and pays only into the PKVault Pokédollar Bank.
- No direct buy-to-save, sell-from-save, wallet selectors, destination selectors, or save-money overflow logic in Shop.
- Moving items between PKVault and game saves remains the job of Storage/Inventory.
- BUY and SELL are sibling modes and each remembers its own basket/state.
- One `Compatible only` switch, in lower-left Shop Settings only.
- No Sell Duplicates helper or duplicate-selling assistant.
- Center catalog and right cart/sale basket scroll independently.
- Quantity uses minus + editable numeric field + plus.
- Show `In PKVault` plus cross-loaded-save `Total` ownership.
- Search recognizes aliases such as `Poke Ball`, `Poké Ball`, and `pokeball`.
- Keep compatibility badges compact.
- Non-sellable/protected items are enforced by backend rules.
- Use canonical PKVault buy/sell prices and the Pokédollar symbol.
- Reuse existing official item icons. Generate new item artwork only when a real item has no usable asset.
- Shop transactions must commit only their own item/money changes and must not save unrelated Pokémon-game edits or unrelated pending PKVault actions.

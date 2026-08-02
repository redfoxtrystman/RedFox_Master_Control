# JOB-09 v0.4.7.0 Focused Runtime Test

## Install

1. Close BeamNG completely.
2. Disable/remove every older JOB-09 ZIP.
3. Install only v0.4.7.0.
4. Clear BeamNG cache if the old page still appears.
5. Load West Coast USA Career.

## Public website

- Open the RedFox Tow app.
- Confirm Home loads with purple/orange RedFox colors.
- Open About, Services, Fleet, Locations, Gallery, Reviews, FAQ, News, Shop, Cart, and Contact.
- Confirm every page can return to Home.

## Critical dropdown test

- Click Services. The menu must be visible in front of the hero/photo area.
- Select all eight service entries at least once.
- Click Fleet and select each truck class.
- Click Locations and select each location.
- Test the same menus after scrolling and at a smaller app/window size.
- FAIL if the menu is invisible but clickable below its apparent position.

## Gallery and photos

- Filter All, Light Duty, Heavy Recovery, and Fleet & Yard.
- Open several photos in the lightbox and close it.
- Replace one placeholder JPG with a screenshot using the exact filename and verify it changes after reload/cache clear.

## Fake shop

- Add each demo product to cart.
- Open Cart and verify quantity/total.
- Remove an item, clear cart, and run Demo Checkout.
- Confirm no Career money changes.

## Public tow actions

- Open Request Tow from Home.
- Test Tow My Current Vehicle.
- Test one generated service request.
- Confirm the Company Dispatch Center receives the request.

## Company side regression

- Open Company Portal.
- Check Dispatch, Scenes, Records, Inventory, Fleet, Yards, Invoices, and Settings.
- Confirm the post-tow summary still appears after a completed tow.
- Confirm the native claim modal still opens for an eligible custody vehicle.

## Evidence on failure

Preserve the newest `beamng.log`, a screenshot of the visible page, the exact button/menu used, and whether the old page appeared despite cache token 0470.

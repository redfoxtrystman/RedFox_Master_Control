# JOB-09 v0.4.4.8 Focused Runtime Test Checklist

## Install

1. Back up the Career save and `settings/redfox/`.
2. Disable every older JOB-09 ZIP, including v0.4.4.7.
3. Install only v0.4.4.8.
4. Fully restart BeamNG.
5. Confirm the Tow Portal reports version `0.4.4.8`.

## Headache-friendly first test — only do this first

1. Open **Tow Yard Management**.
2. Press **Change Linked Garage on Map**.
3. Confirm the full-screen selector opens and shows your owned garages.
4. Select the correct building. Check its name, description/address, used/capacity, and exact facility ID.
5. Press **Save Garage Choice**.
6. Reopen the selector and confirm the correct garage is marked **CURRENT LINK**.

Stop after this and report whether the wrong link could be changed.

## Second test — normal delivery

1. Select one claimed Tow Company Garage item.
2. Open **Change Garage / Delivery Options**.
3. Choose a garage with space.
4. Press **Save & Deliver** without checking force.
5. Save and reload.
6. Confirm exactly one item exists in the selected garage and the virtual record disappeared only after successful placement.

## Third test — full garage recovery option

1. Select a full owned garage.
2. First try without the force checkbox. It should refuse delivery and keep the virtual record safe.
3. Reopen the selector, select the same full garage, check **Force delivery even if full**, and press **Save & Deliver**.
4. Save and reload.
5. Confirm exactly one item is assigned to the selected full garage—not silently redirected to another garage.
6. Use normal Career garage cycling afterward to move items out.

## Relink/unlink safety

- **Unlink Current Garage** must remove only the future destination link.
- Virtual company/custody records must remain.
- Already-delivered Career inventory must stay where it was.
- Relink or unlink should be blocked while a delivery transaction is actively pending.

## Return on failure

Send a screenshot and say:

- which record you selected;
- old garage link;
- chosen garage name and exact ID;
- whether the garage was full;
- whether force was checked;
- where the item appeared after save/reload;
- whether a duplicate or missing record appeared.

Relevant log terms: `[RedFox][TOW]`, `RLS_GARAGE_MOVE`, `forceFull`, `garage_delivery`, `ERROR`, `stack traceback`.

## Deferred

This build does not repair saved-job Resume after a crash and does not yet add the temporary roadside-equipment palette to Scene Manager.

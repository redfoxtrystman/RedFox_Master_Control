# Official BeamNG Career / Vehicle Field Notes — QuickScan v0.4.5

Verified against current official BeamNG documentation on 2026-07-29.

## Spawnable configuration record

Vehicle group entries use:

- `model` — required vehicle folder/id;
- `config` — recommended configuration id.

QuickScan adds a stricter safety check: the matching `.pc` configuration file must actually exist before the record is marked spawn-ready.

Source: `https://documentation.beamng.com/modding/file_formats/vehicle_groups/`

## Native configuration fields exposed by the wizard

- Configuration
- Description
- Value
- Years
- Population
- Drivetrain
- Fuel Type
- Propulsion
- Transmission
- Performance Class
- Config Type
- Body Style
- Derby Class
- Induction Type
- Country
- Power
- Torque
- Weight
- Top Speed
- defaultPaintName1/2/3

QuickScan does not invent missing prices, years, performance values, drivetrain, fuel, or population.

Source: `https://documentation.beamng.com/modding/vehicle/tutorials/configs/`

## Traffic

Generated vehicle groups can use model/config population weighting. Explicit traffic or mission groups use `model` and `config` entries in `*.vehGroup.json` files.

Sources:

- `https://documentation.beamng.com/world_editor/windows/vehicle_groups_editor/`
- `https://documentation.beamng.com/modding/file_formats/vehicle_groups/`

## Dealerships

Current official facility documentation describes dealership inventory filters. The example whitelists `Config Type: Factory`.

There is no single documented universal per-vehicle field meaning “sell this vehicle at dealership X.” QuickScan therefore sets approved native fields such as Config Type and records dealership/facility intent separately as a RedFox planning field.

Source: `https://documentation.beamng.com/modding/levels/level_formats/facilities/`

## Patch rule

The wizard creates a separate patch ZIP. It never silently rewrites the original source ZIP. Traffic requests can create a valid vehicle-group file; dealership intent stays in the plan until a separate facility/filter patch is intentionally created.
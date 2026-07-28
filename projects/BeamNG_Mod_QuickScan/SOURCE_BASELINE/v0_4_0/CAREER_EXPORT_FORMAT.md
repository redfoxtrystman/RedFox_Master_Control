# Career Vehicle Export Format

Schema identifier: `redfox.beamng.career_vehicle_catalog/1.0`

## Purpose

QuickScan writes a plain machine-readable catalog so another RedFox application can find vehicle mods and configurations without opening the scanner UI or reverse-engineering the SQLite database.

## Files

```text
career_exports/career_vehicle_catalog.json
career_exports/career_vehicle_catalog.jsonl
career_exports/career_vehicle_catalog.csv
career_exports/career_vehicle_catalog.schema.json
career_manifests/<zip-hash>.json
```

- `career_vehicle_catalog.json`: complete catalog grouped by source mod and vehicle.
- `career_vehicle_catalog.jsonl`: one flattened configuration per line for fast indexing and streaming.
- `career_vehicle_catalog.csv`: spreadsheet-friendly flattened view.
- `career_vehicle_catalog.schema.json`: minimal machine contract.
- `career_manifests/<zip-hash>.json`: one source-mod manifest.

## Required for QuickScan's spawn-ready record

QuickScan marks a configuration `spawn_ready` only when these are present:

- `model`: vehicle folder/model identifier;
- `config`: configuration identifier;
- `pc_path`: confirms the `.pc` configuration file exists.

BeamNG vehicle-group documentation lists `model` as required and `config` as recommended for reliable spawning. QuickScan uses the stricter three-field rule above so another app does not receive a configuration that has no actual `.pc` file.

## Career-facing metadata captured when present

Configuration metadata:

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
- Power
- Torque
- Weight
- Top Speed
- defaultPaintName1
- defaultPaintName2
- defaultPaintName3

Main vehicle metadata:

- Brand
- Name
- Author
- Type
- Description
- default_pc
- defaultPaintName
- paints

JBeam data:

- count and paths of parts containing `information.value`;
- monetary values are preserved because BeamNG documents this field as being used by career mode when buying and selling parts.

## Per-record supporting data

Each record can also contain:

- source ZIP full path;
- source ZIP filename;
- source ZIP SHA-256;
- detected mod title/version/author;
- vehicle model folder;
- configuration ID;
- configuration `.pc` path;
- metadata source paths;
- extracted preview source and output paths;
- metadata parse status and automatic repairs;
- DRM/protection indicator summary;
- proposed normalized ZIP name;
- load-order rename warning;
- catalog destination;
- `missing_required_fields`;
- `missing_recommended_fields`;
- `inferred_fields`;
- `spawn_ready`.

## Missing data rule

QuickScan never invents prices, years, performance figures, drivetrain, fuel type, population, power, torque, or weight.

Missing data is written to `missing_recommended_fields` so the consuming app can:

- leave it unknown;
- ask the user;
- apply a separate approved data source;
- calculate it later using a dedicated career balancing tool.

Safe inferences are listed separately in `inferred_fields`. An example is deriving a human-readable configuration name from the `.pc` filename when the configuration metadata omits one.

## Consumer behavior

A consuming app should:

1. verify `schema_id` and `schema_version`;
2. index `source_zip_sha256`, `model`, and `config` as the stable record identity;
3. use only records where `spawn_ready` is true for automatic spawning;
4. treat missing price and career values as unknown, not zero;
5. surface DRM and metadata quality flags to the user;
6. avoid modifying the source ZIP based only on this catalog;
7. rescan or invalidate a record when the source ZIP hash changes.

## Official BeamNG references used

- `https://documentation.beamng.com/modding/vehicle/tutorials/configs/`
- `https://documentation.beamng.com/modding/vehicle/sections/information/`
- `https://documentation.beamng.com/modding/file_formats/vehicle_groups/`

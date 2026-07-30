# RedFox Tow Catalog v2 Contract

Schema ID: `redfox.tow_catalog`  
Schema version: `2`

## Stable entry identity

Each entry is keyed from:

```text
source ZIP SHA-256 + exact BeamNG model ID + exact configuration ID
```

A model can therefore contain independent civilian, police, race, stripped, trailer, equipment, prop, and unusable configurations.

## Output location

```text
<Selected BeamNG User Folder>/settings/redfox/tow_catalog/
```

Files:

- `catalog_v2.json`
- `runtime_observed.json`
- `scan_manifest.json`
- `previews/`
- `backups/`

## Main entry sections

- `identity`: model, configuration, `.pc` path, source ZIP/path/hash/version/name/author.
- `display`: display name, make, model name, configuration name, exact preview path/role/hash.
- `year`: exact year or range, source, confidence.
- `classification`: independent physical type, service type, and lien/property type.
- `permissions`: Standard Tow, Abandoned, Lien/Custody, Breakdown, Rollover, Semi, Trailer, Equipment, Police Impound, Police Support, Fire/EMS Support, Tow Support, Scene Prop, Road Hazard, Auction, Scrap, Never Spawn.
- `career`: spawn readiness and available career-facing metadata.
- `detection`: scanner suggestions, evidence, and confidence.
- `onlineMetadata`: source name/URL/date/confidence/approval.
- `dependencies`: required/missing dependencies and warnings.
- `history`: first/last seen, edit/rename/runtime-observed status.
- `reviewStatus`: Unreviewed, approved, restricted, or never use.

## Manual-review law

- New static and runtime-observed entries start Unreviewed.
- Suggestions do not become approved automatically.
- Manual exact-configuration values survive rescans.
- Bulk changes skip manually reviewed exceptions unless David explicitly approves overwriting them.

## Safe-write law

1. Write `catalog_v2.json.new`.
2. Parse and validate schema and unique entry IDs.
3. Copy the previous catalog into `backups/` with a timestamp.
4. Replace `catalog_v2.json` atomically.
5. Keep the backup.

Normal catalog operations never rewrite a source mod ZIP.

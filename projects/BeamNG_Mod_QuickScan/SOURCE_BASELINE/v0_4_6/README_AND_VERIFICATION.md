# BeamNG Mod QuickScan v0.4.6 — Source and Verification

## Custody

Baseline package:

```text
BeamNG_Mod_QuickScan_v0_4_5_Results_Career_History.zip
SHA-256 0337cf723ec915b57296740a57e91562e3282ba1924a48daa938223af23dd939
```

v0.4.6 was built directly from the source contained in that exact package.

## Hashes

```text
Source SHA-256
b9577c76d86a33b9b4b05425f5337dd3cdab7859c004dff2d13455ade9261ae4

Final package SHA-256
436527a8fbbb610104618061c652add4ada96537b6877e95355794292a8b917d

Uploaded caravan source SHA-256
3075c41ab8321702126a2be4d408ecf70de94995720531b467dd1be70ee65568
```

The complete v0.4.6 source is included inside the delivered package as `BeamNG Mod QuickScan.pyw`. A source snapshot was not separately duplicated into this control repository in this commit; use the hash above to verify custody.

## Before-edit gates

```text
PASS  baseline SHA-256 matched release record
PASS  baseline Python compilation
PASS  baseline full self-test
```

## After-edit gates

```text
PASS  Python compilation
PASS  inherited scanner/duplicate/version/image/DRM/Career/history tests
PASS  v0.4.5 extended tests
PASS  v0.4.6 Tow Catalog tests
PASS  exact configuration separation
PASS  police and equipment suggestion tests
PASS  manual exact-config override survives rescan
PASS  runtime_observed import
PASS  catalog schema validation
PASS  catalog_v2.json.new safe replacement
PASS  timestamped catalog backup
PASS  Tow Catalog GUI construction
PASS  real uploaded caravan four-config inventory
PASS  exact caravan configuration preview extraction
PASS  source caravan hash unchanged
PASS  final ZIP CRC
PASS  packaged source compilation
PASS  packaged full self-tests
PASS  packaged GUI smoke
```

## Runtime truth

Static and synthetic verification is complete. The following remain unproven:

- David's physical Windows UI and D-drive path behavior;
- large mod-library resource use;
- JOB-09 reading `catalog_v2.json` and writing `runtime_observed.json`;
- in-game permission/year/lien behavior;
- the complete requested representative configuration proof set;
- automated online research inside the desktop application.

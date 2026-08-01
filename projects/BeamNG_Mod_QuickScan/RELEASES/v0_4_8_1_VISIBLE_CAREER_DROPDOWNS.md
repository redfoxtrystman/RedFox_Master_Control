# BeamNG Mod QuickScan v0.4.8.1 — Visible Career/RLS Dropdowns

**Baseline:** exact verified v0.4.8 Usability + Vehicle Gallery source  
**Package SHA-256:** `0df54be70aa9a44f32bc9073b9c77a87ba56f7d89921f29a597e386bae50ed92`  
**Source SHA-256:** `77987e21a4f9049d6ee8c1bb4c06a0a04f7f60d0f44ce65ea656853834b81e01`

## Owner request

The Career/RLS editor must not require the owner to know BeamNG's exact metadata words. Fields with known choices must use visible dropdown windows, and those windows must not become white-on-white or otherwise invisible under Windows themes or display scaling.

## Implemented

- Replaced every application dropdown with a high-contrast popup choice window.
- Popup includes title, search, visible list, vertical and horizontal scrollbars, exact stored value, explanation panel, Use Selected, and Custom only where safe.
- Career wizard controlled choices now cover Drivetrain, Fuel Type, Propulsion, Transmission, Induction Type, Config Type, Body Style, Population, Performance Class handling, traffic policy, and dealership policy.
- Corrected common/documented BeamNG tokens:
  - Config Type: Factory, Custom, Race, Police, Service, Powerglow, Rally.
  - Drivetrain: FWD, RWD, AWD, 4WD, Other; preserves observed multi-axle values.
  - Fuel Type: Gasoline, Diesel, Battery.
  - Propulsion: ICE, Electric; preserves current official Hybrid metadata.
  - Transmission: Manual, Automatic, DCT, Sequential, CVT, Other.
  - Induction: NA, SC, Turbo, and +N2O combinations.
- Performance Class defaults to blank/automatic BeamNG test rather than asking the owner to guess.
- Population includes community anchors 500 and 10000, clearly marked nonofficial, plus convenience presets and custom numeric entry.
- Career/RLS marketplace readiness separately checks Value, Population, and Config Type; Years remains recommended.
- Existing nonstandard mod values can be preserved but new strict-field text must come from the visible choice window.

## Supplied template result

The uploaded `info_Coupe LHD [B].json` contains an invalid trailing comma after the Years object. QuickScan's tolerant parser recovers it in memory. Generated Career patch JSON is strict and contains no trailing comma.

## Preserved laws

- Ordinary scans never rewrite source ZIPs.
- Career modifications are separate patch output.
- Filename-only renames remain manifest-only with no second ZIP.
- Folder-specific views, Previous Scans, Master Catalog, visual Vehicles, Tow Catalog, and exact-configuration identity remain preserved.
- No uploaded mod ZIPs or images are bundled.

## Verification

```text
PASS Python compilation
PASS inherited v0.4.4-v0.4.8 self-tests
PASS visible-choice self-test
PASS live high-contrast dropdown popup
PASS search and scrollbars
PASS selected value remains visible
PASS Career Powertrain and Classification choice fields
PASS supplied template recovery
PASS strict generated JSON
PASS Career/RLS required-field readiness
PASS final ZIP CRC and extracted-package tests
```

Physical Windows DPI/multi-monitor behavior, very large real libraries, and in-game RLS/Career marketplace behavior remain owner tests.
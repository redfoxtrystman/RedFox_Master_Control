# QuickScan v0.4.8.1 — Verification and field-choice contract

## Exact hashes

```text
Source SHA-256
77987e21a4f9049d6ee8c1bb4c06a0a04f7f60d0f44ce65ea656853834b81e01

Package SHA-256
0df54be70aa9a44f32bc9073b9c77a87ba56f7d89921f29a597e386bae50ed92
```

## Visible dropdown law

```text
FIXED-CHOICE FIELDS MUST NOT BE BLANK FREE-TEXT BOXES.
CHOICES MUST OPEN IN A HIGH-CONTRAST WINDOW.
THE OPTION LIST, SEARCH, SCROLLBARS, EXACT STORED VALUE, AND EXPLANATION MUST BE VISIBLE.
SELECTED VALUES MUST REMAIN READABLE AFTER THE POPUP CLOSES.
```

The implementation avoids native Windows menu/combobox color behavior by using a separate Tk popup with explicitly controlled foreground/background colors.

## Career/RLS exact-choice fields

- Drivetrain
- Fuel Type
- Propulsion
- Transmission
- Induction Type
- Config Type
- Body Style
- Population presets/custom numeric value
- Performance Class safe handling
- Traffic policy
- Dealership policy

## No invented choices

- Value remains a validated vehicle-specific number.
- Years remains a validated year/range.
- Power, Torque, Weight, and Top Speed remain measured numeric values.
- Performance Class defaults to blank/automatic BeamNG test and accepts custom input only as a verified test result.
- Population is documented as a relative weight, not a percentage. Community values 500 and 10000 are labeled as community guidance rather than official thresholds.

## Fuel/propulsion distinction

```text
Fuel Type: Gasoline, Diesel, Battery
Propulsion: ICE, Electric, Hybrid where genuinely declared
```

Do not write `Electric` as Fuel Type simply because Propulsion is Electric.

## Supplied template

`info_Coupe LHD [B].json` parses only after safe trailing-comma recovery. Patch output is strict valid JSON.

## Verification

```text
PASS compile
PASS inherited self-tests
PASS high-contrast popup construction
PASS popup options visible
PASS list foreground differs from background
PASS search and scrollbars
PASS documented Config Type tokens
PASS documented common drivetrain/fuel/propulsion/transmission/induction tokens
PASS Population 500/10000 anchors
PASS template recovery
PASS strict JSON output
PASS marketplace readiness fields
PASS no uploaded mod archive bundled
```

## Remaining owner tests

- Windows display scaling and multiple monitors.
- Large real library performance.
- RLS/Career marketplace behavior in the installed game after enabling a generated patch.
# JOB-01 Phone and PC Host Contract

Contract ID: `job01.platform.v1`  
Baseline: RLS Career Overhaul 2.6.6 only

## RLS phone

- RLS remains the only phone controller and phone shell.
- JOB-01 adds one compiled manifest ID, `redfox-icefox`.
- A saved-layout migration inserts the icon after RLS Marketplace when absent.
- Clicking the icon opens the IceFox phone host.
- Back/close returns through the RLS router; JOB-01 does not toggle a second
  phone controller.

## RLS computer

- RLS facilities and `career_modules_computer` remain authoritative.
- `redfoxPlatformCore.onComputerAddFunctions` contributes one general function:
  `IceFox / FoxNet`.
- Clicking it opens a RedFox desktop route with an actual IceFox desktop icon.
- Clicking the desktop icon opens the IceFox browser.
- `Return to RLS Computer` reopens the originating computer when its ID is
  available; otherwise the Career menu is closed.

## Shared behavior

- Both hosts request `redfoxPlatformCore.getRegistry()`.
- Both show the same enabled destinations and canonical IDs.
- Both load the same app `entryPath`; only responsive presentation differs.
- Platform home is available on every map because it has no map facility
  dependency.
- Apps remain responsible for reporting unavailable map-specific services.

## Compatibility limitation

RLS compiles phone manifests into its Vue distribution. v0.2 therefore ships a
two-file patch pinned to the exact RLS ZIP SHA-256. A different RLS build causes
the builder to stop. A future RLS runtime manifest API should replace this
pinned patch when available.

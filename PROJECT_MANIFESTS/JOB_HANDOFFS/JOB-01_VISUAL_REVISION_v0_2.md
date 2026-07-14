# JOB-01 Visual Revision v0.2

Date: 2026-07-14  
Owner direction: use the original IceFox logo from the working RedFox system and
make the PC and phone browser pages follow the supplied dark IceFox mockup.

Reference image supplied by David in the JOB-01 conversation:

```text
acb58920-5214-479f-9eeb-e174177e166c.png
```

The reference is recorded by filename and translated into the RedFox-owned
source below. The large conversation attachment is not duplicated into the
control repository.

## Frozen brand asset

The original working-system logo was copied unchanged from:

```text
ui/modModules/redfoxCareerWeb/assets/images/logos/icefox_head.svg
```

JOB-01 destination:

```text
ui/modModules/redfoxPlatformCore/assets/brand/icefox_head.svg
```

SHA-256:

```text
27561d917df7885ffb6023fe51e71844aa7f5fc68986e5b71f06965dee76ba8b
```

The temporary generic JOB-01 fox mark was deleted. The original logo now owns
the RLS phone tile, PC launch card, browser titlebar, and IceFox home brand card.

## Implemented visual direction

- dark Windows-style browser chrome;
- titlebar, navigation buttons, locked IceFox address field, favorites, privacy,
  theme, and menu controls;
- coastal-road IceFox hero;
- original IceFox logo card and RedFox blue/orange branding;
- weather and RedFox news panels;
- registry-driven quick-access cards;
- RedFox finance and vehicle-listing ad artwork;
- vehicle-listing preview strip clearly labeled as non-transactional;
- PC start screen with installed destination cards and secure-connection footer;
- the same browser DOM, registry, destinations, and assets on phone and PC;
- phone-only changes are responsive CSS sizing and density.

## Boundary

This revision changes brand and presentation only. It does not add app-owned
pages, fake Career results, car-sale transactions, money, inventory, ownership,
storage, insurance, missions, rewards, or save logic.

The listing strip is explicitly a visual preview until JOB-02 publishes and
integrates the RLS transaction bridge. Registered add-on apps replace platform
preview/navigation space through `job01.platform.v1` without editing the core.

## Verification status

Static package, JavaScript parse, SVG parse, original-logo identity, ZIP CRC,
and duplicate-path checks pass. BeamNG rendering remains runtime untested until
David tests the RLS phone and PC on West Coast and a second map.

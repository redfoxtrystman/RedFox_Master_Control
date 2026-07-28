# RF-HUB01 Input-Action Scanner and Shared WEUI Theme Decision

**Date:** 2026-07-27  
**Project:** RedFox GarageHub controlled rebuild  
**Status:** Architecture decision recorded; no Hub ZIP created in this step  
**Baseline:** `1-RedFox_GarageHub_v0_5_11_RaceManagerLinkFix.zip`

## 1. Confirmed user observation

David confirmed that when compatible native ImGui/WEUI windows are dragged into the GarageHub dock group, most of them inherit the Hub's theme, font sizing, padding, and readability changes.

This is a core Hub feature and must be preserved during the rebuild.

## 2. Why the current Hub can affect other WEUI windows

Static inspection of the uploaded `v0.5.11` source confirms two mechanisms:

1. `getGlobalUISettings()` exposes Hub theme and scaling values to compatible RedFox extensions that deliberately query the Hub.
2. `applyGlobalImGuiScale()` writes shared Dear ImGui values where BeamNG exposes them, including `io.FontGlobalScale` and global style fields such as frame padding, item spacing, scrollbar size, and related style values.

Because Dear ImGui style and IO values are shared within the same gameplay UI context, compatible windows may inherit those settings even when they were not explicitly written to query `getGlobalUISettings()`.

This behavior is useful, but not every mod is guaranteed to inherit every color or local style because a mod can push its own style values after the Hub applies the global settings.

## 3. Locked rebuild rule

The rebuild must preserve both theme paths:

- **Shared/global path:** global ImGui scale and style values for ordinary compatible WEUI windows.
- **Explicit provider path:** `getGlobalUISettings()` for RedFox apps that intentionally consume the Hub's full theme settings.

The Hub rebuild must not reduce theme control to a per-app bridge-only system. Theme control remains a Hub core service even when no apps are registered.

## 4. Manual Connect decision

The existing Manual Connect system is not dependable enough to remain the primary connection method.

New priority order:

1. Scan installed `redfox_module.json` manifests.
2. Scan installed input action definition files for likely UI actions.
3. Show candidates to David for approval.
4. Save approved actions as Hub app entries.
5. Keep a manual entry form only as an advanced fallback for commands the scanner cannot identify.

## 5. Input-action scanner design

The scanner should inspect mounted mod files such as:

```text
lua/ge/extensions/core/input/actions/*.json
settings/inputmaps/*.json
```

Candidate actions should be scored using:

- action title/category text containing `UI`, `window`, `menu`, `panel`, `tool`, `manager`, `open`, `toggle`, or `show`;
- action command containing `extensions.`, `extensions.load`, `toggle`, `open`, `show`, or `setShowUI`;
- RedFox names and known product names;
- matching manifest or extension paths found elsewhere in the same mod.

The scanner must not automatically execute every discovered action. It should present a review list:

```text
Detected action
Source mod/file
Display title
Command
Likely type
[Add to Hub] [Ignore]
```

Approved entries become visible in the Hub's `Apps/Windows` menu.

## 6. Control classification

Each approved app remains classified as:

```text
FULL       = definite open and definite close/hide
TOGGLE     = one toggle command; Hub must track state carefully
OPEN_ONLY  = safe open command, no safe close command
UNMAPPED   = detected candidate but no proven usable command
```

Theme inheritance is separate from control classification. An `OPEN_ONLY` or even `UNMAPPED` WEUI window may still inherit the Hub's global font/theme settings when docked or rendered in the same ImGui context.

## 7. Rebuild implication

The new Hub core should contain only:

```text
Hub | Apps/Windows | Theme | Help | [group minimize]
```

Old permanent menu names such as Flood, Infection, Gravity, VTOL, Spawner, and Race/Event should not appear unless an installed app is discovered and approved.

The Hub's useful identity becomes:

- shared WEUI theme/readability controller;
- installed UI-app scanner;
- approved app launcher;
- selected-window minimize/restore manager;
- compact status and troubleshooting center.

## 8. Verification requirement

Before any next ZIP is delivered, verification must prove that these functions remain present and callable:

```text
getGlobalUISettings
applyGlobalImGuiScale
effectiveFontScale
effectiveButtonScale
effectivePaddingScale
settings save/load
stable Hub window identity
```

Runtime tests must include:

1. Open Hub alone and change font/theme settings.
2. Open a compatible WEUI app independently.
3. Dock it into the Hub during normal gameplay.
4. Verify which font, padding, scale, and color changes it inherits.
5. Undock it and verify whether shared settings remain.
6. Confirm a mod with its own local style does not break the Hub.
7. Confirm scanning and app registration do not require modifying the target mod.

Signed,

**Sol / GPT-5.6 Thinking**

# JOB-09 RedFox Tow & Recovery Website Prototype v0.1

**Date:** 2026-07-28

**Job:** `19 — JOB-09-RedFox_TowRecoveryDispatch`

**Status:** VISUAL PROTOTYPE — NO BEAMNG GAME LOGIC CONNECTED

## Purpose

Create a standalone public-facing towing-company website and a separate animated Company Portal before tying the existing JOB-09 WEUI/game systems into web pages.

## Visual direction

- Dark RedFox operating-system theme
- Purple/seafoam colors carried from the existing JOB-09/Garage Hub theme contract
- Warm orange/copper public towing-company accent
- 24/7 dispatch strip
- Large recovery-focused hero section
- Service, fleet, recovery, yard, about, and request-service sections
- Animated transition between the public site and Company Portal

The referenced real towing website was used only as broad layout and service-presentation inspiration. No third-party site code, branding, photographs, fonts, or assets were copied.

## Company Portal sections

- Operations Overview
- Dispatch Center
- Scene Builder
- Records & History
- Tow Yard Inventory
- Company Fleet
- Tow Yard Management
- Invoices
- Settings & Tools

## Prototype behavior

- Standalone HTML/CSS/JavaScript
- No external libraries, fonts, or internet dependency
- Responsive desktop/mobile layouts
- RedFox Ember and Seafoam/Purple visual themes
- Demo transitions, cards, tables, scene roster, fleet assignments, yard colors, inventory actions, and invoice records
- Public Request Tow modal
- Company Portal navigation and demo dashboard

## Future bridge stubs

The prototype exposes placeholder browser functions for the later BeamNG integration stage:

- `window.RedFoxTowWeb.openPortal(section)`
- `window.RedFoxTowWeb.openSection(section)`
- `window.RedFoxTowWeb.applyTheme(theme)`
- `window.RedFoxTowWeb.setGameData(payload)`

These functions do not currently connect to BeamNG.

## Artifact

- File: `RedFox_Tow_Web_Prototype_v0_1.zip`
- SHA-256: `a54341fb10bae495f5322e200ff66dec3bbf40bb61f2074599aa8340035e7bbd`
- Size: 44,509 bytes
- Includes modular source and a single-file self-contained HTML version
- ZIP integrity: PASS
- JavaScript syntax: PASS
- HTML parser check: PASS

## Boundary

This prototype does not modify or replace the v0.3.5 mod and does not claim runtime integration. David will review the design first. Game data, Hub control, dispatch actions, inventory writes, invoices, scenes, and fleet operations will only be connected after the visual structure is approved.

# JOB-09 — Real-World Crash Scene Research

**Date:** 2026-07-15  
**Purpose:** Translate real roadway crash composition and official traffic-incident-management practice into believable BeamNG recovery scenes.

## Authoritative references

### FHWA Manual on Uniform Traffic Control Devices, 11th Edition, Part 6, Chapter 6O

`https://mutcd.fhwa.dot.gov/pdfs/11th_Edition/part6.pdf`

Useful scene-design rules:

- A traffic incident management area extends from the first warning device until traffic returns to its normal path.
- Incidents are classified as minor, intermediate, or major according to duration and disruption.
- Intermediate incidents commonly divert traffic past a blockage.
- Major incidents use tapered lane closures, upstream warnings, and sometimes detours.
- Minor movable crashes should be cleared to the shoulder quickly.
- Emergency lights warn drivers but do not replace traffic control.

### U.S. Fire Administration — Traffic Incident Management Systems, FA-330

`https://www.usfa.fema.gov/downloads/pdf/publications/fa_330.pdf`

Useful scene-design rules:

- The first emergency vehicle should shield responders and the work area from approaching traffic.
- Preserve access for later-arriving emergency and recovery vehicles.
- Keep a buffer area clear between moving traffic and the work zone.
- Intersections may require shielding from multiple directions.
- Ambulance loading and tow work belong inside the protected area.

## Real-world scene patterns to reproduce

### Two-vehicle lane collision

- One or two lanes partly blocked.
- Vehicles offset from the lane center rather than parked neatly.
- Short debris field around the impact zone.
- Police/service blocker upstream and tow staging downstream or on the shoulder.

### Three-vehicle chain collision

- Wrecks compressed along the direction of travel.
- Front vehicle nearly straight; later vehicles show increasing yaw.
- Damage sequence reflects front/rear impacts.
- Cone taper begins upstream of the outermost wreck.

### Shoulder rollover with secondary collision

- Primary wreck beyond the lane edge or partly in a ditch.
- Secondary vehicle partly remains in the travel lane.
- Tow equipment stages downstream or within the closed lane.
- Police/fire apparatus protects the upstream side.

### Semi and trailer jackknife

- Tractor and trailer use separate yaw angles.
- Trailer can span multiple lanes while the tractor reaches a shoulder, median, or barrier.
- Passenger cars may be trapped near the tractor nose, trailer side, or barrier.
- Requires a long road segment and major-scene traffic control.

### Heavy truck or rotator crash

- Heavy wreckers and rotators may be crash targets, not only player recovery vehicles.
- Their footprint determines lane closure and equipment access.
- Secondary vehicles belong near a plausible impact zone rather than at arbitrary offsets.

### Bus multi-vehicle crash

- Rare event.
- Bus generally follows the roadway or crosses one or two lanes.
- Secondary vehicles cluster near front/rear corners.
- Future support assets should add expanded police, fire, and ambulance staging.

## Visual reference search categories

Non-graphic real-world images were reviewed for:

- aerial interstate pileups involving cars and semis;
- jackknifed tractor-trailers across several lanes;
- rural two-lane crashes with cone tapers and shoulder work;
- divided-highway cleanup with police, barrels, and flatbed staging;
- roadside/shoulder recovery with damaged vehicles and tow operators.

The photographs are composition references only. Do not copy or redistribute identifiable news photographs as mod assets.

## Scene source priority

1. Matching player-built RedFox layout — 80% default priority.
2. Registered random-event provider — 35% chance when no saved layout was selected.
3. RedFox procedural road/shoulder fallback.

## Next integration evidence needed

Return the BeamNG line beginning:

`[RedFox][TOW][EVENT_LIBRARY]`

It will list the functions actually exposed by `gameplay_events_freeroamEvents`. JOB-09 will use that evidence or the exact random-event source files to build an adapter for police lines, cones, barrels, emergency vehicles, crashed-car layouts, and debris without guessing undocumented APIs.
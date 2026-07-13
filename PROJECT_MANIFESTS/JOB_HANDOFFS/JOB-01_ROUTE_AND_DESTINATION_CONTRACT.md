# JOB-01 Route and Destination Contract

Contract ID: `job01.platform.v1`

Phone and PC select the same canonical destination ID. Host layout is not part
of the ID.

## Canonical IDs

- Platform home: `redfox.home`
- App IDs: `redfox.<app-name>`
- IDs are lowercase and stable across versions.
- An app must not create `redfox.<app>.phone` and `redfox.<app>.pc` variants.

## Host URLs

- RLS phone route: `/career/phone-redfox-icefox`
- RLS PC route: `/career/redfox-icefox-desktop`
- Display address: `icefox://<canonical-id>`

The RLS routes launch different responsive shells, but both request the same
registry and resolve the same `entryPath`.

## Entry paths

- Platform-owned internal home: `internal:redfox.home`
- App UI: absolute `/ui/modModules/<app-owned-folder>/...`
- Remote HTTP/HTTPS URLs, parent traversal, `file:` URLs, and arbitrary Lua
  paths are rejected.

## Availability

Destinations default to both phone and PC. An app may set `phone=false` or
`pc=false` only when the feature genuinely cannot run on that host. Map or RLS
service availability must be reported inside the app using the JOB-02 result;
the platform must not fake success or silently switch to a different service.

## Current v0.1 registry

Only `redfox.home` is built in. Other destinations appear only when their
separate add-on mods register successfully.

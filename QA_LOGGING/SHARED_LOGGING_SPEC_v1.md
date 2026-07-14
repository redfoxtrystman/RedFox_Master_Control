# RedFox/FoxNet Shared Logging Specification v1

**Date:** 2026-07-14  
**Timestamp:** 2026-07-14 13:08 PDT (America/Los_Angeles)  
**Owner:** JOB-11 — QA / Logging / Failure Triage  
**Status:** PUBLISHED v1 — CONTRACT-SPECIFIC MESSAGE NAMES STILL REQUIRE JOB-01/JOB-02/JOB-03 HANDOFFS

## Goal

Make phone, PC, platform, app, bridge, and Career/RLS failures traceable without guessing. Logs must identify the first failing boundary while avoiding secrets and excessive per-frame spam.

## Required prefixes

```text
[RedFox][PHONE]
[RedFox][PC]
[RedFox][PLATFORM]
[RedFox][BRIDGE]
[RedFox][BUY]
[RedFox][SELL]
[RedFox][STORE]
[RedFox][SCRAP]
[RedFox][BEAMBOOK]
[RedFox][IMPORT_EXPORT]
[RedFox][CLASSICS]
[RedFox][TOW]
[RedFox][SPONSOR]
[RedFox][FOXMAIL]
[RedFox][FOXTEXT]
[RedFox][QA]
```

New shared prefixes require a documented JOB-11 proposal. Individual jobs may use a more specific third segment, such as `[RedFox][BEAMBOOK][LISTING]`, without replacing the required owning prefix.

## Required line fields

Human-readable line format:

```text
[RedFox][AREA][LEVEL] ts=<ISO-8601> session=<id> job=<JOB-##> version=<version> event=<stable.name> request=<id-or-na> result=<OK|ERROR|BLOCKED|SKIP> code=<stable_code> message=<short text>
```

Minimum fields:

- prefix and severity;
- ISO-8601 timestamp with timezone when available;
- test/session ID;
- exact JOB number;
- component or package version;
- stable event name;
- request/correlation ID for cross-boundary calls;
- result;
- stable error/status code;
- concise message.

Optional fields should be key/value pairs after the required fields:

```text
app=redfox.example map=west_coast_usa mode=career route=redfox.home capability=vehicle.purchase duration_ms=143
```

## Severity levels

```text
TRACE  temporary developer-only detail; disabled by default
DEBUG  useful state transition detail; disabled or limited in release candidates
INFO   successful lifecycle or contract checkpoint
WARN   recoverable issue, fallback, stale state, or manual-review condition
ERROR  requested action failed or contract was rejected
FATAL  component cannot safely continue; candidate test stops
```

## Required lifecycle events

Every build-producing job must define expected messages for applicable events:

```text
component.init.start
component.init.ok
component.init.error
manifest.load.start
manifest.load.ok
manifest.load.error
app.register.start
app.register.ok
app.register.error
app.open.request
app.open.ok
app.open.error
route.resolve.request
route.resolve.ok
route.resolve.error
bridge.request
bridge.result
bridge.error
app.disable
app.enable
app.remove
component.shutdown
```

Transaction-capable jobs must also log validation and authority boundaries without logging sensitive save contents:

```text
buy.validate.request
buy.validate.result
buy.authority.request
buy.authority.result
sell.validate.request
sell.validate.result
sell.authority.request
sell.authority.result
```

## Correlation rules

- One user action receives one request/correlation ID before crossing from UI to platform or bridge.
- The same ID must be preserved through phone/PC, platform, shared event API, bridge, and result handling.
- Retries add `attempt=<n>` but keep the original request ID.
- A result with no matching request is an `ERROR` with code `UNMATCHED_RESULT`.
- A timed-out request must log one timeout result; do not silently retry forever.

## Stable result codes

Each contract-owning job must publish its full code list. Shared minimum codes are:

```text
OK
NOT_READY
NOT_SUPPORTED
NOT_FOUND
INVALID_REQUEST
INVALID_PAYLOAD
VERSION_MISMATCH
PERMISSION_DENIED
DUPLICATE_ID
ROUTE_NOT_REGISTERED
DEPENDENCY_MISSING
TIMEOUT
CANCELLED
RUNTIME_EXCEPTION
UNMATCHED_RESULT
BLOCKED_BY_QA
```

Do not use a raw exception string as the only code.

## Data protection and log hygiene

Do not log:

- authentication tokens, cookies, API keys, passwords, or private connector data;
- full save files or unrelated player data;
- absolute personal Windows usernames or unnecessary local paths;
- entire binary payloads;
- per-frame or per-tick repeats without rate limiting.

Vehicle IDs, listing IDs, app IDs, route IDs, contract versions, and non-secret request payload summaries may be logged when needed for reproduction.

## Rate limiting and duplicate suppression

- Repeated identical warnings should include a suppressed count.
- Per-frame functions must not emit INFO/WARN/ERROR every frame.
- One lifecycle transition should produce one start and one final result.
- Debug logging must have a clear enable/disable control and default to off in release candidates.

## JOB-11 evidence collection

When a failure is reproduced, preserve:

1. exact candidate ZIP name, size, and SHA-256;
2. installed-mod fingerprint;
3. BeamNG version, map, mode, save, UI scale, and timestamp;
4. unfiltered surrounding log context;
5. a filtered copy containing relevant `[RedFox]` prefixes and request IDs;
6. expected versus actual behavior;
7. earliest provable failing layer;
8. owning job and verdict.

Filtering must never delete the original logs.

## Current contract gaps

- JOB-01 must publish exact platform event names and expected lifecycle messages.
- JOB-02 must publish bridge message names, result codes, payload summaries, capability handshake, and test fixtures.
- JOB-03 must publish Store manifest/install-state messages and result codes.
- Feature jobs must publish their app-specific expected events and negative-test messages.

Until those are supplied, JOB-11 may validate this common envelope but must mark contract-specific checks `BLOCKED` rather than invent names.

## Change record

**What changed:** Published the initial shared logging envelope, prefixes, severity levels, correlation rules, minimum result codes, lifecycle checkpoints, and evidence-retention requirements.  
**Why:** The previous Work chat defined required prefixes but did not commit the promised standalone logging specification before becoming inaccessible under the Work-chat limit.  
**Files affected:** `QA_LOGGING/SHARED_LOGGING_SPEC_v1.md`.  
**Current status:** Common logging standard published; component-specific contracts remain incomplete.  
**Known problems:** JOB-01/JOB-02/JOB-03 expected messages and fixtures are not final.  
**Required next step:** Each owning job must publish expected log messages in its QA intake packet; JOB-11 will then add contract-specific checks without editing their implementation.

## Migration note

This specification was reconstructed in the replacement regular chat after the original JOB-11 Work chat became inaccessible on July 14, 2026 until the displayed July 20, 2026 return date. It does not claim recovery of chat-only drafts.

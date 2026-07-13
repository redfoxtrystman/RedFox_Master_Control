# JOB-01 to JOB-02 Bridge Boundary

## Ownership

JOB-01 owns:

- phone and PC launch routes;
- responsive host UI;
- canonical destination registry;
- app navigation;
- delivery of the same host context and destination identity on phone and PC.

JOB-02 owns:

- every UI-to-Lua Career/RLS operation name;
- request and result payloads;
- money, ownership, inventory, garage/storage, insurance, vehicle-shopping,
  mission, reward, and save adapters;
- validation, error codes, idempotency, transaction logs, and runtime evidence.

## Frozen boundary

An app manifest may declare `bridgeContract="job02.bridge.v1"` only after JOB-02
publishes that exact contract and commit. JOB-01 must pass the app's canonical
destination ID and host (`phone` or `pc`) unchanged to the JOB-02 adapter.

JOB-01 must never translate a failed or unavailable JOB-02 result into success.
The app must receive the exact unavailable dependency or validation error.

## v0.1 status

The initial icon/host build implements no Career action forwarding. It proves
only the platform registry and launch surfaces. Apps that require Career data
or actions must remain unregistered or read-only until the JOB-02 contract is
published and integrated.

No temporary purchase, sale, spawn, reward, money, storage, or ownership path
is authorized inside JOB-01.

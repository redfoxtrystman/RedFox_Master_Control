# JOB-13 v0.1.5 rejection and v0.1.6 recovery closure

v0.1.5 is rejected because its Auction route reached the page without a working Lua bridge, left the page in LOADING with zero lots, and retained an unauthorized LIVE lock plus an invented TEST transaction path.

v0.1.6 recovery actions:

- removed the unauthorized lock;
- removed simulated money, invoice, transit and garage handling;
- added a nested-frame bridge that reaches BeamNG `bngApi.engineLua` directly and reports a bridge error instead of loading forever;
- retained only Auction page mirrors, not other FoxNet websites or shared core files;
- used the supplied RLS fallback vehicle configurations as a fixed no-scan pool;
- reused RLS-derived timed/proxy bidding behavior;
- submitted player wins through RLS `vehicleShopping` with `makeDelivery=true`;
- confirmed the native harness charges exact Career total and consumes the temporary shop record;
- confirmed zero extra state writes over 120 idle seconds.

Recovery artifact SHA-256: `8fa86d6fa09287bd07ba97dd4281362e8c05950b31bfd57da5dfc0f2cc39cce4`.

Runtime remains unproven until David tests the exact artifact. No additional version should be built before that result.

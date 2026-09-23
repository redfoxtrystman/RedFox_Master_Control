using Microsoft.Extensions.DependencyInjection;
using PKHeX.Core;
using PKVault.Core;

static async Task<IServiceProvider> Boot()
{
    PKVault.Core.Program.Initialize();
    var services = new ServiceCollection();
    PKVault.Core.Program.ConfigureServices(services);
    var sp = services.BuildServiceProvider();
    var session = sp.GetRequiredService<ISessionService>();
    await session.EnsureSessionCreated();
    return sp;
}

static async Task Seed(IServiceProvider sp, string profile)
{
    var setA = new (ushort Species, string Name, byte Level)[]
    {
        (25, "PIKACHU", 18),
        (1, "BULBASAUR", 12),
        (4, "CHARMANDER", 14),
        (7, "SQUIRTLE", 16),
        (133, "EEVEE", 20),
        (143, "SNORLAX", 30),
    };
    var setB = new (ushort Species, string Name, byte Level)[]
    {
        (26, "RAICHU", 24),
        (2, "IVYSAUR", 18),
        (5, "CHARMELEON", 20),
        (8, "WARTORTLE", 22),
        (134, "VAPOREON", 28),
        (131, "LAPRAS", 32),
    };

    var set = profile.Equals("A", StringComparison.OrdinalIgnoreCase) ? setA : setB;

    using var scope = sp.CreateScope();
    var boxes = scope.ServiceProvider.GetRequiredService<IBoxLoader>();
    var loader = scope.ServiceProvider.GetRequiredService<IPkmVariantLoader>();
    var session = sp.GetRequiredService<ISessionService>();

    var box = await boxes.GetDto("0") ?? throw new Exception("Default Box 0 missing.");

    // Seed only a clean test profile.
    if ((await loader.GetAllEntities()).Count != 0)
        throw new Exception("Refusing to seed non-empty PKVault test profile.");

    for (var i = 0; i < set.Length; i++)
    {
        var s = set[i];
        var p = new PK1
        {
            Species = s.Species,
            TID16 = (ushort)(profile == "A" ? 11000 + i : 22000 + i),
            DV16 = (ushort)(0x1111 * (i + 1)),
            CurrentLevel = s.Level,
        };
        p.OriginalTrainerName = profile == "A" ? "TRADERA" : "TRADERB";
        p.Nickname = s.Name;

        var immutable = new ImmutablePKM(p);
        if (!immutable.IsEnabled)
            throw new Exception($"Seed Pokemon {s.Name} is disabled.");

        await loader.AddEntity(new(
            Box: box,
            BoxSlot: i,
            IsMain: true,
            IsExternal: false,
            AttachedSaveId: null,
            AttachedSavePkmIdBase: null,
            Context: EntityContext.Gen1,
            Generation: 1,
            Pkm: immutable,
            Id: $"trade-test-{profile.ToLowerInvariant()}-{i}"
        ));
    }

    await session.PersistSession(scope);
    Console.WriteLine($"SEEDED {profile}: {string.Join(",", set.Select(x => x.Species))}");
}

static async Task<List<PkmVariantDTO>> MainPkms(IServiceProvider sp)
{
    var q = sp.GetRequiredService<StorageQueryService>();
    return (await q.GetMainPkmVariants())
        .Where(x => x.IsMain)
        .OrderBy(x => x.BoxId)
        .ThenBy(x => x.BoxSlot)
        .ToList();
}

static async Task Trade(IServiceProvider sp, bool host)
{
    var trading = sp.GetRequiredService<TradingService>();

    if (host)
    {
        var state = await trading.HostAsync(localTest: true);
        Console.WriteLine($"HOST {state.HostAddress} internal={state.ListenPort}");

        var deadline = DateTime.UtcNow.AddSeconds(30);
        while (!(await trading.GetStateAsync()).Connected && DateTime.UtcNow < deadline)
            await Task.Delay(100);

        if (!(await trading.GetStateAsync()).Connected)
            throw new Exception("Host timed out waiting for localhost client.");
    }
    else
    {
        await trading.ConnectAsync("localhost:0000");
        Console.WriteLine("JOIN localhost:0000");
    }

    var pkms = await MainPkms(sp);
    if (pkms.Count < 6)
        throw new Exception($"Expected at least six seeded Pokemon, found {pkms.Count}.");

    var offered = pkms[0];
    Console.WriteLine($"OFFER BEFORE species={offered.Species} id={offered.Id} slot={offered.BoxSlot}");

    await trading.SetOfferAsync(offered.Id);
    await trading.SetReadyAsync(true);

    var tradeDeadline = DateTime.UtcNow.AddSeconds(60);
    while (DateTime.UtcNow < tradeDeadline)
    {
        var state = await trading.GetStateAsync();
        if (state.Status == "Completed")
        {
            Console.WriteLine($"TRADE COMPLETE remoteSpecies={state.RemoteOffer?.Species}");
            return;
        }
        if (state.Status == "Error")
            throw new Exception(state.LastError ?? "Trading service entered Error state.");
        await Task.Delay(100);
    }

    throw new Exception("Trade timed out.");
}

static async Task Verify(IServiceProvider sp, string expected)
{
    var expectedSpecies = expected.Split(',').Select(ushort.Parse).ToArray();
    var pkms = await MainPkms(sp);
    var actual = pkms.Select(x => x.Species).ToArray();

    Console.WriteLine("VERIFY " + string.Join(",", actual));

    if (!actual.SequenceEqual(expectedSpecies))
        throw new Exception($"Profile contents mismatch. Expected {string.Join(",", expectedSpecies)}, got {string.Join(",", actual)}");
}

if (args.Length == 0)
    throw new ArgumentException("usage: seed A|B | host | join | verify csv");

var sp = await Boot();

switch (args[0].ToLowerInvariant())
{
    case "seed":
        await Seed(sp, args[1]);
        break;
    case "host":
        await Trade(sp, host: true);
        break;
    case "join":
        await Trade(sp, host: false);
        break;
    case "verify":
        await Verify(sp, args[1]);
        break;
    default:
        throw new ArgumentException($"Unknown command: {args[0]}");
}

PKVault.Core.Program.Dispose();

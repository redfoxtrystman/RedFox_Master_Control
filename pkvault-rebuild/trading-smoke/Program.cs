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
    // Fresh deterministic "random" Gen-1 test sets for v7.1.
    var setA = new (ushort Species, string Name, byte Level)[]
    {
        (63, "ABRA", 17),
        (58, "GROWLITHE", 22),
        (66, "MACHOP", 19),
        (92, "GASTLY", 21),
        (147, "DRATINI", 25),
        (123, "SCYTHER", 28),
    };
    var setB = new (ushort Species, string Name, byte Level)[]
    {
        (27, "SANDSHREW", 18),
        (60, "POLIWAG", 16),
        (104, "CUBONE", 23),
        (116, "HORSEA", 20),
        (127, "PINSIR", 30),
        (124, "JYNX", 31),
    };

    var set = profile.Equals("A", StringComparison.OrdinalIgnoreCase) ? setA : setB;

    var settingsService = sp.GetRequiredService<ISettingsService>();
    var currentSettings = settingsService.GetSettings();
    await settingsService.UpdateSettingsSimple(
        currentSettings.SettingsMutable with
        {
            SAVE_GLOBS = [],
            TRADER_NAME = profile.Equals("A", StringComparison.OrdinalIgnoreCase) ? "Trader A" : "Trader B",
        },
        currentSettings.UserId
    );

    using var scope = sp.CreateScope();
    var boxes = scope.ServiceProvider.GetRequiredService<IBoxLoader>();
    var loader = scope.ServiceProvider.GetRequiredService<IPkmVariantLoader>();
    var session = sp.GetRequiredService<ISessionService>();

    var box = await boxes.GetDto("0") ?? throw new Exception("Default Box 0 missing.");

    if ((await loader.GetAllEntities()).Count != 0)
        throw new Exception("Refusing to seed non-empty PKVault test profile.");

    for (var i = 0; i < set.Length; i++)
    {
        var s = set[i];
        var p = new PK1
        {
            Species = s.Species,
            TID16 = (ushort)(profile == "A" ? 31000 + i : 42000 + i),
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

static async Task WaitConnected(TradingService trading)
{
    var deadline = DateTime.UtcNow.AddSeconds(30);
    while (!(await trading.GetStateAsync()).Connected && DateTime.UtcNow < deadline)
        await Task.Delay(100);
    if (!(await trading.GetStateAsync()).Connected)
        throw new Exception("Timed out waiting for localhost peer.");
}

static async Task WaitPeerName(TradingService trading)
{
    var deadline = DateTime.UtcNow.AddSeconds(10);
    while (string.IsNullOrWhiteSpace((await trading.GetStateAsync()).PeerName) && DateTime.UtcNow < deadline)
        await Task.Delay(50);
    if (string.IsNullOrWhiteSpace((await trading.GetStateAsync()).PeerName))
        throw new Exception("Timed out waiting for trading peer identity.");
}

static async Task WaitRemoteOfferCount(TradingService trading, int minimum)
{
    var deadline = DateTime.UtcNow.AddSeconds(20);
    while (DateTime.UtcNow < deadline)
    {
        if ((await trading.GetStateAsync()).RemoteOffers.Length >= minimum)
            return;
        await Task.Delay(50);
    }
    throw new Exception($"Timed out waiting for at least {minimum} remote offers.");
}

static async Task WaitCompleted(TradingService trading, string label)
{
    var deadline = DateTime.UtcNow.AddSeconds(60);
    while (DateTime.UtcNow < deadline)
    {
        var state = await trading.GetStateAsync();
        if (state.Status == "Completed")
        {
            Console.WriteLine($"{label} COMPLETE");
            return;
        }
        if (state.Status == "Error")
            throw new Exception(state.LastError ?? $"{label} entered Error state.");
        await Task.Delay(100);
    }
    throw new Exception($"{label} timed out.");
}

static async Task Trade(IServiceProvider sp, bool host)
{
    var trading = sp.GetRequiredService<TradingService>();

    if (host)
    {
        var state = await trading.HostAsync(localTest: true);
        Console.WriteLine($"HOST {state.HostAddress} internal={state.ListenPort}");
        await WaitConnected(trading);
    }
    else
    {
        await trading.ConnectAsync("localhost:0000");
        Console.WriteLine("JOIN localhost:0000");
        await WaitConnected(trading);
    }

    await WaitPeerName(trading);
    var connectedState = await trading.GetStateAsync();
    var expectedSelf = host ? "Trader A" : "Trader B";
    var expectedPeer = host ? "Trader B" : "Trader A";
    if (connectedState.ProfileName != expectedSelf)
        throw new Exception($"Configured trading player name was not used. Expected self '{expectedSelf}', got '{connectedState.ProfileName}'.");
    if (connectedState.PeerName != expectedPeer)
        throw new Exception($"Peer trading player name was not exchanged. Expected '{expectedPeer}', got '{connectedState.PeerName}'.");
    Console.WriteLine($"IDENTITY {connectedState.ProfileName} <-> {connectedState.PeerName}");

    // ROUND 1: uneven 2-for-1. A sends two; B sends one.
    var pkms = await MainPkms(sp);
    if (pkms.Count != 6)
        throw new Exception($"Expected six seeded Pokemon before round 1, found {pkms.Count}.");

    var firstRoundIds = host
        ? new[] { pkms[0].Id, pkms[1].Id }
        : new[] { pkms[0].Id };

    await trading.SetOffersAsync(firstRoundIds);

    if (!host)
        await WaitRemoteOfferCount(trading, 2);
    else
        await WaitRemoteOfferCount(trading, 1);

    await trading.SetReadyAsync(true);
    await WaitCompleted(trading, "ROUND1");

    // ROUND 2: one-way gift. A gives its slot-0 Pokemon; B gives nothing.
    pkms = await MainPkms(sp);

    if (host)
    {
        var gift = pkms.First();
        Console.WriteLine($"GIFT species={gift.Species} id={gift.Id}");
        await trading.SetOffersAsync([gift.Id]);
        await trading.SetReadyAsync(true);
    }
    else
    {
        await trading.SetOffersAsync([]);
        await WaitRemoteOfferCount(trading, 1);
        await trading.SetReadyAsync(true);
    }

    await WaitCompleted(trading, "ROUND2");
}


static async Task DirectHost(IServiceProvider sp, string addressFile)
{
    var trading = sp.GetRequiredService<TradingService>();
    var state = await trading.HostAsync(localTest: false);

    if (state.ListenPort is null or <= 0)
        throw new Exception("Direct host did not allocate a real port.");
    if (state.HostAddresses.Length == 0)
        throw new Exception("Direct host did not advertise any addresses.");
    if (state.HostAddresses.Any(a => a == "localhost:0000"))
        throw new Exception("Direct host incorrectly advertised the localhost test alias.");

    var address = state.HostAddresses.FirstOrDefault(a => !a.StartsWith("0.0.0.0:", StringComparison.Ordinal))
        ?? throw new Exception("Direct host did not advertise a concrete IPv4 address.");

    await File.WriteAllTextAsync(addressFile, address);
    Console.WriteLine($"DIRECT HOST {address}");

    // The hello/identity message proves the direct socket connected. Waiting
    // only on Connected can race a fast test peer that disconnects immediately.
    await WaitPeerName(trading);

    var connected = await trading.GetStateAsync();
    if (connected.PeerName != "Trader B")
        throw new Exception($"Direct host expected Trader B, got '{connected.PeerName}'.");

    Console.WriteLine($"DIRECT CONNECTED {connected.ProfileName} <- {connected.PeerName} @ {connected.PeerAddress}");
    await trading.DisconnectAsync();
}

static async Task DirectJoin(IServiceProvider sp, string addressFile)
{
    var deadline = DateTime.UtcNow.AddSeconds(20);
    while (!File.Exists(addressFile) && DateTime.UtcNow < deadline)
        await Task.Delay(100);
    if (!File.Exists(addressFile))
        throw new Exception("Timed out waiting for direct host address file.");

    var address = (await File.ReadAllTextAsync(addressFile)).Trim();
    if (string.IsNullOrWhiteSpace(address))
        throw new Exception("Direct host address file was empty.");

    var trading = sp.GetRequiredService<TradingService>();
    await trading.ConnectAsync(address);
    await WaitConnected(trading);
    await WaitPeerName(trading);

    var connected = await trading.GetStateAsync();
    if (connected.PeerName != "Trader A")
        throw new Exception($"Direct join expected Trader A, got '{connected.PeerName}'.");

    Console.WriteLine($"DIRECT JOIN {address} AS {connected.ProfileName} -> {connected.PeerName}");
    // Give the host-side smoke process time to observe the completed hello.
    await Task.Delay(750);
    await trading.DisconnectAsync();
}

static async Task Verify(IServiceProvider sp, string expected)
{
    var expectedSpecies = expected.Split(',', StringSplitOptions.RemoveEmptyEntries).Select(ushort.Parse).ToArray();
    var pkms = await MainPkms(sp);
    var actual = pkms.Select(x => x.Species).ToArray();

    Console.WriteLine("VERIFY " + string.Join(",", actual));

    if (!actual.SequenceEqual(expectedSpecies))
        throw new Exception($"Profile contents mismatch. Expected {string.Join(",", expectedSpecies)}, got {string.Join(",", actual)}");
}

if (args.Length == 0)
    throw new ArgumentException("usage: seed A|B | host | join | direct-host address-file | direct-join address-file | verify csv");

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
    case "direct-host":
        await DirectHost(sp, args[1]);
        break;
    case "direct-join":
        await DirectJoin(sp, args[1]);
        break;
    case "verify":
        await Verify(sp, args[1]);
        break;
    default:
        throw new ArgumentException($"Unknown command: {args[0]}");
}

PKVault.Core.Program.Dispose();

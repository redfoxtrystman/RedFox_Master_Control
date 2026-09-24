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


static async Task SeedTmt(IServiceProvider sp)
{
    // Mixed-format compatibility profile:
    // - TMT v1.6 direct-species .tmt3
    // - stock Emerald .pk3
    // - native Gen 1 .pk1
    // - native Gen 2 .pk2
    //
    // This is intentionally not one homogeneous format. The whole point is to
    // exercise PKVault's conversion path when the user drags older/vanilla
    // Pokemon into the loaded Too Many Types save.

    var tmtSet = new (ushort Species, byte Form, string Name, byte Level)[]
    {
        (654, 0, "BRAIXEN", 24),   // Fire / Magic / Furry
        (280, 0, "RALTS", 18),     // Space / Fairy
        (728, 0, "POPPLIO", 20),   // Water / Silly
        (778, 0, "MIMIKYU", 28),   // Ghost / Sus
        (885, 0, "DREEPY", 22),    // Gun / Ghost / Baby
        (872, 0, "SNOM", 16),      // Ice / Bean
        (856, 0, "HATENNA", 19),   // Vibe / Magic
        (870, 0, "FALINKS", 30),   // Silly / Little / Guys
        (765, 0, "ORANGURU", 27),  // Monke / Stinky
        (599, 0, "KLINK", 21),     // Steel / Guys / Prime
    };

    var emeraldSet = new (ushort Species, string Name, byte Level)[]
    {
        (257, "BLAZIKEN", 36),   // regression: stock Gen3 internal id 282
        (261, "POOCHYENA", 12),
        (270, "LOTAD", 14),
        (280, "RALTS", 16),
        (282, "GARDEVOIR", 38),
        (292, "SHEDINJA", 25),
        (302, "SABLEYE", 27),
        (327, "SPINDA", 24),
        (334, "ALTARIA", 39),
        (350, "MILOTIC", 42),
        (358, "CHIMECHO", 35),   // regression: stock Gen3 internal id 411
        (359, "ABSOL", 37),
        (376, "METAGROSS", 50),
        (384, "RAYQUAZA", 70),
        (386, "DEOXYS", 50),
    };

    var gen1Set = new (ushort Species, string Name, byte Level)[]
    {
        (25, "PIKACHU", 20),
        (37, "VULPIX", 22),
        (50, "DIGLETT", 19),
        (56, "MANKEY", 21),
        (58, "GROWLITHE", 23),
        (66, "MACHOP", 24),
        (74, "GEODUDE", 20),
        (79, "SLOWPOKE", 25),
        (98, "KRABBY", 22),
        (132, "DITTO", 25),
        (133, "EEVEE", 20),
        (134, "VAPOREON", 30),
        (137, "PORYGON", 28),
        (143, "SNORLAX", 35),
        (151, "MEW", 40),
    };

    var gen2Set = new (ushort Species, string Name, byte Level)[]
    {
        (152, "CHIKORITA", 18),
        (162, "FURRET", 24),
        (169, "CROBAT", 32),
        (172, "PICHU", 12),
        (183, "MARILL", 20),
        (185, "SUDOWOODO", 25),
        (190, "AIPOM", 22),
        (196, "ESPEON", 30),
        (197, "UMBREON", 30),
        (203, "GIRAFARIG", 28),
        (206, "DUNSPARCE", 24),
        (223, "REMORAID", 21),
        (227, "SKARMORY", 30),
        (233, "PORYGON2", 32),
        (235, "SMEARGLE", 26),
    };

    var settingsService = sp.GetRequiredService<ISettingsService>();
    var currentSettings = settingsService.GetSettings();
    await settingsService.UpdateSettingsSimple(
        currentSettings.SettingsMutable with
        {
            SAVE_GLOBS = [],
            TRADER_NAME = "TMT Compatibility Test",
        },
        currentSettings.UserId
    );

    using var scope = sp.CreateScope();
    var boxes = scope.ServiceProvider.GetRequiredService<IBoxLoader>();
    var loader = scope.ServiceProvider.GetRequiredService<IPkmVariantLoader>();
    var session = sp.GetRequiredService<ISessionService>();

    if ((await loader.GetAllEntities()).Count != 0)
        throw new Exception("Refusing to seed non-empty PKVault TMT compatibility profile.");

    var defaultBoxEntity = await boxes.GetEntity("0") ?? throw new Exception("Default Box 0 missing.");
    defaultBoxEntity.Name = "TMT v1.6";
    defaultBoxEntity.SlotCount = 30;
    await boxes.UpdateEntity(defaultBoxEntity);

    async Task<BoxDTO> CreateTestBox(string name)
    {
        var bankBoxes = await boxes.GetEntitiesByBank(defaultBoxEntity.BankId);
        var maxId = await boxes.GetMaxId();
        var maxOrder = bankBoxes.Count == 0 ? 0 : bankBoxes.Values.Max(x => x.Order);

        var entity = await boxes.AddEntity(new BoxEntity
        {
            Id = (maxId + 1).ToString(),
            IdInt = maxId + 1,
            Name = name,
            Order = maxOrder + BoxLoader.OrderGap,
            Type = BoxType.Box,
            SlotCount = 30,
            BankId = defaultBoxEntity.BankId,
        });
        await boxes.NormalizeOrders();
        return boxes.CreateDTO(entity);
    }

    var tmtBox = await boxes.GetDto("0") ?? throw new Exception("TMT test box missing.");
    var emeraldBox = await CreateTestBox("Emerald PK3");
    var gen1Box = await CreateTestBox("Gen 1 PK1");
    var gen2Box = await CreateTestBox("Gen 2 PK2");

    async Task AddToBox(BoxDTO box, int slot, PKM pkm, string id)
    {
        var immutable = new ImmutablePKM(pkm);
        if (!immutable.IsEnabled)
            throw new Exception($"Seed Pokemon {pkm.Species} ({id}) is disabled.");

        await loader.AddEntity(new(
            Box: box,
            BoxSlot: slot,
            IsMain: true,
            IsExternal: false,
            AttachedSaveId: null,
            AttachedSavePkmIdBase: null,
            Context: pkm.Context,
            Generation: pkm.Generation,
            Pkm: immutable,
            Id: id
        ));
    }

    for (var i = 0; i < tmtSet.Length; i++)
    {
        var s = tmtSet[i];
        var entry = TooManyTypesCompat.RequireSupported(s.Species, s.Form);

        var p = new PK3
        {
            DirectSpeciesIDs = true,
            PID = (uint)(0x13570000 + i * 0x101),
            TID16 = (ushort)(51000 + i),
            SID16 = (ushort)(61000 + i),
            Version = GameVersion.E,
            Language = (int)LanguageID.English,
            Ball = 4,
            OriginalTrainerGender = 0,
        };

        p.SpeciesInternal = entry.RawSpecies;
        p.CurrentLevel = s.Level;
        p.OriginalTrainerName = "TMTTEST";
        p.Nickname = s.Name;
        p.Move1 = 33;
        p.Move1_PP = 35;
        p.RefreshChecksum();

        var immutable = new ImmutablePKM(p);
        if (TooManyTypesCompat.GetTypes(immutable) is not { Length: > 0 })
            throw new Exception($"TMT seed Pokemon {s.Name} lost ROM-hack type metadata.");

        await AddToBox(tmtBox, i, p, $"compat-tmt-{i:00}");
    }

    for (var i = 0; i < emeraldSet.Length; i++)
    {
        var s = emeraldSet[i];
        var p = new PK3
        {
            PID = (uint)(0x24680000 + i * 0x111),
            TID16 = (ushort)(22000 + i),
            SID16 = (ushort)(32000 + i),
            Version = GameVersion.E,
            Language = (int)LanguageID.English,
            Ball = 4,
            OriginalTrainerGender = 0,
            Species = s.Species,
            CurrentLevel = s.Level,
            Move1 = 33,
            Move1_PP = 35,
        };
        p.OriginalTrainerName = "EMERALD";
        p.Nickname = s.Name;
        p.RefreshChecksum();

        if (p.DirectSpeciesIDs)
            throw new Exception($"Vanilla Emerald seed {s.Name} incorrectly entered direct-species mode.");

        await AddToBox(emeraldBox, i, p, $"compat-emerald-{i:00}");
    }

    for (var i = 0; i < gen1Set.Length; i++)
    {
        var s = gen1Set[i];
        if (!TooManyTypesProfileGenerated.Entries.Any(e => e.Species == s.Species && e.Form == 0))
            throw new Exception($"Gen1 test species {s.Name} is not supported by TMT v1.6.");

        var p = new PK1
        {
            Species = s.Species,
            TID16 = (ushort)(11000 + i),
            DV16 = (ushort)(0x1111 + (i * 0x0101)),
            CurrentLevel = s.Level,
        };
        p.OriginalTrainerName = "GEN1TEST";
        p.Nickname = s.Name;
        await AddToBox(gen1Box, i, p, $"compat-gen1-{i:00}");
    }

    for (var i = 0; i < gen2Set.Length; i++)
    {
        var s = gen2Set[i];
        if (!TooManyTypesProfileGenerated.Entries.Any(e => e.Species == s.Species && e.Form == 0))
            throw new Exception($"Gen2 test species {s.Name} is not supported by TMT v1.6.");

        var p = new PK2
        {
            Species = s.Species,
            TID16 = (ushort)(12000 + i),
            DV16 = (ushort)(0x2222 + (i * 0x0101)),
            CurrentLevel = s.Level,
            Version = GameVersion.C,
        };
        p.OriginalTrainerName = "GEN2TEST";
        p.Nickname = s.Name;
        await AddToBox(gen2Box, i, p, $"compat-gen2-{i:00}");
    }

    await session.PersistSession(scope);

    var all = await loader.GetAllEntities();
    if (all.Count != 55)
        throw new Exception($"Expected exactly 55 compatibility test Pokemon, got {all.Count}.");

    Console.WriteLine("SEEDED TMT COMPATIBILITY PROFILE: 10 TMT + 15 Emerald + 15 Gen1 + 15 Gen2 = 55");
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

static async Task AssertDexCaught(IServiceProvider sp, params ushort[] species)
{
    using var scope = sp.CreateScope();
    var dexLoader = scope.ServiceProvider.GetRequiredService<IDexLoader>();
    var entries = await dexLoader.GetEntitiesBySpecies(species);

    foreach (var s in species)
    {
        if (!entries.TryGetValue(s, out var forms) || !forms.Any(f => f.IsCaught))
            throw new Exception($"Expected species {s} to remain registered as caught in PKVault Pokedex.");
    }

    Console.WriteLine($"DEX CAUGHT {string.Join(",", species)}");
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

    // Receiving through trade must permanently register the species in PKVault's
    // central Pokedex immediately after the committed trade.
    if (host)
        await AssertDexCaught(sp, 27);      // A received Sandshrew
    else
        await AssertDexCaught(sp, 63, 58); // B received Abra + Growlithe

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

    if (host)
    {
        // A traded the received Sandshrew away again. It must no longer be
        // owned, but the caught dex history must remain permanently registered.
        var afterGift = await MainPkms(sp);
        if (afterGift.Any(p => p.Species == 27))
            throw new Exception("Trader A should no longer own Sandshrew after gifting it away.");
        await AssertDexCaught(sp, 27);
    }
    else
    {
        await AssertDexCaught(sp, 63, 58, 27);
    }
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
    throw new ArgumentException("usage: seed A|B | seed-tmt | host | join | direct-host address-file | direct-join address-file | verify csv");

var sp = await Boot();

switch (args[0].ToLowerInvariant())
{
    case "seed":
        await Seed(sp, args[1]);
        break;
    case "seed-tmt":
        await SeedTmt(sp);
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

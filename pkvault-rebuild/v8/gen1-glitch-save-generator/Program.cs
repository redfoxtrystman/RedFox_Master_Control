using PKHeX.Core;

static void Need(bool value, string message)
{
    if (!value)
        throw new Exception(message);
}

static PK1 MakeGlitch(byte rawIndex, ushort trainerId)
{
    var pk = new PK1(false)
    {
        TID16 = trainerId,
        EXP = 125_000,
        CatchRate = 45,
        DV16 = 0x7777,
        EV_HP = 512,
        EV_ATK = 512,
        EV_DEF = 512,
        EV_SPE = 512,
        EV_SPC = 512,
        Move1 = 33, // Tackle; safe non-zero body data for raw index 00.
        Move1_PP = 35,
        Stat_Level = 50,
        Stat_HPCurrent = 100,
        Stat_HPMax = 100,
        Stat_ATK = 80,
        Stat_DEF = 80,
        Stat_SPE = 80,
        Stat_SPC = 80,
    };

    pk.OriginalTrainerName = "GLITCH";
    pk.Nickname = $"GL{rawIndex:X2}";
    pk.SpeciesInternal = rawIndex; // Set last: preserve the exact raw glitch slot.
    return pk;
}

static byte[] BuildSave(GameVersion version, IReadOnlyList<byte> indices)
{
    var sav = new SAV1(LanguageID.English, version)
    {
        OT = version == GameVersion.YW ? "YGLITCH" : "RBGLITC",
        TID16 = version == GameVersion.YW ? (ushort)5252 : (ushort)5151,
        Money = 999_999,
    };

    // SAV1 detects Yellow from Pikachu's internal starter ID when re-opened.
    sav.Starter = version == GameVersion.YW
        ? (byte)SpeciesConverter.GetInternal1((ushort)Species.Pikachu)
        : (byte)SpeciesConverter.GetInternal1((ushort)Species.Bulbasaur);

    for (var i = 0; i < indices.Count; i++)
        sav.SetBoxSlotAtIndex(MakeGlitch(indices[i], sav.TID16), i, EntityImportSettings.None);

    return sav.Write(BinaryExportSetting.None).ToArray();
}

static void Verify(byte[] data, GameVersion expectedVersion, IReadOnlyList<byte> expected)
{
    var sav = new SAV1(data, LanguageID.English);
    Need(sav.Version == expectedVersion,
        $"Reloaded save identified as {sav.Version}, expected {expectedVersion}.");

    var found = new List<byte>();
    for (var i = 0; i < sav.BoxCount * sav.BoxSlotCount; i++)
    {
        if (sav.GetBoxSlotAtIndex(i) is not PK1 pk || !PokeList1.IsKnownGen1Glitch(pk))
            continue;
        found.Add(pk.SpeciesInternal);
    }

    Need(found.Count == expected.Count,
        $"Reloaded {expectedVersion} save contains {found.Count} glitch entries, expected {expected.Count}.");
    Need(found.SequenceEqual(expected),
        $"Reloaded {expectedVersion} save raw glitch index order does not match the expected catalog.");
}

var outDir = args.Length > 0 ? Path.GetFullPath(args[0]) : Path.GetFullPath("gen1-glitch-test-saves");
Directory.CreateDirectory(outDir);

var indices = Enumerable.Range(0, 256)
    .Select(x => (byte)x)
    .Where(x => SpeciesConverter.GetNational1(x) == 0)
    .ToArray();

Need(indices.Length == 105, $"Expected all 105 unused Gen-I raw species indices, found {indices.Length}.");
Need(indices[0] == 0x00 && indices.Contains((byte)0xBF) && indices[^1] == 0xFF,
    "Gen-I glitch index catalog is incomplete.");

var rb = BuildSave(GameVersion.RB, indices);
var yellow = BuildSave(GameVersion.YW, indices);
Verify(rb, GameVersion.RB, indices);
Verify(yellow, GameVersion.YW, indices);

File.WriteAllBytes(Path.Combine(outDir, "PKVault-Gen1-Glitches-RedBlue.sav"), rb);
File.WriteAllBytes(Path.Combine(outDir, "PKVault-Gen1-Glitches-Yellow.sav"), yellow);
File.WriteAllText(Path.Combine(outDir, "GLITCH_COUNT.txt"), indices.Length + Environment.NewLine);
File.WriteAllText(Path.Combine(outDir, "RAW_INDICES.txt"),
    string.Join(Environment.NewLine, indices.Select(x => $"0x{x:X2} ({x})")) + Environment.NewLine);
File.WriteAllText(Path.Combine(outDir, "README.txt"), """
PKVault alpha52t - Generation I Glitch Pokemon Test Saves
========================================================

PKVault-Gen1-Glitches-RedBlue.sav
  - Red/Blue-family display data.
  - Contains every raw Gen-I species index that does not map to a normal Pokemon.

PKVault-Gen1-Glitches-Yellow.sav
  - Yellow-family display data.
  - Contains the same complete raw-index set so PKVault can exercise Yellow names/sprites.

There are 105 raw glitch slots total: index 0x00, the 39 MissingNo. holes among
0x01-0xBE, and every index 0xBF-0xFF. The two saves keep the same raw slots because
Red/Blue and Yellow interpret many of those slots differently.

These are deliberately synthetic QA saves for PKVault. Use copies only; Generation I
glitch Pokemon can have unsafe behavior in the original games.
""");

Console.WriteLine($"PASS: generated and round-tripped two Gen-I glitch saves with all {indices.Length} raw glitch indices.");

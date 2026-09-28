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

static byte[] BuildSaveFromTemplate(string templatePath, GameVersion version, IReadOnlyList<byte> indices)
{
    var template = File.ReadAllBytes(templatePath);
    Need(template.Length == SaveUtil.SIZE_G1RAW,
        $"Gen-I template must be exactly {SaveUtil.SIZE_G1RAW} bytes; got {template.Length}: {templatePath}");

    var templateProbe = new SAV1(template, LanguageID.English, version);
    Need(templateProbe.ChecksumsValid, $"Gen-I template checksum is invalid: {templatePath}");

    // Empty the *packed SRAM lists* before SAV1 unpacks them. Using ClearBoxes()
    // here is unsafe for this QA build because raw species 00/FF collide with
    // Gen-I list sentinels; a fake BlankPKM can therefore look like a glitch.
    // The packed count/species header is authoritative to the real game.
    var working = template.ToArray();
    const int BoxLength = 0x462;
    static void ClearPackedBox(byte[] data, int offset)
    {
        data[offset] = 0; // occupied count
        data.AsSpan(offset + 1, 21).Fill(0xFF); // 20 species marks + terminator
    }

    for (var i = 0; i < 6; i++)
        ClearPackedBox(working, 0x4000 + (i * BoxLength));
    for (var i = 0; i < 6; i++)
        ClearPackedBox(working, 0x6000 + (i * BoxLength));
    ClearPackedBox(working, 0x30C0); // current-box mirror

    // Box 1 current + initialized. Recalculate the ordinary R/B/Y main checksum
    // because CurrentBoxIndex and the current-box mirror live in the checked area.
    working[0x284C] = 0x80;
    var sum = 0;
    for (var i = 0x2598; i < 0x3523; i++)
        sum = (sum + working[i]) & 0xFF;
    working[0x3523] = (byte)(~sum & 0xFF);

    var sav = new SAV1(working, LanguageID.English, version);
    Need(sav.ChecksumsValid, "Cleared Gen-I working template checksum is invalid.");
    sav.CurrentBox = 0;
    sav.BoxesInitialized = true;
    sav.OT = version == GameVersion.YW ? "YGLITCH" : "RBGLITC";
    sav.TID16 = version == GameVersion.YW ? (ushort)5252 : (ushort)5151;
    sav.Money = 999_999;

    if (version == GameVersion.YW)
        sav.Starter = (byte)SpeciesConverter.GetInternal1((ushort)Species.Pikachu);

    for (var i = 0; i < indices.Count; i++)
        sav.SetBoxSlotAtIndex(MakeGlitch(indices[i], sav.TID16), i, EntityImportSettings.None);

    return sav.Write(BinaryExportSetting.None).ToArray();
}

static void Verify(byte[] data, GameVersion expectedVersion, IReadOnlyList<byte> expected)
{
    Need(data.Length == SaveUtil.SIZE_G1RAW, $"Generated save is not 32 KiB: {data.Length}");
    var sav = new SAV1(data, LanguageID.English, expectedVersion);
    Need(sav.ChecksumsValid, $"Generated {expectedVersion} save checksum is invalid.");

    // Generation-I SRAM box lists carry their own authoritative occupied count.
    // GetBoxSlotAtIndex() still returns a blank PK1 object for an empty position;
    // raw species 00 is also a real glitch species, so scanning all 240 PK1
    // objects falsely counts blank positions as 'M. Validate the packed SRAM
    // headers first, then inspect exactly the occupied catalog slots.
    const int BoxLength = 0x462;
    var boxOffsets = Enumerable.Range(0, 6).Select(i => 0x4000 + (i * BoxLength))
        .Concat(Enumerable.Range(0, 6).Select(i => 0x6000 + (i * BoxLength)))
        .ToArray();
    var boxCounts = boxOffsets.Select(o => (int)data[o]).ToArray();
    var expectedCounts = new[] { 20, 20, 20, 20, 20, 5, 0, 0, 0, 0, 0, 0 };
    Need(boxCounts.SequenceEqual(expectedCounts),
        $"Generated {expectedVersion} packed box counts are wrong: [{string.Join(", ", boxCounts)}].");

    var found = new List<byte>(expected.Count);
    for (var i = 0; i < expected.Count; i++)
    {
        Need(sav.GetBoxSlotAtIndex(i) is PK1, $"Slot {i} did not reload as PK1.");
        var pk = (PK1)sav.GetBoxSlotAtIndex(i);
        Need(PokeList1.IsKnownGen1Glitch(pk),
            $"Occupied QA slot {i} did not reload as a Gen-I glitch Pokemon.");
        found.Add(pk.SpeciesInternal);
    }

    Need(found.SequenceEqual(expected),
        $"Reloaded {expectedVersion} save raw glitch index order does not match the expected catalog.");
}

var outDir = args.Length > 0 ? Path.GetFullPath(args[0]) : Path.GetFullPath("gen1-glitch-test-saves");
Need(args.Length >= 2, "Usage: Gen1GlitchSaveGenerator <outDir> <redBlueTemplate> [yellowTemplate]");
var rbTemplate = Path.GetFullPath(args[1]);
var yellowTemplate = args.Length >= 3 ? Path.GetFullPath(args[2]) : null;
Directory.CreateDirectory(outDir);

var indices = Enumerable.Range(0, 256)
    .Select(x => (byte)x)
    .Where(x => SpeciesConverter.GetNational1(x) == 0)
    .ToArray();

Need(indices.Length == 105, $"Expected all 105 unused Gen-I raw species indices, found {indices.Length}.");
Need(indices[0] == 0x00 && indices.Contains((byte)0xBF) && indices[^1] == 0xFF,
    "Gen-I glitch index catalog is incomplete.");

var rb = BuildSaveFromTemplate(rbTemplate, GameVersion.RB, indices);
Verify(rb, GameVersion.RB, indices);
File.WriteAllBytes(Path.Combine(outDir, "PKVault-Gen1-Glitches-RedBlue.sav"), rb);

if (yellowTemplate is not null)
{
    var yellow = BuildSaveFromTemplate(yellowTemplate, GameVersion.YW, indices);
    Verify(yellow, GameVersion.YW, indices);
    File.WriteAllBytes(Path.Combine(outDir, "PKVault-Gen1-Glitches-Yellow.sav"), yellow);
}
else
{
    File.WriteAllText(
        Path.Combine(outDir, "YELLOW_TEMPLATE_REQUIRED.txt"),
        "A real, game-created Pokemon Yellow save is required before generating the Yellow glitch QA save.\n" +
        "Alpha52u intentionally refuses to manufacture Yellow from blank or Red/Blue SRAM.\n");
}
File.WriteAllText(Path.Combine(outDir, "GLITCH_COUNT.txt"), indices.Length + Environment.NewLine);
File.WriteAllText(Path.Combine(outDir, "RAW_INDICES.txt"),
    string.Join(Environment.NewLine, indices.Select(x => $"0x{x:X2} ({x})")) + Environment.NewLine);
File.WriteAllText(Path.Combine(outDir, "README.txt"), """
PKVault alpha52u - Generation I Glitch Pokemon Test Saves
========================================================

PKVault-Gen1-Glitches-RedBlue.sav
  - Red/Blue-family display data.
  - Contains every raw Gen-I species index that does not map to a normal Pokemon.

The old alpha52t generator built its SRAM from a blank SAV1. That file could pass
PKHeX round-trip checks while still being rejected by an actual Gen-I game/emulator.

Alpha52u builds Red/Blue from a real game-created Gen-I save template and replaces
only PC storage. Yellow is generated only when a real Pokemon Yellow save template
is supplied; Red/Blue SRAM is not relabeled as Yellow.

There are 105 raw glitch slots total: index 0x00, the 39 MissingNo. holes among
0x01-0xBE, and every index 0xBF-0xFF.

Use copies only; Generation I glitch Pokemon can have unsafe behavior in the original games.
""");

Console.WriteLine($"PASS: generated real-template Gen-I glitch save with all {indices.Length} raw glitch indices.");

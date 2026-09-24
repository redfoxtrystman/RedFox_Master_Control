using System.Security.Cryptography;
using PKHeX.Core;

namespace PKVault.Core;

public enum EssentialsGameKind
{
    Unknown = 0,
    Uranium = 1,
    Insurgence = 2,
}

public sealed record EssentialsLegacySaveData(
    EssentialsGameKind Game,
    string ProfileId,
    string ProfileVersion,
    string TrainerName,
    uint TrainerId,
    IReadOnlyList<PKEssentials> Party,
    IReadOnlyList<EssentialsBoxData> Boxes,
    IReadOnlyList<RubyMarshalDocument> Documents,
    byte[] OriginalBytes
)
{
    public int PokemonCount => Party.Count + Boxes.Sum(z => z.Pokemon.Count(p => p != null));
}

public sealed record EssentialsBoxData(string Name, IReadOnlyList<PKEssentials?> Pokemon);

/// <summary>
/// Loader for pre-v19 Pokémon Essentials concatenated Ruby Marshal saves
/// (the structure used by Uranium and Insurgence).
/// </summary>
public static class EssentialsLegacySaveReader
{
    public const int ExpectedLegacyStreamCount = 15;

    public static bool TryRead(byte[] bytes, string path, out EssentialsLegacySaveData? save, out string? error)
    {
        save = null;
        error = null;

        try
        {
            var documents = ReadDocuments(bytes);
            if (documents.Count < 2)
                throw new InvalidDataException($"Expected multiple Ruby Marshal streams, found {documents.Count}.");

            var trainerDoc = documents.FirstOrDefault(z => RubyValue.Object(z.Root, "PokeBattle_Trainer") != null)
                ?? throw new InvalidDataException("PokeBattle_Trainer stream not found.");
            var storageDoc = documents.FirstOrDefault(z => RubyValue.Object(z.Root, "PokemonStorage") != null)
                ?? throw new InvalidDataException("PokemonStorage stream not found.");

            var trainer = (RubyObject)trainerDoc.Root!;
            var storage = (RubyObject)storageDoc.Root!;

            var trainerName = RubyValue.Text(Get(trainer, "@name"), "TRAINER");
            var trainerId = unchecked((uint)RubyValue.Int(Get(trainer, "@id"), 0));

            var rawParty = RubyValue.Array(Get(trainer, "@party"));
            var rawBoxes = RubyValue.Array(Get(storage, "@boxes"));

            var game = DetectGame(path, bytes, rawParty, rawBoxes);
            var profileId = game switch
            {
                EssentialsGameKind.Uranium => "pokemon-uranium",
                EssentialsGameKind.Insurgence => "pokemon-insurgence",
                _ => "pokemon-essentials-unknown",
            };
            var profileVersion = game switch
            {
                EssentialsGameKind.Uranium => "legacy-ruby18",
                EssentialsGameKind.Insurgence => "legacy-ruby18",
                _ => "legacy-ruby18",
            };

            var party = new List<PKEssentials>();
            if (rawParty != null)
            {
                for (var i = 0; i < rawParty.Items.Count; i++)
                {
                    if (RubyValue.Object(rawParty.Items[i], "PokeBattle_Pokemon") is { } raw)
                        party.Add(ConvertPokemon(raw, game, profileId, profileVersion, trainerName, trainerId, path, "party", i));
                }
            }

            var boxes = new List<EssentialsBoxData>();
            if (rawBoxes != null)
            {
                for (var boxIndex = 0; boxIndex < rawBoxes.Items.Count; boxIndex++)
                {
                    if (RubyValue.Object(rawBoxes.Items[boxIndex], "PokemonBox") is not { } box)
                        continue;

                    var name = RubyValue.Text(Get(box, "@name"), $"Box {boxIndex + 1}");
                    var slots = RubyValue.Array(Get(box, "@pokemon"));
                    var mons = new List<PKEssentials?>();

                    if (slots != null)
                    {
                        for (var slot = 0; slot < slots.Items.Count; slot++)
                        {
                            var raw = RubyValue.Object(slots.Items[slot], "PokeBattle_Pokemon");
                            mons.Add(raw == null
                                ? null
                                : ConvertPokemon(raw, game, profileId, profileVersion, trainerName, trainerId, path, $"box:{boxIndex}", slot));
                        }
                    }

                    boxes.Add(new(name, mons));
                }
            }

            save = new(
                Game: game,
                ProfileId: profileId,
                ProfileVersion: profileVersion,
                TrainerName: trainerName,
                TrainerId: trainerId,
                Party: party,
                Boxes: boxes,
                Documents: documents,
                OriginalBytes: bytes
            );
            return true;
        }
        catch (Exception ex)
        {
            error = ex.Message;
            return false;
        }
    }

    public static List<RubyMarshalDocument> ReadDocuments(byte[] bytes)
    {
        var documents = new List<RubyMarshalDocument>();
        var pos = 0;

        // Fast/strict path: each top-level Marshal.dump begins immediately
        // after the preceding root value.
        try
        {
            while (pos < bytes.Length)
            {
                var reader = new RubyMarshal48Reader(bytes, pos);
                var doc = reader.ReadDocument();
                if (doc.Length <= 2)
                    throw new InvalidDataException("Empty Ruby Marshal document.");
                documents.Add(doc);
                pos += doc.Length;
            }

            if (pos == bytes.Length)
                return documents;
        }
        catch
        {
            documents.Clear();
        }

        // Recovery path for a tag not needed by trainer/storage: locate valid
        // independent Marshal headers and retain roots that parse cleanly.
        for (var i = 0; i + 2 <= bytes.Length; i++)
        {
            if (bytes[i] != 4 || bytes[i + 1] != 8)
                continue;

            try
            {
                var reader = new RubyMarshal48Reader(bytes, i);
                var doc = reader.ReadDocument();
                if (doc.Length > 2)
                {
                    documents.Add(doc);
                    i += doc.Length - 1;
                }
            }
            catch
            {
                // False 04 08 byte pair inside another payload.
            }
        }

        return documents
            .GroupBy(z => z.Offset)
            .Select(z => z.First())
            .OrderBy(z => z.Offset)
            .ToList();
    }

    private static EssentialsGameKind DetectGame(
        string path,
        byte[] bytes,
        RubyArray? party,
        RubyArray? boxes)
    {
        var lower = path.ToLowerInvariant();
        if (lower.Contains("uranium"))
            return EssentialsGameKind.Uranium;
        if (lower.Contains("insurgence"))
            return EssentialsGameKind.Insurgence;

        // These are diagnostics/fallback signatures only. Standard install
        // paths remain the preferred detector.
        if (ContainsAscii(bytes, "nextBattleNuclearHorde") || ContainsAscii(bytes, "nuclear"))
            return EssentialsGameKind.Uranium;
        if (ContainsAscii(bytes, "megaforme") || ContainsAscii(bytes, "trainerdetection"))
            return EssentialsGameKind.Insurgence;

        var maxSpecies = EnumeratePokemon(party, boxes)
            .Select(p => RubyValue.Int(Get(p, "@species"), 0))
            .DefaultIfEmpty(0)
            .Max();

        // Uranium's internal local dex is compact; Insurgence Delta/custom
        // species use high Essentials IDs. This is a last-resort heuristic.
        return maxSpecies > 300
            ? EssentialsGameKind.Insurgence
            : EssentialsGameKind.Unknown;
    }

    private static IEnumerable<RubyObject> EnumeratePokemon(RubyArray? party, RubyArray? boxes)
    {
        if (party != null)
            foreach (var item in party.Items)
                if (RubyValue.Object(item, "PokeBattle_Pokemon") is { } p)
                    yield return p;

        if (boxes == null)
            yield break;

        foreach (var boxValue in boxes.Items)
        {
            var box = RubyValue.Object(boxValue, "PokemonBox");
            var slots = box == null ? null : RubyValue.Array(Get(box, "@pokemon"));
            if (slots == null)
                continue;

            foreach (var item in slots.Items)
                if (RubyValue.Object(item, "PokeBattle_Pokemon") is { } p)
                    yield return p;
        }
    }

    private static PKEssentials ConvertPokemon(
        RubyObject raw,
        EssentialsGameKind game,
        string profileId,
        string profileVersion,
        string trainerName,
        uint trainerId,
        string sourcePath,
        string sourceContainer,
        int sourceSlot)
    {
        var species = checked((int)RubyValue.Int(Get(raw, "@species"), 0));
        var form = checked((int)RubyValue.Int(Get(raw, "@form"), 0));
        var nickname = RubyValue.Text(Get(raw, "@name"));
        var exp = checked((uint)Math.Max(0, RubyValue.Int(Get(raw, "@exp"), 0)));
        var personalId = unchecked((uint)RubyValue.Int(Get(raw, "@personalID"), 0));
        var ownerId = unchecked((uint)RubyValue.Int(Get(raw, "@trainerID"), trainerId));

        var moves = new ushort[4];
        var movePp = new int[4];
        var movePpUps = new int[4];
        var moveNames = new string[4];

        if (RubyValue.Array(Get(raw, "@moves")) is { } moveArray)
        {
            for (var i = 0; i < Math.Min(4, moveArray.Items.Count); i++)
            {
                if (RubyValue.Object(moveArray.Items[i], "PBMove") is not { } move)
                    continue;

                moves[i] = checked((ushort)Math.Clamp(RubyValue.Int(Get(move, "@id"), 0), 0, ushort.MaxValue));
                movePp[i] = checked((int)Math.Clamp(RubyValue.Int(Get(move, "@pp"), 0), 0, int.MaxValue));
                movePpUps[i] = checked((int)Math.Clamp(RubyValue.Int(Get(move, "@ppup"), 0), 0, 3));
            }
        }

        var iv = ReadStatArray(Get(raw, "@iv"));
        var ev = ReadStatArray(Get(raw, "@ev"));

        // Essentials save order: HP, Atk, Def, Speed, SpAtk, SpDef.
        var storedLevel = checked((byte)Math.Clamp(RubyValue.Int(Get(raw, "@level"), 1), 1, 255));
        var speciesName = EssentialsProfileFallback.GetSpeciesName(game, species, form, nickname);

        var payload = new EssentialsPkmPayload
        {
            ProfileId = profileId,
            ProfileVersion = profileVersion,
            SpeciesName = speciesName,
            TypeNames = EssentialsProfileFallback.GetTypes(game, species, form),
            MoveNames = moveNames,
            LocalSpeciesId = species,
            LocalFormId = form,
            Level = storedLevel,
            ReadOnlySource = false,
            SourceSavePath = sourcePath,
            SourceContainer = sourceContainer,
            SourceSlot = sourceSlot,
            SourceFingerprint = Fingerprint(raw, sourceContainer, sourceSlot),
            SourceRubyMarshal = RubyMarshal48Writer.WriteDocument(raw),

            Nickname = string.IsNullOrWhiteSpace(nickname) ? speciesName : nickname,
            OriginalTrainerName = RubyValue.Text(Get(raw, "@ot"), trainerName),
            TID16 = (ushort)ownerId,
            SID16 = (ushort)(ownerId >> 16),
            PID = personalId,
            EXP = exp,
            Gender = checked((byte)Math.Clamp(RubyValue.Int(Get(raw, "@genderflag"), 2), 0, 2)),
            Nature = checked((byte)Math.Clamp(RubyValue.Int(Get(raw, "@natureflag"), personalId % 25), 0, 24)),
            HeldItem = checked((int)RubyValue.Int(Get(raw, "@item"), 0)),
            Ability = checked((int)RubyValue.Int(Get(raw, "@abilityflag"), 0)),
            AbilityNumber = checked((int)RubyValue.Int(Get(raw, "@abilityflag"), 0)),
            Friendship = checked((byte)Math.Clamp(RubyValue.Int(Get(raw, "@happiness"), 70), 0, 255)),
            IsEgg = RubyValue.Int(Get(raw, "@eggsteps"), 0) > 0,
            Ball = checked((byte)Math.Clamp(RubyValue.Int(Get(raw, "@ballused"), 0), 0, 255)),
            MetLevel = checked((byte)Math.Clamp(RubyValue.Int(Get(raw, "@obtainLevel"), 0), 0, 255)),
            OriginalTrainerGender = checked((byte)Math.Clamp(RubyValue.Int(Get(raw, "@otgender"), 0), 0, 1)),

            Moves = moves,
            MovePP = movePp,
            MovePPUps = movePpUps,
            IVs = iv,
            EVs = ev,
            BaseStats = EssentialsProfileFallback.GetBaseStats(game, species, form),
            Stats = [
                checked((int)RubyValue.Int(Get(raw, "@totalhp"), 0)),
                checked((int)RubyValue.Int(Get(raw, "@attack"), 0)),
                checked((int)RubyValue.Int(Get(raw, "@defense"), 0)),
                checked((int)RubyValue.Int(Get(raw, "@speed"), 0)),
                checked((int)RubyValue.Int(Get(raw, "@spatk"), 0)),
                checked((int)RubyValue.Int(Get(raw, "@spdef"), 0)),
            ],
            CurrentHP = checked((int)RubyValue.Int(Get(raw, "@hp"), 0)),
            StatusCondition = checked((int)RubyValue.Int(Get(raw, "@status"), 0)),
        };

        return new(payload);
    }

    private static int[] ReadStatArray(object? value)
    {
        var arr = RubyValue.Array(value);
        var result = new int[6];
        if (arr == null)
            return result;

        for (var i = 0; i < Math.Min(6, arr.Items.Count); i++)
            result[i] = checked((int)RubyValue.Int(arr.Items[i], 0));
        return result;
    }

    private static object? Get(RubyObject obj, string key)
        => obj.Fields.TryGetValue(key, out var value) ? value : null;

    private static string Fingerprint(RubyObject raw, string container, int slot)
    {
        var species = RubyValue.Int(Get(raw, "@species"));
        var pid = RubyValue.Int(Get(raw, "@personalID"));
        var tid = RubyValue.Int(Get(raw, "@trainerID"));
        var input = System.Text.Encoding.UTF8.GetBytes($"{container}|{slot}|{species}|{pid}|{tid}");
        return Convert.ToHexString(SHA256.HashData(input)).ToLowerInvariant();
    }

    private static bool ContainsAscii(byte[] data, string value)
    {
        var needle = System.Text.Encoding.ASCII.GetBytes(value);
        return data.AsSpan().IndexOf(needle) >= 0;
    }
}

/// <summary>
/// Small bootstrap table only. Exact full species/type/move data will be
/// generated from the user's installed game data/profile in the next layer.
/// Never aliases unknown profile-local IDs to official National Dex IDs.
/// </summary>
public static class EssentialsProfileFallback
{
    private static readonly Dictionary<int, (string Name, string[] Types, int[] Stats)> Uranium = new()
    {
        [1] = ("Orchynx", ["Grass", "Steel"], [50,55,55,50,70,70]),
        [2] = ("Metalynx", ["Grass", "Steel"], [85,95,115,65,70,100]),
        [3] = ("Raptorch", ["Fire", "Ground"], [40,55,45,70,65,50]),
        [4] = ("Archilles", ["Fire", "Ground"], [75,90,80,125,90,80]),
        [5] = ("Eletux", ["Water", "Electric"], [60,50,65,45,50,65]),
        [6] = ("Electruxo", ["Water", "Electric"], [95,80,95,85,90,105]),
        [7] = ("Chyinmunk", ["Normal"], [35,40,50,55,55,50]),
        [8] = ("Kinetmunk", ["Normal", "Electric"], [65,45,70,90,75,70]),
        [9] = ("Birbie", ["Normal", "Flying"], [50,36,30,43,55,50]),
        [10] = ("Aveden", ["Normal", "Flying"], [62,50,42,65,77,62]),
        [11] = ("Splendifowl", ["Normal", "Flying"], [80,65,55,93,105,80]),
        [12] = ("Cubbug", ["Bug"], [45,53,70,42,40,60]),
    };

    public static string GetSpeciesName(EssentialsGameKind game, int species, int form, string nickname)
    {
        if (game == EssentialsGameKind.Uranium && Uranium.TryGetValue(species, out var u))
            return u.Name;

        if (game == EssentialsGameKind.Insurgence && species > 0 && species < GameInfo.Strings.Species.Count)
            return GameInfo.Strings.Species[species];

        return game switch
        {
            EssentialsGameKind.Uranium => $"Uranium #{species}",
            EssentialsGameKind.Insurgence => $"Insurgence #{species}",
            _ => $"Essentials #{species}",
        };
    }

    public static string[] GetTypes(EssentialsGameKind game, int species, int form)
        => game == EssentialsGameKind.Uranium && Uranium.TryGetValue(species, out var u) ? u.Types : [];

    public static int[] GetBaseStats(EssentialsGameKind game, int species, int form)
        => game == EssentialsGameKind.Uranium && Uranium.TryGetValue(species, out var u) ? u.Stats : [1,1,1,1,1,1];
}

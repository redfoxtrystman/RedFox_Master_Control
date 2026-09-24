using System.Text;
using PKHeX.Core;

namespace PKVault.Core;

/// <summary>
/// Safe writer for pre-v19 Pokémon Essentials saves. Only the trainer stream
/// (party) and PokemonStorage stream (boxes) are rebuilt; all other top-level
/// Marshal streams and any bytes between them are copied byte-for-byte.
/// </summary>
public static class EssentialsLegacySaveWriter
{
    public static byte[] Write(
        EssentialsLegacySaveData source,
        IReadOnlyList<PKEssentials> party,
        IReadOnlyList<EssentialsBoxData> boxes)
    {
        ValidateProfiles(source.ProfileId, party, boxes);

        var trainerDoc = source.Documents.FirstOrDefault(z => RubyValue.Object(z.Root, "PokeBattle_Trainer") != null)
            ?? throw new InvalidDataException("PokeBattle_Trainer stream not found.");
        var storageDoc = source.Documents.FirstOrDefault(z => RubyValue.Object(z.Root, "PokemonStorage") != null)
            ?? throw new InvalidDataException("PokemonStorage stream not found.");

        var trainer = CloneObject((RubyObject)trainerDoc.Root!, "PokeBattle_Trainer");
        var storage = CloneObject((RubyObject)storageDoc.Root!, "PokemonStorage");

        var rawParty = RubyValue.Array(Get(trainer, "@party"))
            ?? throw new InvalidDataException("Trainer @party array not found.");
        rawParty.Items.Clear();
        foreach (var pkm in party)
            rawParty.Items.Add(BuildPokemon(pkm, source.ProfileId));

        var rawBoxes = RubyValue.Array(Get(storage, "@boxes"))
            ?? throw new InvalidDataException("PokemonStorage @boxes array not found.");

        for (var boxIndex = 0; boxIndex < rawBoxes.Items.Count; boxIndex++)
        {
            if (RubyValue.Object(rawBoxes.Items[boxIndex], "PokemonBox") is not { } rawBox)
                continue;

            var slots = RubyValue.Array(Get(rawBox, "@pokemon"))
                ?? throw new InvalidDataException($"PokemonBox {boxIndex} @pokemon array not found.");
            var desired = boxIndex < boxes.Count ? boxes[boxIndex].Pokemon : [];

            for (var slot = 0; slot < slots.Items.Count; slot++)
            {
                var pkm = slot < desired.Count ? desired[slot] : null;
                slots.Items[slot] = pkm == null ? null : BuildPokemon(pkm, source.ProfileId);
            }
        }

        var trainerBytes = RubyMarshal48Writer.WriteDocument(trainer);
        var storageBytes = RubyMarshal48Writer.WriteDocument(storage);

        using var output = new MemoryStream(source.OriginalBytes.Length + 4096);
        var cursor = 0;
        foreach (var doc in source.Documents.OrderBy(z => z.Offset))
        {
            if (doc.Offset < cursor)
                throw new InvalidDataException("Overlapping Ruby Marshal documents in source save.");

            if (doc.Offset > cursor)
                output.Write(source.OriginalBytes, cursor, doc.Offset - cursor);

            if (doc.Offset == trainerDoc.Offset)
                output.Write(trainerBytes);
            else if (doc.Offset == storageDoc.Offset)
                output.Write(storageBytes);
            else
                output.Write(source.OriginalBytes, doc.Offset, doc.Length);

            cursor = doc.Offset + doc.Length;
        }

        if (cursor < source.OriginalBytes.Length)
            output.Write(source.OriginalBytes, cursor, source.OriginalBytes.Length - cursor);

        return output.ToArray();
    }

    private static RubyObject BuildPokemon(PKEssentials pkm, string profileId)
    {
        if (!string.Equals(pkm.ProfileId, profileId, StringComparison.Ordinal))
            throw new InvalidOperationException($"Cannot write {pkm.ProfileId} Pokémon into {profileId} save.");
        if (pkm.ReadOnlySource || pkm.SourceRubyMarshal.Length == 0)
            throw new InvalidOperationException(
                "This Essentials Pokémon predates writable source-template support. Re-import it from its game save before writing it back.");

        var parsed = new RubyMarshal48Reader(pkm.SourceRubyMarshal).ReadDocument();
        var raw = RubyValue.Object(parsed.Root, "PokeBattle_Pokemon")
            ?? throw new InvalidDataException("Stored Essentials source template is not a PokeBattle_Pokemon.");

        SetInt(raw, "@species", pkm.LocalSpeciesId);
        SetInt(raw, "@form", pkm.LocalFormId);
        SetText(raw, "@name", pkm.Nickname);
        SetText(raw, "@ot", pkm.OriginalTrainerName);
        SetInt(raw, "@exp", pkm.EXP);
        SetInt(raw, "@personalID", pkm.PID);
        SetInt(raw, "@trainerID", pkm.ID32);
        SetInt(raw, "@level", pkm.StoredLevel);
        SetInt(raw, "@genderflag", pkm.Gender);
        SetInt(raw, "@natureflag", (int)pkm.Nature);
        SetInt(raw, "@item", pkm.HeldItem);
        SetInt(raw, "@abilityflag", pkm.AbilityNumber);
        SetInt(raw, "@happiness", pkm.CurrentFriendship);
        SetInt(raw, "@ballused", pkm.Ball);
        SetInt(raw, "@obtainLevel", pkm.MetLevel);
        SetInt(raw, "@otgender", pkm.OriginalTrainerGender);
        SetInt(raw, "@totalhp", pkm.Stat_HPMax);
        SetInt(raw, "@hp", pkm.Stat_HPCurrent);
        SetInt(raw, "@attack", pkm.Stat_ATK);
        SetInt(raw, "@defense", pkm.Stat_DEF);
        SetInt(raw, "@speed", pkm.Stat_SPE);
        SetInt(raw, "@spatk", pkm.Stat_SPA);
        SetInt(raw, "@spdef", pkm.Stat_SPD);
        SetInt(raw, "@status", pkm.Status_Condition);

        if (raw.Fields.ContainsKey("@eggsteps"))
        {
            var oldEggSteps = RubyValue.Int(Get(raw, "@eggsteps"), 0);
            raw.Fields["@eggsteps"] = pkm.IsEgg ? Math.Max(1, oldEggSteps) : 0L;
        }

        PatchStatArray(raw, "@iv", [pkm.IV_HP, pkm.IV_ATK, pkm.IV_DEF, pkm.IV_SPE, pkm.IV_SPA, pkm.IV_SPD]);
        PatchStatArray(raw, "@ev", [pkm.EV_HP, pkm.EV_ATK, pkm.EV_DEF, pkm.EV_SPE, pkm.EV_SPA, pkm.EV_SPD]);
        PatchMoves(raw, pkm);

        return raw;
    }

    private static void PatchMoves(RubyObject raw, PKEssentials pkm)
    {
        var moves = RubyValue.Array(Get(raw, "@moves"));
        if (moves == null)
            return;

        var ids = new[] { pkm.Move1, pkm.Move2, pkm.Move3, pkm.Move4 };
        var pp = new[] { pkm.Move1_PP, pkm.Move2_PP, pkm.Move3_PP, pkm.Move4_PP };
        var ppUps = new[] { pkm.Move1_PPUps, pkm.Move2_PPUps, pkm.Move3_PPUps, pkm.Move4_PPUps };

        for (var i = 0; i < Math.Min(4, moves.Items.Count); i++)
        {
            if (RubyValue.Object(moves.Items[i], "PBMove") is not { } move)
                continue;
            SetInt(move, "@id", ids[i]);
            SetInt(move, "@pp", pp[i]);
            SetInt(move, "@ppup", ppUps[i]);
        }
    }

    private static void PatchStatArray(RubyObject raw, string key, IReadOnlyList<int> values)
    {
        var array = RubyValue.Array(Get(raw, key));
        if (array == null)
            return;
        for (var i = 0; i < Math.Min(array.Items.Count, values.Count); i++)
            array.Items[i] = (long)values[i];
    }

    private static void SetInt(RubyObject obj, string key, long value)
    {
        if (obj.Fields.ContainsKey(key))
            obj.Fields[key] = value;
    }

    private static void SetText(RubyObject obj, string key, string value)
    {
        if (!obj.Fields.TryGetValue(key, out var current))
            return;

        if (current is RubyString rubyString)
        {
            rubyString.SetText(value);
            return;
        }

        obj.Fields[key] = new RubyString(Encoding.UTF8.GetBytes(value));
    }

    private static RubyObject CloneObject(RubyObject source, string className)
    {
        var clone = RubyMarshal48Writer.CloneValue(source);
        return RubyValue.Object(clone, className)
            ?? throw new InvalidDataException($"Failed to clone Ruby object {className}.");
    }

    private static object? Get(RubyObject obj, string key)
        => obj.Fields.TryGetValue(key, out var value) ? value : null;

    private static void ValidateProfiles(
        string profileId,
        IEnumerable<PKEssentials> party,
        IEnumerable<EssentialsBoxData> boxes)
    {
        foreach (var pkm in party.Concat(boxes.SelectMany(b => b.Pokemon).OfType<PKEssentials>()))
        {
            if (!string.Equals(pkm.ProfileId, profileId, StringComparison.Ordinal))
                throw new InvalidOperationException($"Cross-profile Essentials write blocked: {pkm.ProfileId} -> {profileId}.");
        }
    }
}

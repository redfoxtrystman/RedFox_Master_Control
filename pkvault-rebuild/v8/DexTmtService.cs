using PKHeX.Core;

namespace PKVault.Core;

/// <summary>
/// Pokédex adapter for Too Many Types v1.6 / direct-species Gen3 saves.
/// TMT contains post-Gen3 species and expansion forms, so the normal PKVault
/// Gen3 dex path cannot use StaticSpecies.Forms[EntityContext.Gen3].
/// </summary>
public sealed class DexTmtService(SAV3 save) : DexGenService(save)
{
    private readonly SAV3 TmtSave = save;

    public override Task<bool> UpdateDexWithSave(
        Dictionary<ushort, Dictionary<uint, DexItemDTO>> dex,
        StaticSpeciesData staticSpecies,
        HashSet<ushort>? speciesSet)
    {
        var owned = TmtSave.GetAllPKM()
            .Where(p => !p.IsEgg && p.Species != 0)
            .Select(p => new ImmutablePKM(p))
            .ToList();

        var saveId = new SaveWrapper(TmtSave).Id;

        foreach (var speciesGroup in TooManyTypesProfileGenerated.Entries.GroupBy(e => e.Species))
        {
            var species = speciesGroup.Key;
            if (speciesSet != null && !speciesSet.Contains(species))
                continue;

            var forms = new List<DexItemForm>();

            foreach (var entry in speciesGroup.OrderBy(e => e.Form))
            {
                var pi = Gen3DirectSpecies.GetPersonal(entry.Species, entry.Form);

                foreach (var gender in GetGenders(pi))
                {
                    var matches = owned.FindAll(p =>
                        p.Species == entry.Species &&
                        p.Form == entry.Form &&
                        p.Gender == gender);

                    var isOwned = matches.Count != 0;
                    var isOwnedShiny = matches.Any(p => p.IsShiny);
                    var isOwnedAlpha = matches.Any(p => p.IsAlpha);

                    forms.Add(new DexItemForm(
                        Id: DexLoader.GetId(entry.Species, entry.Form, gender),
                        Species: entry.Species,
                        Form: entry.Form,
                        Gender: gender,
                        Types: GetTypes(TmtSave.Generation, pi),
                        Abilities: GetAbilities(pi),
                        AbilityHidden: GetAbilityHidden(pi),
                        BaseStats: GetBaseStats(pi),
                        IsSeen: isOwned,
                        IsSeenShiny: isOwnedShiny,
                        IsSeenAlpha: isOwnedAlpha,
                        IsCaught: isOwned,
                        IsOwned: isOwned,
                        IsOwnedShiny: isOwnedShiny,
                        Context: TmtSave.Context,
                        Generation: TmtSave.Generation,
                        RomHackTypes: entry.Types
                    ));
                }
            }

            var item = new DexItemDTO(
                Id: GetDexItemID(species),
                Species: species,
                SaveId: saveId,
                Forms: forms,
                Languages: [GetSaveLanguage()]
            );

            if (!dex.TryGetValue(species, out var bySave))
            {
                bySave = [];
                dex.Add(species, bySave);
            }

            bySave[saveId] = item;
        }

        return Task.FromResult(true);
    }

    protected override DexItemForm GetDexItemForm(
        ushort species,
        bool isOwned,
        bool isOwnedShiny,
        byte form,
        Gender gender)
    {
        var entry = TooManyTypesCompat.RequireSupported(species, form);
        var pi = Gen3DirectSpecies.GetPersonal(species, form);

        return new DexItemForm(
            Id: DexLoader.GetId(species, form, gender),
            Species: species,
            Form: form,
            Gender: gender,
            Types: GetTypes(TmtSave.Generation, pi),
            Abilities: GetAbilities(pi),
            AbilityHidden: GetAbilityHidden(pi),
            BaseStats: GetBaseStats(pi),
            IsSeen: isOwned,
            IsSeenShiny: isOwnedShiny,
            IsSeenAlpha: false,
            IsCaught: isOwned,
            IsOwned: isOwned,
            IsOwnedShiny: isOwnedShiny,
            Context: TmtSave.Context,
            Generation: TmtSave.Generation,
            RomHackTypes: entry.Types
        );
    }

    protected override IEnumerable<LanguageID> GetDexLanguages(ushort species) => [];

    public override Task EnableSpeciesForm(EnableSpeciesFormPayload payload)
    {
        // TMT's custom dex bit layout is not mapped yet. Refuse to write
        // vanilla Emerald dex bits into a ROM-hack save.
        return Task.CompletedTask;
    }

    private static IEnumerable<Gender> GetGenders(PersonalInfo pi)
    {
        if (pi.OnlyMale)
            return [Gender.Male];
        if (pi.OnlyFemale)
            return [Gender.Female];
        if (pi.Genderless)
            return [Gender.Genderless];
        return [Gender.Male, Gender.Female];
    }
}

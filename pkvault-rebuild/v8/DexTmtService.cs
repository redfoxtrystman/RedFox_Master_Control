using PKHeX.Core;

namespace PKVault.Core;

/// <summary>
/// Pokédex adapter for Too Many Types v1.6 / direct-species Gen3 saves.
///
/// V8 alpha7 deliberately treats the TMT save as an ownership source only.
/// The normal PKVault/National Pokédex must never inherit ROM-hack type,
/// ability, stat, or generation presentation. Those TMT details belong on the
/// storage Pokemon cards, where the ROM-hack profile is explicit.
///
/// This service therefore maps every supported TMT species/form to an official
/// PKHeX personal entry for display, while preserving seen/caught/owned state
/// from the actual TMT save.
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
                var official = GetOfficialPresentation(entry.Species, entry.Form);
                var pi = official.PersonalInfo;

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
                        Types: GetTypes(official.Generation, pi),
                        Abilities: GetAbilities(pi),
                        AbilityHidden: GetAbilityHidden(pi),
                        BaseStats: GetBaseStats(pi),
                        IsSeen: isOwned,
                        IsSeenShiny: isOwnedShiny,
                        IsSeenAlpha: isOwnedAlpha,
                        IsCaught: isOwned,
                        IsOwned: isOwned,
                        IsOwnedShiny: isOwnedShiny,
                        Context: official.Context,
                        Generation: official.Generation
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
        TooManyTypesCompat.RequireSupported(species, form);

        var official = GetOfficialPresentation(species, form);
        var pi = official.PersonalInfo;

        return new DexItemForm(
            Id: DexLoader.GetId(species, form, gender),
            Species: species,
            Form: form,
            Gender: gender,
            Types: GetTypes(official.Generation, pi),
            Abilities: GetAbilities(pi),
            AbilityHidden: GetAbilityHidden(pi),
            BaseStats: GetBaseStats(pi),
            IsSeen: isOwned,
            IsSeenShiny: isOwnedShiny,
            IsSeenAlpha: false,
            IsCaught: isOwned,
            IsOwned: isOwned,
            IsOwnedShiny: isOwnedShiny,
            Context: official.Context,
            Generation: official.Generation
        );
    }

    protected override IEnumerable<LanguageID> GetDexLanguages(ushort species) => [];

    public override Task EnableSpeciesForm(EnableSpeciesFormPayload payload)
    {
        // TMT's custom dex bit layout is not mapped yet. Refuse to write
        // vanilla Emerald dex bits into a ROM-hack save.
        return Task.CompletedTask;
    }

    private static PKM GetOfficialPresentation(ushort species, byte form)
    {
        var blank = EntityBlank.GetIdealBlank(species, form);
        blank.Species = species;
        blank.Form = form;
        return blank;
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

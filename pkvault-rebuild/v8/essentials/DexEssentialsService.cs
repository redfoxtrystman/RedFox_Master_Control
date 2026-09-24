using PKHeX.Core;

namespace PKVault.Core;

/// <summary>
/// Projects only official Pokémon from Essentials fan-game saves into PKVault's
/// ordinary National Dex. Profile-local Uranium/Insurgence species are excluded
/// and rendered by their own ROM-hack dex UI instead.
/// </summary>
public sealed class DexEssentialsService(EssentialsLegacySaveFile save) : DexGenService(save)
{
    public override async Task<bool> UpdateDexWithSave(
        Dictionary<ushort, Dictionary<uint, DexItemDTO>> dex,
        StaticSpeciesData staticSpecies,
        HashSet<ushort>? speciesSet)
    {
        var official = save.GetAllPKM()
            .OfType<PKEssentials>()
            .Where(p => p.OfficialNationalDexId > 0)
            .GroupBy(p => checked((ushort)p.OfficialNationalDexId));

        foreach (var group in official)
        {
            var species = group.Key;
            if (speciesSet != null && !speciesSet.Contains(species))
                continue;
            if (!staticSpecies.TryGetValue(species, out var speciesData) || speciesData.Forms.Count == 0)
                continue;

            var contextKey = speciesData.Forms.Keys.Max();
            var context = (EntityContext)contextKey;
            var presentationSave = BlankSaveFile.Get(context);
            var helper = new Dex123Service(presentationSave);
            var staticForms = speciesData.Forms[contextKey];

            var forms = new List<DexItemForm>();
            for (byte form = 0; form < staticForms.Length; form++)
            {
                foreach (var gender in speciesData.Genders)
                {
                    var owned = group.Where(p => p.Form == form && (Gender)p.Gender == gender).ToArray();
                    var isOwned = owned.Length > 0;
                    var isOwnedShiny = owned.Any(p => p.IsShiny);
                    var isOwnedAlpha = owned.Any(p => p.IsAlpha);

                    forms.Add(helper.GetDexItemFormComplete(
                        species,
                        isOwned,
                        isOwnedShiny,
                        isOwnedAlpha,
                        form,
                        gender,
                        staticSpecies
                    ));
                }
            }

            if (!dex.TryGetValue(species, out var bySave))
            {
                bySave = [];
                dex.Add(species, bySave);
            }

            bySave[new SaveWrapper(save).Id] = new DexItemDTO(
                Id: $"{species}_{new SaveWrapper(save).Id}",
                Species: species,
                SaveId: new SaveWrapper(save).Id,
                Forms: forms,
                Languages: [LanguageID.English]
            );
        }

        await Task.CompletedTask;
        return true;
    }

    protected override DexItemForm GetDexItemForm(ushort species, bool isOwned, bool isOwnedShiny, byte form, Gender gender)
        => throw new NotSupportedException();

    protected override IEnumerable<LanguageID> GetDexLanguages(ushort species) => [];

    public override Task EnableSpeciesForm(EnableSpeciesFormPayload payload)
        => Task.CompletedTask;
}

from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def replace_once(path: Path, old: str, new: str, marker: str):
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    if old not in text:
        raise RuntimeError(f"alpha53j anchor missing: {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

# ---------------------------------------------------------------------------
# Item bank: add a normal session-scoped deposit path for a held item.
# Unlike quest rewards, this must remain undoable until Save is pressed.
# ---------------------------------------------------------------------------
item_bank = root / "PKVault.Core/storage/services/ItemBankService.cs"
replace_once(
    item_bank,
    '''    public async Task<long> GetBankItemCount(string itemKey)
''',
    '''    public async Task<ItemBankMoveResult> DepositHeldItem(
        string itemKey,
        byte generation,
        GameVersion version,
        string owner,
        uint? saveId
    )
    {
        if (string.IsNullOrWhiteSpace(itemKey))
            throw new ArgumentException("Held item cannot be mapped to the PKVault Item Bank.", nameof(itemKey));

        var bank = await LoadBankState();
        var origin = new ItemOriginDTO(
            Generation: generation,
            Version: version,
            Owner: owner,
            SaveId: saveId,
            Count: 1
        );

        var existingKey = FindEquivalentStackKey(bank, itemKey);
        if (existingKey is not null)
        {
            var stack = bank[existingKey];
            bank[existingKey] = stack with
            {
                Count = checked(stack.Count + 1),
                Origins = MergeOrigins(stack.Origins, [origin]),
            };
        }
        else
        {
            var pageSizes = await LoadPageSizes();
            var pageCount = await GetPageCount(bank);
            var (page, slot) = FindRewardSlot(bank, pageCount, pageSizes);
            if (page > pageCount)
                await SavePageCount(page);

            bank[BankKey(page, slot)] = new BankStack(
                Id: NewStackId(),
                Page: page,
                Slot: slot,
                ItemKey: itemKey,
                Count: 1,
                SpriteVersion: version,
                Origins: [origin]
            );
        }

        await SaveBankState(bank);

        var others = await staticDataService.GetStaticOthers();
        return new(
            ItemName: GetItemName(others, itemKey),
            MovedCount: 1,
            SourceVersion: version,
            TargetVersion: null
        );
    }

    public async Task<long> GetBankItemCount(string itemKey)
''',
    "public async Task<ItemBankMoveResult> DepositHeldItem(",
)

# ---------------------------------------------------------------------------
# Data action: remove a held item from a save Pokémon or PKVault main variant.
# Uses MOVE_ITEM in action history, so existing UI/undo descriptions stay correct.
# ---------------------------------------------------------------------------
action = root / "PKVault.Core/storage/data-action/TakeHeldItemAction.cs"
action.write_text(r'''using PKHeX.Core;

namespace PKVault.Core;

public record TakeHeldItemActionInput(uint? SaveId, string PkmId);

public class TakeHeldItemAction(
    SynchronizePkmAction synchronizePkmAction,
    IPkmVariantLoader pkmVariantLoader,
    ISavesLoadersService savesLoadersService,
    ItemBankService itemBankService
) : DataAction<TakeHeldItemActionInput>
{
    protected override async Task<DataActionPayload> Execute(TakeHeldItemActionInput input, DataUpdateFlags flags)
    {
        var result = input.SaveId is null
            ? await ExecuteForMain(input.PkmId)
            : await ExecuteForSave(input.SaveId.Value, input.PkmId);

        flags.SaveInfos = true;

        return new(
            type: DataActionType.MOVE_ITEM,
            parameters: [
                result.ItemName,
                result.SourceVersion,
                result.TargetVersion,
                result.MovedCount,
            ]
        );
    }

    private async Task<ItemBankMoveResult> ExecuteForSave(uint saveId, string pkmId)
    {
        var saveLoaders = savesLoadersService.GetLoadersRequired(saveId);
        var dto = saveLoaders.Pkms.GetDto(pkmId)
            ?? throw new ArgumentException("Save Pokémon not found.");

        if (!dto.CanEdit)
            throw new InvalidOperationException("This Pokémon cannot be edited.");
        if (dto.HeldItem <= 0)
            throw new InvalidOperationException("This Pokémon is not holding an item.");

        var source = dto.Pkm;
        var itemKey = GetItemKey(source);
        var owner = BuildOwner(source);

        var updated = ClearHeldItem(source);
        saveLoaders.Pkms.WriteDto(dto with { Pkm = updated });

        var attached = await pkmVariantLoader.GetEntityBySave(dto.SaveId, dto.IdBase);
        if (attached is not null)
            await synchronizePkmAction.SynchronizeSaveToPkmVariant(new([(attached.Id, dto.IdBase)]));

        return await itemBankService.DepositHeldItem(
            itemKey,
            source.Generation,
            source.Version,
            owner,
            saveId
        );
    }

    private async Task<ItemBankMoveResult> ExecuteForMain(string pkmId)
    {
        var entity = await pkmVariantLoader.GetEntity(pkmId)
            ?? throw new KeyNotFoundException("PKVault Pokémon variant not found.");
        var dto = await pkmVariantLoader.CreateDTO(entity);

        if (!dto.CanEdit)
            throw new InvalidOperationException("This Pokémon cannot be edited.");

        var source = await pkmVariantLoader.GetPKM(entity);
        if (source.HeldItem <= 0)
            throw new InvalidOperationException("This Pokémon is not holding an item.");

        var itemKey = GetItemKey(source);
        var owner = BuildOwner(source);
        var convertedHeldItem = source.GetConvertedHeldItem();

        var related = await Task.WhenAll(
            (await pkmVariantLoader.GetEntitiesByBox(entity.BoxId, entity.BoxSlot)).Values
                .Where(value => value.Id != entity.Id)
                .Select(async value => (Entity: value, Pkm: await pkmVariantLoader.GetPKM(value)))
        );

        await pkmVariantLoader.UpdateEntity(entity, ClearHeldItem(source));

        foreach (var variant in related)
        {
            if (!RepresentsSameHeldItem(variant.Pkm, itemKey, convertedHeldItem))
                continue;

            await pkmVariantLoader.UpdateEntity(variant.Entity, ClearHeldItem(variant.Pkm));
        }

        var attachedEntity = entity.AttachedSaveId is not null
            ? entity
            : related.Select(entry => entry.Entity).FirstOrDefault(value => value.AttachedSaveId is not null);

        if (attachedEntity is not null)
            await synchronizePkmAction.SynchronizePkmVariantToSave(
                new([(attachedEntity.Id, attachedEntity.AttachedSavePkmIdBase!)])
            );

        return await itemBankService.DepositHeldItem(
            itemKey,
            source.Generation,
            source.Version,
            owner,
            null
        );
    }

    private static bool RepresentsSameHeldItem(ImmutablePKM pkm, string itemKey, int convertedHeldItem)
    {
        if (pkm.HeldItem <= 0)
            return false;

        if (convertedHeldItem > 0 && pkm.GetConvertedHeldItem() == convertedHeldItem)
            return true;

        return string.Equals(
            pkm.GetHeldItemPokeapiName(),
            itemKey,
            StringComparison.OrdinalIgnoreCase
        );
    }

    private static string GetItemKey(ImmutablePKM pkm)
    {
        var itemKey = pkm.GetHeldItemPokeapiName();
        if (string.IsNullOrWhiteSpace(itemKey))
            throw new InvalidOperationException(
                $"Held item #{pkm.HeldItem} cannot be mapped into the PKVault Item Bank."
            );

        return itemKey;
    }

    private static string BuildOwner(ImmutablePKM pkm)
    {
        var name = string.IsNullOrWhiteSpace(pkm.Nickname) ? $"species #{pkm.Species}" : pkm.Nickname;
        var trainer = string.IsNullOrWhiteSpace(pkm.OriginalTrainerName) ? "unknown OT" : $"OT {pkm.OriginalTrainerName}";
        return $"Held item from {name} ({trainer})";
    }

    private static ImmutablePKM ClearHeldItem(ImmutablePKM source) => source.Update(pkm =>
    {
        pkm.HeldItem = 0;
        pkm.ResetPartyStats();
        pkm.RefreshChecksum();
    });
}
''', encoding="utf-8")

# Action service entry point.
action_service = root / "PKVault.Core/storage/services/ActionService.cs"
replace_once(
    action_service,
    '''    public async Task<DataUpdateFlags> EvolvePkms(uint? saveId, string[] ids, string? itemKey = null)
''',
    '''    public async Task<DataUpdateFlags> TakeHeldItem(uint? saveId, string pkmId)
    {
        using var scope = sp.CreateScope();

        return await AddAction(
            scope,
            scope => scope.ServiceProvider.GetRequiredService<TakeHeldItemAction>(),
            new(saveId, pkmId)
        );
    }

    public async Task<DataUpdateFlags> EvolvePkms(uint? saveId, string[] ids, string? itemKey = null)
''',
    "public async Task<DataUpdateFlags> TakeHeldItem(",
)

# DI registration.
program = root / "PKVault.Core/Program.cs"
replace_once(
    program,
    '''        services.AddScoped<EvolvePkmAction>();
''',
    '''        services.AddScoped<TakeHeldItemAction>();
        services.AddScoped<EvolvePkmAction>();
''',
    "services.AddScoped<TakeHeldItemAction>();",
)

# API route. Keep this custom/manual so the generated SDK doesn't need to change.
route = root / "PKVault.Core/storage/routes/StorageRoute.cs"
replace_once(
    route,
    '''    [HttpGet("pkm/evolution-items")]
''',
    '''    [HttpPut("pkm/take-held-item")]
    public async Task<DataDTO> TakeHeldItem(string id, uint? saveId)
    {
        var flags = await actionService.TakeHeldItem(saveId, id);
        return await dataService.CreateDataFromUpdateFlags(flags);
    }

    [HttpGet("pkm/evolution-items")]
''',
    '[HttpPut("pkm/take-held-item")]',
)

# ---------------------------------------------------------------------------
# Frontend helper + button in normal Pokémon action bar.
# ---------------------------------------------------------------------------
held_api = root / "frontend/src/storage/details/held-item-api.ts"
held_api.write_text(r'''import { customInstance } from '../../data/mutator/custom-instance';

export const takeHeldItem = async (id: string, saveId: number | null) => {
    const params = new URLSearchParams({ id });
    if (saveId !== null)
        params.set('saveId', String(saveId));

    return customInstance<{ data: unknown; status: number; headers: Headers }>(
        '/api/storage/pkm/take-held-item?' + params.toString(),
        { method: 'PUT' },
    );
};
''', encoding="utf-8")

details = root / "frontend/src/storage/details/details-actions.tsx"
replace_once(
    details,
    "import { LinkIcon, MoveIcon, PencilIcon, SparklesIcon, TrashIcon, UnlinkIcon } from 'lucide-react';\n",
    "import { LinkIcon, MoveIcon, PackagePlusIcon, PencilIcon, SparklesIcon, TrashIcon, UnlinkIcon } from 'lucide-react';\n",
    "PackagePlusIcon",
)
replace_once(
    details,
    "import { useQuery, useQueryClient } from '@tanstack/react-query';\n",
    "import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';\n",
    "useMutation, useQuery",
)
replace_once(
    details,
    "import { evolveWithItem, loadItemEvolutionOptions, type ItemEvolutionOption } from './evolution-api';\n",
    "import { evolveWithItem, loadItemEvolutionOptions, type ItemEvolutionOption } from './evolution-api';\nimport { takeHeldItem } from './held-item-api';\n",
    "from './held-item-api'",
)
replace_once(
    details,
    "                    ...pick(pkm, [ 'id', 'boxId', 'boxSlot', 'canEdit', 'canEvolve', 'canDelete', 'isDuplicate' ]),\n",
    "                    ...pick(pkm, [ 'id', 'boxId', 'boxSlot', 'canEdit', 'canEvolve', 'canDelete', 'isDuplicate', 'heldItem' ]),\n",
    "'heldItem' ]",
)
replace_once(
    details,
    '''    const queryClient = useQueryClient();
    const singlePkmId = pkms.length === 1 ? pkms[ 0 ]?.id : undefined;
''',
    '''    const queryClient = useQueryClient();
    const singlePkmId = pkms.length === 1 ? pkms[ 0 ]?.id : undefined;
    const takeHeldItemMutation = useMutation({
        mutationFn: async () => {
            if (!singlePkmId)
                throw new Error('Select exactly one Pokémon.');

            return takeHeldItem(singlePkmId, saveId);
        },
        onSuccess: async () => {
            // DataDTO updates the active Pokémon cache via the global mutation handler.
            // The Item Bank has a separate custom query, so invalidate active queries too.
            await queryClient.invalidateQueries();
        },
    });
''',
    "const takeHeldItemMutation = useMutation({",
)
replace_once(
    details,
    '''        {canEvolveList.length > 0 && <UIConfirmPopover
''',
    '''        {pkms.length === 1 && (pkms[ 0 ]?.heldItem ?? 0) > 0 && <Tooltip
            multiline
            w={300}
            label='Remove the held item from this Pokémon and put it into the PKVault Item Bank. This stays undoable until you Save.'
        >
            <UIButton
                name='take-held-item'
                controlLabel='Take held item'
                onClick={() => takeHeldItemMutation.mutate()}
                size='compact-md'
                leftSection={<PackagePlusIcon />}
                disabled={!pkms[ 0 ]?.canEdit || takeHeldItemMutation.isPending}
            >
                Take Item
            </UIButton>
        </Tooltip>}

        {canEvolveList.length > 0 && <UIConfirmPopover
''',
    "name='take-held-item'",
)

print("PASS alpha53j Take Held Item action + Item Bank deposit + GUI button")

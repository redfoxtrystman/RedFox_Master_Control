from pathlib import Path

def put25(rel, text):
    path = PKVAULT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

# ===========================================================================
# V8 alpha25: storage-style item inventory.
# ===========================================================================
put25("PKVault.Core/storage/services/ItemBankService.cs", r'''using PKHeX.Core;

namespace PKVault.Core;

public record InventorySlotDTO(
    int Slot,
    string? ItemKey,
    string? Name,
    int? ItemId,
    long Count,
    long MaxCount,
    GameVersion SpriteVersion,
    bool Movable
);

public record InventoryBankPageDTO(
    int Page,
    int SlotCount,
    List<InventorySlotDTO> Slots
);

public record SaveInventoryPocketDTO(
    string Pouch,
    string Label,
    int SlotCount,
    bool Protected,
    List<InventorySlotDTO> Slots
);

public record SaveInventoryDTO(
    uint SaveId,
    GameVersion Version,
    string TrainerName,
    bool Supported,
    List<SaveInventoryPocketDTO> Pockets
);

public record ItemInventoryStateDTO(
    List<InventoryBankPageDTO> BankPages,
    List<SaveInventoryDTO> Saves
);

public record MoveInventoryItemActionInput(
    string SourceKind,
    string SourceId,
    string? SourcePouch,
    int SourceSlot,
    string TargetKind,
    string TargetId,
    string? TargetPouch,
    int TargetSlot,
    int Count
);

public record ItemBankMoveResult(
    string ItemName,
    int MovedCount,
    GameVersion? SourceVersion,
    GameVersion? TargetVersion
);

internal record BankStack(
    int Page,
    int Slot,
    string ItemKey,
    long Count,
    GameVersion SpriteVersion
);

public class ItemBankService(
    ISavesLoadersService savesLoadersService,
    IMetaLoader metaLoader,
    StaticDataService staticDataService,
    IFileIOService fileIOService
)
{
    public const int BankPageSlots = 30;
    private static string InventoryRoot => Path.Combine(Directory.GetCurrentDirectory(), "inventory");

    private static bool IsProtectedPouch(InventoryType type) => type switch
    {
        InventoryType.KeyItems => true,
        InventoryType.TMHMs => true,
        InventoryType.ZCrystals => true,
        _ => false,
    };

    private static bool IsMovablePouch(InventoryType type)
        => type != InventoryType.None && !IsProtectedPouch(type);

    public async Task<ItemInventoryStateDTO> GetState()
    {
        var bank = await LoadBankState();
        var others = await staticDataService.GetStaticOthers();

        var maxStoredPage = bank.Count == 0 ? 1 : Math.Max(1, bank.Values.Max(x => x.Page));
        var lastHasItems = bank.Values.Any(x => x.Page == maxStoredPage);
        var pageCount = lastHasItems ? maxStoredPage + 1 : maxStoredPage;

        var bankPages = Enumerable.Range(1, pageCount)
            .Select(page => new InventoryBankPageDTO(
                Page: page,
                SlotCount: BankPageSlots,
                Slots: Enumerable.Range(0, BankPageSlots)
                    .Select(slot => ToBankSlotDto(bank.GetValueOrDefault(BankKey(page, slot)), others, slot))
                    .ToList()
            ))
            .ToList();

        var saves = new List<SaveInventoryDTO>();
        foreach (var loaders in savesLoadersService.GetAllLoaders().OrderBy(x => x.Save.Version))
        {
            var save = loaders.Save;
            var bag = save.GetSave().Inventory;
            var map = GetVersionMap(others, save.Version);
            var pockets = new List<SaveInventoryPocketDTO>();

            foreach (var pouch in bag.Pouches.Where(x => x.Type != InventoryType.None))
            {
                var protectedPocket = IsProtectedPouch(pouch.Type);
                var slots = new List<InventorySlotDTO>(pouch.Items.Length);

                for (var slot = 0; slot < pouch.Items.Length; slot++)
                {
                    var item = pouch.Items[slot];
                    if (item.Index <= 0 || item.Count <= 0)
                    {
                        slots.Add(new(
                            Slot: slot,
                            ItemKey: null,
                            Name: null,
                            ItemId: null,
                            Count: 0,
                            MaxCount: pouch.MaxCount,
                            SpriteVersion: save.Version,
                            Movable: !protectedPocket
                        ));
                        continue;
                    }

                    map.TryGetValue(item.Index, out var itemKey);
                    var mapped = !string.IsNullOrWhiteSpace(itemKey);

                    slots.Add(new(
                        Slot: slot,
                        ItemKey: mapped ? itemKey : null,
                        Name: mapped ? GetItemName(others, itemKey!) : $"Item #{item.Index}",
                        ItemId: item.Index,
                        Count: item.Count,
                        MaxCount: bag.GetMaxCount(pouch.Type, item.Index),
                        SpriteVersion: save.Version,
                        Movable: !protectedPocket && mapped
                    ));
                }

                pockets.Add(new(
                    Pouch: pouch.Type.ToString(),
                    Label: GetPouchLabel(pouch.Type),
                    SlotCount: pouch.Items.Length,
                    Protected: protectedPocket,
                    Slots: slots
                ));
            }

            saves.Add(new(
                SaveId: save.Id,
                Version: save.Version,
                TrainerName: save.OT,
                Supported: bag.Pouches.Count > 0,
                Pockets: pockets
            ));
        }

        return new(bankPages, saves);
    }

    public async Task<ItemBankMoveResult> Move(MoveInventoryItemActionInput input)
    {
        if (input.Count <= 0)
            throw new ArgumentException("Item transfer count must be greater than zero.");

        var others = await staticDataService.GetStaticOthers();
        var bank = await LoadBankState();
        var source = ResolveSource(input, bank, others);

        if (input.SourceKind == input.TargetKind
            && input.SourceId == input.TargetId
            && input.SourcePouch == input.TargetPouch
            && input.SourceSlot == input.TargetSlot)
        {
            return new(source.ItemName, 0, source.Version, source.Version);
        }

        if (IsBank(input.SourceKind) && IsBank(input.TargetKind))
        {
            var targetKey = BankKey(ParseBankPage(input.TargetId), input.TargetSlot);
            var targetStack = bank.GetValueOrDefault(targetKey);
            if (targetStack is not null
                && targetStack.ItemKey != source.ItemKey
                && input.Count >= source.Available)
            {
                var sourceKey = BankKey(ParseBankPage(input.SourceId), input.SourceSlot);
                var sourceStack = bank[sourceKey];

                bank[targetKey] = sourceStack with
                {
                    Page = ParseBankPage(input.TargetId),
                    Slot = input.TargetSlot
                };
                bank[sourceKey] = targetStack with
                {
                    Page = ParseBankPage(input.SourceId),
                    Slot = input.SourceSlot
                };

                await SaveBankState(bank);
                return new(source.ItemName, checked((int)Math.Min(source.Available, int.MaxValue)), null, null);
            }
        }

        var requested = checked((int)Math.Min(source.Available, input.Count));
        var target = ApplyTarget(input, source, requested, bank, others);

        if (target.Moved <= 0)
            throw new InvalidOperationException("The target stack has no room; nothing was moved.");

        source.Deduct(target.Moved);

        if (source.UsesBank || target.UsesBank)
            await SaveBankState(bank);

        return new(
            ItemName: source.ItemName,
            MovedCount: target.Moved,
            SourceVersion: source.Version,
            TargetVersion: target.Version
        );
    }

    public async Task WriteToFiles()
    {
        var bank = await LoadBankState();

        fileIOService.Delete(InventoryRoot);
        fileIOService.CreateDirectory(Path.Combine(InventoryRoot, "1"));

        foreach (var stack in bank.Values.OrderBy(x => x.Page).ThenBy(x => x.Slot))
        {
            var pageDir = Path.Combine(InventoryRoot, stack.Page.ToString());
            fileIOService.CreateDirectory(pageDir);

            var path = Path.Combine(pageDir, $"{stack.Slot:00}.item");
            var bytes = System.Text.Encoding.UTF8.GetBytes(
                $"{stack.ItemKey}\t{stack.Count}\t{(int)stack.SpriteVersion}\n"
            );
            await fileIOService.WriteBytes(path, bytes);
        }
    }

    private sealed record SourceStack(
        string ItemKey,
        string ItemName,
        long Available,
        GameVersion SpriteVersion,
        GameVersion? Version,
        bool UsesBank,
        Action<int> Deduct
    );

    private sealed record TargetResult(
        int Moved,
        GameVersion? Version,
        bool UsesBank
    );

    private SourceStack ResolveSource(
        MoveInventoryItemActionInput input,
        Dictionary<string, BankStack> bank,
        StaticOthersData others
    )
    {
        if (IsBank(input.SourceKind))
        {
            var page = ParseBankPage(input.SourceId);
            ValidateBankSlot(input.SourceSlot);
            var key = BankKey(page, input.SourceSlot);
            var stack = bank.GetValueOrDefault(key)
                ?? throw new InvalidOperationException("The source PKVault inventory slot is empty.");

            return new(
                stack.ItemKey,
                GetItemName(others, stack.ItemKey),
                stack.Count,
                stack.SpriteVersion,
                null,
                true,
                moved =>
                {
                    var left = stack.Count - moved;
                    if (left <= 0)
                        bank.Remove(key);
                    else
                        bank[key] = stack with { Count = left };
                }
            );
        }

        if (!IsSave(input.SourceKind))
            throw new ArgumentException($"Unknown inventory source kind: {input.SourceKind}");

        var saveId = ParseSaveId(input.SourceId);
        var loaders = savesLoadersService.GetLoaders(saveId)
            ?? throw new KeyNotFoundException($"Save {saveId} not found.");
        var save = loaders.Save;
        var bag = save.GetSave().Inventory;
        var pouch = GetPouch(bag, input.SourcePouch);

        if (!IsMovablePouch(pouch.Type))
            throw new InvalidOperationException($"{GetPouchLabel(pouch.Type)} is protected and cannot be moved.");

        if ((uint)input.SourceSlot >= pouch.Items.Length)
            throw new ArgumentOutOfRangeException(nameof(input.SourceSlot));

        var item = pouch.Items[input.SourceSlot];
        if (item.Index <= 0 || item.Count <= 0)
            throw new InvalidOperationException("The source save inventory slot is empty.");

        var map = GetVersionMap(others, save.Version);
        if (!map.TryGetValue(item.Index, out var itemKey) || string.IsNullOrWhiteSpace(itemKey))
            throw new InvalidOperationException($"Item {item.Index} in {save.Version} has no safe cross-generation mapping.");

        return new(
            itemKey,
            GetItemName(others, itemKey),
            item.Count,
            save.Version,
            save.Version,
            false,
            moved =>
            {
                item.Count -= moved;
                if (item.Count <= 0)
                    item.Clear();

                pouch.ClearCount0();
                bag.CopyTo(save.GetSave());
                loaders.Pkms.HasWritten = true;
            }
        );
    }

    private TargetResult ApplyTarget(
        MoveInventoryItemActionInput input,
        SourceStack source,
        int requested,
        Dictionary<string, BankStack> bank,
        StaticOthersData others
    )
    {
        if (IsBank(input.TargetKind))
        {
            var page = ParseBankPage(input.TargetId);
            ValidateBankSlot(input.TargetSlot);
            var key = BankKey(page, input.TargetSlot);
            var target = bank.GetValueOrDefault(key);

            if (target is not null && target.ItemKey != source.ItemKey)
                throw new InvalidOperationException("Target PKVault inventory slot contains a different item.");

            if (target is null)
            {
                bank[key] = new(
                    Page: page,
                    Slot: input.TargetSlot,
                    ItemKey: source.ItemKey,
                    Count: requested,
                    SpriteVersion: source.SpriteVersion
                );
            }
            else
            {
                bank[key] = target with { Count = checked(target.Count + requested) };
            }

            return new(requested, null, true);
        }

        if (!IsSave(input.TargetKind))
            throw new ArgumentException($"Unknown inventory target kind: {input.TargetKind}");

        var saveId = ParseSaveId(input.TargetId);
        var loaders = savesLoadersService.GetLoaders(saveId)
            ?? throw new KeyNotFoundException($"Save {saveId} not found.");
        var save = loaders.Save;
        var bag = save.GetSave().Inventory;
        var pouch = GetPouch(bag, input.TargetPouch);

        if (!IsMovablePouch(pouch.Type))
            throw new InvalidOperationException($"{GetPouchLabel(pouch.Type)} is protected and cannot receive transferred items.");

        if ((uint)input.TargetSlot >= pouch.Items.Length)
            throw new ArgumentOutOfRangeException(nameof(input.TargetSlot));

        if (IsSave(input.SourceKind)
            && input.SourceId == input.TargetId
            && requested < source.Available
            && pouch.Items[input.TargetSlot].Index == 0)
        {
            throw new InvalidOperationException(
                "Game-save bags keep one stack per item. Split this stack in a PKVault inventory page instead."
            );
        }

        var map = GetVersionMap(others, save.Version);
        var targetPair = map.FirstOrDefault(kv => string.Equals(kv.Value, source.ItemKey, StringComparison.Ordinal));
        if (targetPair.Key <= 0)
            throw new InvalidOperationException($"{source.ItemName} does not exist in {save.Version}.");

        var targetItemId = (ushort)targetPair.Key;
        if (!pouch.CanContain(targetItemId))
            throw new InvalidOperationException($"{source.ItemName} does not belong in the {GetPouchLabel(pouch.Type)} pocket.");

        var target = pouch.Items[input.TargetSlot];
        if (target.Index != 0 && target.Index != targetItemId)
            throw new InvalidOperationException("Target save slot contains a different item.");

        var max = bag.GetMaxCount(pouch.Type, targetItemId);
        var before = target.Index == targetItemId ? target.Count : 0;
        var capacity = Math.Max(0, max - before);
        var moved = Math.Min(requested, capacity);

        if (moved <= 0)
            return new(0, save.Version, false);

        if (target.Index == 0)
        {
            target.Index = targetItemId;
            target.SetNewDetails(0);
            target.Count = moved;
        }
        else
        {
            target.Count = before + moved;
        }

        bag.CopyTo(save.GetSave());
        loaders.Pkms.HasWritten = true;

        return new(moved, save.Version, false);
    }

    private async Task<Dictionary<string, BankStack>> LoadBankState()
    {
        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK);
        if (entity is not null)
            return ParseMeta(entity.Value);

        var fromFiles = ReadBankFiles();
        await SaveBankState(fromFiles);
        return fromFiles;
    }

    private Dictionary<string, BankStack> ReadBankFiles()
    {
        var result = new Dictionary<string, BankStack>(StringComparer.Ordinal);
        if (!Directory.Exists(InventoryRoot))
            return result;

        foreach (var dir in Directory.EnumerateDirectories(InventoryRoot))
        {
            if (!int.TryParse(Path.GetFileName(dir), out var page) || page <= 0)
                continue;

            foreach (var file in Directory.EnumerateFiles(dir, "*.item"))
            {
                if (!int.TryParse(Path.GetFileNameWithoutExtension(file), out var slot))
                    continue;
                if ((uint)slot >= BankPageSlots)
                    continue;

                var parts = File.ReadAllText(file).Trim().Split('\t');
                if (parts.Length < 2 || !long.TryParse(parts[1], out var count) || count <= 0)
                    continue;

                var spriteVersion = GameVersion.RD;
                if (parts.Length >= 3 && int.TryParse(parts[2], out var rawVersion))
                    spriteVersion = (GameVersion)rawVersion;

                var stack = new BankStack(page, slot, parts[0], count, spriteVersion);
                result[BankKey(page, slot)] = stack;
            }
        }

        return result;
    }

    private static Dictionary<string, BankStack> ParseMeta(string? value)
    {
        var result = new Dictionary<string, BankStack>(StringComparer.Ordinal);
        if (string.IsNullOrWhiteSpace(value))
            return result;

        var legacySlot = 0;

        foreach (var line in value.Split('\n', StringSplitOptions.RemoveEmptyEntries))
        {
            var parts = line.Split('\t');

            if (parts.Length >= 5
                && int.TryParse(parts[0], out var page)
                && int.TryParse(parts[1], out var slot)
                && long.TryParse(parts[3], out var count)
                && int.TryParse(parts[4], out var version)
                && page > 0
                && (uint)slot < BankPageSlots
                && count > 0)
            {
                var stack = new BankStack(page, slot, parts[2], count, (GameVersion)version);
                result[BankKey(page, slot)] = stack;
                continue;
            }

            if (parts.Length == 2
                && long.TryParse(parts[1], out var legacyCount)
                && legacyCount > 0)
            {
                var page = legacySlot / BankPageSlots + 1;
                var slot = legacySlot % BankPageSlots;
                var stack = new BankStack(page, slot, parts[0], legacyCount, GameVersion.RD);
                result[BankKey(page, slot)] = stack;
                legacySlot++;
            }
        }

        return result;
    }

    private async Task SaveBankState(Dictionary<string, BankStack> bank)
    {
        var value = string.Join('\n', bank.Values
            .Where(x => x.Count > 0)
            .OrderBy(x => x.Page)
            .ThenBy(x => x.Slot)
            .Select(x => $"{x.Page}\t{x.Slot}\t{x.ItemKey}\t{x.Count}\t{(int)x.SpriteVersion}"));

        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK);
        if (entity is null)
        {
            await metaLoader.AddEntity(new()
            {
                Key = MetaKey.ITEM_BANK,
                Value = value
            });
        }
        else
        {
            entity.Value = value;
            await metaLoader.UpdateEntity(entity);
        }
    }

    private static InventorySlotDTO ToBankSlotDto(
        BankStack? stack,
        StaticOthersData others,
        int slot
    )
    {
        if (stack is null)
        {
            return new(
                Slot: slot,
                ItemKey: null,
                Name: null,
                ItemId: null,
                Count: 0,
                MaxCount: long.MaxValue,
                SpriteVersion: GameVersion.RD,
                Movable: true
            );
        }

        return new(
            Slot: slot,
            ItemKey: stack.ItemKey,
            Name: GetItemName(others, stack.ItemKey),
            ItemId: null,
            Count: stack.Count,
            MaxCount: long.MaxValue,
            SpriteVersion: stack.SpriteVersion,
            Movable: true
        );
    }

    private static string BankKey(int page, int slot) => $"{page}:{slot}";

    private static int ParseBankPage(string id)
    {
        if (!int.TryParse(id, out var page) || page <= 0)
            throw new ArgumentException($"Invalid PKVault inventory page: {id}");
        return page;
    }

    private static uint ParseSaveId(string id)
    {
        if (!uint.TryParse(id, out var saveId))
            throw new ArgumentException($"Invalid save id: {id}");
        return saveId;
    }

    private static void ValidateBankSlot(int slot)
    {
        if ((uint)slot >= BankPageSlots)
            throw new ArgumentOutOfRangeException(nameof(slot));
    }

    private static InventoryPouch GetPouch(PlayerBag bag, string? pouchName)
    {
        if (!Enum.TryParse<InventoryType>(pouchName, out var pouchType))
            throw new ArgumentException($"Invalid inventory pocket: {pouchName}");

        return bag.Pouches.FirstOrDefault(x => x.Type == pouchType)
            ?? throw new InvalidOperationException($"Save does not contain the {GetPouchLabel(pouchType)} pocket.");
    }

    private static bool IsBank(string kind) => string.Equals(kind, "bank", StringComparison.OrdinalIgnoreCase);
    private static bool IsSave(string kind) => string.Equals(kind, "save", StringComparison.OrdinalIgnoreCase);

    private static Dictionary<int, string> GetVersionMap(StaticOthersData others, GameVersion version)
    {
        return others.Items.VersionItems
            .FirstOrDefault(x => x.Versions.Contains((byte)version))
            ?.ComboItems
            ?? [];
    }

    private static string GetItemName(StaticOthersData others, string itemKey)
    {
        return others.Items.Items.TryGetValue(itemKey, out var item)
            ? item.Name
            : itemKey.Replace('-', ' ');
    }

    private static string GetPouchLabel(InventoryType type)
    {
        return type switch
        {
            InventoryType.TMHMs => "TMs / HMs",
            InventoryType.PCItems => "PC Items",
            InventoryType.KeyItems => "Key Items",
            InventoryType.BattleItems => "Battle Items",
            InventoryType.FreeSpace => "Free Space",
            _ => type.ToString(),
        };
    }
}
''')

put25("PKVault.Core/storage/data-action/MoveInventoryItemAction.cs", r'''namespace PKVault.Core;

public class MoveInventoryItemAction(ItemBankService itemBankService) : DataAction<MoveInventoryItemActionInput>
{
    protected override async Task<DataActionPayload> Execute(MoveInventoryItemActionInput input, DataUpdateFlags flags)
    {
        var result = await itemBankService.Move(input);
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
}
''')

action_service25 = PKVAULT / "PKVault.Core/storage/services/ActionService.cs"
replace_once(action_service25,
'''    public async Task<DataUpdateFlags> MoveInventoryItem(
        uint? sourceSaveId, uint? targetSaveId,
        string itemKey, int? sourceItemId, InventoryType? sourcePouch, int count
    )
    {
        using var scope = sp.CreateScope();

        return await AddAction(
            scope,
            (scope) => scope.ServiceProvider.GetRequiredService<MoveInventoryItemAction>(),
            new(sourceSaveId, targetSaveId, itemKey, sourceItemId, sourcePouch, count)
        );
    }
''',
'''    public async Task<DataUpdateFlags> MoveInventoryItem(
        string sourceKind, string sourceId, string? sourcePouch, int sourceSlot,
        string targetKind, string targetId, string? targetPouch, int targetSlot,
        int count
    )
    {
        using var scope = sp.CreateScope();

        return await AddAction(
            scope,
            (scope) => scope.ServiceProvider.GetRequiredService<MoveInventoryItemAction>(),
            new(
                sourceKind, sourceId, sourcePouch, sourceSlot,
                targetKind, targetId, targetPouch, targetSlot,
                count
            )
        );
    }
''')

storage_route25 = PKVAULT / "PKVault.Core/storage/routes/StorageRoute.cs"
replace_once(storage_route25,
'''    [HttpPut("inventory/move")]
    public async Task<ItemInventoryStateDTO> MoveInventoryItem(
        uint? sourceSaveId,
        uint? targetSaveId,
        string itemKey,
        int? sourceItemId,
        InventoryType? sourcePouch,
        int count
    )
    {
        await actionService.MoveInventoryItem(
            sourceSaveId, targetSaveId,
            itemKey, sourceItemId, sourcePouch, count
        );

        return await itemBankService.GetState();
    }
''',
'''    [HttpPut("inventory/move")]
    public async Task<ItemInventoryStateDTO> MoveInventoryItem(
        string sourceKind,
        string sourceId,
        string? sourcePouch,
        int sourceSlot,
        string targetKind,
        string targetId,
        string? targetPouch,
        int targetSlot,
        int count
    )
    {
        await actionService.MoveInventoryItem(
            sourceKind, sourceId, sourcePouch, sourceSlot,
            targetKind, targetId, targetPouch, targetSlot,
            count
        );

        return await itemBankService.GetState();
    }
''')

session_service25 = PKVAULT / "PKVault.Core/db/services/SessionService.cs"
replace_once(session_service25,
'''        var pkmFileLoader = scope.ServiceProvider.GetRequiredService<IPkmFileLoader>();
        await pkmFileLoader.WriteToFiles();

        await savesLoadersService.WriteToFiles();
''',
'''        var itemBankService = scope.ServiceProvider.GetRequiredService<ItemBankService>();
        await itemBankService.WriteToFiles();

        var pkmFileLoader = scope.ServiceProvider.GetRequiredService<IPkmFileLoader>();
        await pkmFileLoader.WriteToFiles();

        await savesLoadersService.WriteToFiles();
''')

put25("frontend/src/inventory/types.ts", r'''import type { GameVersion } from '../data/sdk/model';

export type InventorySlot = {
    slot: number;
    itemKey?: string | null;
    name?: string | null;
    itemId?: number | null;
    count: number;
    maxCount: number;
    spriteVersion: GameVersion;
    movable: boolean;
};

export type InventoryBankPage = {
    page: number;
    slotCount: number;
    slots: InventorySlot[];
};

export type SaveInventoryPocket = {
    pouch: string;
    label: string;
    slotCount: number;
    protected: boolean;
    slots: InventorySlot[];
};

export type SaveInventory = {
    saveId: number;
    version: GameVersion;
    trainerName: string;
    supported: boolean;
    pockets: SaveInventoryPocket[];
};

export type InventoryState = {
    bankPages: InventoryBankPage[];
    saves: SaveInventory[];
};

export type InventoryLocation = {
    kind: 'bank' | 'save';
    id: string;
    pouch?: string;
    slot: number;
};

export type InventoryDragPayload = {
    location: InventoryLocation;
    count: number;
    itemKey: string;
};
''')

put25("frontend/src/inventory/inventory-api.ts", r'''import { customInstance } from '../data/mutator/custom-instance';
import type { InventoryLocation, InventoryState } from './types';

export const loadInventory = async () =>
    (await customInstance<{ data: InventoryState; status: number; headers: Headers }>(
        '/api/storage/inventory'
    )).data;

export const moveInventory = async (
    source: InventoryLocation,
    target: InventoryLocation,
    count: number,
) => {
    const p = new URLSearchParams({
        sourceKind: source.kind,
        sourceId: source.id,
        sourceSlot: String(source.slot),
        targetKind: target.kind,
        targetId: target.id,
        targetSlot: String(target.slot),
        count: String(count),
    });

    if (source.pouch)
        p.set('sourcePouch', source.pouch);
    if (target.pouch)
        p.set('targetPouch', target.pouch);

    return (await customInstance<{ data: InventoryState; status: number; headers: Headers }>(
        '/api/storage/inventory/move?' + p.toString(),
        { method: 'PUT' }
    )).data;
};
''')

put25("frontend/src/inventory/inventory-item.tsx", r'''import { Badge, Button, Group, NumberInput, Popover, Stack, Text } from '@mantine/core';
import { LockIcon, SplitIcon } from 'lucide-react';
import React from 'react';
import { ItemImg } from '../img/item-img';
import { UIStorageItemBase } from '../ui/storage/storage-item/base/ui-storage-item-base';
import type { InventoryDragPayload, InventoryLocation, InventorySlot } from './types';

const dragMime = 'application/x-pkvault-inventory';

type InventoryItemProps = {
    slot: InventorySlot;
    location: InventoryLocation;
    isBank: boolean;
    nearestEmptySlot?: number;
    onMove: (source: InventoryLocation, target: InventoryLocation, count: number) => Promise<void>;
    onError: (message: string) => void;
};

export const InventoryItem: React.FC<InventoryItemProps> = ({
    slot, location, isBank, nearestEmptySlot, onMove, onError
}) => {
    const [ opened, setOpened ] = React.useState(false);
    const [ amount, setAmount ] = React.useState<number>(Math.max(1, Number(slot.count)));

    React.useEffect(() => {
        setAmount(Math.max(1, Number(slot.count)));
    }, [ slot.count ]);

    const hasItem = !!slot.itemKey && slot.count > 0;
    const canDrag = hasItem && slot.movable;
    const transferAmount = Math.max(1, Math.min(Number(slot.count), amount || Number(slot.count)));

    const split = async () => {
        if (!isBank || nearestEmptySlot === undefined || !hasItem)
            return;
        if (transferAmount >= slot.count) {
            onError('Split amount must be smaller than the current stack.');
            return;
        }

        await onMove(
            location,
            { ...location, slot: nearestEmptySlot },
            transferAmount
        );
        setOpened(false);
    };

    const onDragStart = (e: React.DragEvent) => {
        if (!canDrag || !slot.itemKey) {
            e.preventDefault();
            return;
        }

        const payload: InventoryDragPayload = {
            location,
            count: transferAmount,
            itemKey: slot.itemKey,
        };
        e.dataTransfer.setData(dragMime, JSON.stringify(payload));
        e.dataTransfer.effectAllowed = 'move';
    };

    const onDrop = async (e: React.DragEvent) => {
        e.preventDefault();
        const raw = e.dataTransfer.getData(dragMime);
        if (!raw)
            return;

        try {
            const payload = JSON.parse(raw) as InventoryDragPayload;
            await onMove(payload.location, location, payload.count);
        } catch (error) {
            onError(error instanceof Error ? error.message : String(error));
        }
    };

    const card = <UIStorageItemBase
        label={hasItem
            ? <Group gap='xs'>
                <Text>{slot.name}</Text>
                <Badge variant='light'>×{slot.count}</Badge>
            </Group>
            : undefined}
        draggable={canDrag}
        onDragStart={onDragStart}
        onDragOver={e => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        }}
        onDrop={onDrop}
        onClick={() => hasItem && setOpened(true)}
        pos='relative'
        mih={84}
        p='xs'
        style={{
            cursor: canDrag ? 'grab' : hasItem ? 'pointer' : 'default',
        }}
    >
        {hasItem && <ItemImg
            item={slot.itemKey!}
            version={slot.spriteVersion}
            style={{ width: 48, height: 48 }}
        />}

        {hasItem && <Badge
            size='sm'
            variant='filled'
            pos='absolute'
            right={4}
            bottom={4}
        >
            {slot.count}
        </Badge>}

        {hasItem && !slot.movable && <LockIcon
            size={15}
            style={{ position: 'absolute', left: 5, bottom: 5 }}
        />}
    </UIStorageItemBase>;

    if (!hasItem)
        return card;

    return <Popover
        opened={opened}
        onChange={setOpened}
        position='bottom'
        withArrow
        shadow='md'
    >
        <Popover.Target>
            {card}
        </Popover.Target>

        <Popover.Dropdown>
            <Stack gap='xs' w={220}>
                <Text fw={600}>{slot.name}</Text>
                <Text size='xs' c='dimmed'>
                    Choose how many this stack will move when you drag it.
                </Text>

                <NumberInput
                    min={1}
                    max={Number(slot.count)}
                    value={transferAmount}
                    onChange={v => setAmount(Number(v) || 1)}
                />

                {isBank && <Button
                    size='xs'
                    variant='light'
                    leftSection={<SplitIcon size={14} />}
                    disabled={nearestEmptySlot === undefined || slot.count <= 1}
                    onClick={() => void split()}
                >
                    Split to nearest empty slot
                </Button>}

                {!isBank && <Text size='xs' c='dimmed'>
                    Game bags keep one stack per item. Drag a partial amount to another game or into PKVault to split it safely.
                </Text>}
            </Stack>
        </Popover.Dropdown>
    </Popover>;
};
''')

put25("frontend/src/inventory/inventory-panel.tsx", r'''import { Alert, Group, Tabs, Text } from '@mantine/core';
import React from 'react';
import { getGameInfos } from '../pokedex/details/util/get-game-infos';
import { useStaticData } from '../hooks/use-static-data';
import { UIStoragePanel } from '../ui/storage/storage-panel/ui-storage-panel';
import { UIStoragePanelGameList, type UIGameData } from '../ui/storage/storage-panel/game-list/ui-storage-panel-game-list';
import { getBoxColumns } from '../ui/storage/storage-panel/get-box-columns';
import { InventoryItem } from './inventory-item';
import type {
    InventoryBankPage,
    InventoryLocation,
    InventorySlot,
    InventoryState,
    SaveInventory,
    SaveInventoryPocket,
} from './types';

type ContainerSelection =
    | { kind: 'bank'; page: number }
    | { kind: 'save'; saveId: number; pouch?: string };

type InventoryPanelProps = {
    state: InventoryState;
    initial: ContainerSelection;
    onMove: (source: InventoryLocation, target: InventoryLocation, count: number) => Promise<void>;
    onError: (message: string) => void;
};

const pkvaultId = 'pkvault';

export const InventoryPanel: React.FC<InventoryPanelProps> = ({
    state, initial, onMove, onError
}) => {
    const staticData = useStaticData();
    const [ selection, setSelection ] = React.useState<ContainerSelection>(initial);

    React.useEffect(() => {
        if (selection.kind === 'save' && !state.saves.some(s => s.saveId === selection.saveId)) {
            setSelection({ kind: 'bank', page: 1 });
        }
    }, [ selection, state.saves ]);

    const selectedSave: SaveInventory | undefined = selection.kind === 'save'
        ? state.saves.find(s => s.saveId === selection.saveId)
        : undefined;

    const selectedBank: InventoryBankPage | undefined = selection.kind === 'bank'
        ? state.bankPages.find(p => p.page === selection.page) ?? state.bankPages[0]
        : undefined;

    const selectedPocket: SaveInventoryPocket | undefined = selectedSave
        ? selectedSave.pockets.find(p => p.pouch === selection.pouch) ?? selectedSave.pockets[0]
        : undefined;

    React.useEffect(() => {
        if (selection.kind === 'save' && selectedSave && !selection.pouch && selectedSave.pockets[0]) {
            setSelection({
                kind: 'save',
                saveId: selectedSave.saveId,
                pouch: selectedSave.pockets[0].pouch,
            });
        }
    }, [ selection, selectedSave ]);

    const gameValue = selection.kind === 'bank' ? pkvaultId : String(selection.saveId);
    const gameData: UIGameData[] = [
        {
            id: pkvaultId,
            imgSrc: '/logo.svg',
            label: 'PKVault',
        },
        ...state.saves.map(save => ({
            id: String(save.saveId),
            imgSrc: getGameInfos(save.version).img,
            label: staticData.versions[save.version]?.name ?? String(save.version),
            disabled: !save.supported,
        })),
    ];

    const selectGame = (id: string) => {
        if (id === pkvaultId) {
            setSelection({ kind: 'bank', page: selectedBank?.page ?? 1 });
            return;
        }

        const save = state.saves.find(s => String(s.saveId) === id);
        if (!save)
            return;

        setSelection({
            kind: 'save',
            saveId: save.saveId,
            pouch: save.pockets[0]?.pouch,
        });
    };

    let slots: InventorySlot[] = [];
    let header: React.ReactNode = null;

    if (selection.kind === 'bank') {
        const page = selectedBank ?? state.bankPages[0];
        slots = page?.slots ?? [];
        header = <Tabs
            value={String(page?.page ?? 1)}
            onChange={value => value && setSelection({ kind: 'bank', page: Number(value) })}
            variant='pills'
        >
            <Tabs.List>
                {state.bankPages.map(p => <Tabs.Tab key={p.page} value={String(p.page)}>
                    {p.page}
                </Tabs.Tab>)}
            </Tabs.List>
        </Tabs>;
    } else {
        slots = selectedPocket?.slots ?? [];
        header = <Tabs
            value={selectedPocket?.pouch ?? null}
            onChange={value => value && setSelection({
                kind: 'save',
                saveId: selection.saveId,
                pouch: value,
            })}
            variant='pills'
        >
            <Tabs.List>
                {(selectedSave?.pockets ?? []).map(p => <Tabs.Tab
                    key={p.pouch}
                    value={p.pouch}
                >
                    {p.label}
                </Tabs.Tab>)}
            </Tabs.List>
        </Tabs>;
    }

    const nearestEmpty = (slot: number) => {
        const empty = slots
            .filter(s => !s.itemKey)
            .map(s => s.slot)
            .sort((a, b) => Math.abs(a - slot) - Math.abs(b - slot) || a - b);
        return empty[0];
    };

    const cols = getBoxColumns(slots.length) ?? 6;

    return <UIStoragePanel
        gameTabs={<UIStoragePanelGameList
            value={gameValue}
            data={gameData}
            onChange={selectGame}
            expanded={false}
            sortValue='inventory'
            sortData={[ { value: 'inventory', label: 'Inventory' } ]}
            onSortChange={() => undefined}
            createActions={null}
            renderHoverCard={({ item }) => <Text>{item.label}</Text>}
            renderExpanded={() => null}
        />}
        header={header}
        footer={selection.kind === 'save' && selectedPocket?.protected
            ? <Alert color='yellow' py='xs'>
                {selectedPocket.label} is visible but protected from cross-game moves.
            </Alert>
            : null}
    >
        <Group
            gap='sm'
            wrap='wrap'
            mx='auto'
            pos='relative'
            w='fit-content'
            style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(' + cols + ', 1fr)',
            }}
        >
            {slots.map(slot => {
                const location: InventoryLocation = selection.kind === 'bank'
                    ? {
                        kind: 'bank',
                        id: String(selectedBank?.page ?? 1),
                        slot: slot.slot,
                    }
                    : {
                        kind: 'save',
                        id: String(selection.saveId),
                        pouch: selectedPocket?.pouch,
                        slot: slot.slot,
                    };

                return <InventoryItem
                    key={slot.slot}
                    slot={slot}
                    location={location}
                    isBank={selection.kind === 'bank'}
                    nearestEmptySlot={selection.kind === 'bank' ? nearestEmpty(slot.slot) : undefined}
                    onMove={onMove}
                    onError={onError}
                />;
            })}
        </Group>
    </UIStoragePanel>;
};
''')

put25("frontend/src/inventory/inventory-page.tsx", r'''import { Alert, Box } from '@mantine/core';
import { useQueryClient } from '@tanstack/react-query';
import { ArrowLeftRightIcon } from 'lucide-react';
import React from 'react';
import { withErrorCatcher } from '../error/with-error-catcher';
import { UIStorageContent } from '../ui/storage/storage-content/ui-storage-content';
import { UIStorageContentMiddle } from '../ui/storage/storage-content/middle/ui-storage-content-middle';
import { loadInventory, moveInventory } from './inventory-api';
import { InventoryPanel } from './inventory-panel';
import type { InventoryLocation, InventoryState } from './types';

export const InventoryPage: React.FC = withErrorCatcher('default', () => {
    const queryClient = useQueryClient();
    const [ state, setState ] = React.useState<InventoryState>();
    const [ error, setError ] = React.useState<string>();

    const reload = React.useCallback(async () => {
        try {
            setState(await loadInventory());
            setError(undefined);
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
        }
    }, []);

    React.useEffect(() => {
        void reload();
    }, [ reload ]);

    const onMove = React.useCallback(async (
        source: InventoryLocation,
        target: InventoryLocation,
        count: number,
    ) => {
        try {
            setState(await moveInventory(source, target, count));
            setError(undefined);
            await queryClient.invalidateQueries();
        } catch (e) {
            const message = e instanceof Error ? e.message : String(e);
            setError(message);
            throw e;
        }
    }, [ queryClient ]);

    if (!state)
        return <Box p='md'>{error ? <Alert color='red'>{error}</Alert> : 'Loading inventory…'}</Box>;

    const firstSave = state.saves[0];

    return <Box h='100%' pos='relative'>
        {error && <Alert
            color='red'
            pos='absolute'
            top={8}
            left='50%'
            style={{ transform: 'translateX(-50%)', zIndex: 20 }}
            withCloseButton
            onClose={() => setError(undefined)}
        >
            {error}
        </Alert>}

        <UIStorageContent
            id='inventory-move-container'
            left={<InventoryPanel
                state={state}
                initial={{ kind: 'bank', page: 1 }}
                onMove={onMove}
                onError={setError}
            />}
            right={<InventoryPanel
                state={state}
                initial={firstSave
                    ? { kind: 'save', saveId: firstSave.saveId, pouch: firstSave.pockets[0]?.pouch }
                    : { kind: 'bank', page: 1 }}
                onMove={onMove}
                onError={setError}
            />}
            middle={<UIStorageContentMiddle>
                <ArrowLeftRightIcon />
            </UIStorageContentMiddle>}
        />
    </Box>;
});
''')

put25("frontend/src/pages/inventory.tsx", r'''export { InventoryPage } from '../inventory/inventory-page';
''')

print("PKVault V8 alpha25 storage-style inventory UI + slot bank applied")

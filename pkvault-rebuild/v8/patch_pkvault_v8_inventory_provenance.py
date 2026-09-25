from pathlib import Path

def put29(rel, text):
    path = PKVAULT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

# ===========================================================================
# V8 alpha29: persistent item-stack identity + provenance.
#
# IMPORTANT MODEL:
#   Inventory Box 1/2/3 = UI layout metadata only.
#   inventory/1/, inventory/2/, ... = ORIGIN GENERATION folders.
#   Physical stack files = <item-key>_<stable-random-id>.item
# ===========================================================================

# Save-side provenance ledger survives bank -> save -> bank round-trips.
meta_entity29 = PKVAULT / "PKVault.Core/db/entity/MetaEntity.cs"
replace_once(meta_entity29,
'''    ITEM_BANK,
    ITEM_BANK_PAGES,
}
''',
'''    ITEM_BANK,
    ITEM_BANK_PAGES,
    ITEM_SAVE_PROVENANCE,
}
''')

put29("PKVault.Core/storage/services/ItemBankService.cs", r'''using System.Text.Json;
using PKHeX.Core;

namespace PKVault.Core;

public record ItemOriginDTO(
    byte Generation,
    GameVersion Version,
    string Owner,
    uint? SaveId,
    long Count
);

public record InventorySlotDTO(
    int Slot,
    string? ItemKey,
    string? Name,
    int? ItemId,
    long Count,
    long MaxCount,
    GameVersion SpriteVersion,
    bool Movable,
    string? StackId,
    List<ItemOriginDTO> Origins
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
    string Id,
    int Page,
    int Slot,
    string ItemKey,
    long Count,
    GameVersion SpriteVersion,
    List<ItemOriginDTO> Origins
);

internal record ItemBankFileDTO(
    string Id,
    string ItemKey,
    long Count,
    int Box,
    int Slot,
    GameVersion SpriteVersion,
    List<ItemOriginDTO> Origins
);

public class ItemBankService(
    ISavesLoadersService savesLoadersService,
    IMetaLoader metaLoader,
    StaticDataService staticDataService,
    IFileIOService fileIOService
)
{
    public const int BankPageSlots = 30;

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        WriteIndented = true,
        PropertyNameCaseInsensitive = true,
    };

    private static string InventoryRoot
        => Path.Combine(Directory.GetCurrentDirectory(), "inventory");

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
        var saveProvenance = await LoadSaveProvenance();
        var others = await staticDataService.GetStaticOthers();

        var pageCount = await GetPageCount(bank);

        var bankPages = Enumerable.Range(1, pageCount)
            .Select(page => new InventoryBankPageDTO(
                Page: page,
                SlotCount: BankPageSlots,
                Slots: Enumerable.Range(0, BankPageSlots)
                    .Select(slot => ToBankSlotDto(
                        bank.GetValueOrDefault(BankKey(page, slot)),
                        others,
                        slot
                    ))
                    .ToList()
            ))
            .ToList();

        var saves = new List<SaveInventoryDTO>();

        foreach (var loaders in savesLoadersService.GetAllLoaders().OrderBy(x => x.Save.Version))
        {
            var save = loaders.Save;
            var saveFile = save.GetSave();
            var bag = saveFile.Inventory;
            var map = GetVersionMap(others, saveFile);
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
                            Movable: !protectedPocket,
                            StackId: null,
                            Origins: []
                        ));
                        continue;
                    }

                    map.TryGetValue(item.Index, out var itemKey);
                    var mapped = !string.IsNullOrWhiteSpace(itemKey);

                    var origins = mapped
                        ? GetEffectiveSaveOrigins(
                            saveProvenance,
                            save,
                            pouch.Type,
                            itemKey!,
                            item.Count
                        )
                        : [];

                    slots.Add(new(
                        Slot: slot,
                        ItemKey: mapped ? itemKey : null,
                        Name: mapped
                            ? GetItemName(others, itemKey!)
                            : $"Item #{item.Index}",
                        ItemId: item.Index,
                        Count: item.Count,
                        MaxCount: bag.GetMaxCount(pouch.Type, item.Index),
                        SpriteVersion: save.Version,
                        Movable: !protectedPocket && mapped,
                        StackId: mapped
                            ? SaveProvenanceKey(save.Id, pouch.Type, itemKey!)
                            : null,
                        Origins: origins
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

    public async Task<int> CreatePage()
    {
        var bank = await LoadBankState();
        var nextPage = await GetPageCount(bank) + 1;
        await SavePageCount(nextPage);
        return nextPage;
    }

    public async Task<ItemBankMoveResult> Move(MoveInventoryItemActionInput input)
    {
        if (input.Count <= 0)
            throw new ArgumentException("Item transfer count must be greater than zero.");

        var others = await staticDataService.GetStaticOthers();
        var bank = await LoadBankState();
        var saveProvenance = await LoadSaveProvenance();

        var source = ResolveSource(input, bank, saveProvenance, others);

        if (input.SourceKind == input.TargetKind
            && input.SourceId == input.TargetId
            && input.SourcePouch == input.TargetPouch
            && input.SourceSlot == input.TargetSlot)
        {
            return new(source.ItemName, 0, source.Version, source.Version);
        }

        // PKVault bank -> bank whole-stack relocation/swap keeps the exact same
        // persistent stack identity, just like moving a .pkm around PKVault.
        if (IsBank(input.SourceKind) && IsBank(input.TargetKind))
        {
            var sourcePage = ParseBankPage(input.SourceId);
            var targetPage = ParseBankPage(input.TargetId);
            ValidateBankSlot(input.SourceSlot);
            ValidateBankSlot(input.TargetSlot);

            var sourceKey = BankKey(sourcePage, input.SourceSlot);
            var targetKey = BankKey(targetPage, input.TargetSlot);
            var sourceStack = bank[sourceKey];
            var targetStack = bank.GetValueOrDefault(targetKey);

            if (input.Count >= source.Available)
            {
                if (targetStack is null)
                {
                    bank.Remove(sourceKey);
                    bank[targetKey] = sourceStack with
                    {
                        Page = targetPage,
                        Slot = input.TargetSlot,
                    };

                    await SaveBankState(bank);

                    return new(
                        source.ItemName,
                        checked((int)Math.Min(source.Available, int.MaxValue)),
                        null,
                        null
                    );
                }

                if (targetStack.ItemKey != source.ItemKey)
                {
                    bank[targetKey] = sourceStack with
                    {
                        Page = targetPage,
                        Slot = input.TargetSlot,
                    };
                    bank[sourceKey] = targetStack with
                    {
                        Page = sourcePage,
                        Slot = input.SourceSlot,
                    };

                    await SaveBankState(bank);

                    return new(
                        source.ItemName,
                        checked((int)Math.Min(source.Available, int.MaxValue)),
                        null,
                        null
                    );
                }
            }
        }

        var requested = checked((int)Math.Min(source.Available, input.Count));

        var target = ApplyTarget(
            input,
            source,
            requested,
            bank,
            saveProvenance,
            others,
            count => TakeOrigins(source.Origins, count)
        );

        if (target.Moved <= 0)
            throw new InvalidOperationException(
                "The target stack has no room; nothing was moved."
            );

        source.Deduct(target.Moved);

        if (source.UsesBank || target.UsesBank)
            await SaveBankState(bank);

        if (source.UsesSaveProvenance || target.UsesSaveProvenance)
            await SaveSaveProvenance(saveProvenance);

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

        // Box/page placement is NOT represented by these folders.
        // Folders represent the generation where the stack originated.
        fileIOService.Delete(InventoryRoot);

        foreach (var stack in bank.Values
            .Where(x => x.Count > 0)
            .OrderBy(x => x.Page)
            .ThenBy(x => x.Slot))
        {
            var folder = GetOriginFolder(stack);
            var originDir = Path.Combine(InventoryRoot, folder);
            fileIOService.CreateDirectory(originDir);

            var safeItem = SanitizeFilePart(stack.ItemKey);
            var path = Path.Combine(originDir, $"{safeItem}_{stack.Id}.item");

            var payload = new ItemBankFileDTO(
                Id: stack.Id,
                ItemKey: stack.ItemKey,
                Count: stack.Count,
                Box: stack.Page,
                Slot: stack.Slot,
                SpriteVersion: stack.SpriteVersion,
                Origins: NormalizeOrigins(stack.Origins)
            );

            var bytes = System.Text.Encoding.UTF8.GetBytes(
                JsonSerializer.Serialize(payload, JsonOptions) + "\n"
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
        bool UsesSaveProvenance,
        List<ItemOriginDTO> Origins,
        Action<int> Deduct
    );

    private sealed record TargetResult(
        int Moved,
        GameVersion? Version,
        bool UsesBank,
        bool UsesSaveProvenance
    );

    private SourceStack ResolveSource(
        MoveInventoryItemActionInput input,
        Dictionary<string, BankStack> bank,
        Dictionary<string, List<ItemOriginDTO>> saveProvenance,
        StaticOthersData others
    )
    {
        if (IsBank(input.SourceKind))
        {
            var page = ParseBankPage(input.SourceId);
            ValidateBankSlot(input.SourceSlot);

            var key = BankKey(page, input.SourceSlot);
            var stack = bank.GetValueOrDefault(key)
                ?? throw new InvalidOperationException(
                    "The source PKVault inventory slot is empty."
                );

            var bankOrigins = ReconcileOrigins(
                stack.Origins,
                stack.Count,
                LegacyOrigin(stack.SpriteVersion, stack.Count)
            );

            return new(
                stack.ItemKey,
                GetItemName(others, stack.ItemKey),
                stack.Count,
                stack.SpriteVersion,
                null,
                true,
                false,
                bankOrigins,
                moved =>
                {
                    var left = stack.Count - moved;

                    if (left <= 0)
                    {
                        bank.Remove(key);
                        return;
                    }

                    bank[key] = stack with
                    {
                        Count = left,
                        Origins = RemoveOrigins(bankOrigins, moved),
                    };
                }
            );
        }

        if (!IsSave(input.SourceKind))
            throw new ArgumentException(
                $"Unknown inventory source kind: {input.SourceKind}"
            );

        var saveId = ParseSaveId(input.SourceId);
        var loaders = savesLoadersService.GetLoaders(saveId)
            ?? throw new KeyNotFoundException($"Save {saveId} not found.");

        var save = loaders.Save;
        var saveFile = save.GetSave();
        var bag = saveFile.Inventory;
        var pouch = GetPouch(bag, input.SourcePouch);

        if (!IsMovablePouch(pouch.Type))
            throw new InvalidOperationException(
                $"{GetPouchLabel(pouch.Type)} is protected and cannot be moved."
            );

        if ((uint)input.SourceSlot >= pouch.Items.Length)
            throw new ArgumentOutOfRangeException(nameof(input.SourceSlot));

        var item = pouch.Items[input.SourceSlot];

        if (item.Index <= 0 || item.Count <= 0)
            throw new InvalidOperationException(
                "The source save inventory slot is empty."
            );

        var map = GetVersionMap(others, saveFile);

        if (!map.TryGetValue(item.Index, out var itemKey)
            || string.IsNullOrWhiteSpace(itemKey))
        {
            throw new InvalidOperationException(
                $"Item {item.Index} in {save.Version} has no safe cross-generation mapping."
            );
        }

        var provenanceKey = SaveProvenanceKey(save.Id, pouch.Type, itemKey);
        var saveOrigins = GetEffectiveSaveOrigins(
            saveProvenance,
            save,
            pouch.Type,
            itemKey,
            item.Count
        );

        return new(
            itemKey,
            GetItemName(others, itemKey),
            item.Count,
            save.Version,
            save.Version,
            false,
            true,
            saveOrigins,
            moved =>
            {
                item.Count -= moved;
                var left = item.Count;

                if (left <= 0)
                {
                    item.Clear();
                    saveProvenance.Remove(provenanceKey);
                }
                else
                {
                    saveProvenance[provenanceKey] =
                        RemoveOrigins(saveOrigins, moved);
                }

                pouch.ClearCount0();
                bag.CopyTo(saveFile);
                loaders.Pkms.HasWritten = true;
            }
        );
    }

    private TargetResult ApplyTarget(
        MoveInventoryItemActionInput input,
        SourceStack source,
        int requested,
        Dictionary<string, BankStack> bank,
        Dictionary<string, List<ItemOriginDTO>> saveProvenance,
        StaticOthersData others,
        Func<int, List<ItemOriginDTO>> getMovedOrigins
    )
    {
        if (IsBank(input.TargetKind))
        {
            var page = ParseBankPage(input.TargetId);
            ValidateBankSlot(input.TargetSlot);

            var key = BankKey(page, input.TargetSlot);
            var bankTarget = bank.GetValueOrDefault(key);

            if (bankTarget is not null
                && bankTarget.ItemKey != source.ItemKey)
            {
                throw new InvalidOperationException(
                    "Target PKVault inventory slot contains a different item."
                );
            }

            var movedOrigins = getMovedOrigins(requested);

            if (bankTarget is null)
            {
                bank[key] = new(
                    Id: NewStackId(),
                    Page: page,
                    Slot: input.TargetSlot,
                    ItemKey: source.ItemKey,
                    Count: requested,
                    SpriteVersion: source.SpriteVersion,
                    Origins: movedOrigins
                );
            }
            else
            {
                bank[key] = bankTarget with
                {
                    Count = checked(bankTarget.Count + requested),
                    Origins = MergeOrigins(
                        bankTarget.Origins,
                        movedOrigins
                    ),
                };
            }

            return new(
                requested,
                null,
                true,
                false
            );
        }

        if (!IsSave(input.TargetKind))
            throw new ArgumentException(
                $"Unknown inventory target kind: {input.TargetKind}"
            );

        var saveId = ParseSaveId(input.TargetId);
        var loaders = savesLoadersService.GetLoaders(saveId)
            ?? throw new KeyNotFoundException($"Save {saveId} not found.");

        var save = loaders.Save;
        var saveFile = save.GetSave();
        var bag = saveFile.Inventory;
        var pouch = GetPouch(bag, input.TargetPouch);

        if (!IsMovablePouch(pouch.Type))
            throw new InvalidOperationException(
                $"{GetPouchLabel(pouch.Type)} is protected and cannot receive transferred items."
            );

        if ((uint)input.TargetSlot >= pouch.Items.Length)
            throw new ArgumentOutOfRangeException(nameof(input.TargetSlot));

        if (IsSave(input.SourceKind)
            && input.SourceId == input.TargetId
            && requested < source.Available
            && pouch.Items[input.TargetSlot].Index == 0)
        {
            throw new InvalidOperationException(
                "Game-save bags keep one stack per item. Split this stack in a PKVault inventory box instead."
            );
        }

        var map = GetVersionMap(others, saveFile);

        var targetPair = map.FirstOrDefault(kv =>
            string.Equals(
                kv.Value,
                source.ItemKey,
                StringComparison.Ordinal
            )
        );

        if (targetPair.Key <= 0)
            throw new InvalidOperationException(
                $"{source.ItemName} does not exist in {save.Version}."
            );

        var targetItemId = (ushort)targetPair.Key;

        if (!pouch.CanContain(targetItemId))
            throw new InvalidOperationException(
                $"{source.ItemName} does not belong in the {GetPouchLabel(pouch.Type)} pocket."
            );

        var saveTarget = pouch.Items[input.TargetSlot];

        if (saveTarget.Index != 0
            && saveTarget.Index != targetItemId)
        {
            throw new InvalidOperationException(
                "Target save slot contains a different item."
            );
        }

        var max = bag.GetMaxCount(pouch.Type, targetItemId);
        var before = saveTarget.Index == targetItemId
            ? saveTarget.Count
            : 0;

        var capacity = Math.Max(0, max - before);
        var moved = Math.Min(requested, capacity);

        if (moved <= 0)
            return new(0, save.Version, false, false);

        if (saveTarget.Index == 0)
        {
            saveTarget.Index = targetItemId;
            saveTarget.SetNewDetails(0);
            saveTarget.Count = moved;
        }
        else
        {
            saveTarget.Count = before + moved;
        }

        var provenanceKey = SaveProvenanceKey(
            save.Id,
            pouch.Type,
            source.ItemKey
        );

        var existingOrigins = before > 0
            ? GetEffectiveSaveOrigins(
                saveProvenance,
                save,
                pouch.Type,
                source.ItemKey,
                before
            )
            : [];

        saveProvenance[provenanceKey] = MergeOrigins(
            existingOrigins,
            getMovedOrigins(moved)
        );

        bag.CopyTo(saveFile);
        loaders.Pkms.HasWritten = true;

        return new(
            moved,
            save.Version,
            false,
            true
        );
    }

    private async Task<int> GetPageCount(
        Dictionary<string, BankStack> bank
    )
    {
        // Disk folders are origin generations, NOT UI boxes.
        var inferred = bank.Count == 0
            ? 1
            : Math.Max(1, bank.Values.Max(x => x.Page));

        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK_PAGES);

        return entity is not null
            && int.TryParse(entity.Value, out var stored)
            && stored > 0
                ? Math.Max(stored, inferred)
                : inferred;
    }

    private async Task SavePageCount(int pageCount)
    {
        pageCount = Math.Max(1, pageCount);

        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK_PAGES);

        if (entity is null)
        {
            await metaLoader.AddEntity(new()
            {
                Key = MetaKey.ITEM_BANK_PAGES,
                Value = pageCount.ToString(),
            });
        }
        else
        {
            entity.Value = pageCount.ToString();
            await metaLoader.UpdateEntity(entity);
        }
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
        var result = new Dictionary<string, BankStack>(
            StringComparer.Ordinal
        );

        if (!Directory.Exists(InventoryRoot))
            return result;

        foreach (var dir in Directory.EnumerateDirectories(InventoryRoot))
        {
            foreach (var file in Directory.EnumerateFiles(dir, "*.item"))
            {
                var text = File.ReadAllText(file).Trim();

                if (text.StartsWith('{'))
                {
                    try
                    {
                        var data = JsonSerializer.Deserialize<ItemBankFileDTO>(
                            text,
                            JsonOptions
                        );

                        if (data is null
                            || data.Count <= 0
                            || data.Box <= 0
                            || (uint)data.Slot >= BankPageSlots
                            || string.IsNullOrWhiteSpace(data.ItemKey))
                        {
                            continue;
                        }

                        var origins = ReconcileOrigins(
                            data.Origins,
                            data.Count,
                            LegacyOrigin(
                                data.SpriteVersion,
                                data.Count
                            )
                        );

                        var parsedStack = new BankStack(
                            Id: string.IsNullOrWhiteSpace(data.Id)
                                ? NewStackId()
                                : data.Id,
                            Page: data.Box,
                            Slot: data.Slot,
                            ItemKey: data.ItemKey,
                            Count: data.Count,
                            SpriteVersion: data.SpriteVersion,
                            Origins: origins
                        );

                        result[BankKey(parsedStack.Page, parsedStack.Slot)] = parsedStack;
                        continue;
                    }
                    catch (JsonException)
                    {
                        // Fall through to alpha25/26 legacy format.
                    }
                }

                // alpha25/26 legacy:
                // inventory/<box>/<slot>.item containing key/count/version.
                if (!int.TryParse(Path.GetFileName(dir), out var legacyPage)
                    || legacyPage <= 0
                    || !int.TryParse(
                        Path.GetFileNameWithoutExtension(file),
                        out var legacySlot
                    )
                    || (uint)legacySlot >= BankPageSlots)
                {
                    continue;
                }

                var parts = text.Split('\t');

                if (parts.Length < 2
                    || !long.TryParse(parts[1], out var count)
                    || count <= 0)
                {
                    continue;
                }

                var spriteVersion = GameVersion.RD;

                if (parts.Length >= 3
                    && int.TryParse(parts[2], out var rawVersion))
                {
                    spriteVersion = (GameVersion)rawVersion;
                }

                var legacyFileStack = new BankStack(
                    Id: NewStackId(),
                    Page: legacyPage,
                    Slot: legacySlot,
                    ItemKey: parts[0],
                    Count: count,
                    SpriteVersion: spriteVersion,
                    Origins: LegacyOrigin(spriteVersion, count)
                );

                result[BankKey(legacyPage, legacySlot)] = legacyFileStack;
            }
        }

        return result;
    }

    private static Dictionary<string, BankStack> ParseMeta(string? value)
    {
        var result = new Dictionary<string, BankStack>(
            StringComparer.Ordinal
        );

        if (string.IsNullOrWhiteSpace(value))
            return result;

        if (value.TrimStart().StartsWith('['))
        {
            try
            {
                var stacks = JsonSerializer.Deserialize<List<BankStack>>(
                    value,
                    JsonOptions
                ) ?? [];

                foreach (var raw in stacks)
                {
                    if (raw.Page <= 0
                        || (uint)raw.Slot >= BankPageSlots
                        || raw.Count <= 0
                        || string.IsNullOrWhiteSpace(raw.ItemKey))
                    {
                        continue;
                    }

                    var stack = raw with
                    {
                        Id = string.IsNullOrWhiteSpace(raw.Id)
                            ? NewStackId()
                            : raw.Id,
                        Origins = ReconcileOrigins(
                            raw.Origins,
                            raw.Count,
                            LegacyOrigin(raw.SpriteVersion, raw.Count)
                        ),
                    };

                    result[BankKey(stack.Page, stack.Slot)] = stack;
                }

                return result;
            }
            catch (JsonException)
            {
                // Fall through to alpha24/25 tab migration.
            }
        }

        var legacySlotCounter = 0;

        foreach (var line in value.Split(
            '\n',
            StringSplitOptions.RemoveEmptyEntries
        ))
        {
            var parts = line.Split('\t');

            // alpha25/26:
            // page slot item-key count sprite-version
            if (parts.Length >= 5
                && int.TryParse(parts[0], out var page)
                && int.TryParse(parts[1], out var slot)
                && long.TryParse(parts[3], out var count)
                && int.TryParse(parts[4], out var version)
                && page > 0
                && (uint)slot < BankPageSlots
                && count > 0)
            {
                var spriteVersion = (GameVersion)version;

                var stack = new BankStack(
                    Id: NewStackId(),
                    Page: page,
                    Slot: slot,
                    ItemKey: parts[2],
                    Count: count,
                    SpriteVersion: spriteVersion,
                    Origins: LegacyOrigin(spriteVersion, count)
                );

                result[BankKey(page, slot)] = stack;
                continue;
            }

            // alpha24:
            // item-key count
            if (parts.Length == 2
                && long.TryParse(parts[1], out var legacyCount)
                && legacyCount > 0)
            {
                var legacyPage2 = legacySlotCounter / BankPageSlots + 1;
                var legacySlot2 = legacySlotCounter % BankPageSlots;
                var spriteVersion = GameVersion.RD;

                var stack = new BankStack(
                    Id: NewStackId(),
                    Page: legacyPage2,
                    Slot: legacySlot2,
                    ItemKey: parts[0],
                    Count: legacyCount,
                    SpriteVersion: spriteVersion,
                    Origins: LegacyOrigin(spriteVersion, legacyCount)
                );

                result[BankKey(legacyPage2, legacySlot2)] = stack;
                legacySlotCounter++;
            }
        }

        return result;
    }

    private async Task SaveBankState(
        Dictionary<string, BankStack> bank
    )
    {
        var value = JsonSerializer.Serialize(
            bank.Values
                .Where(x => x.Count > 0)
                .OrderBy(x => x.Page)
                .ThenBy(x => x.Slot)
                .Select(x => x with
                {
                    Origins = NormalizeOrigins(x.Origins),
                })
                .ToList(),
            JsonOptions
        );

        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK);

        if (entity is null)
        {
            await metaLoader.AddEntity(new()
            {
                Key = MetaKey.ITEM_BANK,
                Value = value,
            });
        }
        else
        {
            entity.Value = value;
            await metaLoader.UpdateEntity(entity);
        }
    }

    private async Task<Dictionary<string, List<ItemOriginDTO>>>
        LoadSaveProvenance()
    {
        var entity = await metaLoader.GetEntity(
            MetaKey.ITEM_SAVE_PROVENANCE
        );

        if (entity is null || string.IsNullOrWhiteSpace(entity.Value))
            return new(StringComparer.Ordinal);

        try
        {
            return JsonSerializer.Deserialize<
                Dictionary<string, List<ItemOriginDTO>>
            >(entity.Value, JsonOptions)
                ?? new(StringComparer.Ordinal);
        }
        catch (JsonException)
        {
            return new(StringComparer.Ordinal);
        }
    }

    private async Task SaveSaveProvenance(
        Dictionary<string, List<ItemOriginDTO>> provenance
    )
    {
        var cleaned = provenance
            .Where(x => x.Value.Any(o => o.Count > 0))
            .ToDictionary(
                x => x.Key,
                x => NormalizeOrigins(x.Value),
                StringComparer.Ordinal
            );

        var value = JsonSerializer.Serialize(cleaned, JsonOptions);

        var entity = await metaLoader.GetEntity(
            MetaKey.ITEM_SAVE_PROVENANCE
        );

        if (entity is null)
        {
            await metaLoader.AddEntity(new()
            {
                Key = MetaKey.ITEM_SAVE_PROVENANCE,
                Value = value,
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
                Movable: true,
                StackId: null,
                Origins: []
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
            Movable: true,
            StackId: stack.Id,
            Origins: NormalizeOrigins(stack.Origins)
        );
    }

    private static List<ItemOriginDTO> GetEffectiveSaveOrigins(
        Dictionary<string, List<ItemOriginDTO>> provenance,
        SaveWrapper save,
        InventoryType pouchType,
        string itemKey,
        long currentCount
    )
    {
        var key = SaveProvenanceKey(
            save.Id,
            pouchType,
            itemKey
        );

        var fallback = DefaultOrigin(save, currentCount);

        if (!provenance.TryGetValue(key, out var stored)
            || stored.Count == 0)
        {
            return fallback;
        }

        return ReconcileOrigins(
            stored,
            currentCount,
            fallback
        );
    }

    private static List<ItemOriginDTO> DefaultOrigin(
        SaveWrapper save,
        long count
    )
    {
        if (count <= 0)
            return [];

        var saveFile = save.GetSave();

        return [
            new(
                Generation: saveFile.Generation,
                Version: save.Version,
                Owner: string.IsNullOrWhiteSpace(save.OT)
                    ? "Unknown"
                    : save.OT,
                SaveId: save.Id,
                Count: count
            ),
        ];
    }

    private static List<ItemOriginDTO> LegacyOrigin(
        GameVersion version,
        long count
    )
    {
        if (count <= 0)
            return [];

        return [
            new(
                Generation: version.Generation,
                Version: version,
                Owner: "Unknown",
                SaveId: null,
                Count: count
            ),
        ];
    }

    private static List<ItemOriginDTO> ReconcileOrigins(
        IEnumerable<ItemOriginDTO>? existing,
        long targetCount,
        List<ItemOriginDTO> fallback
    )
    {
        if (targetCount <= 0)
            return [];

        var normalized = NormalizeOrigins(existing ?? []);

        if (normalized.Count == 0)
            return ResizeFallback(fallback, targetCount);

        var total = normalized.Sum(x => x.Count);

        if (total == targetCount)
            return normalized;

        if (total > targetCount)
            return TakeOrigins(normalized, targetCount);

        var missing = targetCount - total;
        var add = ResizeFallback(fallback, missing);

        return MergeOrigins(normalized, add);
    }

    private static List<ItemOriginDTO> ResizeFallback(
        List<ItemOriginDTO> fallback,
        long count
    )
    {
        if (count <= 0)
            return [];

        if (fallback.Count == 0)
        {
            return [
                new(
                    Generation: 0,
                    Version: GameVersion.Any,
                    Owner: "Unknown",
                    SaveId: null,
                    Count: count
                ),
            ];
        }

        var first = fallback[0];
        return [ first with { Count = count } ];
    }

    private static List<ItemOriginDTO> NormalizeOrigins(
        IEnumerable<ItemOriginDTO> origins
    )
    {
        var result = new List<ItemOriginDTO>();

        foreach (var origin in origins.Where(x => x.Count > 0))
        {
            var index = result.FindIndex(x =>
                x.Generation == origin.Generation
                && x.Version == origin.Version
                && string.Equals(
                    x.Owner,
                    origin.Owner,
                    StringComparison.Ordinal
                )
                && x.SaveId == origin.SaveId
            );

            if (index < 0)
            {
                result.Add(origin);
            }
            else
            {
                var current = result[index];
                result[index] = current with
                {
                    Count = checked(current.Count + origin.Count),
                };
            }
        }

        return result;
    }

    private static List<ItemOriginDTO> MergeOrigins(
        IEnumerable<ItemOriginDTO> left,
        IEnumerable<ItemOriginDTO> right
    )
        => NormalizeOrigins(left.Concat(right));

    private static List<ItemOriginDTO> TakeOrigins(
        IEnumerable<ItemOriginDTO> origins,
        long count
    )
    {
        var result = new List<ItemOriginDTO>();
        var remaining = count;

        foreach (var origin in NormalizeOrigins(origins))
        {
            if (remaining <= 0)
                break;

            var take = Math.Min(origin.Count, remaining);

            if (take > 0)
                result.Add(origin with { Count = take });

            remaining -= take;
        }

        if (remaining > 0)
        {
            result.Add(new(
                Generation: 0,
                Version: GameVersion.Any,
                Owner: "Unknown",
                SaveId: null,
                Count: remaining
            ));
        }

        return NormalizeOrigins(result);
    }

    private static List<ItemOriginDTO> RemoveOrigins(
        IEnumerable<ItemOriginDTO> origins,
        long count
    )
    {
        var result = new List<ItemOriginDTO>();
        var remainingToRemove = count;

        foreach (var origin in NormalizeOrigins(origins))
        {
            if (remainingToRemove <= 0)
            {
                result.Add(origin);
                continue;
            }

            var remove = Math.Min(origin.Count, remainingToRemove);
            var left = origin.Count - remove;
            remainingToRemove -= remove;

            if (left > 0)
                result.Add(origin with { Count = left });
        }

        return NormalizeOrigins(result);
    }

    private static string GetOriginFolder(BankStack stack)
    {
        var generations = NormalizeOrigins(stack.Origins)
            .Where(x => x.Generation > 0)
            .Select(x => x.Generation)
            .Distinct()
            .Order()
            .ToList();

        return generations.Count switch
        {
            1 => generations[0].ToString(),
            > 1 => "mixed",
            _ => "unknown",
        };
    }

    private static string SanitizeFilePart(string value)
    {
        var invalid = Path.GetInvalidFileNameChars().ToHashSet();

        var cleaned = new string(
            value
                .ToLowerInvariant()
                .Select(ch => invalid.Contains(ch) ? '-' : ch)
                .ToArray()
        ).Trim('-', '.', ' ');

        return string.IsNullOrWhiteSpace(cleaned)
            ? "item"
            : cleaned;
    }

    private static string NewStackId()
        => Guid.NewGuid().ToString("N")[..10];

    private static string BankKey(int page, int slot)
        => $"{page}:{slot}";

    private static string SaveProvenanceKey(
        uint saveId,
        InventoryType pouch,
        string itemKey
    )
        => $"{saveId}:{pouch}:{itemKey}";

    private static int ParseBankPage(string id)
    {
        if (!int.TryParse(id, out var page) || page <= 0)
            throw new ArgumentException(
                $"Invalid PKVault inventory page: {id}"
            );

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

    private static InventoryPouch GetPouch(
        PlayerBag bag,
        string? pouchName
    )
    {
        if (!Enum.TryParse<InventoryType>(
            pouchName,
            out var pouchType
        ))
        {
            throw new ArgumentException(
                $"Invalid inventory pocket: {pouchName}"
            );
        }

        return bag.Pouches.FirstOrDefault(x => x.Type == pouchType)
            ?? throw new InvalidOperationException(
                $"Save does not contain the {GetPouchLabel(pouchType)} pocket."
            );
    }

    private static bool IsBank(string kind)
        => string.Equals(
            kind,
            "bank",
            StringComparison.OrdinalIgnoreCase
        );

    private static bool IsSave(string kind)
        => string.Equals(
            kind,
            "save",
            StringComparison.OrdinalIgnoreCase
        );

    private static Dictionary<int, string> GetVersionMap(
        StaticOthersData others,
        SaveFile save
    )
    {
        var mapped = others.Items.VersionItems
            .FirstOrDefault(
                x => x.Versions.Contains((byte)save.Version)
            )
            ?.ComboItems;

        if (mapped is { Count: > 0 })
            return mapped;

        // Gen 1 has no held items, so the ordinary static item map is empty.
        // PlayerBag1 still exposes the complete bag/PC item table.
        var result = new Dictionary<int, string>();
        var itemNames = GameInfo.Strings.GetItemStrings(
            save.Context,
            save.Version
        );
        var bag = save.Inventory;

        foreach (var pouch in bag.Pouches)
        {
            foreach (var itemId in bag.Info.GetItems(pouch.Type))
            {
                if (itemId <= 0 || itemId >= itemNames.Length)
                    continue;

                var key = PokeApiFromPKHeX.GetPokeapiItemName(
                    itemNames[itemId]
                );

                if (string.IsNullOrWhiteSpace(key)
                    || key == "???")
                {
                    continue;
                }

                if (others.Items.Items.ContainsKey(key))
                    result[itemId] = key;
            }
        }

        return result;
    }

    private static string GetItemName(
        StaticOthersData others,
        string itemKey
    )
    {
        return others.Items.Items.TryGetValue(
            itemKey,
            out var item
        )
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

# Frontend DTOs receive persistent stack ID + provenance.
put29("frontend/src/inventory/types.ts", r'''import type { GameVersion } from '../data/sdk/model';

export type ItemOrigin = {
    generation: number;
    version: GameVersion;
    owner: string;
    saveId?: number | null;
    count: number;
};

export type InventorySlot = {
    slot: number;
    itemKey?: string | null;
    name?: string | null;
    itemId?: number | null;
    count: number;
    maxCount: number;
    spriteVersion: GameVersion;
    movable: boolean;
    stackId?: string | null;
    origins: ItemOrigin[];
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
''')

# Exact Pokemon-storage interaction code remains; add Stack/Origin tabs to the
# item click popover. Drag always moves whole stack; Split is independent.
put29("frontend/src/inventory/inventory-item.tsx", r'''import {
    Badge,
    Box,
    Button,
    Group,
    Image,
    NumberInput,
    Popover,
    Stack,
    Tabs,
    Text,
} from '@mantine/core';
import { useMergedRef } from '@mantine/hooks';
import { LockIcon, SplitIcon } from 'lucide-react';
import React from 'react';
import { ItemImg } from '../img/item-img';
import { getGameInfos } from '../pokedex/details/util/get-game-infos';
import { useStaticData } from '../hooks/use-static-data';
import { WithControlsIcons } from '../ui/interaction/controls/icons/with-controls-icons';
import { getSelectControl } from '../ui/interaction/focus-controls/common-controls/select-controls';
import { useDragControls } from '../ui/interaction/focus-controls/common-controls/drag-controls';
import { useFocusControls } from '../ui/interaction/focus-controls/use-focus-controls';
import { DragRender } from '../ui/interaction/move/components/drag-render';
import { useDragSubmitting } from '../ui/interaction/move/hooks/use-drag-submitting';
import { useDragging } from '../ui/interaction/move/hooks/use-dragging';
import { useDroppable } from '../ui/interaction/move/hooks/use-droppable';
import { UIStorageItemBase } from '../ui/storage/storage-item/base/ui-storage-item-base';
import { UIStorageItemPlaceholder } from '../ui/storage/storage-item/placeholder/ui-storage-item-placeholder';
import { useCurrentPanel } from '../ui/storage/storage-content/context/ui-panel-context';
import { UISpeciesImgSkeleton } from '../ui/sprite-img/species-img/ui-species-img-skeleton';
import type {
    InventoryLocation,
    InventorySlot,
    ItemOrigin,
} from './types';
import type { InventoryMoveContainer } from './inventory-move-provider';

type InventoryItemProps = {
    slot: InventorySlot;
    location: InventoryLocation;
    isBank: boolean;
    nearestEmptySlot?: number;
    globalOrder: number;
    nodeId: string;
    onSplit: (
        source: InventoryLocation,
        target: InventoryLocation,
        count: number,
    ) => Promise<void>;
    onError: (message: string) => void;
};

const ItemSprite: React.FC<{ slot: InventorySlot }> = ({ slot }) => <>
    <UISpeciesImgSkeleton visible={false} />

    {!!slot.itemKey && <Box
        pos='absolute'
        inset={0}
        display='flex'
        style={{
            alignItems: 'center',
            justifyContent: 'center',
            pointerEvents: 'none',
        }}
    >
        <ItemImg
            item={slot.itemKey}
            version={slot.spriteVersion}
            sourceRealHeight={32}
            style={{
                '--sprite-item-size-multiplier':
                    'calc(var(--sprite-species-size-multiplier, 1) * 2.5)',
            } as React.CSSProperties}
        />
    </Box>}

    {slot.count > 0 && <Badge
        size='md'
        variant='filled'
        pos='absolute'
        right={4}
        bottom={4}
    >
        {slot.count}
    </Badge>}

    {slot.count > 0 && !slot.movable && <LockIcon
        size={17}
        style={{
            position: 'absolute',
            left: 5,
            bottom: 5,
        }}
    />}
</>;

const OriginLine: React.FC<{ origin: ItemOrigin }> = ({ origin }) => {
    const staticData = useStaticData();
    const game = staticData.versions[origin.version]?.name
        ?? String(origin.version);

    let image: string | undefined;
    try {
        image = getGameInfos(origin.version).img;
    } catch {
        image = undefined;
    }

    return <Stack gap={4} p='xs'>
        <Group gap='xs'>
            {image && <Image src={image} w={22} h={22} fit='contain' />}
            <Text fw={600}>{game}</Text>
        </Group>

        <Group justify='space-between' gap='lg'>
            <Text size='xs' c='dimmed'>Generation</Text>
            <Text size='sm'>{origin.generation || '-'}</Text>
        </Group>

        <Group justify='space-between' gap='lg'>
            <Text size='xs' c='dimmed'>Original owner</Text>
            <Text size='sm'>{origin.owner || 'Unknown'}</Text>
        </Group>

        <Group justify='space-between' gap='lg'>
            <Text size='xs' c='dimmed'>Quantity</Text>
            <Text size='sm'>×{origin.count}</Text>
        </Group>
    </Stack>;
};

const InventoryFilledItem: React.FC<InventoryItemProps> = ({
    slot,
    location,
    isBank,
    nearestEmptySlot,
    globalOrder,
    nodeId,
    onSplit,
    onError,
}) => {
    const panel = useCurrentPanel();
    const [ opened, setOpened ] = React.useState(false);
    const [ splitAmount, setSplitAmount ] = React.useState(1);
    const [ tab, setTab ] = React.useState<string | null>('stack');

    const container: InventoryMoveContainer = {
        kind: location.kind,
        id: location.id,
        pouch: location.pouch,
    };

    const itemId = String(slot.slot);

    const dragging = useDragging(itemId, container);
    const draggingMove = dragging.useDrag();

    const droppable = useDroppable({
        targetContainer: container,
        targetPosition: slot.slot,
        targetId: itemId,
    });

    const submitting = useDragSubmitting(
        container,
        slot.slot,
        itemId
    );

    const disabled = !slot.movable || droppable.canDrop === false;
    const loading = submitting;
    const isDraggingState =
        dragging.isDragging || droppable.isDroppable;

    const dragControls = useDragControls({
        dragging,
        draggingMove,
        droppable,
        disabled: disabled || loading,
    });

    const { focusProps, controlProps, controlIcons } =
        useFocusControls({
            scopeNodeId: nodeId,
            order: globalOrder,
            onFocus: ({ node }) => {
                dragging.focusNode(node);
                panel.normalizeCurrentPanel();
            },
            controls: [
                !isDraggingState
                    && !disabled
                    && !loading
                    && getSelectControl({
                        label: 'Open',
                        action: () => setOpened(value => !value),
                    }),
                ...dragControls,
            ],
        });

    const ref = useMergedRef(
        dragging.ref,
        focusProps.ref
    );

    const split = async () => {
        if (!isBank || nearestEmptySlot === undefined)
            return;

        const amount = Math.max(
            1,
            Math.min(Number(slot.count) - 1, splitAmount)
        );

        if (amount <= 0 || amount >= slot.count) {
            onError(
                'Split amount must be smaller than the current stack.'
            );
            return;
        }

        try {
            await onSplit(
                location,
                {
                    ...location,
                    slot: nearestEmptySlot,
                },
                amount
            );

            setOpened(false);
            setSplitAmount(1);
        } catch (error) {
            onError(
                error instanceof Error
                    ? error.message
                    : String(error)
            );
        }
    };

    const itemButton = <WithControlsIcons
        placement='out'
        icons={controlIcons('open', 'drag', 'drop')}
    >
        <UIStorageItemBase
            label={droppable.helpText ?? <Group gap='xs'>
                <Text>{slot.name}</Text>
                <Badge variant='light'>×{slot.count}</Badge>
            </Group>}
            loading={loading}
            disabled={disabled}
            {...focusProps}
            {...controlProps('open', 'drag', 'drop')}
            ref={ref}
        >
            <ItemSprite slot={slot} />
        </UIStorageItemBase>
    </WithControlsIcons>;

    return <>
        <Popover
            opened={opened}
            onChange={setOpened}
            position='bottom'
            withArrow
            shadow='md'
        >
            <Popover.Target>
                {itemButton}
            </Popover.Target>

            <Popover.Dropdown p={0}>
                <Tabs
                    value={tab}
                    onChange={setTab}
                    w={270}
                >
                    <Tabs.List>
                        <Tabs.Tab value='stack'>Stack</Tabs.Tab>
                        <Tabs.Tab value='origin'>Origin</Tabs.Tab>
                    </Tabs.List>

                    <Tabs.Panel value='stack' p='sm'>
                        <Stack gap='xs'>
                            <Text fw={600}>{slot.name}</Text>

                            <Group justify='space-between'>
                                <Text size='xs' c='dimmed'>
                                    Stack size
                                </Text>
                                <Text size='sm'>
                                    {slot.count}
                                </Text>
                            </Group>

                            {slot.stackId && <Group justify='space-between'>
                                <Text size='xs' c='dimmed'>
                                    Stack ID
                                </Text>
                                <Text size='xs' ff='monospace'>
                                    {slot.stackId}
                                </Text>
                            </Group>}

                            {isBank
                                ? <>
                                    <Text size='xs'>
                                        Amount to split into the nearest empty slot:
                                    </Text>

                                    <NumberInput
                                        min={1}
                                        max={Math.max(
                                            1,
                                            Number(slot.count) - 1
                                        )}
                                        value={splitAmount}
                                        onChange={value =>
                                            setSplitAmount(
                                                Number(value) || 1
                                            )
                                        }
                                    />

                                    <Button
                                        leftSection={
                                            <SplitIcon size={14} />
                                        }
                                        disabled={
                                            nearestEmptySlot === undefined
                                            || slot.count <= 1
                                            || splitAmount <= 0
                                            || splitAmount >= slot.count
                                        }
                                        onClick={() => void split()}
                                    >
                                        Split
                                    </Button>
                                </>
                                : <Text size='xs' c='dimmed'>
                                    Dragging moves the whole stack.
                                    Move it into PKVault if you want to split it.
                                </Text>}
                        </Stack>
                    </Tabs.Panel>

                    <Tabs.Panel value='origin' p='sm'>
                        <Stack gap='xs'>
                            {slot.origins.length > 1 && <Text
                                size='xs'
                                c='dimmed'
                            >
                                This stack contains items from multiple origins.
                            </Text>}

                            {slot.origins.length > 0
                                ? slot.origins.map((origin, index) =>
                                    <OriginLine
                                        key={[
                                            origin.generation,
                                            origin.version,
                                            origin.owner,
                                            origin.saveId,
                                            index,
                                        ].join('-')}
                                        origin={origin}
                                    />
                                )
                                : <Text size='sm' c='dimmed'>
                                    Origin is unknown.
                                </Text>}
                        </Stack>
                    </Tabs.Panel>
                </Tabs>
            </Popover.Dropdown>
        </Popover>

        {dragging.isDragging && <DragRender
            elementRef={dragging.ref}
        >
            <UIStorageItemBase opacity={0.75}>
                <ItemSprite slot={slot} />
            </UIStorageItemBase>
        </DragRender>}
    </>;
};

export const InventoryItem: React.FC<InventoryItemProps> = props => {
    const { slot, location, nodeId, globalOrder } = props;
    const hasItem = !!slot.itemKey && slot.count > 0;

    if (hasItem)
        return <InventoryFilledItem {...props} />;

    const container: InventoryMoveContainer = {
        kind: location.kind,
        id: location.id,
        pouch: location.pouch,
    };

    return <UIStorageItemPlaceholder
        nodeId={nodeId}
        container={container}
        slot={slot.slot}
        globalOrder={globalOrder}
    />;
};
''')

print("PKVault V8 alpha29 provenance-aware item stack storage applied")

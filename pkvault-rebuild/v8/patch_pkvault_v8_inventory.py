from pathlib import Path

def put(rel, text):
    path = PKVAULT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

put("PKVault.Core/storage/services/ItemBankService.cs", r'''using PKHeX.Core;

namespace PKVault.Core;

public record ItemBankEntryDTO(string ItemKey, string Name, long Count);

public record SaveInventoryItemDTO(
    string ItemKey,
    string Name,
    int ItemId,
    int Count,
    InventoryType Pouch,
    int MaxCount
);

public record SaveInventoryDTO(
    uint SaveId,
    GameVersion Version,
    string TrainerName,
    bool Supported,
    List<SaveInventoryItemDTO> Items
);

public record ItemInventoryStateDTO(
    List<ItemBankEntryDTO> Bank,
    List<SaveInventoryDTO> Saves
);

public record MoveInventoryItemActionInput(
    uint? SourceSaveId,
    uint? TargetSaveId,
    string ItemKey,
    int? SourceItemId,
    InventoryType? SourcePouch,
    int Count
);

public record ItemBankMoveResult(
    string ItemName,
    int MovedCount,
    GameVersion? SourceVersion,
    GameVersion? TargetVersion
);

public class ItemBankService(
    ISavesLoadersService savesLoadersService,
    IMetaLoader metaLoader,
    StaticDataService staticDataService
)
{
    private static bool IsBankablePouch(InventoryType type) => type switch
    {
        InventoryType.None => false,
        InventoryType.KeyItems => false,
        InventoryType.TMHMs => false,
        InventoryType.ZCrystals => false,
        _ => true,
    };

    public async Task<ItemInventoryStateDTO> GetState()
    {
        var bank = await LoadBank();
        var others = await staticDataService.GetStaticOthers();

        var bankDtos = bank
            .Where(kv => kv.Value > 0)
            .OrderBy(kv => GetItemName(others, kv.Key), StringComparer.CurrentCultureIgnoreCase)
            .Select(kv => new ItemBankEntryDTO(
                kv.Key,
                GetItemName(others, kv.Key),
                kv.Value
            ))
            .ToList();

        var saveDtos = new List<SaveInventoryDTO>();

        foreach (var loaders in savesLoadersService.GetAllLoaders().OrderBy(x => x.Save.Version))
        {
            var save = loaders.Save;
            var bag = save.GetSave().Inventory;
            var map = GetVersionMap(others, save.Version);
            var items = new List<SaveInventoryItemDTO>();

            foreach (var pouch in bag.Pouches)
            {
                if (!IsBankablePouch(pouch.Type))
                    continue;

                foreach (var item in pouch.Items.Where(x => x.Index > 0 && x.Count > 0))
                {
                    if (!map.TryGetValue(item.Index, out var itemKey) || string.IsNullOrWhiteSpace(itemKey))
                        continue;

                    items.Add(new(
                        itemKey,
                        GetItemName(others, itemKey),
                        item.Index,
                        item.Count,
                        pouch.Type,
                        bag.GetMaxCount(pouch.Type, item.Index)
                    ));
                }
            }

            saveDtos.Add(new(
                save.Id,
                save.Version,
                save.OT,
                bag.Pouches.Count > 0,
                items.OrderBy(x => x.Pouch)
                    .ThenBy(x => x.Name, StringComparer.CurrentCultureIgnoreCase)
                    .ToList()
            ));
        }

        return new(bankDtos, saveDtos);
    }

    public async Task<ItemBankMoveResult> Move(MoveInventoryItemActionInput input)
    {
        if (input.Count <= 0)
            throw new ArgumentException("Item transfer count must be greater than zero.");

        if (input.SourceSaveId.HasValue == input.TargetSaveId.HasValue)
            throw new ArgumentException("Exactly one side of an item transfer must be a save; the other side is the PKVault Item Bank.");

        return input.SourceSaveId.HasValue
            ? await WithdrawFromSave(input)
            : await DepositToSave(input);
    }

    private async Task<ItemBankMoveResult> WithdrawFromSave(MoveInventoryItemActionInput input)
    {
        if (!input.SourceSaveId.HasValue || !input.SourceItemId.HasValue || !input.SourcePouch.HasValue)
            throw new ArgumentException("Withdrawing requires a source save, pouch, and item id.");

        if (!IsBankablePouch(input.SourcePouch.Value))
            throw new InvalidOperationException($"The {input.SourcePouch.Value} pocket is protected and cannot be moved into PKVault.");

        var loaders = savesLoadersService.GetLoaders(input.SourceSaveId.Value)
            ?? throw new KeyNotFoundException($"Save {input.SourceSaveId.Value} not found.");

        var save = loaders.Save;
        var bag = save.GetSave().Inventory;
        var pouch = bag.Pouches.FirstOrDefault(x => x.Type == input.SourcePouch.Value)
            ?? throw new InvalidOperationException($"Save does not contain the {input.SourcePouch.Value} pocket.");

        var source = pouch.Items.FirstOrDefault(x => x.Index == input.SourceItemId.Value && x.Count > 0)
            ?? throw new InvalidOperationException("Item stack no longer exists in the source save.");

        var others = await staticDataService.GetStaticOthers();
        var map = GetVersionMap(others, save.Version);

        if (!map.TryGetValue(source.Index, out var actualKey) || string.IsNullOrWhiteSpace(actualKey))
            throw new InvalidOperationException($"Item {source.Index} in {save.Version} does not have a safe cross-generation mapping.");

        if (!string.Equals(input.ItemKey, actualKey, StringComparison.Ordinal))
            throw new InvalidOperationException("Item identity changed since the inventory was loaded; reload inventory and retry.");

        var moved = Math.Min(input.Count, source.Count);
        source.Count -= moved;

        if (source.Count <= 0)
            source.Clear();

        pouch.ClearCount0();
        bag.CopyTo(save.GetSave());
        loaders.Pkms.HasWritten = true;

        var bank = await LoadBank();
        bank[actualKey] = checked(bank.GetValueOrDefault(actualKey) + moved);
        await SaveBank(bank);

        return new(
            GetItemName(others, actualKey),
            moved,
            save.Version,
            null
        );
    }

    private async Task<ItemBankMoveResult> DepositToSave(MoveInventoryItemActionInput input)
    {
        if (!input.TargetSaveId.HasValue)
            throw new ArgumentException("Depositing requires a target save.");

        var loaders = savesLoadersService.GetLoaders(input.TargetSaveId.Value)
            ?? throw new KeyNotFoundException($"Save {input.TargetSaveId.Value} not found.");

        var save = loaders.Save;
        var bag = save.GetSave().Inventory;

        if (bag.Pouches.Count == 0)
            throw new InvalidOperationException("This save format does not expose a writable item inventory.");

        var bank = await LoadBank();
        var bankCount = bank.GetValueOrDefault(input.ItemKey);

        if (bankCount <= 0)
            throw new InvalidOperationException("That item is no longer present in the PKVault Item Bank.");

        var requested = (int)Math.Min(Math.Min(bankCount, int.MaxValue), input.Count);
        var others = await staticDataService.GetStaticOthers();
        var map = GetVersionMap(others, save.Version);
        var targetPair = map.FirstOrDefault(kv => string.Equals(kv.Value, input.ItemKey, StringComparison.Ordinal));

        if (targetPair.Key <= 0)
            throw new InvalidOperationException($"{GetItemName(others, input.ItemKey)} does not exist in {save.Version}.");

        var targetItemId = (ushort)targetPair.Key;
        var candidatePouches = bag.Pouches
            .Where(p => IsBankablePouch(p.Type) && p.CanContain(targetItemId))
            .OrderBy(p => p.Type == InventoryType.PCItems ? 1 : 0)
            .ToList();

        if (candidatePouches.Count == 0)
            throw new InvalidOperationException($"{GetItemName(others, input.ItemKey)} has no compatible pocket in {save.Version}.");

        var remaining = requested;
        var moved = 0;

        foreach (var pouch in candidatePouches)
        {
            if (remaining <= 0)
                break;

            var existing = pouch.Items.FirstOrDefault(x => x.Index == targetItemId);
            var before = existing?.Count ?? 0;

            if (existing is null && pouch.FindIndexFirstEmptySlot() < 0)
                continue;

            pouch.GiveItem(bag, targetItemId, remaining);

            var after = pouch.Items.FirstOrDefault(x => x.Index == targetItemId)?.Count ?? before;
            var added = Math.Max(0, after - before);
            moved += added;
            remaining -= added;
        }

        if (moved <= 0)
            throw new InvalidOperationException($"No room for {GetItemName(others, input.ItemKey)} in {save.Version}; the bank stack was left unchanged.");

        bag.CopyTo(save.GetSave());
        loaders.Pkms.HasWritten = true;

        var left = bankCount - moved;
        if (left <= 0)
            bank.Remove(input.ItemKey);
        else
            bank[input.ItemKey] = left;

        await SaveBank(bank);

        return new(
            GetItemName(others, input.ItemKey),
            moved,
            null,
            save.Version
        );
    }

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

    private async Task<Dictionary<string, long>> LoadBank()
    {
        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK);
        var result = new Dictionary<string, long>(StringComparer.Ordinal);

        if (entity is null || string.IsNullOrWhiteSpace(entity.Value))
            return result;

        foreach (var line in entity.Value.Split('\n', StringSplitOptions.RemoveEmptyEntries))
        {
            var parts = line.Split('\t');
            if (parts.Length == 2 && long.TryParse(parts[1], out var count) && count > 0)
                result[parts[0]] = count;
        }

        return result;
    }

    private async Task SaveBank(Dictionary<string, long> bank)
    {
        var value = string.Join('\n', bank
            .Where(kv => kv.Value > 0)
            .OrderBy(kv => kv.Key, StringComparer.Ordinal)
            .Select(kv => $"{kv.Key}\t{kv.Value}"));

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
}
''')

put("PKVault.Core/storage/data-action/MoveInventoryItemAction.cs", r'''namespace PKVault.Core;

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

meta_entity = PKVAULT / "PKVault.Core/db/entity/MetaEntity.cs"
replace_once(meta_entity,
'''public enum MetaKey
{
    APP_VERSION,
    USER_ID
}
''',
'''public enum MetaKey
{
    APP_VERSION,
    USER_ID,
    ITEM_BANK,
}
''')

program = PKVAULT / "PKVault.Core/Program.cs"
replace_once(program,
'''        services.AddSingleton<TradingService>();

        Log.Information($"Setup services - Actions");
''',
'''        services.AddSingleton<TradingService>();
        services.AddScoped<ItemBankService>();

        Log.Information($"Setup services - Actions");
''')
replace_once(program,
'''        services.AddScoped<TradeSwapAction>();

        Log.Information($"Setup services - Loaders");
''',
'''        services.AddScoped<TradeSwapAction>();
        services.AddScoped<MoveInventoryItemAction>();

        Log.Information($"Setup services - Loaders");
''')

data_action = PKVAULT / "PKVault.Core/storage/data-action/DataAction.cs"
replace_once(data_action,
'''    UPDATE_EXTERNAL_PKM,
    SET_PKM_VERSION_MAIN,
}
''',
'''    UPDATE_EXTERNAL_PKM,
    SET_PKM_VERSION_MAIN,
    MOVE_ITEM,
}
''')

action_service = PKVAULT / "PKVault.Core/storage/services/ActionService.cs"
replace_once(action_service,
'''    public async Task<DataUpdateFlags> Save()
    {
''',
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

    public async Task<DataUpdateFlags> Save()
    {
''')

storage_route = PKVAULT / "PKVault.Core/storage/routes/StorageRoute.cs"
replace_once(storage_route,
'''public class StorageController(DataService dataService, StorageQueryService storageQueryService, ActionService actionService, ISessionService sessionService)
{
''',
'''public class StorageController(
    DataService dataService,
    StorageQueryService storageQueryService,
    ActionService actionService,
    ISessionService sessionService,
    ItemBankService itemBankService
)
{
''')
replace_once(storage_route,
'''    [HttpGet("action")]
    public List<DataActionPayload> GetActions()
''',
'''    [HttpGet("inventory")]
    public async Task<ItemInventoryStateDTO> GetInventory()
    {
        return await itemBankService.GetState();
    }

    [HttpPut("inventory/move")]
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

    [HttpGet("action")]
    public List<DataActionPayload> GetActions()
''')

route_json = PKVAULT / "PKVault.Core/router/RouteJsonContext.cs"
replace_once(route_json,
'''[JsonSerializable(typeof(Dictionary<string, PkmLegalityDTO>))]
[JsonSerializable(typeof(EditPkmVariantPayload))]
''',
'''[JsonSerializable(typeof(Dictionary<string, PkmLegalityDTO>))]
[JsonSerializable(typeof(ItemInventoryStateDTO))]
[JsonSerializable(typeof(EditPkmVariantPayload))]
''')

swagger = PKVAULT / "PKVault.Core/swagger.json"
swagger_text = swagger.read_text(encoding="utf-8")
old_names = '''          "UPDATE_EXTERNAL_PKM",
          "SET_PKM_VERSION_MAIN"
'''
new_names = '''          "UPDATE_EXTERNAL_PKM",
          "SET_PKM_VERSION_MAIN",
          "MOVE_ITEM"
'''
if old_names not in swagger_text:
    raise RuntimeError("alpha24 swagger enum-name anchor missing")
swagger_text = swagger_text.replace(old_names, new_names, 1)
old_vals = '''          18,
          19
'''
new_vals = '''          18,
          19,
          20
'''
if old_vals not in swagger_text:
    raise RuntimeError("alpha24 swagger enum-value anchor missing")
swagger.write_text(swagger_text.replace(old_vals, new_vals, 1), encoding="utf-8")

put("frontend/src/pages/inventory.tsx", r'''import {
  Alert,
  Badge,
  Button,
  Card,
  Group,
  NumberInput,
  ScrollArea,
  Select,
  Stack,
  Table,
  Text,
  Title,
} from '@mantine/core';
import { PackageOpenIcon, ShieldAlertIcon } from 'lucide-react';
import React from 'react';
import { customInstance } from '../data/mutator/custom-instance';
import type { GameVersion } from '../data/sdk/model';
import { useStaticData } from '../hooks/use-static-data';
import { withErrorCatcher } from '../ui/error-boundary/error-boundary';

type InventoryType =
  | 'None' | 'Items' | 'KeyItems' | 'TMHMs' | 'Medicine' | 'Berries'
  | 'Balls' | 'BattleItems' | 'MailItems' | 'PCItems' | 'FreeSpace'
  | 'ZCrystals' | 'Candy' | 'Treasure' | 'Ingredients' | 'MegaStones';

type BankEntry = { itemKey: string; name: string; count: number };
type SaveItem = {
  itemKey: string;
  name: string;
  itemId: number;
  count: number;
  pouch: InventoryType;
  maxCount: number;
};
type SaveInventory = {
  saveId: number;
  version: GameVersion;
  trainerName: string;
  supported: boolean;
  items: SaveItem[];
};
type InventoryState = { bank: BankEntry[]; saves: SaveInventory[] };

const loadInventory = async () =>
  (await customInstance<{ data: InventoryState; status: number; headers: Headers }>(
    '/api/storage/inventory',
  )).data;

const moveInventory = async (params: URLSearchParams) =>
  (await customInstance<{ data: InventoryState; status: number; headers: Headers }>(
    '/api/storage/inventory/move?' + params.toString(),
    { method: 'PUT' },
  )).data;

export const InventoryPage: React.FC = withErrorCatcher('default', () => {
  const staticData = useStaticData();
  const [state, setState] = React.useState<InventoryState>();
  const [saveId, setSaveId] = React.useState<string | null>(null);
  const [busy, setBusy] = React.useState<string | null>(null);
  const [amounts, setAmounts] = React.useState<Record<string, number>>({});

  const reload = React.useCallback(async () => {
    const next = await loadInventory();
    setState(next);
    setSaveId(current => current ?? (next.saves[0] ? String(next.saves[0].saveId) : null));
  }, []);

  React.useEffect(() => {
    void reload();
  }, [reload]);

  const selected = state?.saves.find(s => String(s.saveId) === saveId);
  const saveOptions = (state?.saves ?? []).map(s => ({
    value: String(s.saveId),
    label: (staticData.versions[s.version]?.name ?? String(s.version)) + ' — ' + (s.trainerName || 'Trainer'),
  }));

  const doMove = async (key: string, params: URLSearchParams) => {
    setBusy(key);
    try {
      setState(await moveInventory(params));
    } finally {
      setBusy(null);
    }
  };

  const amountFor = (key: string, max: number) =>
    Math.max(1, Math.min(max, amounts[key] ?? max));

  return <Stack p='md' gap='md'>
    <Group justify='space-between' align='end'>
      <div>
        <Title order={2}>Inventory</Title>
        <Text c='dimmed'>Move real save-file item stacks through the PKVault Item Bank.</Text>
      </div>
      <Select
        label='Game save'
        data={saveOptions}
        value={saveId}
        onChange={setSaveId}
        w={320}
        searchable
      />
    </Group>

    <Alert icon={<ShieldAlertIcon />} color='yellow' title='Protected pockets'>
      Key Items, TMs/HMs, and Z-Crystals are intentionally excluded in alpha24.
      PKVault will not move story-critical inventory between games.
    </Alert>

    <Group align='stretch' grow wrap='nowrap'>
      <Card withBorder style={{ minWidth: 0, flex: 1 }}>
        <Group justify='space-between' mb='sm'>
          <Group gap='xs'>
            <PackageOpenIcon />
            <Title order={3}>PKVault Item Bank</Title>
          </Group>
          <Badge variant='light'>{state?.bank.length ?? 0} item types</Badge>
        </Group>
        <Text size='sm' c='dimmed' mb='md'>
          Bank quantities are not limited by a game's bag stack cap.
        </Text>

        <ScrollArea h='60vh'>
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Item</Table.Th>
                <Table.Th>Bank</Table.Th>
                <Table.Th>Amount</Table.Th>
                <Table.Th />
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {(state?.bank ?? []).map(item => {
                const rowKey = 'bank:' + item.itemKey;
                const amount = amountFor(rowKey, item.count);
                return <Table.Tr key={item.itemKey}>
                  <Table.Td>{item.name}</Table.Td>
                  <Table.Td><Badge variant='outline'>×{item.count}</Badge></Table.Td>
                  <Table.Td>
                    <NumberInput
                      min={1}
                      max={item.count}
                      value={amount}
                      onChange={v => setAmounts(a => ({ ...a, [rowKey]: Number(v) || 1 }))}
                      w={95}
                    />
                  </Table.Td>
                  <Table.Td>
                    <Button
                      size='xs'
                      disabled={!selected?.supported}
                      loading={busy === rowKey}
                      onClick={() => {
                        if (!selected) return;
                        const p = new URLSearchParams({
                          targetSaveId: String(selected.saveId),
                          itemKey: item.itemKey,
                          count: String(amount),
                        });
                        void doMove(rowKey, p);
                      }}
                    >
                      Deposit
                    </Button>
                  </Table.Td>
                </Table.Tr>;
              })}
            </Table.Tbody>
          </Table>
        </ScrollArea>
      </Card>

      <Card withBorder style={{ minWidth: 0, flex: 1 }}>
        <Group justify='space-between' mb='sm'>
          <Title order={3}>
            {selected
              ? (staticData.versions[selected.version]?.name ?? String(selected.version)) + ' Bag'
              : 'Save Bag'}
          </Title>
          {selected && <Badge variant='light'>{selected.items.length} stacks</Badge>}
        </Group>

        {selected && !selected.supported
          ? <Alert color='orange'>
              This save format does not currently expose a writable PKHeX inventory.
            </Alert>
          : <ScrollArea h='60vh'>
              <Table striped highlightOnHover>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Item</Table.Th>
                    <Table.Th>Pocket</Table.Th>
                    <Table.Th>Save</Table.Th>
                    <Table.Th>Amount</Table.Th>
                    <Table.Th />
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {(selected?.items ?? []).map((item, index) => {
                    const rowKey = 'save:' + String(selected?.saveId) + ':' + item.pouch + ':' + item.itemId + ':' + index;
                    const amount = amountFor(rowKey, item.count);
                    return <Table.Tr key={rowKey}>
                      <Table.Td>{item.name}</Table.Td>
                      <Table.Td><Badge variant='light'>{item.pouch}</Badge></Table.Td>
                      <Table.Td>×{item.count}</Table.Td>
                      <Table.Td>
                        <NumberInput
                          min={1}
                          max={item.count}
                          value={amount}
                          onChange={v => setAmounts(a => ({ ...a, [rowKey]: Number(v) || 1 }))}
                          w={95}
                        />
                      </Table.Td>
                      <Table.Td>
                        <Button
                          size='xs'
                          variant='light'
                          loading={busy === rowKey}
                          onClick={() => {
                            if (!selected) return;
                            const p = new URLSearchParams({
                              sourceSaveId: String(selected.saveId),
                              itemKey: item.itemKey,
                              sourceItemId: String(item.itemId),
                              sourcePouch: item.pouch,
                              count: String(amount),
                            });
                            void doMove(rowKey, p);
                          }}
                        >
                          Withdraw
                        </Button>
                      </Table.Td>
                    </Table.Tr>;
                  })}
                </Table.Tbody>
              </Table>
            </ScrollArea>}
      </Card>
    </Group>
  </Stack>;
});
''')

put("frontend/src/routes/inventory.tsx", r'''import { createFileRoute } from '@tanstack/react-router';
import { InventoryPage } from '../pages/inventory';

export const Route = createFileRoute('/inventory')({
  component: InventoryPage,
});
''')

header = PKVAULT / "frontend/src/header/header.tsx"
replace_once(header,
'''            <UIHeaderItem
                id={'pokedex' satisfies HeaderValue}
                to={"/pokedex"}
''',
'''            <UIHeaderItem
                id={'inventory' satisfies HeaderValue}
                to={"/inventory"}
                selected={value === 'inventory'}
                label='Inventory'
            >
                Inventory
            </UIHeaderItem>

            <UIHeaderItem
                id={'pokedex' satisfies HeaderValue}
                to={"/pokedex"}
''')
replace_once(header,
'''            'saves': () => null,
            'settings': () => <SettingsSubMenu />,
''',
'''            'saves': () => null,
            'inventory': () => null,
            'settings': () => <SettingsSubMenu />,
''')

action_label = PKVAULT / "frontend/src/storage/actions/action-label.tsx"
replace_once(action_label,
'''import { BoxIcon, CalendarSyncIcon, ChevronsRight, CircleSmallIcon, Database, ImportIcon, LandmarkIcon, LinkIcon, MoveIcon, PenIcon, PlusCircleIcon, RefreshCcw, SortDescIcon, TrashIcon, UnlinkIcon } from 'lucide-react';
''',
'''import { BoxIcon, CalendarSyncIcon, ChevronsRight, CircleSmallIcon, Database, ImportIcon, LandmarkIcon, LinkIcon, MoveIcon, PackageOpenIcon, PenIcon, PlusCircleIcon, RefreshCcw, SortDescIcon, TrashIcon, UnlinkIcon } from 'lucide-react';
''')
replace_once(action_label,
'''    UpdateExternal: () => {
        return <>
            <UIBallIcon />

            <ThemeIcon variant='transparent' color='primary' size='xs' fz='sm'>
                <ImportIcon />
            </ThemeIcon>
        </>;
    },
};
''',
'''    UpdateExternal: () => {
        return <>
            <UIBallIcon />

            <ThemeIcon variant='transparent' color='primary' size='xs' fz='sm'>
                <ImportIcon />
            </ThemeIcon>
        </>;
    },
    MoveItem: () => {
        return <>
            <PackageOpenIcon />
            <ThemeIcon variant='transparent' color='gray' size='xs' fz='sm'>
                <MoveIcon />
            </ThemeIcon>
        </>;
    },
};
''')
replace_once(action_label,
'''        [ DataActionType.UPDATE_EXTERNAL_PKM ]: ActionLabelMap.UpdateExternal,
    });
''',
'''        [ DataActionType.UPDATE_EXTERNAL_PKM ]: ActionLabelMap.UpdateExternal,
        [ DataActionType.MOVE_ITEM ]: ActionLabelMap.MoveItem,
    });
''')

action_desc = PKVAULT / "frontend/src/storage/actions/hooks/use-action-description.ts"
replace_once(action_desc,
'''            [ DataActionType.UPDATE_EXTERNAL_PKM ]: () =>
                t('storage.save-actions.type.update-external-pkm', {
                    addCount: Number(parameters[ 0 ]),
                    removeCount: Number(parameters[ 1 ]),
                }),
''',
'''            [ DataActionType.UPDATE_EXTERNAL_PKM ]: () =>
                t('storage.save-actions.type.update-external-pkm', {
                    addCount: Number(parameters[ 0 ]),
                    removeCount: Number(parameters[ 1 ]),
                }),
            [ DataActionType.MOVE_ITEM ]: () => {
                const source = typeof parameters[ 1 ] === 'number'
                    ? staticData.versions[ parameters[ 1 ] ]?.name
                    : 'PKVault Item Bank';
                const target = typeof parameters[ 2 ] === 'number'
                    ? staticData.versions[ parameters[ 2 ] ]?.name
                    : 'PKVault Item Bank';
                return 'Move ×' + parameters[ 3 ] + ' ' + parameters[ 0 ] + ' from ' + source + ' to ' + target;
            },
''')

action_color = PKVAULT / "frontend/src/ui/actions-panel/utils/get-action-color.ts"
replace_once(action_color,
'''        case DataActionType.MOVE_PKM:
            return 'gray';
''',
'''        case DataActionType.MOVE_PKM:
        case DataActionType.MOVE_ITEM:
            return 'gray';
''')

print("PKVault V8 alpha24 cross-save inventory bank applied")

from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52m2 anchor not found: {label}")
    return text.replace(old, new, 1)

meta_path = root / "PKVault.Core/db/entity/MetaEntity.cs"
meta = meta_path.read_text(encoding="utf-8")
meta = rep(meta,
"""    ITEM_BANK_PAGE_SIZES,
    ITEM_SAVE_PROVENANCE,
""",
"""    ITEM_BANK_PAGE_SIZES,
    ITEM_BANK_PAGE_NAMES,
    ITEM_SAVE_PROVENANCE,
""",
"page names meta key")
meta_path.write_text(meta, encoding="utf-8")

item_path = root / "PKVault.Core/storage/services/ItemBankService.cs"
item = item_path.read_text(encoding="utf-8")

item = rep(item,
"""public record InventoryBankPageDTO(
    int Page,
    int SlotCount,
    List<InventorySlotDTO> Slots
);
""",
"""public record InventoryBankPageDTO(
    int Page,
    string Name,
    int SlotCount,
    List<InventorySlotDTO> Slots
);
""",
"bank page name DTO")

item = rep(item,
"""[JsonSerializable(typeof(Dictionary<int, int>))]
internal partial class ItemBankJsonContext : JsonSerializerContext
""",
"""[JsonSerializable(typeof(Dictionary<int, int>))]
[JsonSerializable(typeof(Dictionary<int, string>))]
internal partial class ItemBankJsonContext : JsonSerializerContext
""",
"page name JSON context")

item = rep(item,
"""        var pageCount = await GetPageCount(bank);
        var pageSizes = await LoadPageSizes();

        var bankPages = Enumerable.Range(1, pageCount)
""",
"""        var pageCount = await GetPageCount(bank);
        var pageSizes = await LoadPageSizes();
        var pageNames = await LoadPageNames();

        var bankPages = Enumerable.Range(1, pageCount)
""",
"load page names")

item = rep(item,
"""                return new InventoryBankPageDTO(
                    Page: page,
                    SlotCount: slotCount,
""",
"""                return new InventoryBankPageDTO(
                    Page: page,
                    Name: pageNames.GetValueOrDefault(page, $"Box {page}"),
                    SlotCount: slotCount,
""",
"page name DTO output")

item = rep(item,
"""    public async Task UpdatePageSize(int page, int slotCount)
    {
""",
"""    public async Task UpdatePage(int page, string name, int slotCount)
    {
        await UpdatePageName(page, name);
        await UpdatePageSize(page, slotCount);
    }

    public async Task UpdatePageName(int page, string name)
    {
        var bank = await LoadBankState();
        var pageCount = await GetPageCount(bank);

        if (page <= 0 || page > pageCount)
            throw new ArgumentOutOfRangeException(nameof(page));

        name = (name ?? string.Empty).Trim();
        if (name.Length > 40)
            throw new ArgumentException("Item box names can be at most 40 characters.", nameof(name));

        var names = await LoadPageNames();
        var defaultName = $"Box {page}";
        if (string.IsNullOrWhiteSpace(name)
            || string.Equals(name, defaultName, StringComparison.Ordinal))
        {
            names.Remove(page);
        }
        else
        {
            names[page] = name;
        }

        await SavePageNames(names);
    }

    public async Task UpdatePageSize(int page, int slotCount)
    {
""",
"page edit method")

anchor = """    private static int GetPageSlotCount(
        int page,
        Dictionary<string, BankStack> bank,
        Dictionary<int, int> pageSizes
    )
"""
insert = """    private async Task<Dictionary<int, string>> LoadPageNames()
    {
        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK_PAGE_NAMES);
        if (entity is null || string.IsNullOrWhiteSpace(entity.Value))
            return [];

        try
        {
            return JsonSerializer.Deserialize<Dictionary<int, string>>(
                entity.Value,
                JsonOptions
            ) ?? [];
        }
        catch (JsonException)
        {
            return [];
        }
    }

    private async Task SavePageNames(Dictionary<int, string> pageNames)
    {
        var value = JsonSerializer.Serialize(
            pageNames
                .Where(x => x.Key > 0 && !string.IsNullOrWhiteSpace(x.Value))
                .ToDictionary(
                    x => x.Key,
                    x => x.Value.Trim()[..Math.Min(40, x.Value.Trim().Length)]
                ),
            JsonOptions
        );

        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK_PAGE_NAMES);
        if (entity is null)
        {
            await metaLoader.AddEntity(new()
            {
                Key = MetaKey.ITEM_BANK_PAGE_NAMES,
                Value = value,
            });
        }
        else
        {
            entity.Value = value;
            await metaLoader.UpdateEntity(entity);
        }
    }

""" + anchor
item = rep(item, anchor, insert, "page names storage helpers")
item_path.write_text(item, encoding="utf-8")

route_path = root / "PKVault.Core/storage/routes/StorageRoute.cs"
route = route_path.read_text(encoding="utf-8")
route = rep(route,
"""    [HttpPut("inventory/page/size")]
    public async Task<ItemInventoryStateDTO> ResizeInventoryPage(
        int page,
        int slotCount
    )
    {
        await itemBankService.UpdatePageSize(page, slotCount);
        return await itemBankService.GetState();
    }
""",
"""    [HttpPut("inventory/page")]
    public async Task<ItemInventoryStateDTO> EditInventoryPage(
        int page,
        string name,
        int slotCount
    )
    {
        await itemBankService.UpdatePage(page, name, slotCount);
        return await itemBankService.GetState();
    }

    [HttpPut("inventory/page/size")]
    public async Task<ItemInventoryStateDTO> ResizeInventoryPage(
        int page,
        int slotCount
    )
    {
        await itemBankService.UpdatePageSize(page, slotCount);
        return await itemBankService.GetState();
    }
""",
"inventory page edit route")
route_path.write_text(route, encoding="utf-8")

types_path = root / "frontend/src/inventory/types.ts"
types = types_path.read_text(encoding="utf-8")
types = rep(types,
"""export type InventoryBankPage = {
    page: number;
    slotCount: number;
""",
"""export type InventoryBankPage = {
    page: number;
    name: string;
    slotCount: number;
""",
"frontend bank page name")
types_path.write_text(types, encoding="utf-8")

api_path = root / "frontend/src/inventory/inventory-api.ts"
api = api_path.read_text(encoding="utf-8")
api = rep(api,
"""export const resizeInventoryPage = async (page: number, slotCount: number) => {
""",
"""export const editInventoryPage = async (page: number, name: string, slotCount: number) => {
    const p = new URLSearchParams({
        page: String(page),
        name,
        slotCount: String(slotCount),
    });

    return (await customInstance<{ data: InventoryState; status: number; headers: Headers }>(
        '/api/storage/inventory/page?' + p.toString(),
        { method: 'PUT' }
    )).data;
};

export const resizeInventoryPage = async (page: number, slotCount: number) => {
""",
"edit inventory page API")
api_path.write_text(api, encoding="utf-8")

edit_path = root / "frontend/src/inventory/inventory-page-edit.tsx"
edit = edit_path.read_text(encoding="utf-8")
edit = edit.replace("import { NumberInput, Text } from '@mantine/core';", "import { NumberInput, Text, TextInput } from '@mantine/core';")
edit = rep(edit,
"""type InventoryPageEditProps = {
    page: number;
    slotCount: number;
    minSlotCount: number;
    onSubmit: (slotCount: number) => Promise<void>;
};
""",
"""type InventoryPageEditProps = {
    page: number;
    name: string;
    slotCount: number;
    minSlotCount: number;
    onSubmit: (name: string, slotCount: number) => Promise<void>;
};
""",
"edit props")
edit = rep(edit,
"""    page,
    slotCount,
    minSlotCount,
    onSubmit: onSubmitRaw,
}) => {
    const popover = usePopover();
    const [ value, setValue ] = React.useState(slotCount);

    const valid = Number.isFinite(value)
        && value >= minSlotCount
        && value <= 300;
""",
"""    page,
    name,
    slotCount,
    minSlotCount,
    onSubmit: onSubmitRaw,
}) => {
    const popover = usePopover();
    const [ value, setValue ] = React.useState(slotCount);
    const [ nameValue, setNameValue ] = React.useState(name);

    const cleanName = nameValue.trim();
    const valid = Number.isFinite(value)
        && value >= minSlotCount
        && value <= 300
        && cleanName.length <= 40;
    const changed = value !== slotCount || cleanName !== name;
""",
"edit local state")
edit = rep(edit,
"""        disabled={!valid || value === slotCount}
""",
"""        disabled={!valid || !changed}
""",
"edit changed state")
edit = rep(edit,
"""            await onSubmitRaw(value);
""",
"""            await onSubmitRaw(cleanName || ('Box ' + page), value);
""",
"edit submit")
edit = rep(edit,
"""    >
        <NumberInput
""",
"""    >
        <TextInput
            label='Box name'
            description='Up to 40 characters'
            value={nameValue}
            maxLength={40}
            onChange={event => setNameValue(event.currentTarget.value)}
        />

        <NumberInput
""",
"box name input")
edit_path.write_text(edit, encoding="utf-8")

panel_path = root / "frontend/src/inventory/inventory-panel.tsx"
panel = panel_path.read_text(encoding="utf-8")
panel = rep(panel,
"""    onCreatePage: () => Promise<number>;
    onResizePage: (page: number, slotCount: number) => Promise<void>;
    onError: (message: string) => void;
};
""",
"""    onCreatePage: () => Promise<number>;
    onEditPage: (page: number, name: string, slotCount: number) => Promise<void>;
    onError: (message: string) => void;
};
""",
"panel edit prop")
panel = rep(panel,
"""    state, initial, onSplit, onTrash, onCreatePage, onResizePage, onError
""",
"""    state, initial, onSplit, onTrash, onCreatePage, onEditPage, onError
""",
"panel destructure")
panel = rep(panel,
"""            label: 'Box ' + p.page,
""",
"""            label: p.name,
""",
"page tab label")
panel = rep(panel,
"""                        page={itemPage.page}
                        slotCount={itemPage.slotCount}
                        minSlotCount={minSlotCount}
                        onSubmit={slotCount => onResizePage(itemPage.page, slotCount)}
""",
"""                        page={itemPage.page}
                        name={itemPage.name}
                        slotCount={itemPage.slotCount}
                        minSlotCount={minSlotCount}
                        onSubmit={(name, slotCount) => onEditPage(itemPage.page, name, slotCount)}
""",
"page edit wiring")
panel_path.write_text(panel, encoding="utf-8")

page_path = root / "frontend/src/inventory/inventory-page.tsx"
page = page_path.read_text(encoding="utf-8")
page = page.replace(
    "import { createInventoryPage, loadInventory, moveInventory, moveMoney, resizeInventoryPage, trashInventory } from './inventory-api';",
    "import { createInventoryPage, editInventoryPage, loadInventory, moveInventory, moveMoney, trashInventory } from './inventory-api';"
)
page = rep(page,
"""    const onResizePage = React.useCallback(async (page: number, slotCount: number) => {
        try {
            const next = await resizeInventoryPage(page, slotCount);
""",
"""    const onEditPage = React.useCallback(async (page: number, name: string, slotCount: number) => {
        try {
            const next = await editInventoryPage(page, name, slotCount);
""",
"page edit callback")
page = page.replace("onResizePage={onResizePage}", "onEditPage={onEditPage}")
page_path.write_text(page, encoding="utf-8")

print("PKVault V8 alpha52m2 item-bank box renaming applied")

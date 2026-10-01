from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(path: str, old: str, new: str, label: str):
    p = root / path
    text = p.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            print(f"ALREADY {path}: {label}")
            return
        raise RuntimeError(f"alpha53l anchor not found: {label} in {path}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"PATCHED {path}: {label}")

def insert_before(path: str, marker: str, insertion: str, label: str):
    p = root / path
    text = p.read_text(encoding="utf-8")
    if insertion in text:
        print(f"ALREADY {path}: {label}")
        return
    if marker not in text:
        raise RuntimeError(f"alpha53l marker not found: {label} in {path}")
    p.write_text(text.replace(marker, insertion + marker, 1), encoding="utf-8")
    print(f"PATCHED {path}: {label}")

# ===========================================================================
# Settings: dedicated Trade Box + optional header buttons.
# All new fields have defaults so every existing settings.json upgrades with
# the three buttons visible and no dedicated Trade Box selected.
# ===========================================================================
rep(
    "PKVault.Core/settings/dto/SettingsDTO.cs",
    '''    string LANGUAGE = "en",
    string? TRADER_NAME = null
);
''',
    '''    string LANGUAGE = "en",
    string? TRADER_NAME = null,
    string? TRADE_BOX_ID = null,
    bool SHOW_INVENTORY = true,
    bool SHOW_SHOP = true,
    bool SHOW_QUESTS = true
);
''',
    "settings fields",
)

header = "frontend/src/header/header.tsx"
for name, field in [
    ("inventory", "shoW_INVENTORY"),
    ("shop", "shoW_SHOP"),
    ("quests", "shoW_QUESTS"),
]:
    block = f'''            <UIHeaderItem
                id={{'{name}' satisfies HeaderValue}}
                to={{"/{name}"}}
                selected={{value === '{name}'}}
                label='{name.title()}'
            >
                {name.title()}
            </UIHeaderItem>
'''
    wrapped = f'''            {{settings?.settingsMutable.{field} !== false && <UIHeaderItem
                id={{'{name}' satisfies HeaderValue}}
                to={{"/{name}"}}
                selected={{value === '{name}'}}
                label='{name.title()}'
            >
                {name.title()}
            </UIHeaderItem>}}
'''
    rep(header, block, wrapped, f"{name} header visibility")

main = "frontend/src/settings/main/settings-main-left.tsx"
rep(
    main,
    "import { FileIcon, FolderIcon, GlobeIcon, PenOffIcon, ShieldOff } from 'lucide-react';",
    "import { FileIcon, FolderIcon, GlobeIcon, ListChecksIcon, PackageIcon, PenOffIcon, ShieldOff, ShoppingBagIcon } from 'lucide-react';",
    "settings visibility icons",
)
rep(
    main,
    '''        </Card>
    </>;
};
''',
    '''        </Card>

        <Card>
            <SimpleGrid cols={2}>
                <UIInputLabel
                    leftSection={<PackageIcon />}
                    forInput='shoW_INVENTORY'
                    label='Show Inventory button'
                    description='Show the Inventory button in the main PKVault header.'
                />
                <UISwitch
                    {...form.register('shoW_INVENTORY')}
                    defaultChecked={form.getValues('shoW_INVENTORY') !== false}
                    controlLabel='Show Inventory button'
                    ml='auto'
                    my='sm'
                />

                <UIInputLabel
                    leftSection={<ShoppingBagIcon />}
                    forInput='shoW_SHOP'
                    label='Show Shop button'
                    description='Show the Shop button in the main PKVault header.'
                />
                <UISwitch
                    {...form.register('shoW_SHOP')}
                    defaultChecked={form.getValues('shoW_SHOP') !== false}
                    controlLabel='Show Shop button'
                    ml='auto'
                    my='sm'
                />

                <UIInputLabel
                    leftSection={<ListChecksIcon />}
                    forInput='shoW_QUESTS'
                    label='Show Quests button'
                    description='Show the Quests button in the main PKVault header.'
                />
                <UISwitch
                    {...form.register('shoW_QUESTS')}
                    defaultChecked={form.getValues('shoW_QUESTS') !== false}
                    controlLabel='Show Quests button'
                    ml='auto'
                    my='sm'
                />
            </SimpleGrid>
        </Card>
    </>;
};
''',
    "header visibility settings UI",
)

# ===========================================================================
# SQLite session lifecycle: stop renaming/deleting the one fixed live database.
#
# Every logical editing session gets a unique SQLite file. Save uses SQLite's
# online backup API to copy a consistent snapshot into pkvault.db. Existing
# request-scoped DbContexts can finish against the retired session file without
# holding the next session hostage. Retired files are cleanup-only; a cleanup
# failure is never allowed to fail Save.
# ===========================================================================
session = "PKVault.Core/db/services/SessionService.cs"
rep(
    session,
    '''    public string SessionDbPath => Path.Combine(DbFolderPath, "pkvault-session.db");
''',
    '''    private string? CurrentSessionDbPath;
    public string SessionDbPath => CurrentSessionDbPath ??= NewSessionDbPath();

    private string NewSessionDbPath()
        => Path.Combine(DbFolderPath, $"pkvault-session-{Guid.NewGuid():N}.db");
''',
    "unique session database path",
)
rep(
    session,
    '''    public async Task StartNewSession(bool checkInitialActions, DataUpdateFlags? flags)
    {
        StartTime = timeProvider.GetUtcNow().DateTime;
''',
    '''    public async Task StartNewSession(bool checkInitialActions, DataUpdateFlags? flags)
    {
        // Rotate before any loader/DbContext is created for this logical session.
        // Older request-scoped contexts keep their old filename and can drain
        // harmlessly instead of blocking deletion/rename of the next session.
        CurrentSessionDbPath = NewSessionDbPath();
        StartTime = timeProvider.GetUtcNow().DateTime;
''',
    "rotate session path",
)
rep(
    session,
    '''            await Task.WhenAll(
                ResetDbSession(flags),
                savesLoadersService.Setup(flags)
            );
''',
    '''            // A GUID session database starts empty. Complete its SQLite
            // copy/migrations before any save loader is allowed to query it.
            // Running these concurrently can race on first open and produce
            // "no such table" errors such as PkmVersions.
            await ResetDbSession(flags);
            await savesLoadersService.Setup(flags);
''',
    "migrate unique session before save loaders",
)
rep(
    session,
    '''        await SessionFileTransitionLock.WaitAsync();
        try
        {
            await CloseConnection();
            StartTask = null;

            Log.Logger.Debug($"Move session DB to main");
            await RetryFileOperation(
                "move session DB to main",
                () =>
                {
                    fileIOService.Move(SessionDbPath, MainDbPath, overwrite: true);
                    return true;
                }
            );

            StartTime = null;
        }
        finally
        {
            SessionFileTransitionLock.Release();
        }
''',
    '''        var retiredSessionPath = SessionDbPath;

        await SessionFileTransitionLock.WaitAsync();
        try
        {
            await CloseConnection();

            Log.Logger.Debug($"Backup session DB to main");
            await BackupDatabase(
                retiredSessionPath,
                MainDbPath,
                "backup session DB to main"
            );

            StartTask = null;
            StartTime = null;
        }
        finally
        {
            SessionFileTransitionLock.Release();
        }

        // Do not delete the retired GUID database in-process. A scoped loader
        // created before Save can still legitimately open its captured database
        // path after PersistSession returns. Deleting that path is especially
        // dangerous on Unix, where deletion succeeds and the late open creates
        // a brand-new empty SQLite file ("no such table"). GUID session files
        // are therefore retirement snapshots, not files Save must remove.
''',
    "save session with SQLite backup",
)
# Replace alpha53e's fixed-file reset body.
start_marker = '''    private async Task ResetDbSession(DataUpdateFlags flags)
    {
        await SessionFileTransitionLock.WaitAsync();
        try
        {
            if (fileIOService.Exists(SessionDbPath))
            {
                bool deleted1;
'''
end_marker = '''        flags.Warnings = true;
    }

    private async Task RunDbMigrations()
'''
sp = root / session
st = sp.read_text(encoding="utf-8")
i = st.find(start_marker)
j = st.find(end_marker)
if i < 0 or j < 0 or j <= i:
    raise RuntimeError("alpha53l ResetDbSession block anchors missing")
new_reset = '''    private async Task ResetDbSession(DataUpdateFlags flags)
    {
        await SessionFileTransitionLock.WaitAsync();
        try
        {
            var newSessionPath = SessionDbPath;

            // New sessions are unique, so creating one never depends on deleting
            // the previous session database. Copy through SQLite itself so WAL
            // state is included in a consistent snapshot.
            if (fileIOService.Exists(MainDbPath))
            {
                await BackupDatabase(
                    MainDbPath,
                    newSessionPath,
                    "backup main DB to new session"
                );

                Log.Logger.Debug($"DB main backed up to unique session {newSessionPath}");
            }

            await RunDbMigrations();

            // A pre-alpha53l fixed session file may remain after a crash. Its
            // cleanup is optional and cannot block startup.
            TryDeleteRetiredSessionDatabase(Path.Combine(DbFolderPath, "pkvault-session.db"));
        }
        finally
        {
            SessionFileTransitionLock.Release();
        }

        flags.MainBanks.All = true;
        flags.MainBoxes.All = true;
        flags.MainPkmVariants.All = true;
        flags.Dex.All = true;
        flags.Warnings = true;
    }

    private async Task RunDbMigrations()
'''
st = st[:i] + new_reset + st[j + len('''        flags.Warnings = true;
    }

    private async Task RunDbMigrations()
'''):]
sp.write_text(st, encoding="utf-8")
print(f"PATCHED {session}: unique reset")

insert_before(
    session,
    '''    private async Task<T> RetryFileOperation<T>(string operationName, Func<T> operation)
''',
    '''    private async Task BackupDatabase(string sourcePath, string targetPath, string operationName)
    {
        fileIOService.CreateDirectoryIfAny(sourcePath);
        fileIOService.CreateDirectoryIfAny(targetPath);

        const int maxAttempts = 20;
        for (var attempt = 1; ; attempt++)
        {
            try
            {
                await using var source = new SqliteConnection(new SqliteConnectionStringBuilder
                {
                    DataSource = sourcePath,
                    Mode = SqliteOpenMode.ReadWrite,
                    Pooling = false,
                }.ToString());
                await using var target = new SqliteConnection(new SqliteConnectionStringBuilder
                {
                    DataSource = targetPath,
                    Mode = SqliteOpenMode.ReadWriteCreate,
                    Pooling = false,
                }.ToString());

                await source.OpenAsync();
                await target.OpenAsync();
                source.BackupDatabase(target);
                return;
            }
            catch (Exception ex) when (attempt < maxAttempts && IsTransientSqliteFileException(ex))
            {
                SqliteConnection.ClearAllPools();
                var delayMs = Math.Min(300, 25 * attempt);
                Log.Logger.Warning(
                    ex,
                    "SQLite backup '{Operation}' is temporarily busy; retry {Attempt}/{MaxAttempts} in {DelayMs} ms",
                    operationName,
                    attempt,
                    maxAttempts,
                    delayMs
                );
                await Task.Delay(delayMs);
            }
        }
    }

    private static bool IsTransientSqliteFileException(Exception ex)
        => ex is IOException
            || ex is SqliteException sqlite && sqlite.SqliteErrorCode is 5 or 6;

    private void TryDeleteRetiredSessionDatabase(string path)
    {
        foreach (var candidate in new[] { path, path + "-shm", path + "-wal" })
        {
            try
            {
                if (fileIOService.Exists(candidate))
                    fileIOService.Delete(candidate);
            }
            catch (Exception ex) when (ex is IOException or UnauthorizedAccessException)
            {
                Log.Logger.Debug(
                    ex,
                    "Retired session DB cleanup deferred for {Path}; it is still in use",
                    candidate
                );
            }
        }
    }

''',
    "SQLite backup and best-effort cleanup",
)

# ===========================================================================
# HG/SS Apricorn Box: PKHeX stores these seven values outside the normal bag
# pouches. Expose them as a virtual movable pocket backed by SAV4HGSS's exact
# Get/SetApricornCount methods. This also makes the existing Apricorn Rainbow
# achievement see the seven colors.
# ===========================================================================
item = "PKVault.Core/storage/services/ItemBankService.cs"
insert_before(
    item,
    '''    public async Task<ItemInventoryStateDTO> GetState()
''',
    '''    private const string HGSSApricornPouch = "ApricornBox";
    private const int HGSSApricornMaxCount = 99;

    // PKHeX's HG/SS save order is Red, Yellow, Blue, Green, Pink, White, Black.
    // Item IDs are not numerically ordered for Yellow/Blue, so keep this table
    // explicit rather than deriving an ID from the slot.
    private static readonly (int ItemId, string Key)[] HGSSApricornItems =
    [
        (485, "red-apricorn"),
        (487, "yellow-apricorn"),
        (486, "blue-apricorn"),
        (488, "green-apricorn"),
        (489, "pink-apricorn"),
        (490, "white-apricorn"),
        (491, "black-apricorn"),
    ];

    private static bool IsHGSSApricornPouch(string? pouch)
        => string.Equals(pouch, HGSSApricornPouch, StringComparison.Ordinal);

''',
    "HGSS Apricorn constants",
)
rep(
    item,
    '''            saves.Add(new(
                SaveId: save.Id,
''',
    '''            if (saveFile is SAV4HGSS hgss)
            {
                var apricornSlots = HGSSApricornItems
                    .Select((entry, slot) =>
                    {
                        var count = hgss.GetApricornCount(slot);
                        var origins = count > 0
                            ? GetEffectiveSaveOrigins(
                                saveProvenance,
                                save,
                                InventoryType.None,
                                entry.Key,
                                count
                            )
                            : [];

                        return new InventorySlotDTO(
                            Slot: slot,
                            ItemKey: entry.Key,
                            Name: GetItemName(others, entry.Key),
                            ItemId: entry.ItemId,
                            Count: count,
                            MaxCount: HGSSApricornMaxCount,
                            SpriteVersion: save.Version,
                            Movable: true,
                            StackId: SaveProvenanceKey(
                                save.Id,
                                InventoryType.None,
                                entry.Key
                            ),
                            Origins: origins
                        );
                    })
                    .ToList();

                pockets.Add(new(
                    Pouch: HGSSApricornPouch,
                    Label: "Apricorn Box",
                    SlotCount: HGSSApricornItems.Length,
                    Protected: false,
                    AcceptedItemKeys: HGSSApricornItems
                        .Select(x => x.Key)
                        .ToList(),
                    Slots: apricornSlots
                ));
            }

            saves.Add(new(
                SaveId: save.Id,
''',
    "HGSS Apricorn pocket in inventory state",
)
rep(
    item,
    '''            && string.Equals(input.SourcePouch, input.TargetPouch, StringComparison.Ordinal)
            && input.SourceSlot != input.TargetSlot)
''',
    '''            && string.Equals(input.SourcePouch, input.TargetPouch, StringComparison.Ordinal)
            && !IsHGSSApricornPouch(input.SourcePouch)
            && input.SourceSlot != input.TargetSlot)
''',
    "bypass normal same-pouch mover for Apricorn Box",
)
rep(
    item,
    '''        if (saveFile is EssentialsLegacySaveFile essentials)
            return ResolveEssentialsSource(input, save, loaders, essentials, others);

        var bag = saveFile.Inventory;
''',
    '''        if (saveFile is EssentialsLegacySaveFile essentials)
            return ResolveEssentialsSource(input, save, loaders, essentials, others);

        if (saveFile is SAV4HGSS hgss && IsHGSSApricornPouch(input.SourcePouch))
            return ResolveHGSSApricornSource(
                input,
                save,
                loaders,
                hgss,
                saveProvenance,
                others
            );

        var bag = saveFile.Inventory;
''',
    "resolve HGSS Apricorn source",
)
insert_before(
    item,
    '''    private ItemBankMoveResult MoveWithinSameSavePouch(
''',
    '''    private SourceStack ResolveHGSSApricornSource(
        MoveInventoryItemActionInput input,
        SaveWrapper save,
        SaveLoadersRecord loaders,
        SAV4HGSS hgss,
        Dictionary<string, List<ItemOriginDTO>> saveProvenance,
        StaticOthersData others
    )
    {
        if ((uint)input.SourceSlot >= HGSSApricornItems.Length)
            throw new ArgumentOutOfRangeException(nameof(input.SourceSlot));

        var entry = HGSSApricornItems[input.SourceSlot];
        var count = hgss.GetApricornCount(input.SourceSlot);
        if (count <= 0)
            throw new InvalidOperationException("The source Apricorn Box slot is empty.");

        var provenanceKey = SaveProvenanceKey(
            save.Id,
            InventoryType.None,
            entry.Key
        );
        var origins = GetEffectiveSaveOrigins(
            saveProvenance,
            save,
            InventoryType.None,
            entry.Key,
            count
        );

        return new(
            entry.Key,
            GetItemName(others, entry.Key),
            count,
            save.Version,
            save.Version,
            false,
            true,
            origins,
            moved =>
            {
                var left = Math.Max(0, count - moved);
                hgss.SetApricornCount(input.SourceSlot, left);

                if (left == 0)
                    saveProvenance.Remove(provenanceKey);
                else
                    saveProvenance[provenanceKey] = RemoveOrigins(origins, moved);

                loaders.Pkms.HasWritten = true;
            }
        );
    }

''',
    "HGSS Apricorn source helper",
)
rep(
    item,
    '''        if (saveFile is EssentialsLegacySaveFile essentials)
            return ApplyEssentialsTarget(input, source, requested, save, loaders, essentials, others);

        var bag = saveFile.Inventory;
''',
    '''        if (saveFile is EssentialsLegacySaveFile essentials)
            return ApplyEssentialsTarget(input, source, requested, save, loaders, essentials, others);

        if (saveFile is SAV4HGSS hgss && IsHGSSApricornPouch(input.TargetPouch))
            return ApplyHGSSApricornTarget(
                input,
                source,
                requested,
                save,
                loaders,
                hgss,
                saveProvenance,
                getMovedOrigins
            );

        var bag = saveFile.Inventory;
''',
    "apply HGSS Apricorn target",
)
insert_before(
    item,
    '''    private static Dictionary<int, string> GetVersionMap(
''',
    '''    private TargetResult ApplyHGSSApricornTarget(
        MoveInventoryItemActionInput input,
        SourceStack source,
        int requested,
        SaveWrapper save,
        SaveLoadersRecord loaders,
        SAV4HGSS hgss,
        Dictionary<string, List<ItemOriginDTO>> saveProvenance,
        Func<int, List<ItemOriginDTO>> getMovedOrigins
    )
    {
        if ((uint)input.TargetSlot >= HGSSApricornItems.Length)
            throw new ArgumentOutOfRangeException(nameof(input.TargetSlot));

        var entry = HGSSApricornItems[input.TargetSlot];
        if (!AreEquivalentItemKeys(entry.Key, source.ItemKey))
        {
            throw new InvalidOperationException(
                $"{source.ItemName} can only be placed in its matching HG/SS Apricorn Box color slot."
            );
        }

        var before = hgss.GetApricornCount(input.TargetSlot);
        var capacity = Math.Max(0, HGSSApricornMaxCount - before);
        var moved = Math.Min(requested, capacity);
        if (moved <= 0)
            return new(0, save.Version, false, false);

        hgss.SetApricornCount(input.TargetSlot, before + moved);

        var provenanceKey = SaveProvenanceKey(
            save.Id,
            InventoryType.None,
            entry.Key
        );
        var existingOrigins = before > 0
            ? GetEffectiveSaveOrigins(
                saveProvenance,
                save,
                InventoryType.None,
                entry.Key,
                before
            )
            : [];

        saveProvenance[provenanceKey] = MergeOrigins(
            existingOrigins,
            getMovedOrigins(moved)
        );

        loaders.Pkms.HasWritten = true;
        return new(moved, save.Version, false, true);
    }

''',
    "HGSS Apricorn target helper",
)

# ===========================================================================
# Shop evolution items: every supported evolution item is a permanent purchase
# unlock after PKVault sees the player own it once. Prices scale by rarity /
# scarcity rather than the old flat ₽3,000 stone price.
# ===========================================================================
shop = "PKVault.Core/shop/ShopService.cs"
rep(
    shop,
    '''        new("fire-stone", "Evolution Items", 3000, 1500),
        new("water-stone", "Evolution Items", 3000, 1500),
        new("thunder-stone", "Evolution Items", 3000, 1500),
        new("leaf-stone", "Evolution Items", 3000, 1500),
        new("moon-stone", "Evolution Items", 3000, 1500),
        new("sun-stone", "Evolution Items", 3000, 1500),
        new("dusk-stone", "Evolution Items", 3000, 1500),
        new("dawn-stone", "Evolution Items", 3000, 1500),
        new("shiny-stone", "Evolution Items", 3000, 1500),
        new("ice-stone", "Evolution Items", 3000, 1500),
''',
    '''        // Evolution stock is discovery-gated. CanBuy starts false and is
        // permanently enabled per item after PKVault observes one owned.
        new("fire-stone", "Evolution Items", 12_000, 6_000, false, true),
        new("water-stone", "Evolution Items", 12_000, 6_000, false, true),
        new("thunder-stone", "Evolution Items", 12_000, 6_000, false, true),
        new("leaf-stone", "Evolution Items", 12_000, 6_000, false, true),
        new("moon-stone", "Evolution Items", 15_000, 7_500, false, true),
        new("sun-stone", "Evolution Items", 15_000, 7_500, false, true),

        new("shiny-stone", "Evolution Items", 18_000, 9_000, false, true),
        new("dusk-stone", "Evolution Items", 18_000, 9_000, false, true),
        new("dawn-stone", "Evolution Items", 18_000, 9_000, false, true),
        new("ice-stone", "Evolution Items", 18_000, 9_000, false, true),
        new("oval-stone", "Evolution Items", 18_000, 9_000, false, true),

        new("kings-rock", "Evolution Items", 25_000, 12_500, false, true, "king's rock"),
        new("metal-coat", "Evolution Items", 25_000, 12_500, false, true),
        new("dragon-scale", "Evolution Items", 25_000, 12_500, false, true),
        new("up-grade", "Evolution Items", 25_000, 12_500, false, true, "upgrade"),
        new("deep-sea-tooth", "Evolution Items", 25_000, 12_500, false, true),
        new("deep-sea-scale", "Evolution Items", 25_000, 12_500, false, true),
        new("protector", "Evolution Items", 25_000, 12_500, false, true),
        new("electirizer", "Evolution Items", 25_000, 12_500, false, true),
        new("magmarizer", "Evolution Items", 25_000, 12_500, false, true),
        new("dubious-disc", "Evolution Items", 25_000, 12_500, false, true),
        new("reaper-cloth", "Evolution Items", 25_000, 12_500, false, true),
        new("razor-claw", "Evolution Items", 25_000, 12_500, false, true),
        new("razor-fang", "Evolution Items", 25_000, 12_500, false, true),
        new("prism-scale", "Evolution Items", 25_000, 12_500, false, true),
        new("whipped-dream", "Evolution Items", 25_000, 12_500, false, true),
        new("sachet", "Evolution Items", 25_000, 12_500, false, true),

        new("strawberry-sweet", "Evolution Items", 20_000, 10_000, false, true),
        new("love-sweet", "Evolution Items", 20_000, 10_000, false, true),
        new("berry-sweet", "Evolution Items", 20_000, 10_000, false, true),
        new("clover-sweet", "Evolution Items", 20_000, 10_000, false, true),
        new("flower-sweet", "Evolution Items", 20_000, 10_000, false, true),
        new("star-sweet", "Evolution Items", 30_000, 15_000, false, true),
        new("ribbon-sweet", "Evolution Items", 30_000, 15_000, false, true),

        new("tart-apple", "Evolution Items", 30_000, 15_000, false, true),
        new("sweet-apple", "Evolution Items", 30_000, 15_000, false, true),
        new("cracked-pot", "Evolution Items", 30_000, 15_000, false, true),
        new("chipped-pot", "Evolution Items", 40_000, 20_000, false, true),
        new("galarica-cuff", "Evolution Items", 30_000, 15_000, false, true),
        new("galarica-wreath", "Evolution Items", 40_000, 20_000, false, true),
        new("black-augurite", "Evolution Items", 30_000, 15_000, false, true),
        new("peat-block", "Evolution Items", 40_000, 20_000, false, true),
        new("linking-cord", "Evolution Items", 40_000, 20_000, false, true),

        new("auspicious-armor", "Evolution Items", 40_000, 20_000, false, true),
        new("malicious-armor", "Evolution Items", 40_000, 20_000, false, true),
        new("leaders-crest", "Evolution Items", 40_000, 20_000, false, true, "leader's crest"),
        new("syrupy-apple", "Evolution Items", 40_000, 20_000, false, true),
        new("unremarkable-teacup", "Evolution Items", 30_000, 15_000, false, true),
        new("masterpiece-teacup", "Evolution Items", 50_000, 25_000, false, true),
        new("metal-alloy", "Evolution Items", 50_000, 25_000, false, true),
''',
    "expanded discovery-gated evolution catalog",
)
rep(
    shop,
    '''    private const string TmUnlockProgressionKey = "shop.tm.unlocks";
    private const string MasterBallUnlockProgressionKey = "shop.master-ball.unlocked";
    private const string ApricornUnlockProgressionKey = "shop.apricorn.unlocked";
''',
    '''    private const string TmUnlockProgressionKey = "shop.tm.unlocks";
    private const string EvolutionItemUnlockProgressionKey = "shop.evolution-item.unlocks";
    private const string MasterBallUnlockProgressionKey = "shop.master-ball.unlocked";
    private const string ApricornUnlockProgressionKey = "shop.apricorn.unlocked";

    private static readonly HashSet<string> EvolutionItemKeys = Prices
        .Where(price => string.Equals(price.Category, "Evolution Items", StringComparison.Ordinal))
        .Select(price => price.Key)
        .ToHashSet(StringComparer.Ordinal);
''',
    "evolution unlock progression key",
)
rep(
    shop,
    '''        var unlockedTms = await LoadAndUpdateTmUnlocks(inventory);
''',
    '''        var unlockedEvolutionItems = await LoadAndUpdateEvolutionItemUnlocks(inventory);
        catalog = catalog
            .Select(price => EvolutionItemKeys.Contains(Canonical(price.Key))
                && unlockedEvolutionItems.Contains(Canonical(price.Key))
                && GetMinimumGeneration(price.Key) <= maxGeneration
                    ? price with { CanBuy = true }
                    : price)
            .ToList();

        var unlockedTms = await LoadAndUpdateTmUnlocks(inventory);
''',
    "enable discovered evolution purchases",
)
insert_before(
    shop,
    '''    private async Task<HashSet<string>> LoadAndUpdateTmUnlocks(ItemInventoryStateDTO inventory)
''',
    '''    private async Task<HashSet<string>> LoadAndUpdateEvolutionItemUnlocks(ItemInventoryStateDTO inventory)
    {
        var persisted = await progressionStore.Get(EvolutionItemUnlockProgressionKey);
        var unlocked = new HashSet<string>(
            (persisted ?? string.Empty)
                .Split('\\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
                .Select(Canonical),
            StringComparer.Ordinal
        );

        var observed = inventory.BankPages
            .SelectMany(page => page.Slots)
            .Concat(inventory.Saves.SelectMany(save => save.Pockets).SelectMany(pocket => pocket.Slots))
            .Where(slot => slot.ItemKey is not null && slot.Count > 0)
            .Select(slot => Canonical(slot.ItemKey!))
            .Where(EvolutionItemKeys.Contains);

        var beforeCount = unlocked.Count;
        unlocked.UnionWith(observed);
        if (unlocked.Count != beforeCount)
        {
            await progressionStore.Set(
                EvolutionItemUnlockProgressionKey,
                string.Join('\\n', unlocked.OrderBy(x => x, StringComparer.Ordinal))
            );
        }

        return unlocked;
    }

''',
    "persist discovered evolution item unlocks",
)

print("PASS alpha53l DB/trade/settings/evolution/HGSS Apricorn patch")

from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def replace_once(rel, old, new, marker):
    path = root / rel
    text = path.read_text(encoding='utf-8')
    if marker in text:
        return
    if old not in text:
        raise RuntimeError(f'alpha53l anchor missing: {rel} :: {marker}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')

# ---------------------------------------------------------------------------
# A real barrier around SQLite file transitions.
# Only contexts that have completed EnsureSessionCreated and are about to use
# SQLite are counted. This avoids startup deadlocks while still preventing Save,
# Undo and Reset from moving/deleting pkvault-session.db under an active request.
# ---------------------------------------------------------------------------
(root / 'PKVault.Core/db/SessionDbContextTracker.cs').write_text(r'''using Serilog;

namespace PKVault.Core;

public sealed class SessionDbContextTracker
{
    private readonly object Sync = new();
    private readonly HashSet<Guid> ActiveContextIds = [];
    private bool FileTransitionActive;
    private TaskCompletionSource? DrainTcs;

    public IDisposable Register(Guid contextId)
    {
        lock (Sync)
        {
            while (FileTransitionActive)
                Monitor.Wait(Sync);

            if (!ActiveContextIds.Add(contextId))
                throw new InvalidOperationException($"Session DB context already registered: {contextId}");

            return new ContextLease(this, contextId);
        }
    }

    public async Task<IDisposable> BeginFileTransitionAsync(
        string operation,
        CancellationToken cancellationToken = default
    )
    {
        Task? drainTask = null;

        lock (Sync)
        {
            if (FileTransitionActive)
                throw new InvalidOperationException("A Session DB file transition is already active.");

            FileTransitionActive = true;
            if (ActiveContextIds.Count > 0)
            {
                DrainTcs = new(TaskCreationOptions.RunContinuationsAsynchronously);
                drainTask = DrainTcs.Task;
                Log.Information(
                    "Waiting for {Count} Session DB context(s) to drain before '{Operation}': {ContextIds}",
                    ActiveContextIds.Count,
                    operation,
                    string.Join(", ", ActiveContextIds)
                );
            }
        }

        if (drainTask is not null)
        {
            try
            {
                await drainTask.WaitAsync(TimeSpan.FromSeconds(30), cancellationToken);
            }
            catch
            {
                string contextIds;
                lock (Sync)
                    contextIds = string.Join(", ", ActiveContextIds);

                EndFileTransition();
                throw new IOException(
                    $"Timed out waiting for PKVault database users to finish before '{operation}'. "
                    + $"Active contexts: {contextIds}"
                );
            }
        }

        return new FileTransitionLease(this);
    }

    private void ReleaseContext(Guid contextId)
    {
        lock (Sync)
        {
            ActiveContextIds.Remove(contextId);
            if (FileTransitionActive && ActiveContextIds.Count == 0)
                DrainTcs?.TrySetResult();
        }
    }

    private void EndFileTransition()
    {
        lock (Sync)
        {
            FileTransitionActive = false;
            DrainTcs = null;
            Monitor.PulseAll(Sync);
        }
    }

    private sealed class ContextLease(SessionDbContextTracker owner, Guid contextId) : IDisposable
    {
        private int Disposed;

        public void Dispose()
        {
            if (Interlocked.Exchange(ref Disposed, 1) == 0)
                owner.ReleaseContext(contextId);
        }
    }

    private sealed class FileTransitionLease(SessionDbContextTracker owner) : IDisposable
    {
        private int Disposed;

        public void Dispose()
        {
            if (Interlocked.Exchange(ref Disposed, 1) == 0)
                owner.EndFileTransition();
        }
    }
}
''', encoding='utf-8')

# ---------------------------------------------------------------------------
# SessionDbContext activates its file lease lazily, after EnsureSessionCreated.
# SaveChanges is also protected in case a caller writes directly through the DB.
# ---------------------------------------------------------------------------
ctx_path = root / 'PKVault.Core/db/SessionDbContext.cs'
ctx = ctx_path.read_text(encoding='utf-8')
old_header = '''public class SessionDbContext(
    ISessionServiceMinimal sessionService, IDbSeedingService dbSeedingService
) : DbContext
{
'''
new_header = '''public class SessionDbContext : DbContext
{
    private readonly ISessionServiceMinimal sessionService;
    private readonly IDbSeedingService dbSeedingService;
    private readonly SessionDbContextTracker contextTracker;
    private IDisposable? contextLease;
    private int trackerActivated;

    public SessionDbContext(
        ISessionServiceMinimal sessionService,
        IDbSeedingService dbSeedingService,
        SessionDbContextTracker contextTracker
    )
    {
        this.sessionService = sessionService;
        this.dbSeedingService = dbSeedingService;
        this.contextTracker = contextTracker;
    }

    public void ActivateFileLease()
    {
        if (Interlocked.CompareExchange(ref trackerActivated, 1, 0) != 0)
            return;

        try
        {
            contextLease = contextTracker.Register(ContextId.InstanceId);
        }
        catch
        {
            Volatile.Write(ref trackerActivated, 0);
            throw;
        }
    }

'''
if 'public void ActivateFileLease()' not in ctx:
    if old_header not in ctx:
        raise RuntimeError('alpha53l SessionDbContext header anchor missing')
    ctx = ctx.replace(old_header, new_header, 1)

old = '''    public override Task<int> SaveChangesAsync(bool acceptAllChangesOnSuccess, CancellationToken cancellationToken = default)
    {
        TrackChangesToFlags();
        return base.SaveChangesAsync(acceptAllChangesOnSuccess, cancellationToken);
    }

    public override int SaveChanges(bool acceptAllChangesOnSuccess)
    {
        TrackChangesToFlags();
        return base.SaveChanges(acceptAllChangesOnSuccess);
    }
'''
new = '''    public override Task<int> SaveChangesAsync(bool acceptAllChangesOnSuccess, CancellationToken cancellationToken = default)
    {
        ActivateFileLease();
        TrackChangesToFlags();
        return base.SaveChangesAsync(acceptAllChangesOnSuccess, cancellationToken);
    }

    public override int SaveChanges(bool acceptAllChangesOnSuccess)
    {
        ActivateFileLease();
        TrackChangesToFlags();
        return base.SaveChanges(acceptAllChangesOnSuccess);
    }
'''
if 'ActivateFileLease();
        TrackChangesToFlags();' not in ctx:
    if old not in ctx:
        raise RuntimeError('alpha53l SaveChanges anchor missing')
    ctx = ctx.replace(old, new, 1)

insert_anchor = '''    protected override void OnModelCreating(ModelBuilder modelBuilder)
'''
insert = '''    public override void Dispose()
    {
        contextLease?.Dispose();
        contextLease = null;
        base.Dispose();
    }

    public override async ValueTask DisposeAsync()
    {
        contextLease?.Dispose();
        contextLease = null;
        await base.DisposeAsync();
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
'''
if 'contextLease?.Dispose();' not in ctx:
    if insert_anchor not in ctx:
        raise RuntimeError('alpha53l SessionDbContext dispose anchor missing')
    ctx = ctx.replace(insert_anchor, insert, 1)
ctx_path.write_text(ctx, encoding='utf-8')

replace_once(
    'PKVault.Core/db/loader/EntityLoader.cs',
    '''        await sessionService.EnsureSessionCreated(db.ContextId.InstanceId);

        return GetDbSetRaw();
''',
    '''        await sessionService.EnsureSessionCreated(db.ContextId.InstanceId);
        db.ActivateFileLease();

        return GetDbSetRaw();
''',
    'db.ActivateFileLease();'
)
replace_once(
    'PKVault.Core/db/loader/MetaLoader.cs',
    '''        await sessionService.EnsureSessionCreated(db.ContextId.InstanceId);

        return GetDbSetRaw();
''',
    '''        await sessionService.EnsureSessionCreated(db.ContextId.InstanceId);
        db.ActivateFileLease();

        return GetDbSetRaw();
''',
    'db.ActivateFileLease();'
)
replace_once(
    'PKVault.Core/db/loader/PkmFileLoader.cs',
    '''        await sessionService.EnsureSessionCreated(db.ContextId.InstanceId);

        return db.PkmFiles;
''',
    '''        await sessionService.EnsureSessionCreated(db.ContextId.InstanceId);
        db.ActivateFileLease();

        return db.PkmFiles;
''',
    'db.ActivateFileLease();'
)

replace_once(
    'PKVault.Core/Program.cs',
    '''        Log.Information($"Setup services - DB");
        services.AddDbContext<SessionDbContext>();
''',
    '''        Log.Information($"Setup services - DB");
        services.AddSingleton<SessionDbContextTracker>();
        services.AddDbContext<SessionDbContext>();
''',
    'services.AddSingleton<SessionDbContextTracker>();'
)

# ---------------------------------------------------------------------------
# StorageController had acquired DB-backed scoped dependencies even for Save and
# Undo routes that never use them. Resolve those services lazily only on routes
# that actually need them.
# ---------------------------------------------------------------------------
route_path = root / 'PKVault.Core/storage/routes/StorageRoute.cs'
route = route_path.read_text(encoding='utf-8')
if 'IServiceProvider scopedProvider' not in route:
    old = '''public class StorageController(
    DataService dataService,
    StorageQueryService storageQueryService,
    ActionService actionService,
    ISessionService sessionService,
    ItemBankService itemBankService,
    ISavesLoadersService savesLoadersService,
    IPkmVariantLoader pkmVariantLoader,
    EvolutionService evolutionService
)
{
'''
    new = '''public class StorageController(
    DataService dataService,
    StorageQueryService storageQueryService,
    ActionService actionService,
    ISessionService sessionService,
    ISavesLoadersService savesLoadersService,
    IServiceProvider scopedProvider
)
{
    private ItemBankService ItemBankService => scopedProvider.GetRequiredService<ItemBankService>();
    private IPkmVariantLoader PkmVariantLoader => scopedProvider.GetRequiredService<IPkmVariantLoader>();
    private EvolutionService EvolutionService => scopedProvider.GetRequiredService<EvolutionService>();
'''
    if old not in route:
        raise RuntimeError('alpha53l StorageController constructor anchor missing')
    route = route.replace(old, new, 1)
    route = 'using Microsoft.Extensions.DependencyInjection;
' + route
route = route.replace('itemBankService.', 'ItemBankService.')
route = route.replace('pkmVariantLoader.', 'PkmVariantLoader.')
route = route.replace('evolutionService.', 'EvolutionService.')
route_path.write_text(route, encoding='utf-8')

# ---------------------------------------------------------------------------
# SessionService: write through a short-lived scope, fully dispose it, then take
# the DB barrier before touching the SQLite file. Reset uses the same barrier and
# no longer creates a throwaway EF context merely to delete the DB.
# ---------------------------------------------------------------------------
session_path = root / 'PKVault.Core/db/services/SessionService.cs'
session = session_path.read_text(encoding='utf-8')
session = session.replace('public Task PersistSession(IServiceScope scope);', 'public Task PersistSession();')
old_ctor = '''public class SessionService(
    IServiceProvider sp, TimeProvider timeProvider,
    IFileIOService fileIOService, ISettingsService settingsService,
    ISavesLoadersService savesLoadersService
) : ISessionService
'''
new_ctor = '''public class SessionService(
    IServiceProvider sp, TimeProvider timeProvider,
    IFileIOService fileIOService, ISettingsService settingsService,
    ISavesLoadersService savesLoadersService,
    SessionDbContextTracker dbContextTracker
) : ISessionService
'''
if 'SessionDbContextTracker dbContextTracker' not in session:
    if old_ctor not in session:
        raise RuntimeError('alpha53l SessionService ctor anchor missing')
    session = session.replace(old_ctor, new_ctor, 1)

old = '''            // Every fresh/reset session must start from the committed .item mirror,
            // including action undo/cancel rebuilds (checkInitialActions=false).
            // This keeps automatic quest rewards in the baseline while pending
            // Trash/Move actions remain fully reversible until Save.
            using (var scope = sp.CreateScope())
            {
                // required to avoid deadlocks, ex: SessionService => SynchronizeAction => loaders => SessionService
                ByPassContextId = scope.ServiceProvider.GetRequiredService<SessionDbContext>()
                    .ContextId.InstanceId;

                try
                {
                    var itemBankService = scope.ServiceProvider.GetRequiredService<ItemBankService>();
                    if (await itemBankService.ReconcilePersistedBankFiles())
                        Log.Logger.Information("PKVault item bank reconciled from persisted .item files");

                    if (checkInitialActions)
                    {
                        var hadDataToNormalize = await CheckDataToNormalize(scope, flags);
                        Log.Logger.Debug($"Session - hadDataToNormalize={hadDataToNormalize}");

                        await CheckSaveToSynchronize(scope, flags);

                        if (hadDataToNormalize)
                        {
                            await CheckFirstRunAutoSave(scope, flags);
                        }
                    }
                }
                finally
                {
                    ByPassContextId = null;
                }
            }

            return flags;
'''
new = '''            var shouldAutoSaveFreshStart = false;

            // Every fresh/reset session must start from the committed .item mirror,
            // including action undo/cancel rebuilds (checkInitialActions=false).
            // This keeps automatic quest rewards in the baseline while pending
            // Trash/Move actions remain fully reversible until Save.
            using (var scope = sp.CreateScope())
            {
                // required to avoid deadlocks, ex: SessionService => SynchronizeAction => loaders => SessionService
                ByPassContextId = scope.ServiceProvider.GetRequiredService<SessionDbContext>()
                    .ContextId.InstanceId;

                try
                {
                    var itemBankService = scope.ServiceProvider.GetRequiredService<ItemBankService>();
                    if (await itemBankService.ReconcilePersistedBankFiles())
                        Log.Logger.Information("PKVault item bank reconciled from persisted .item files");

                    if (checkInitialActions)
                    {
                        var hadDataToNormalize = await CheckDataToNormalize(scope, flags);
                        Log.Logger.Debug($"Session - hadDataToNormalize={hadDataToNormalize}");

                        await CheckSaveToSynchronize(scope, flags);
                        shouldAutoSaveFreshStart = hadDataToNormalize && !HasMainDb();
                    }
                }
                finally
                {
                    ByPassContextId = null;
                }
            }

            if (shouldAutoSaveFreshStart)
                await CheckFirstRunAutoSave(flags);

            return flags;
'''
if 'shouldAutoSaveFreshStart' not in session:
    if old not in session:
        raise RuntimeError('alpha53l startup scope anchor missing')
    session = session.replace(old, new, 1)

old = '''    private async Task CheckFirstRunAutoSave(IServiceScope scope, DataUpdateFlags flags)
    {
        var hasAnyData = HasMainDb();
        Log.Logger.Debug($"Check fresh start auto-save, hasAnyData={hasAnyData}");

        if (!hasAnyData)
        {
            Log.Logger.Information($"Fresh start detected - Session persisting & restart");
            await PersistSession(scope);
            await StartNewSession(checkInitialActions: false, flags);
        }
    }
'''
new = '''    private async Task CheckFirstRunAutoSave(DataUpdateFlags flags)
    {
        var hasAnyData = HasMainDb();
        Log.Logger.Debug($"Check fresh start auto-save, hasAnyData={hasAnyData}");

        if (!hasAnyData)
        {
            Log.Logger.Information($"Fresh start detected - Session persisting & restart");
            await PersistSession();
            await StartNewSession(checkInitialActions: false, flags);
        }
    }
'''
if 'CheckFirstRunAutoSave(DataUpdateFlags flags)' not in session:
    if old not in session:
        raise RuntimeError('alpha53l first-run autosave anchor missing')
    session = session.replace(old, new, 1)

start = session.find('    public async Task PersistSession(')
end = session.find('    private async Task ResetDbSession', start)
if start < 0 or end < 0:
    raise RuntimeError('alpha53l PersistSession block missing')
new_persist = r'''    public async Task PersistSession()
    {
        using var _ = Log.Logger.Time($"Persist session with copy session to main");

        // Use a private short-lived scope and dispose every DB-backed service
        // before the SQLite file transition begins.
        using (var writeScope = sp.CreateScope())
        {
            var itemBankService = writeScope.ServiceProvider.GetRequiredService<ItemBankService>();
            await itemBankService.WriteToFiles();

            var pkmFileLoader = writeScope.ServiceProvider.GetRequiredService<IPkmFileLoader>();
            await pkmFileLoader.WriteToFiles();
        }

        await savesLoadersService.WriteToFiles();
        savesLoadersService.Clear();
        Actions.Clear();

        await SessionFileTransitionLock.WaitAsync();
        try
        {
            using var dbTransition = await dbContextTracker.BeginFileTransitionAsync(
                "save session DB to main"
            );

            SqliteConnection.ClearAllPools();
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
    }

'''
session = session[:start] + new_persist + session[end:]

start = session.find('    private async Task ResetDbSession(')
end = session.find('    private async Task RunDbMigrations()', start)
if start < 0 or end < 0:
    raise RuntimeError('alpha53l ResetDbSession block missing')
new_reset = r'''    private async Task ResetDbSession(DataUpdateFlags flags)
    {
        await SessionFileTransitionLock.WaitAsync();
        try
        {
            using var dbTransition = await dbContextTracker.BeginFileTransitionAsync(
                "reset session DB"
            );

            SqliteConnection.ClearAllPools();

            if (fileIOService.Exists(SessionDbPath))
            {
                var deleted = await RetryFileOperation(
                    "delete stale session DB",
                    () => fileIOService.Delete(SessionDbPath)
                );
                await RetryFileOperation(
                    "delete stale session DB shm",
                    () => fileIOService.Delete(SessionDbPath + "-shm")
                );
                await RetryFileOperation(
                    "delete stale session DB wal",
                    () => fileIOService.Delete(SessionDbPath + "-wal")
                );

                Log.Logger.Debug($"DB session deleted={deleted}");
            }

            if (fileIOService.Exists(MainDbPath))
            {
                await RetryFileOperation(
                    "copy main DB to session",
                    () =>
                    {
                        fileIOService.Copy(MainDbPath, SessionDbPath, overwrite: true);
                        return true;
                    }
                );

                Log.Logger.Debug($"DB main copied to session");
            }
        }
        finally
        {
            SessionFileTransitionLock.Release();
        }

        await RunDbMigrations();

        flags.MainBanks.All = true;
        flags.MainBoxes.All = true;
        flags.MainPkmVariants.All = true;
        flags.Dex.All = true;
        flags.Warnings = true;
    }

'''
session = session[:start] + new_reset + session[end:]

old = '''        using var scope = sp.CreateScope();
        using var db = scope.ServiceProvider.GetRequiredService<SessionDbContext>();

        // Log.Logger.Information($"CONTEXT ID = {db.ContextId.InstanceId}");
'''
new = '''        using var scope = sp.CreateScope();
        using var db = scope.ServiceProvider.GetRequiredService<SessionDbContext>();
        db.ActivateFileLease();

        // Log.Logger.Information($"CONTEXT ID = {db.ContextId.InstanceId}");
'''
if 'using var db = scope.ServiceProvider.GetRequiredService<SessionDbContext>();
        db.ActivateFileLease();' not in session:
    if old not in session:
        raise RuntimeError('alpha53l migration activation anchor missing')
    session = session.replace(old, new, 1)

start = session.find('    private async Task CloseConnection()')
if start >= 0:
    end = session.find('    private async Task<T> RetryFileOperation', start)
    if end < 0:
        raise RuntimeError('alpha53l CloseConnection end anchor missing')
    session = session[:start] + session[end:]
session_path.write_text(session, encoding='utf-8')

# ---------------------------------------------------------------------------
# Save callers no longer pass a live DB scope into PersistSession.
# ---------------------------------------------------------------------------
action_path = root / 'PKVault.Core/storage/services/ActionService.cs'
action = action_path.read_text(encoding='utf-8')
old = '''        await backupService.PrepareBackupThenRun("backup_before_save", flags, async () =>
        {
            using var scope = sp.CreateScope();

            await sessionService.PersistSession(scope);

            if (committedEvolutionEvents.Length > 0)
            {
                var questService = scope.ServiceProvider.GetRequiredService<QuestService>();
                var contractService = scope.ServiceProvider.GetRequiredService<ContractService>();
'''
new = '''        await backupService.PrepareBackupThenRun("backup_before_save", flags, async () =>
        {
            await sessionService.PersistSession();

            if (committedEvolutionEvents.Length > 0)
            {
                using var scope = sp.CreateScope();
                var questService = scope.ServiceProvider.GetRequiredService<QuestService>();
                var contractService = scope.ServiceProvider.GetRequiredService<ContractService>();
'''
if 'await sessionService.PersistSession();' not in action:
    if old not in action:
        raise RuntimeError('alpha53l ActionService Save anchor missing')
    action = action.replace(old, new, 1)
action_path.write_text(action, encoding='utf-8')

trade_path = root / 'PKVault.Core/trading/TradingService.cs'
trade = trade_path.read_text(encoding='utf-8')
trade = trade.replace(
    '''            using var scope = sp.CreateScope();
            await sessionService.PersistSession(scope);
            await sessionService.StartNewSession(checkInitialActions: false, flags);
''',
    '''            await sessionService.PersistSession();
            await sessionService.StartNewSession(checkInitialActions: false, flags);
''',
    1
)
trade_path.write_text(trade, encoding='utf-8')

# ---------------------------------------------------------------------------
# Fix the actual long-lived scope leak in SettingsService and don't hold a DB
# scope across settings-triggered restart/persist operations.
# ---------------------------------------------------------------------------
settings_path = root / 'PKVault.Core/settings/services/SettingsService.cs'
settings = settings_path.read_text(encoding='utf-8')
old = '''    public async Task UpdateSettings(SettingsMutableDTO settingsMutable, bool restartSession, bool scanSaves, DataUpdateFlags flags)
    {
        using var scope = sp.CreateScope();

        var userId = string.IsNullOrEmpty(BaseSettings?.UserId)
            ? await scope.ServiceProvider.GetRequiredService<IMetaLoader>().GetUserId()
            : BaseSettings.UserId;

        await UpdateSettingsSimple(settingsMutable, userId);
        flags.Settings = true;

        if (restartSession)
        {
            await sessionService.StartNewSession(checkInitialActions: true, flags);

            if (!sessionService.HasEmptyActionList())
            {
                await sessionService.PersistSession(scope);
                await sessionService.StartNewSession(checkInitialActions: false, flags);
            }
        }
        else if (scanSaves)
        {
            await savesLoadersService.Setup(flags);
        }
    }
'''
new = '''    public async Task UpdateSettings(SettingsMutableDTO settingsMutable, bool restartSession, bool scanSaves, DataUpdateFlags flags)
    {
        string userId;
        if (string.IsNullOrEmpty(BaseSettings?.UserId))
        {
            using var userScope = sp.CreateScope();
            userId = await userScope.ServiceProvider.GetRequiredService<IMetaLoader>().GetUserId();
        }
        else
        {
            userId = BaseSettings.UserId;
        }

        await UpdateSettingsSimple(settingsMutable, userId);
        flags.Settings = true;

        if (restartSession)
        {
            await sessionService.StartNewSession(checkInitialActions: true, flags);

            if (!sessionService.HasEmptyActionList())
            {
                await sessionService.PersistSession();
                await sessionService.StartNewSession(checkInitialActions: false, flags);
            }
        }
        else if (scanSaves)
        {
            await savesLoadersService.Setup(flags);
        }
    }
'''
if 'using var userScope = sp.CreateScope();' not in settings:
    if old not in settings:
        raise RuntimeError('alpha53l Settings UpdateSettings anchor missing')
    settings = settings.replace(old, new, 1)
settings = settings.replace(
    '            var scope = sp.CreateScope();

            // DB use is required to avoid rare first-run app crash after language selection',
    '            using var scope = sp.CreateScope();

            // DB use is required to avoid rare first-run app crash after language selection',
    1
)
settings_path.write_text(settings, encoding='utf-8')

for path in (root / 'PKVault.Core').rglob('*.cs'):
    text = path.read_text(encoding='utf-8')
    if 'PersistSession(scope)' in text:
        raise RuntimeError(f'alpha53l stale PersistSession(scope) remains: {path}')

settings = settings_path.read_text(encoding='utf-8')
if '            var scope = sp.CreateScope();' in settings:
    raise RuntimeError('alpha53l SettingsService still contains an undisposed scope')

print('PASS alpha53l DB lifetime barrier + settings scope leak fix')

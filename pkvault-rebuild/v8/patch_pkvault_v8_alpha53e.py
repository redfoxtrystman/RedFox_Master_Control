from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()


def replace_once(rel: str, old: str, new: str, marker: str | None = None):
    path = root / rel
    text = path.read_text(encoding='utf-8')
    if old in text:
        text = text.replace(old, new, 1)
        path.write_text(text, encoding='utf-8')
        print(f'PATCHED {rel}')
        return
    if marker and marker in text:
        print(f'ALREADY {rel}')
        return
    raise RuntimeError(f'alpha53e anchor missing in {rel}: {old[:120]!r}')


# 1) Do not let Microsoft.Data.Sqlite retain pooled handles to the disposable
# session database. Windows cannot atomically replace/delete a SQLite file while
# a pooled handle remains open.
replace_once(
    'PKVault.Core/db/SessionDbContext.cs',
    '.UseSqlite($"Data Source={sessionService.SessionDbPath}")',
    '.UseSqlite($"Data Source={sessionService.SessionDbPath};Pooling=False")',
    'SessionDbPath};Pooling=False',
)

# 2) Make the session-file transition resilient to a request that was already in
# flight when Save/Reload began. Close our context, clear every SQLite pool, then
# retry only the filesystem transition for a short bounded window.
session_rel = 'PKVault.Core/db/services/SessionService.cs'
session_path = root / session_rel
text = session_path.read_text(encoding='utf-8')

old_persist = '''        await CloseConnection();
        StartTask = null;

        Log.Logger.Debug($"Move session DB to main");
        fileIOService.Move(SessionDbPath, MainDbPath, overwrite: true);

        StartTime = null;
'''
new_persist = '''        await CloseConnection();
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
'''
if old_persist in text:
    text = text.replace(old_persist, new_persist, 1)
elif '"move session DB to main"' not in text:
    raise RuntimeError('alpha53e PersistSession anchor missing')

old_reset = '''        if (fileIOService.Exists(SessionDbPath))
        {
            using var scope = sp.CreateScope();
            using var db = scope.ServiceProvider.GetRequiredService<SessionDbContext>();

            var deleted1 = await db.Database.EnsureDeletedAsync();
            var deleted2 = fileIOService.Delete(SessionDbPath);
            fileIOService.Delete(SessionDbPath + "-shm");
            fileIOService.Delete(SessionDbPath + "-wal");

            Log.Logger.Debug($"DB session deleted={deleted1}/{deleted2}");
        }

        if (fileIOService.Exists(MainDbPath))
        {
            fileIOService.Copy(MainDbPath, SessionDbPath, overwrite: true);

            Log.Logger.Debug($"DB main copied to session");
        }
'''
new_reset = '''        if (fileIOService.Exists(SessionDbPath))
        {
            bool deleted1;
            using (var scope = sp.CreateScope())
            using (var db = scope.ServiceProvider.GetRequiredService<SessionDbContext>())
            {
                deleted1 = await db.Database.EnsureDeletedAsync();
                await db.Database.CloseConnectionAsync();
            }

            // Ensure the DbContext above is disposed before touching the file.
            // This is especially important on Windows, where an open SQLite handle
            // prevents deletion/replacement of the session database.
            SqliteConnection.ClearAllPools();

            var deleted2 = await RetryFileOperation(
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

            Log.Logger.Debug($"DB session deleted={deleted1}/{deleted2}");
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
'''
if old_reset in text:
    text = text.replace(old_reset, new_reset, 1)
elif 'delete stale session DB' not in text:
    raise RuntimeError('alpha53e ResetDbSession anchor missing')

old_close = '''    private async Task CloseConnection()
    {
        using var _ = Log.Logger.Time($"SessionService.CloseConnection");

        using var scope = sp.CreateScope();
        using var db = scope.ServiceProvider.GetRequiredService<SessionDbContext>();

        // required to really close connection
        if (db.Database.GetDbConnection() is SqliteConnection sqliteConnection)
        {
            SqliteConnection.ClearPool(sqliteConnection);
        }

        await db.Database.CloseConnectionAsync();

        Log.Logger.Information($"DB session connection closed");
    }
'''
new_close = '''    private async Task CloseConnection()
    {
        using var _ = Log.Logger.Time($"SessionService.CloseConnection");

        using (var scope = sp.CreateScope())
        using (var db = scope.ServiceProvider.GetRequiredService<SessionDbContext>())
        {
            await db.Database.CloseConnectionAsync();
        }

        // Clear after disposal. ClearPool-before-Close can leave the connection
        // being closed eligible to return to a pool; ClearAllPools also catches
        // any older pooled connection created before alpha53e disabled pooling.
        SqliteConnection.ClearAllPools();

        Log.Logger.Information($"DB session connection closed");
    }

    private async Task<T> RetryFileOperation<T>(string operationName, Func<T> operation)
    {
        const int maxAttempts = 20;

        for (var attempt = 1; ; attempt++)
        {
            try
            {
                return operation();
            }
            catch (IOException ex) when (attempt < maxAttempts)
            {
                // An HTTP request can already be inside SQLite when Save begins.
                // With pooling disabled it will release the handle as soon as that
                // request finishes. Keep new polling paused on the frontend and give
                // the existing request a short bounded window to drain.
                SqliteConnection.ClearAllPools();
                var delayMs = Math.Min(250, 25 * attempt);
                Log.Logger.Warning(
                    ex,
                    "Session DB file operation '{Operation}' is temporarily busy; retry {Attempt}/{MaxAttempts} in {DelayMs} ms",
                    operationName,
                    attempt,
                    maxAttempts,
                    delayMs
                );
                await Task.Delay(delayMs);
            }
        }
    }
'''
if old_close in text:
    text = text.replace(old_close, new_close, 1)
elif 'RetryFileOperation<T>' not in text:
    raise RuntimeError('alpha53e CloseConnection anchor missing')

session_path.write_text(text, encoding='utf-8')
print(f'PATCHED {session_rel}')

# 3) If an emulator or sync process is writing a .sav at the exact instant of a
# scan, retry the read instead of dropping that save loader for the whole session.
saves_rel = 'PKVault.Core/db/loader/save/SavesLoadersService.cs'
saves_path = root / saves_rel
text = saves_path.read_text(encoding='utf-8')
old_read = '''            var data = await fileIOService.ReadBytes(path);
            return await GetSaveFile(data, path);
'''
new_read = '''            byte[] data;
            const int maxReadAttempts = 12;
            for (var attempt = 1; ; attempt++)
            {
                try
                {
                    data = await fileIOService.ReadBytes(path);
                    break;
                }
                catch (IOException ex) when (attempt < maxReadAttempts)
                {
                    var delayMs = Math.Min(250, 50 * attempt);
                    Log.Warning(
                        ex,
                        "Save file is temporarily busy; retry {Attempt}/{MaxAttempts} in {DelayMs} ms, path={Path}",
                        attempt,
                        maxReadAttempts,
                        delayMs,
                        path
                    );
                    await Task.Delay(delayMs);
                }
            }

            return await GetSaveFile(data, path);
'''
if old_read in text:
    text = text.replace(old_read, new_read, 1)
elif 'Save file is temporarily busy; retry' not in text:
    raise RuntimeError('alpha53e save-file retry anchor missing')
saves_path.write_text(text, encoding='utf-8')
print(f'PATCHED {saves_rel}')

# 4) Pause the 1.5s Quest/Contract polling before Save. Reuse the existing reload
# pause events so both the Quest page and global Quest toast stop issuing reads.
actions_rel = 'frontend/src/storage/actions/actions-panel.tsx'
actions_path = root / actions_rel
text = actions_path.read_text(encoding='utf-8')
old_import = "import React from 'react';\n"
new_import = "import React from 'react';\nimport { useQueryClient } from '@tanstack/react-query';\n"
if new_import not in text:
    if old_import not in text:
        raise RuntimeError('alpha53e actions import anchor missing')
    text = text.replace(old_import, new_import, 1)

old_query = '''    const saveMutation = useStorageSave();

    const getActionDescription = useActionDescription();
'''
new_query = '''    const saveMutation = useStorageSave();
    const queryClient = useQueryClient();

    const getActionDescription = useActionDescription();
'''
if old_query in text:
    text = text.replace(old_query, new_query, 1)
elif 'const queryClient = useQueryClient();' not in text:
    raise RuntimeError('alpha53e queryClient anchor missing')

old_save = '''        onSave={settingsQuery.data?.data.demoMode
            ? undefined
            : () => saveMutation.mutateAsync()}
'''
new_save = '''        onSave={settingsQuery.data?.data.demoMode
            ? undefined
            : async () => {
                window.dispatchEvent(new Event('pkvault:reload-start'));
                try {
                    await Promise.all([
                        queryClient.cancelQueries({ queryKey: ['quest-state'] }),
                        queryClient.cancelQueries({ queryKey: ['contract-state'] }),
                    ]);
                    // Give requests that were already on the wire a moment to leave
                    // their scoped SQLite DbContext before the backend swaps files.
                    await new Promise(resolve => window.setTimeout(resolve, 75));
                    return await saveMutation.mutateAsync();
                } finally {
                    window.dispatchEvent(new Event('pkvault:reload-end'));
                }
            }}
'''
if old_save in text:
    text = text.replace(old_save, new_save, 1)
elif 'queryClient.cancelQueries' not in text:
    raise RuntimeError('alpha53e save handler anchor missing')

actions_path.write_text(text, encoding='utf-8')
print(f'PATCHED {actions_rel}')

print('PASS alpha53e SQLite/save-file lock hardening')

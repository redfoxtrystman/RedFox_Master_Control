from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "PKVault.Core/db/services/SessionService.cs"
text = path.read_text(encoding="utf-8")

old = """            // Reconcile the persisted .item mirror only at fresh-session/reload
            // boundaries. Normal inventory reads keep the session DB authoritative
            // so undoable drag/drop changes are not reverted.
            using (var inventoryScope = sp.CreateScope())
            {
                var itemBankService = inventoryScope.ServiceProvider.GetRequiredService<ItemBankService>();
                if (await itemBankService.ReconcilePersistedBankFiles())
                    Log.Logger.Information("PKVault item bank reconciled from persisted .item files");
            }

            if (checkInitialActions)
            {
                using var scope = sp.CreateScope();

                // required to avoid deadlocks, ex: SessionService => SynchronizeAction => loaders => SessionService
                ByPassContextId = scope.ServiceProvider.GetRequiredService<SessionDbContext>()
                    .ContextId.InstanceId;

                var hadDataToNormalize = await CheckDataToNormalize(scope, flags);
                Log.Logger.Debug($"Session - hadDataToNormalize={hadDataToNormalize}");

                await CheckSaveToSynchronize(scope, flags);

                if (hadDataToNormalize)
                {
                    await CheckFirstRunAutoSave(scope, flags);
                }

                ByPassContextId = null;
            }
"""

new = """            if (checkInitialActions)
            {
                using var scope = sp.CreateScope();

                // required to avoid deadlocks, ex: SessionService => SynchronizeAction => loaders => SessionService
                ByPassContextId = scope.ServiceProvider.GetRequiredService<SessionDbContext>()
                    .ContextId.InstanceId;

                try
                {
                    // Reconcile the persisted .item mirror only after the session-context
                    // bypass is active. ItemBankService uses MetaLoader, and MetaLoader
                    // calls EnsureSessionCreated(); doing this before ByPassContextId was
                    // set caused StartNewSession to await its own StartTask forever.
                    var itemBankService = scope.ServiceProvider.GetRequiredService<ItemBankService>();
                    if (await itemBankService.ReconcilePersistedBankFiles())
                        Log.Logger.Information("PKVault item bank reconciled from persisted .item files");

                    var hadDataToNormalize = await CheckDataToNormalize(scope, flags);
                    Log.Logger.Debug($"Session - hadDataToNormalize={hadDataToNormalize}");

                    await CheckSaveToSynchronize(scope, flags);

                    if (hadDataToNormalize)
                    {
                        await CheckFirstRunAutoSave(scope, flags);
                    }
                }
                finally
                {
                    ByPassContextId = null;
                }
            }
"""

if old not in text:
    raise RuntimeError(f"{path}: alpha49 deadlock-fix anchor missing")

path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("PKVault V8 alpha49 item-bank reconciliation startup deadlock fix applied")

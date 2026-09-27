from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52i anchor not found: {label}")
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# Dedicated progression file.
# This file is OUTSIDE pkvault-session.db so "Reload all data & saves" cannot
# erase dailies, contract state, achievement completion, or anti-reuse history.
# ---------------------------------------------------------------------------
store_path = root / "PKVault.Core/progression/ProgressionFileStore.cs"
store_path.parent.mkdir(parents=True, exist_ok=True)
store_path.write_text(r'''using System.Text;
using Serilog;

namespace PKVault.Core;

public class ProgressionFileStore(ISettingsService settingsService)
{
    private static readonly SemaphoreSlim Gate = new(1, 1);

    private string ProgressionPath
        => Path.Combine(settingsService.GetSettings().GetDbPath(), "pkvault-progression.dat");

    public async Task<string?> Get(string key)
    {
        await Gate.WaitAsync();
        try
        {
            var values = await LoadNoLock();
            return values.GetValueOrDefault(key);
        }
        finally
        {
            Gate.Release();
        }
    }

    public async Task Set(string key, string value)
    {
        await Gate.WaitAsync();
        try
        {
            var values = await LoadNoLock();
            if (values.TryGetValue(key, out var existing)
                && string.Equals(existing, value, StringComparison.Ordinal))
                return;

            values[key] = value;
            await SaveNoLock(values);
            Log.Logger.Debug("PKVault progression persisted key={ProgressionKey}", key);
        }
        finally
        {
            Gate.Release();
        }
    }

    private async Task<Dictionary<string, string>> LoadNoLock()
    {
        var result = new Dictionary<string, string>(StringComparer.Ordinal);
        if (!File.Exists(ProgressionPath))
            return result;

        foreach (var line in await File.ReadAllLinesAsync(ProgressionPath))
        {
            if (string.IsNullOrWhiteSpace(line) || line.StartsWith('#'))
                continue;

            var split = line.IndexOf('\t');
            if (split <= 0 || split >= line.Length - 1)
                continue;

            var key = line[..split];
            try
            {
                var raw = Convert.FromBase64String(line[(split + 1)..]);
                result[key] = Encoding.UTF8.GetString(raw);
            }
            catch (FormatException)
            {
                Log.Logger.Warning("Ignoring malformed PKVault progression entry {ProgressionKey}", key);
            }
        }

        return result;
    }

    private async Task SaveNoLock(Dictionary<string, string> values)
    {
        var directory = Path.GetDirectoryName(ProgressionPath);
        if (!string.IsNullOrWhiteSpace(directory))
            Directory.CreateDirectory(directory);

        var lines = new List<string> { "# PKVault progression v1" };
        lines.AddRange(values
            .OrderBy(x => x.Key, StringComparer.Ordinal)
            .Select(x => $"{x.Key}\t{Convert.ToBase64String(Encoding.UTF8.GetBytes(x.Value))}"));

        var temp = ProgressionPath + ".tmp";
        await File.WriteAllLinesAsync(temp, lines);
        File.Move(temp, ProgressionPath, overwrite: true);
    }
}
''', encoding="utf-8")

# Register one persistent store shared by Quest + Contract services.
program_path = root / "PKVault.Core/Program.cs"
program = program_path.read_text(encoding="utf-8")
program = rep(
    program,
    """        services.AddSingleton<DataService>();
        services.AddSingleton<IPkmConvertService, PkmConvertService>();
""",
    """        services.AddSingleton<DataService>();
        services.AddSingleton<ProgressionFileStore>();
        services.AddSingleton<IPkmConvertService, PkmConvertService>();
""",
    "ProgressionFileStore registration",
)
program_path.write_text(program, encoding="utf-8")

# ---------------------------------------------------------------------------
# QuestService: progression file is the source of truth.
# Existing session/main DB values are migrated into it on first read.
# ---------------------------------------------------------------------------
quest_path = root / "PKVault.Core/quest/QuestService.cs"
quest = quest_path.read_text(encoding="utf-8")

quest = rep(
    quest,
    """    MainCreateBoxAction mainCreateBoxAction,
    ISessionService sessionService
)
""",
    """    MainCreateBoxAction mainCreateBoxAction,
    ISessionService sessionService,
    ProgressionFileStore progressionStore
)
""",
    "QuestService progression dependency",
)

quest = rep(
    quest,
    """        var identityReady = string.Equals((await metaLoader.GetEntity(MetaKey.QUEST_PKM_IDENTITIES_READY))?.Value, "1", StringComparison.Ordinal);
""",
    """        var identityReady = string.Equals(await LoadMetaValue(MetaKey.QUEST_PKM_IDENTITIES_READY), "1", StringComparison.Ordinal);
""",
    "Quest identity-ready persistent read",
)

quest = rep(
    quest,
    """        var entity = await metaLoader.GetEntity(MetaKey.QUEST_DAILY_STATE);
        if (entity is null || string.IsNullOrWhiteSpace(entity.Value))
            return state;

        var lines = entity.Value.Split('\\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
""",
    """        var persisted = await LoadMetaValue(MetaKey.QUEST_DAILY_STATE);
        if (string.IsNullOrWhiteSpace(persisted))
            return state;

        var lines = persisted.Split('\\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
""",
    "Quest daily state persistent read",
)

quest = rep(
    quest,
    """        var entity = await metaLoader.GetEntity(key);
        var result = new Dictionary<string, int>(StringComparer.Ordinal);
        if (entity is null || string.IsNullOrWhiteSpace(entity.Value))
            return result;

        foreach (var line in entity.Value.Split('\\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
""",
    """        var persisted = await LoadMetaValue(key);
        var result = new Dictionary<string, int>(StringComparer.Ordinal);
        if (string.IsNullOrWhiteSpace(persisted))
            return result;

        foreach (var line in persisted.Split('\\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
""",
    "Quest int-map persistent read",
)

quest = rep(
    quest,
    """        var entity = await metaLoader.GetEntity(key);
        if (entity is null || string.IsNullOrWhiteSpace(entity.Value))
            return new(StringComparer.Ordinal);

        return entity.Value
""",
    """        var persisted = await LoadMetaValue(key);
        if (string.IsNullOrWhiteSpace(persisted))
            return new(StringComparer.Ordinal);

        return persisted
""",
    "Quest string-set persistent read",
)

old_save = """    private async Task SaveMetaValue(MetaKey key, string value)
    {
        var entity = await metaLoader.GetEntity(key);
        var changed = false;
        if (entity is null)
        {
            await metaLoader.AddEntity(new() { Key = key, Value = value });
            changed = true;
        }
        else if (!string.Equals(entity.Value, value, StringComparison.Ordinal))
        {
            entity.Value = value;
            await metaLoader.UpdateEntity(entity);
            changed = true;
        }

        if (changed)
            await PersistMetaToMainDb(key, value);
    }
"""
new_save = """    private async Task<string?> LoadMetaValue(MetaKey key)
    {
        var fileValue = await progressionStore.Get(key.ToString());
        if (fileValue is not null)
            return fileValue;

        var entity = await metaLoader.GetEntity(key);
        if (entity is not null)
            await progressionStore.Set(key.ToString(), entity.Value);
        return entity?.Value;
    }

    private async Task SaveMetaValue(MetaKey key, string value)
    {
        // File first: even if a session reload starts at this exact moment,
        // progression is already durable and cannot be discarded.
        await progressionStore.Set(key.ToString(), value);

        try
        {
            var entity = await metaLoader.GetEntity(key);
            var changed = false;
            if (entity is null)
            {
                await metaLoader.AddEntity(new() { Key = key, Value = value });
                changed = true;
            }
            else if (!string.Equals(entity.Value, value, StringComparison.Ordinal))
            {
                entity.Value = value;
                await metaLoader.UpdateEntity(entity);
                changed = true;
            }

            if (changed)
                await PersistMetaToMainDb(key, value);
        }
        catch (IOException ex)
        {
            Log.Logger.Warning(ex, "Session DB was reloading; quest progression is safe in pkvault-progression.dat");
        }
    }
"""
quest = rep(quest, old_save, new_save, "Quest durable SaveMetaValue")
quest_path.write_text(quest, encoding="utf-8")

# ---------------------------------------------------------------------------
# ContractService: same dedicated file source of truth + stable board seed.
# ---------------------------------------------------------------------------
contract_path = root / "PKVault.Core/contract/ContractService.cs"
contract = contract_path.read_text(encoding="utf-8")

contract = rep(
    contract,
    """    IPkmVariantLoader pkmVariantLoader,
    ISessionService sessionService
)
""",
    """    IPkmVariantLoader pkmVariantLoader,
    ISessionService sessionService,
    ProgressionFileStore progressionStore
)
""",
    "ContractService progression dependency",
)

contract = rep(
    contract,
    """        var userId = await metaLoader.GetUserId();
        await PersistMetaToMainDb(MetaKey.USER_ID, userId);
        await PersistProgressionClock();
        var now = DateTime.Now;
""",
    """        var userId = await LoadMetaValue(MetaKey.USER_ID);
        if (string.IsNullOrWhiteSpace(userId))
        {
            userId = await metaLoader.GetUserId();
            await SaveMeta(MetaKey.USER_ID, userId);
        }
        await PersistProgressionClock();
        var now = DateTime.Now;
""",
    "Contract stable persistent seed",
)

contract = rep(
    contract,
    """        var value = (await metaLoader.GetEntity(MetaKey.CONTRACT_TRACKER_STATE))?.Value;
""",
    """        var value = await LoadMetaValue(MetaKey.CONTRACT_TRACKER_STATE);
""",
    "Contract tracker persistent read",
)

contract = rep(
    contract,
    """        var value = (await metaLoader.GetEntity(MetaKey.CONTRACT_STATE))?.Value;
""",
    """        var value = await LoadMetaValue(MetaKey.CONTRACT_STATE);
""",
    "Contract store persistent read",
)

old_contract_save = """    private async Task SaveMeta(MetaKey key, string value)
    {
        var entity = await metaLoader.GetEntity(key);
        var changed = false;
        if (entity is null)
        {
            await metaLoader.AddEntity(new() { Key = key, Value = value });
            changed = true;
        }
        else if (!string.Equals(entity.Value, value, StringComparison.Ordinal))
        {
            entity.Value = value;
            await metaLoader.UpdateEntity(entity);
            changed = true;
        }

        if (changed)
            await PersistMetaToMainDb(key, value);
    }
"""
new_contract_save = """    private async Task<string?> LoadMetaValue(MetaKey key)
    {
        var fileValue = await progressionStore.Get(key.ToString());
        if (fileValue is not null)
            return fileValue;

        var entity = await metaLoader.GetEntity(key);
        if (entity is not null)
            await progressionStore.Set(key.ToString(), entity.Value);
        return entity?.Value;
    }

    private async Task SaveMeta(MetaKey key, string value)
    {
        await progressionStore.Set(key.ToString(), value);

        try
        {
            var entity = await metaLoader.GetEntity(key);
            var changed = false;
            if (entity is null)
            {
                await metaLoader.AddEntity(new() { Key = key, Value = value });
                changed = true;
            }
            else if (!string.Equals(entity.Value, value, StringComparison.Ordinal))
            {
                entity.Value = value;
                await metaLoader.UpdateEntity(entity);
                changed = true;
            }

            if (changed)
                await PersistMetaToMainDb(key, value);
        }
        catch (IOException ex)
        {
            Log.Logger.Warning(ex, "Session DB was reloading; contract progression is safe in pkvault-progression.dat");
        }
    }
"""
contract = rep(contract, old_contract_save, new_contract_save, "Contract durable SaveMeta")
contract_path.write_text(contract, encoding="utf-8")

# ---------------------------------------------------------------------------
# Persist quest-toast seen IDs in the UI as a second line of defense against
# permanent-achievement notification replay.
# ---------------------------------------------------------------------------
toast_path = root / "frontend/src/quests/quest-toast.tsx"
toast = toast_path.read_text(encoding="utf-8")
toast = rep(
    toast,
    """export const QuestToast: React.FC = () => {
""",
    """const seenStorageKey = 'pkvault-quest-toast-seen-v1';

const loadSeenCompletionIds = () => {
  try {
    const raw = window.localStorage.getItem(seenStorageKey);
    const parsed = raw ? JSON.parse(raw) : [];
    return new Set<string>(Array.isArray(parsed) ? parsed.filter(x => typeof x === 'string') : []);
  } catch {
    return new Set<string>();
  }
};

const persistSeenCompletionIds = (seen: Set<string>) => {
  try {
    window.localStorage.setItem(seenStorageKey, JSON.stringify(Array.from(seen).slice(-5000)));
  } catch {
    // Backend progression persistence remains authoritative.
  }
};

export const QuestToast: React.FC = () => {
""",
    "toast persistent seen helpers",
)

toast = rep(
    toast,
    """  const seen = React.useRef(new Set<string>());
""",
    """  const seen = React.useRef(loadSeenCompletionIds());
""",
    "toast persistent seen initialization",
)

toast = rep(
    toast,
    """    incoming.forEach(item => seen.current.add(item.id));
    setQueue(old => [...old, ...incoming]);
""",
    """    incoming.forEach(item => seen.current.add(item.id));
    persistSeenCompletionIds(seen.current);
    setQueue(old => [...old, ...incoming]);
""",
    "toast persistent seen write",
)
toast_path.write_text(toast, encoding="utf-8")

# ---------------------------------------------------------------------------
# Reload safety: stop quest/contract polling before SessionService deletes the
# disposable DB. The user's log showed polling holding pkvault-session.db open.
# ---------------------------------------------------------------------------
header_path = root / "frontend/src/header/header.tsx"
header = header_path.read_text(encoding="utf-8")
header = rep(
    header,
    """                    onClick={async () => {
                        await savesScanMutation.mutateAsync();
                        window.dispatchEvent(new Event('pkvault:reload-all'));
                    }}
""",
    """                    onClick={async () => {
                        window.dispatchEvent(new Event('pkvault:reload-start'));
                        try {
                            await savesScanMutation.mutateAsync();
                            window.dispatchEvent(new Event('pkvault:reload-all'));
                        } finally {
                            window.dispatchEvent(new Event('pkvault:reload-end'));
                        }
                    }}
""",
    "reload start/end events",
)
header_path.write_text(header, encoding="utf-8")

quest_page_path = root / "frontend/src/quests/quest-page.tsx"
qp = quest_page_path.read_text(encoding="utf-8")
qp = rep(
    qp,
    """export const QuestPage: React.FC = () => {
  const queryClient = useQueryClient();
  const query = useQuery({
""",
    """export const QuestPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [reloadPaused, setReloadPaused] = React.useState(false);

  React.useEffect(() => {
    const start = () => setReloadPaused(true);
    const end = () => setReloadPaused(false);
    window.addEventListener('pkvault:reload-start', start);
    window.addEventListener('pkvault:reload-end', end);
    return () => {
      window.removeEventListener('pkvault:reload-start', start);
      window.removeEventListener('pkvault:reload-end', end);
    };
  }, []);

  const query = useQuery({
""",
    "QuestPage reload pause state",
)
qp = rep(
    qp,
    """    queryKey: ['quest-state'],
    queryFn: loadQuestState,
    refetchInterval: 1500,
  });
""",
    """    queryKey: ['quest-state'],
    queryFn: loadQuestState,
    enabled: !reloadPaused,
    refetchInterval: reloadPaused ? false : 1500,
  });
""",
    "QuestPage quest polling pause",
)
qp = rep(
    qp,
    """    queryKey: ['contract-state'],
    queryFn: loadContracts,
    refetchInterval: 1500,
  });
""",
    """    queryKey: ['contract-state'],
    queryFn: loadContracts,
    enabled: !reloadPaused,
    refetchInterval: reloadPaused ? false : 1500,
  });
""",
    "QuestPage contract polling pause",
)
quest_page_path.write_text(qp, encoding="utf-8")

toast = toast_path.read_text(encoding="utf-8")
toast = rep(
    toast,
    """export const QuestToast: React.FC = () => {
  const query = useQuery({
""",
    """export const QuestToast: React.FC = () => {
  const [reloadPaused, setReloadPaused] = React.useState(false);

  React.useEffect(() => {
    const start = () => setReloadPaused(true);
    const end = () => setReloadPaused(false);
    window.addEventListener('pkvault:reload-start', start);
    window.addEventListener('pkvault:reload-end', end);
    return () => {
      window.removeEventListener('pkvault:reload-start', start);
      window.removeEventListener('pkvault:reload-end', end);
    };
  }, []);

  const query = useQuery({
""",
    "QuestToast reload pause state",
)
toast = rep(
    toast,
    """    queryKey: ['quest-state'],
    queryFn: loadQuestState,
    refetchInterval: 1500,
  });
""",
    """    queryKey: ['quest-state'],
    queryFn: loadQuestState,
    enabled: !reloadPaused,
    refetchInterval: reloadPaused ? false : 1500,
  });
""",
    "QuestToast polling pause",
)
toast_path.write_text(toast, encoding="utf-8")

print("PKVault V8 alpha52i dedicated progression file + reload-safe polling applied")

from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text, old, new, label):
    if old not in text:
        raise RuntimeError(f"alpha52h1 anchor not found: {label}")
    return text.replace(old, new, 1)

meta_path = root / "PKVault.Core/db/entity/MetaEntity.cs"
meta = meta_path.read_text(encoding="utf-8")
meta = rep(meta,
"""    CONTRACT_STATE,
    CONTRACT_TRACKER_STATE,
}
""",
"""    CONTRACT_STATE,
    CONTRACT_TRACKER_STATE,
    PROGRESSION_CLOCK_STATE,
}
""",
"clock meta key")
meta_path.write_text(meta, encoding="utf-8")

q = root / "PKVault.Core/quest/QuestService.cs"
text = q.read_text(encoding="utf-8")
text = rep(text,
"""using System.Text;
using PKHeX.Core;
""",
"""using System.Text;
using Microsoft.Data.Sqlite;
using PKHeX.Core;
""",
"sqlite import")
text = rep(text,
"""    IPkmVariantLoader pkmVariantLoader,
    MainCreateBoxAction mainCreateBoxAction
)
""",
"""    IPkmVariantLoader pkmVariantLoader,
    MainCreateBoxAction mainCreateBoxAction,
    ISessionService sessionService
)
""",
"session dependency")
text = rep(text,
"""        var today = Today();
        var daily = await LoadDailyState(today);
""",
"""        var today = Today();
        await PersistProgressionClock();
        var daily = await LoadDailyState(today);
""",
"clock call")
text = rep(text,
"""            if (cost > 0)
            {
                await itemBankService.SpendMoneyBank(cost);
                daily.PaidRerolls++;
            }
""",
"""            if (cost > 0)
            {
                await itemBankService.ApplyProgressionMoneyDelta(-cost);
                daily.PaidRerolls++;
            }
""",
"reroll money")

old = """    private async Task SaveMetaValue(MetaKey key, string value)
    {
        var entity = await metaLoader.GetEntity(key);
        if (entity is null)
        {
            await metaLoader.AddEntity(new()
            {
                Key = key,
                Value = value,
            });
        }
        else if (!string.Equals(entity.Value, value, StringComparison.Ordinal))
        {
            entity.Value = value;
            await metaLoader.UpdateEntity(entity);
        }
    }
"""
new = """    private async Task SaveMetaValue(MetaKey key, string value)
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

    private async Task PersistMetaToMainDb(MetaKey key, string value)
    {
        if (!File.Exists(sessionService.MainDbPath))
            return;

        await using var connection = new SqliteConnection($"Data Source={sessionService.MainDbPath}");
        await connection.OpenAsync();
        await using var command = connection.CreateCommand();
        command.CommandText = "INSERT INTO Metas (Key, Value) VALUES ($key, $value) ON CONFLICT(Key) DO UPDATE SET Value = excluded.Value;";
        command.Parameters.AddWithValue("$key", (int)key);
        command.Parameters.AddWithValue("$value", value);
        await command.ExecuteNonQueryAsync();
    }

    private async Task PersistProgressionClock()
    {
        var now = DateTimeOffset.Now;
        var local = now.LocalDateTime;
        var startUtc = sessionService.StartTime ?? DateTime.UtcNow;
        var startLocal = new DateTimeOffset(DateTime.SpecifyKind(startUtc, DateTimeKind.Utc)).ToLocalTime();
        var weekKey = $"{ISOWeek.GetYear(local):0000}-W{ISOWeek.GetWeekOfYear(local):00}";
        var value = string.Join('\\n',
            "version=1",
            $"sessionStartedLocal={startLocal:O}",
            $"timeZoneId={TimeZoneInfo.Local.Id}",
            $"utcOffsetMinutes={(int)now.Offset.TotalMinutes}",
            $"dailyKey={local:yyyy-MM-dd}",
            $"weeklyKey={weekKey}");
        await SaveMetaValue(MetaKey.PROGRESSION_CLOCK_STATE, value);
    }
"""
text = rep(text, old, new, "committed quest meta")
q.write_text(text, encoding="utf-8")

print("alpha52h1 quest persistence applied")

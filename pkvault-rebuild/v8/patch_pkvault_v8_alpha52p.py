from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def rep(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"alpha52p anchor not found: {label}")
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# CRITICAL: MetaKey values are persisted as INTEGER PRIMARY KEY values in
# pkvault.db. Never insert a new enum member between existing keys.
#
# alpha52m accidentally inserted ITEM_BANK_PAGE_NAMES at ordinal 5, shifting
# money/quest/contract IDs by +1. Old DBs therefore still had money at key 6
# while newer builds looked at key 7 and displayed ₽0.
#
# Pin every historical key explicitly forever. New keys append after 23.
# ---------------------------------------------------------------------------
meta_path = root / "PKVault.Core/db/entity/MetaEntity.cs"
meta = meta_path.read_text(encoding="utf-8")

old_enum = """public enum MetaKey
{
    APP_VERSION,
    USER_ID,
    ITEM_BANK,
    ITEM_BANK_PAGES,
    ITEM_BANK_PAGE_SIZES,
    ITEM_BANK_PAGE_NAMES,
    ITEM_SAVE_PROVENANCE,
    POKE_DOLLAR_BANK,
    QUEST_COMPLETED,
    QUEST_CAUGHT_HISTORY,
    QUEST_PKM_FINGERPRINTS,
    QUEST_DAILY_STATE,
    QUEST_PLAYTIME_SNAPSHOTS,
    QUEST_MONEY_REWARDS,
    QUEST_PKM_IDENTITIES,
    QUEST_PKM_IDENTITIES_READY,
    QUEST_PKM_LEVELS,
    QUEST_PKM_SPECIES_BY_ID,
    QUEST_EVOLUTION_EVENTS,
    QUEST_SHINY_IDENTITIES,
    QUEST_SHINY_SPECIES,
    QUEST_UNOWN_FORMS,
    CONTRACT_STATE,
    CONTRACT_TRACKER_STATE,
    PROGRESSION_CLOCK_STATE,
}
"""

new_enum = """public enum MetaKey
{
    APP_VERSION = 0,
    USER_ID = 1,
    ITEM_BANK = 2,
    ITEM_BANK_PAGES = 3,
    ITEM_BANK_PAGE_SIZES = 4,
    ITEM_SAVE_PROVENANCE = 5,
    POKE_DOLLAR_BANK = 6,
    QUEST_COMPLETED = 7,
    QUEST_CAUGHT_HISTORY = 8,
    QUEST_PKM_FINGERPRINTS = 9,
    QUEST_DAILY_STATE = 10,
    QUEST_PLAYTIME_SNAPSHOTS = 11,
    QUEST_MONEY_REWARDS = 12,
    QUEST_PKM_IDENTITIES = 13,
    QUEST_PKM_IDENTITIES_READY = 14,
    QUEST_PKM_LEVELS = 15,
    QUEST_PKM_SPECIES_BY_ID = 16,
    QUEST_EVOLUTION_EVENTS = 17,
    QUEST_SHINY_IDENTITIES = 18,
    QUEST_SHINY_SPECIES = 19,
    QUEST_UNOWN_FORMS = 20,
    CONTRACT_STATE = 21,
    CONTRACT_TRACKER_STATE = 22,
    PROGRESSION_CLOCK_STATE = 23,

    // Added after the historical IDs above were already persisted in user DBs.
    // Future MetaKeys MUST be appended with explicit values.
    ITEM_BANK_PAGE_NAMES = 24,
}
"""

meta = rep(meta, old_enum, new_enum, "pinned MetaKey values")
meta_path.write_text(meta, encoding="utf-8")

# ---------------------------------------------------------------------------
# Money migration guard.
#
# Canonical old/current layout:
#   key 6 = Pokédollar bank
#
# Broken alpha52m-o layout:
#   key 7 = Pokédollar bank
#
# If canonical key 6 is missing/non-numeric but raw key 7 is numeric, recover
# it into key 6. If key 6 is already numeric, NEVER replace it: that is the
# user's original balance and is the most trustworthy value.
# ---------------------------------------------------------------------------
item_path = root / "PKVault.Core/storage/services/ItemBankService.cs"
item = item_path.read_text(encoding="utf-8")

item = rep(
    item,
    """    private async Task<long> LoadMoneyBank()
    {
        var entity = await metaLoader.GetEntity(MetaKey.POKE_DOLLAR_BANK);
        if (entity is not null && long.TryParse(entity.Value, out var value))
            return Math.Clamp(value, 0, MaxMoneyBank);

        // Test packages can opt into a one-time starting balance without shipping
""",
    """    private async Task<long> LoadMoneyBank()
    {
        var entity = await metaLoader.GetEntity(MetaKey.POKE_DOLLAR_BANK);
        if (entity is not null && long.TryParse(entity.Value, out var value))
            return Math.Clamp(value, 0, MaxMoneyBank);

        // alpha52m-o temporarily shifted MetaKey ordinals by inserting page names
        // before the money key. Recover a numeric balance written under raw key 7
        // only when canonical key 6 is absent/non-numeric.
        var shiftedMoney = await TryLoadShiftedMoneyBank();
        if (shiftedMoney is not null)
        {
            await SaveMoneyBank(shiftedMoney.Value);
            return shiftedMoney.Value;
        }

        // Test packages can opt into a one-time starting balance without shipping
""",
    "money recovery call",
)

item = rep(
    item,
    """    private async Task SaveMoneyBank(long value)
    {
""",
    """    private async Task<long?> TryLoadShiftedMoneyBank()
    {
        if (!File.Exists(sessionService.SessionDbPath))
            return null;

        try
        {
            await using var connection = new SqliteConnection(
                $"Data Source={sessionService.SessionDbPath};Mode=ReadOnly;Pooling=False"
            );
            await connection.OpenAsync();
            await using var command = connection.CreateCommand();
            command.CommandText = "SELECT Value FROM Metas WHERE Key = 7 LIMIT 1;";
            var raw = await command.ExecuteScalarAsync();
            if (raw is string text
                && long.TryParse(text, NumberStyles.Integer, CultureInfo.InvariantCulture, out var value))
            {
                return Math.Clamp(value, 0, MaxMoneyBank);
            }
        }
        catch (SqliteException)
        {
            // Normal startup/session recreation can briefly make the session DB
            // unavailable. Canonical key 6 will be tried again on the next load.
        }

        return null;
    }

    private async Task SaveMoneyBank(long value)
    {
""",
    "shifted money recovery helper",
)

# ---------------------------------------------------------------------------
# Page-name migration.
#
# During the broken enum window, page names were stored at raw key 5. Key 5 is
# historically ITEM_SAVE_PROVENANCE, so only migrate it when the value actually
# parses as Dictionary<int,string>. Never overwrite real provenance data.
# ---------------------------------------------------------------------------
item = rep(
    item,
    """    private async Task<Dictionary<int, string>> LoadPageNames()
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
""",
    """    private async Task<Dictionary<int, string>> LoadPageNames()
    {
        var entity = await metaLoader.GetEntity(MetaKey.ITEM_BANK_PAGE_NAMES);
        if (entity is not null && !string.IsNullOrWhiteSpace(entity.Value))
        {
            try
            {
                return JsonSerializer.Deserialize<Dictionary<int, string>>(
                    entity.Value,
                    JsonOptions
                ) ?? [];
            }
            catch (JsonException)
            {
                // Fall through to one-time broken-layout migration.
            }
        }

        var migrated = await TryLoadShiftedPageNames();
        if (migrated.Count > 0)
        {
            await SavePageNames(migrated);
            return migrated;
        }

        return [];
    }

    private async Task<Dictionary<int, string>> TryLoadShiftedPageNames()
    {
        var oldSlot = await metaLoader.GetEntity(MetaKey.ITEM_SAVE_PROVENANCE);
        if (oldSlot is null || string.IsNullOrWhiteSpace(oldSlot.Value))
            return [];

        try
        {
            var names = JsonSerializer.Deserialize<Dictionary<int, string>>(
                oldSlot.Value,
                JsonOptions
            ) ?? [];

            return names
                .Where(x => x.Key > 0 && !string.IsNullOrWhiteSpace(x.Value))
                .ToDictionary(x => x.Key, x => x.Value);
        }
        catch (JsonException)
        {
            // Real ITEM_SAVE_PROVENANCE has string keys and origin arrays and must
            // never be treated as page names.
            return [];
        }
    }
""",
    "page name migration",
)

item_path.write_text(item, encoding="utf-8")

print("PKVault V8 alpha52p pinned MetaKey IDs + Pokédollar recovery applied")

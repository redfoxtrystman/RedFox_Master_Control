from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit('usage: patch_pkvault_gen1.py <pkvault-root> <pkhex-root>')

PKVAULT = Path(sys.argv[1]).resolve()
PKHEX = Path(sys.argv[2]).resolve()

def replace_once(path: Path, old: str, new: str):
    text = path.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{path}: expected exactly one match, found {count}\n--- needle ---\n{old[:800]}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')
    print(f'patched {path}')

poke = PKHEX / 'PKHeX.Core/PKM/Shared/PokeList1.cs'
replace_once(poke,
'''    public static byte GetHeaderIdentifierMark(PK1 pk)
    {
        var species = pk.SpeciesInternal;
        if (species == 0)
            return SlotEmpty;
        // Let out-of-bounds species fall through.
        return species;
    }
''',
'''    public static bool IsRawZeroGlitch(PK1 pk)
    {
        if (pk.SpeciesInternal != 0)
            return false;
        // Only the stored 0x21-byte body decides raw-00 occupancy. Party-only
        // stats are intentionally ignored so a blank slot mutated by party
        // stat calculation never becomes a phantom Pokemon.
        return pk.Data[..PokeCrypto.SIZE_1STORED].ContainsAnyExcept<byte>(0);
    }

    public static bool IsMissingNo50(PK1 pk) => pk.SpeciesInternal == 0x50;

    public static bool IsKnownGen1Glitch(PK1 pk) => IsRawZeroGlitch(pk) || IsMissingNo50(pk);

    public static bool IsOccupied(PK1 pk) => pk.SpeciesInternal != 0 || IsRawZeroGlitch(pk);

    public static bool IsSingleSlotOccupied(ReadOnlySpan<byte> single)
    {
        if (single.Length < 3 + PokeCrypto.SIZE_1STORED)
            return false;

        var marker = single[1];
        if (marker == SlotEmpty)
            return false;
        if (marker != 0)
            return true;

        return single.Slice(3, PokeCrypto.SIZE_1STORED).ContainsAnyExcept<byte>(0);
    }

    public static byte GetHeaderIdentifierMark(PK1 pk)
    {
        var species = pk.SpeciesInternal;
        if (species == 0 && !IsRawZeroGlitch(pk))
            return SlotEmpty;
        // Raw 00 is deliberately retained for an occupied Gen-1 glitch slot.
        // Let other out-of-bounds species fall through unchanged.
        return species;
    }
''')

replace_once(poke,
'''    public static int CountPresent(ReadOnlySpan<byte> input, int capacity, int lerp = 0)
    {
        var count = 0;
        for (int i = 0; i < capacity; i++)
        {
            var mark = input[(i * lerp) + 1];
            if (IsPresent(mark))
                count++;
        }
        return count;
    }
''',
'''    public static int CountPresent(ReadOnlySpan<byte> input, int capacity, int lerp = 0)
    {
        var count = 0;
        for (int i = 0; i < capacity; i++)
        {
            if (lerp > 0)
            {
                var offset = i * lerp;
                if (offset < input.Length && IsSingleSlotOccupied(input[offset..]))
                    count++;
                continue;
            }

            var mark = input[1 + i];
            if (IsPresent(mark))
                count++;
        }
        return count;
    }
''')

replace_once(poke,
'''        for (int i = 0; i < capacity; i++)
        {
            var mark = input[1 + i];
            bool present = IsPresent(mark);
            if (present != (i < count))
                return false;
        }
''',
'''        for (int i = 0; i < capacity; i++)
        {
            var mark = input[1 + i];
            var expectedPresent = i < count;
            // A raw-00 header is legal only inside the occupied prefix. The
            // body-level glitch check happens once the PK1 is materialized.
            bool present = IsPresent(mark) || (mark == 0 && expectedPresent);
            if (present != expectedPresent)
                return false;
        }
''')

replace_once(poke,
'''        output[1 + index] = GetHeaderIdentifierMark(pk);
        output[0] = (byte)CountPresent(output, capacity);
        output[1 + capacity] = SlotEmpty; // cap off the list
''',
'''        output[1 + index] = GetHeaderIdentifierMark(pk);

        // Count normal markers normally, but treat raw-00 as occupied only
        // when its stored Gen-1 body is actually populated.
        var count = 0;
        for (int i = 0; i < capacity; i++)
        {
            var marker = output[1 + i];
            if (IsPresent(marker))
            {
                count++;
                continue;
            }
            if (marker != 0)
                continue;

            var bodyOffset = start + (sizeBody * i);
            if (output.Slice(bodyOffset, PokeCrypto.SIZE_1STORED).ContainsAnyExcept<byte>(0))
                count++;
        }
        output[0] = (byte)count;
        output[1 + capacity] = SlotEmpty; // cap off the list
''')

replace_once(poke,
'''        int count = CountPresent(input, capacity, size);
        if (count == 0 && (!isDestInitialized || !output.ContainsAnyExcept<byte>(0)))
            return false; // No need to merge if all empty and dest is not initialized.
''',
'''        int count = 0;
        for (int i = 0; i < capacity; i++)
        {
            var single = input.Slice(i * size, size);
            if (IsSingleSlotOccupied(single))
                count++;
        }
        if (count == 0 && (!isDestInitialized || !output.ContainsAnyExcept<byte>(0)))
            return false; // No need to merge if all empty and dest is not initialized.
''')

replace_once(poke,
'''            var single = input.Slice(i * size, size);
            var marker = single[1]; // assume correct, don't look in body data.
            if (marker is 0) // Ensure deleted (zeroed) slots act as an Empty (FF) slot.
                marker = SlotEmpty;

            var index = IsPresent(marker) ? ctr++ : emptyIndex++;
            output[1 + index] = marker;
''',
'''            var single = input.Slice(i * size, size);
            var present = IsSingleSlotOccupied(single);
            var marker = present ? single[1] : SlotEmpty;

            var index = present ? ctr++ : emptyIndex++;
            output[1 + index] = marker;
''')

savefile = PKHEX / 'PKHeX.Core/Saves/SaveFile.cs'
replace_once(savefile,
'''    private const int MaxPartyCount = 6;

    public IList<PKM> PartyData
''',
'''    private const int MaxPartyCount = 6;

    private static bool IsPartySlotOccupied(PKM pk)
        => pk.Species != 0 || (pk is PK1 pk1 && PokeList1.IsKnownGen1Glitch(pk1));

    public IList<PKM> PartyData
''')
replace_once(savefile,
'''            foreach (var exist in value.Where(pk => pk.Species != 0))
                SetPartySlotAtIndex(exist, ctr++);
''',
'''            foreach (var exist in value.Where(IsPartySlotOccupied))
                SetPartySlotAtIndex(exist, ctr++);
''')
replace_once(savefile,
'''    public void SetBoxSlotAtIndex(PKM pk, int box, int slot, EntityImportSettings settings = default)
        => SetBoxSlot(pk, BoxBuffer[GetBoxSlotOffset(box, slot)..], settings);

    public void SetBoxSlotAtIndex(PKM pk, int index, EntityImportSettings settings = default)
        => SetBoxSlot(pk, BoxBuffer[GetBoxSlotOffset(index)..], settings);
''',
'''    private bool TryClearBlankGen1BoxSlot(PKM pk, Span<byte> data)
    {
        if (pk is not PK1 pk1 || PokeList1.IsOccupied(pk1))
            return false;

        // Canonical empty single-slot Gen-1 list. Write it directly instead of
        // entering the normal import path, which normalizes a blank PK1 into
        // level 1 and makes the raw-00 detector think it is MissingNo.
        data[..SIZE_BOXSLOT].Clear();
        data[1] = PokeList1.SlotEmpty;
        data[2] = PokeList1.SlotEmpty;
        return true;
    }

    public void SetBoxSlotAtIndex(PKM pk, int box, int slot, EntityImportSettings settings = default)
    {
        var data = BoxBuffer[GetBoxSlotOffset(box, slot)..];
        if (TryClearBlankGen1BoxSlot(pk, data))
            return;
        SetBoxSlot(pk, data, settings);
    }

    public void SetBoxSlotAtIndex(PKM pk, int index, EntityImportSettings settings = default)
    {
        var data = BoxBuffer[GetBoxSlotOffset(index)..];
        if (TryClearBlankGen1BoxSlot(pk, data))
            return;
        SetBoxSlot(pk, data, settings);
    }
''')

replace_once(savefile,
'''        int currentCount = PartyCount;
        if (pk.Species != 0)
        {
            if (currentCount <= index)
                PartyCount = index + 1;
        }
        else if (currentCount > index)
        {
            PartyCount = index;
        }

        SetPartySlot(pk, GetPartySpan(index), settings);
''',
'''        int currentCount = PartyCount;
        var occupied = IsPartySlotOccupied(pk);
        if (occupied)
        {
            if (currentCount <= index)
                PartyCount = index + 1;
        }
        else if (currentCount > index)
        {
            PartyCount = index;
        }

        // Do not send an actually blank PK1 through party-stat mutation. That
        // was the source of the phantom Lv.1 '?' slot fixed after v3.
        if (!occupied && pk is PK1)
        {
            GetPartySpan(index)[..SIZE_PARTY].Clear();
            return;
        }

        SetPartySlot(pk, GetPartySpan(index), settings);
''')

replace_once(savefile,
'''    public void SetBoxSlot(PKM pk, Span<byte> data, EntityImportSettings settings = default)
    {
        if (pk.GetType() != PKMType)
            throw new ArgumentException($"PKM Format needs to be {PKMType} when setting to this Save File.");

        UpdatePKM(pk, isParty: false, settings);
        SetPartyValues(pk, isParty: false);
        WriteSlotBox(pk, data);
    }
''',
'''    public void SetBoxSlot(PKM pk, Span<byte> data, EntityImportSettings settings = default)
    {
        if (pk.GetType() != PKMType)
            throw new ArgumentException($"PKM Format needs to be {PKMType} when setting to this Save File.");

        // A genuinely blank Gen-1 PK1 must be serialized before update hooks
        // can normalize it into a non-zero body. Otherwise the raw-00 glitch
        // detector sees the mutated blank as occupied and resurrects it.
        if (pk is PK1 pk1 && !PokeList1.IsOccupied(pk1))
        {
            WriteSlotBox(pk, data);
            return;
        }

        UpdatePKM(pk, isParty: false, settings);
        SetPartyValues(pk, isParty: false);
        WriteSlotBox(pk, data);
    }
''')

sav1 = PKHEX / 'PKHeX.Core/Saves/SAV1.cs'
replace_once(sav1,
'''            int count = PokeList1.CountPresent(src, boxSlotCount);
''',
'''            int count = PokeList1.CountPresent(src, boxSlotCount, SIZE_STORED);
''')
replace_once(sav1,
'''    public override bool IsPKMPresent(ReadOnlySpan<byte> data) => EntityDetection.IsPresentGB(data);
''',
'''    public override bool IsPKMPresent(ReadOnlySpan<byte> data) => PokeList1.IsSingleSlotOccupied(data);
''')

imm = PKVAULT / 'PKVault.Core/storage/wrapper/ImmutablePKM.cs'
replace_once(imm,
'''    public bool IsSpeciesValid => Species > 0 && Species < GameInfo.Strings.Species.Count;

    public PKMLoadError? LoadError => loadError;

    public bool HasLoadError => loadError != null;

    public bool IsEnabled => !HasLoadError && IsSpeciesValid;
''',
'''    public bool IsSpeciesValid => Species > 0 && Species < GameInfo.Strings.Species.Count;

    public bool IsGen1RawZeroGlitch => Pkm is PK1 pk1 && PokeList1.IsRawZeroGlitch(pk1);
    public bool IsGen1MissingNo50 => Pkm is PK1 pk1 && PokeList1.IsMissingNo50(pk1);
    public bool IsGen1Glitch => Pkm is PK1 pk1 && PokeList1.IsKnownGen1Glitch(pk1);

    // General storage occupancy. Normal Pokemon remain normal; only the two
    // explicitly supported Gen-1 glitch families bypass Species==0.
    public bool IsStorageOccupied => IsSpeciesValid || IsGen1Glitch;

    public PKMLoadError? LoadError => loadError;

    public bool HasLoadError => loadError != null;

    public bool IsEnabled => !HasLoadError && IsStorageOccupied;
''')

loader = PKVAULT / 'PKVault.Core/db/loader/save/SavePkmLoader.cs'
text = loader.read_text(encoding='utf-8')
if text.count('.IsSpeciesValid') < 3:
    raise RuntimeError('SavePkmLoader.cs: expected Gen-1 relevant IsSpeciesValid checks')
text = text.replace('.IsSpeciesValid', '.IsStorageOccupied')
loader.write_text(text, encoding='utf-8')
print(f'patched {loader}')

convert = PKVAULT / 'PKVault.Core/storage/services/PkmConvertService/PkmConvertService.cs'
replace_once(convert,
'''    public ImmutablePKM ConvertTo(ImmutablePKM sourcePkm, Type targetPkmType, PKMRndValues? rndValues, SaveFile? targetSave = null)
    {
        Log.Debug($"Convert {sourcePkm.GetMutablePkm().GetType().Name} -> {targetPkmType.Name}");
''',
'''    public ImmutablePKM ConvertTo(ImmutablePKM sourcePkm, Type targetPkmType, PKMRndValues? rndValues, SaveFile? targetSave = null)
    {
        // Supported Gen-1 glitches are intentionally Gen-1-only. Do not run
        // 'M (00) or MissingNo (50) through legality healing or conversion.
        if (sourcePkm.IsGen1Glitch)
        {
            if (targetPkmType != typeof(PK1))
                throw new InvalidOperationException("Gen-1 glitch Pokemon cannot leave Gen 1.");
            return new(sourcePkm.GetMutablePkm().Clone());
        }

        Log.Debug($"Convert {sourcePkm.GetMutablePkm().GetType().Name} -> {targetPkmType.Name}");
''')

wrapper = PKVAULT / 'PKVault.Core/storage/wrapper/SaveWrapper.cs'
replace_once(wrapper,
'''    public bool IsSpeciesAllowed(ushort species)
    {
        return species <= Save.MaxSpeciesID && Save.Personal.IsSpeciesInGame(species);
    }
''',
'''    public bool IsSpeciesAllowed(ushort species)
    {
        // Species 0 is never a normal Pokemon, but an enabled raw-00 PK1
        // glitch is allowed to move between Gen-1 save slots.
        if (species == 0 && Save is SAV1)
            return true;
        return species <= Save.MaxSpeciesID && Save.Personal.IsSpeciesInGame(species);
    }
''')

pfl = PKVAULT / 'PKVault.Core/db/loader/PkmFileLoader.cs'
replace_once(pfl,
'''        var star = pkm.IsShiny ? " ★" : string.Empty;
        var speciesName = GameInfo.Strings.Species[pkm.Species].ToUpperInvariant().Replace(":", "");
        return $"{pkm.Species:0000}{star} - {speciesName} - {id}.{pkm.Extension}";
''',
'''        var star = pkm.IsShiny ? " ★" : string.Empty;
        var speciesName = pkm.IsGen1RawZeroGlitch
            ? "'M-RAW00"
            : pkm.IsGen1MissingNo50
                ? "MISSINGNO-RAW50"
                : GameInfo.Strings.Species[pkm.Species].ToUpperInvariant().Replace(":", "");
        return $"{pkm.Species:0000}{star} - {speciesName} - {id}.{pkm.Extension}";
''')

img = PKVAULT / 'frontend/src/img/species-img.tsx'
replace_once(img,
'''export const SpeciesImg: React.FC<SpeciesImgProps> = ({ species, context, form, isFemale, isShiny, isEgg, isShadow, ...imgProps }) => {
    const staticData = useStaticData();
    const settings = useSettingsGet();

    const usedSpecies = species === 0
        ? 1
        : species;
''',
'''export const SpeciesImg: React.FC<SpeciesImgProps> = ({ species, context, form, isFemale, isShiny, isEgg, isShadow, ...imgProps }) => {
    const staticData = useStaticData();
    const settings = useSettingsGet();

    if (species === 0 && context === EntityContext.Gen1) {
        return <UISpeciesImg
            {...imgProps}
            data-species-id={0}
            data-glitch-species="gen1"
            sheetUrl="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAD7klEQVR42u2cvW7iQBDHx6d0UOTjFXgTP0ROaS3oSQQSRYJyKSIRAT0RbRQegjfhFQIUTs01t9ZmmNl1YnMaS/+fhOxgN3h3vv4zDhEAAAAAAAAAAAAAAAAAAAAAAABghMtW6+Az6M4Og+6sOOff8b+t/Z6zpi3AR56L3w97c5os+sXfk0Wfhr15ce7uARU5MLRdL9036M7MWcCvpi9IaKfzo0XOmvjQ+QP1XU9ooYiIXl5v4UaqsH1/CLoYKSBbdkGNzIK27w8H7ShlP5azoMbFgOzmiYiINss78ai5KcSAmhile7q4ftRvWM+DMQDU5II0N8TjAr+OJ1iRWL6vBWh3RAyoyPLtPprra9/BDdVkAdLO5i6Hf6y6oKSJUoS/o/1jqEJ25y+vtwm2ccUFkHa5C8x+/i/dgzS0BhlilB7n/UREnWxKGyJavk2/1AxQQ08gRWhSQ6gXYLESTpq4AEe73rOGTjYtKmN+vlne0eXvP4gBVQsxKcfn59CCThwHeG4fqgsmiz5qgDpdkJ/Xc2kiJlXjCdaQhsYa7yEXhTS0IrvVmJ7X56JLIiK6are/XNss72i3GhcBGdRkAaGmfGg8BRZQQuspG4R9mcEdNUnCBWL0hL+5wyUfz4Ow/4lZA9LQCNyHS9e5DOG3Jf3dzgU7i5hbAG3yzdd0/ArXr4YRaE/sgvw8P9QZC42nQAsqUWjxNFOzBj4RJ1XH3BVZ6weYW4DLVusQG8B1cUIS4bKbJ7VBQ0SUJAnEuJgLCrUUtRpAE+Osj6c3wgJ4FhPKlD7yXGy8OMvZfn7CAmILIM38uHO3m6UxxFCVbLUSTiy6oFD168ZSeArquLh+DAZnxIASFhDSdKQmi6T5aFYBC/ihFiRlNjzDCV0f9ua0fLs3FwPMiXGjdE9SHeBcyG41JiIirVaQJAf38P/1hGEBsRjg9Hu/ma7JDVos4HSyKX3kOWJAmUo4lONrWZA2De1nTxZHExvXlB+l+yLbGaV72q3GdNVu0241Lt4dyG6ejo7OBSEIl3BBkobDZWXtzUi3QBLP63NoQT+tA/wq2FXKvEKOjR6O0j0Gs8oswHeJ1QF4QeNE8B5wrE6w2BVrTCGmFVf8ofJFcIEZUkRNLkiTINzRF+7cBy7oRGhzobwoszwXaj4L0jpbkuIZy4QsuiBzWlBosEp7uP71UMEVG3mBBShBWFoEKQhLE3Mca4WYOQso668lq4gthsXRxMb3A/iCObnaV00tv6JkfjzdH7rVtH5/h7s+AW/sZ+tzel7b+33m01A+61nWMqT0FJVwhTRUaztq/zNOsxa8KQ8AAAAAAAAAAAAAAAAAAAAAAOB/8RdrIr6c7MaA6QAAAABJRU5ErkJggg=="
            spriteInfos={{ x: 0, y: 0, width: 96, height: 96 }}
            sourceRealHeight={96}
            species={1}
            isShadow={false}
            title="MissingNo / 'M Gen 1 glitch Pokemon"
        />;
    }

    const usedSpecies = species === 0
        ? 1
        : species;
''')


# PKVault direct-IP trading MVP.
TRADING = Path(__file__).resolve().parent / 'trading'

def copy_text(src_name: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text((TRADING / src_name).read_text(encoding='utf-8'), encoding='utf-8')
    print(f'added {dest}')

copy_text('TradingService.cs', PKVAULT / 'PKVault.Core/trading/TradingService.cs')
copy_text('TradingRoute.cs', PKVAULT / 'PKVault.Core/trading/routes/TradingRoute.cs')
copy_text('TradeSwapAction.cs', PKVAULT / 'PKVault.Core/storage/data-action/TradeSwapAction.cs')
copy_text('trading-page.tsx', PKVAULT / 'frontend/src/pages/trading.tsx')
copy_text('trading-route.tsx', PKVAULT / 'frontend/src/routes/trading.tsx')

program = PKVAULT / 'PKVault.Core/Program.cs'
replace_once(program,
'''using PKVault.Core.storage.routes;
using PKVault.Core.warnings.routes;
''',
'''using PKVault.Core.storage.routes;
using PKVault.Core.trading.routes;
using PKVault.Core.warnings.routes;
''')
replace_once(program,
'''        services.AddSingleton<PkmLegalityService>();

        Log.Information($"Setup services - Actions");
''',
'''        services.AddSingleton<PkmLegalityService>();
        services.AddSingleton<TradingService>();

        Log.Information($"Setup services - Actions");
''')
replace_once(program,
'''        services.AddScoped<DexSyncAction>();

        Log.Information($"Setup services - Loaders");
''',
'''        services.AddScoped<DexSyncAction>();
        services.AddScoped<TradeSwapAction>();

        Log.Information($"Setup services - Loaders");
''')
replace_once(program,
'''        services.AddScoped<StaticDataController>();

        Log.Information($"Setup services - Finished");
''',
'''        services.AddScoped<StaticDataController>();
        services.AddScoped<TradingController>();

        Log.Information($"Setup services - Finished");
''')

router = PKVAULT / 'PKVault.Core/router/CoreRouter.cs'
replace_once(router,
'''using PKVault.Core.storage.routes;
using PKVault.Core.warnings.routes;
''',
'''using PKVault.Core.storage.routes;
using PKVault.Core.trading.routes;
using PKVault.Core.warnings.routes;
''')
replace_once(router,
'''        typeof(WarningsController),
        typeof(StaticDataController),
''',
'''        typeof(WarningsController),
        typeof(StaticDataController),
        typeof(TradingController),
''')

route_json = PKVAULT / 'PKVault.Core/router/RouteJsonContext.cs'
replace_once(route_json,
'''[JsonSerializable(typeof(BankEntity.BankViewSave))]

[JsonSerializable(typeof(DesktopMessageRequest))]
''',
'''[JsonSerializable(typeof(BankEntity.BankViewSave))]
[JsonSerializable(typeof(TradeStateDTO))]
[JsonSerializable(typeof(TradeHostPayload))]
[JsonSerializable(typeof(TradeConnectPayload))]
[JsonSerializable(typeof(TradeOfferPayload))]
[JsonSerializable(typeof(TradeReadyPayload))]
[JsonSerializable(typeof(TradePokemonDTO))]
[JsonSerializable(typeof(TradeWireMessage))]
[JsonSerializable(typeof(TradeJournal))]

[JsonSerializable(typeof(DesktopMessageRequest))]
''')

actions = PKVAULT / 'PKVault.Core/storage/services/ActionService.cs'
replace_once(actions,
'''    public async Task<DataUpdateFlags> MovePkmBank(
        string[] pkmIds, uint? sourceSaveId,
''',
'''    public async Task<DataUpdateFlags> TradeSwap(TradeSwapActionInput input)
    {
        using var scope = sp.CreateScope();

        return await AddAction(
            scope,
            (scope) => scope.ServiceProvider.GetRequiredService<TradeSwapAction>(),
            input
        );
    }

    public async Task<DataUpdateFlags> MovePkmBank(
        string[] pkmIds, uint? sourceSaveId,
''')

header = PKVAULT / 'frontend/src/header/header.tsx'
replace_once(header,
'''            <UIHeaderItem
                id={'pokedex' satisfies HeaderValue}
                to={"/pokedex"}
                selected={value === 'pokedex'}
                label={t('header.dex')}
            >
                {t('header.dex')}
            </UIHeaderItem>

            <Tooltip
''',
'''            <UIHeaderItem
                id={'pokedex' satisfies HeaderValue}
                to={"/pokedex"}
                selected={value === 'pokedex'}
                label={t('header.dex')}
            >
                {t('header.dex')}
            </UIHeaderItem>

            <UIHeaderItem
                id={'trading' satisfies HeaderValue}
                to={"/trading"}
                selected={value === 'trading'}
                label="Trading"
            >
                Trading
            </UIHeaderItem>

            <Tooltip
''')
replace_once(header,
'''            'saves': () => null,
            'settings': () => <SettingsSubMenu />,
''',
'''            'saves': () => null,
            'trading': () => null,
            'settings': () => <SettingsSubMenu />,
''')

(PKVAULT / 'PKVAULT_GEN1_REBUILD.txt').write_text(
    'PKVault Gen1 MissingNo + Direct Trading rebuild v7.1-test\n'
    'Baseline: Chnapy/PKVault 88993b8702a3ec7fc54b67ea1e2dbb1827822cec\n'
    'PKHeX: 26.08.26 / 74b88906e935e4a52d6d9243b8e373056409c738\n'
    'Fixes: v5 occupancy separation, raw-00 and raw-50 glitch preservation, real MissingNo sprite normalized to standard PKVault icon sizing, canonical blank box writes, phantom-slot guard, Party->Red Box stored-format packing, direct-IP PKVault trading with localhost:0000 local test alias, 0-5 batch/gift offers, drag/drop trade box UI, and automatic cache refresh after commit.\n',
    encoding='utf-8'
)
print('all patches applied')

from pathlib import Path
import shutil
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: patch_pkvault_v8.py <pkvault-root> <pkhex-root>")

PKVAULT = Path(sys.argv[1]).resolve()
PKHEX = Path(sys.argv[2]).resolve()
HERE = Path(__file__).resolve().parent

def replace_once(path: Path, old: str, new: str):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one match, found {count}\n--- needle ---\n{old[:1200]}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"patched {path}")

# ---------------------------------------------------------------------------
# PKHeX.Core: opt-in direct Gen-3 species semantics for pokeemerald-expansion.
# ---------------------------------------------------------------------------
shared = PKHEX / "PKHeX.Core/PKM/Shared"
shutil.copyfile(HERE / "Gen3DirectSpecies.cs", shared / "Gen3DirectSpecies.cs")

pk3 = PKHEX / "PKHeX.Core/PKM/PK3.cs"
replace_once(pk3,
'''    public override EntityContext Context => EntityContext.Gen3;
    public override PersonalInfo3 PersonalInfo => PersonalTable.RS[Species];
''',
'''    public override EntityContext Context => EntityContext.Gen3;
    public bool DirectSpeciesIDs { get; set; }
    public override PersonalInfo3 PersonalInfo => DirectSpeciesIDs ? Gen3DirectSpecies.GetPersonal(Species, Form) : PersonalTable.RS[Species];
''')
replace_once(pk3,
'''        PK3 pk = new();
        Data.CopyTo(pk.Data);
        return pk;
''',
'''        PK3 pk = new() { DirectSpeciesIDs = DirectSpeciesIDs };
        Data.CopyTo(pk.Data);
        return pk;
''')
replace_once(pk3,
'''    public override ushort Species
    {
        get => SpeciesConverter.GetNational3(SpeciesInternal);
        set
        {
            var s3 = SpeciesConverter.GetInternal3(value);
            FlagHasSpecies = (SpeciesInternal = s3) != 0;
        }
    }
''',
'''    public override ushort Species
    {
        get => DirectSpeciesIDs ? Gen3DirectSpecies.GetSpecies(SpeciesInternal) : SpeciesConverter.GetNational3(SpeciesInternal);
        set
        {
            if (DirectSpeciesIDs)
            {
                if (!Gen3DirectSpecies.TryGetRaw(value, 0, out var raw))
                    raw = value;
                FlagHasSpecies = (SpeciesInternal = raw) != 0;
                return;
            }

            var s3 = SpeciesConverter.GetInternal3(value);
            FlagHasSpecies = (SpeciesInternal = s3) != 0;
        }
    }
''')

g3 = PKHEX / "PKHeX.Core/PKM/Shared/G3PKM.cs"
replace_once(g3,
'''    public sealed override ushort MaxMoveID => Legal.MaxMoveID_3;
    public sealed override ushort MaxSpeciesID => Legal.MaxSpeciesID_3;
''',
'''    public sealed override ushort MaxMoveID => (ushort)(this is PK3 { DirectSpeciesIDs: true } ? Gen3DirectSpecies.MaxDirectMove : Legal.MaxMoveID_3);
    public sealed override ushort MaxSpeciesID => (ushort)(this is PK3 { DirectSpeciesIDs: true } ? Gen3DirectSpecies.MaxBaseSpecies : Legal.MaxSpeciesID_3);
''')
replace_once(g3,
'''    public sealed override byte Form
    {
        get => Species == (int)Core.Species.Unown ? EntityPID.GetUnownForm3(PID) : (byte)0;
        set
        {
            if (Species != (int)Core.Species.Unown)
                return;
            var rnd = Util.Rand;
            while (EntityPID.GetUnownForm3(PID) != value)
                PID = rnd.Rand32();
        }
    }
''',
'''    public sealed override byte Form
    {
        get
        {
            if (this is PK3 { DirectSpeciesIDs: true } p3)
                return Gen3DirectSpecies.GetForm(p3.SpeciesInternal);
            return Species == (int)Core.Species.Unown ? EntityPID.GetUnownForm3(PID) : (byte)0;
        }
        set
        {
            if (this is PK3 { DirectSpeciesIDs: true } p3)
            {
                var species = Gen3DirectSpecies.GetSpecies(p3.SpeciesInternal);
                if (!Gen3DirectSpecies.TryGetRaw(species, value, out var raw))
                    throw new ArgumentOutOfRangeException(nameof(value), value, $"Unsupported direct Gen-3 form for species {species}.");
                p3.SpeciesInternal = raw;
                return;
            }

            if (Species != (int)Core.Species.Unown)
                return;
            var rnd = Util.Rand;
            while (EntityPID.GetUnownForm3(PID) != value)
                PID = rnd.Rand32();
        }
    }
''')

sav3 = PKHEX / "PKHeX.Core/Saves/SAV3.cs"
replace_once(sav3,
'''    public sealed override int SIZE_STORED => PokeCrypto.SIZE_3STORED;
    public sealed override int SIZE_PARTY => PokeCrypto.SIZE_3PARTY;
    public sealed override PK3 BlankPKM => new();
    public sealed override Type PKMType => typeof(PK3);

    public sealed override ushort MaxMoveID => Legal.MaxMoveID_3;
    public sealed override ushort MaxSpeciesID => Legal.MaxSpeciesID_3;
''',
'''    public sealed override int SIZE_STORED => PokeCrypto.SIZE_3STORED;
    public sealed override int SIZE_PARTY => PokeCrypto.SIZE_3PARTY;
    public bool DirectSpeciesIDs { get; set; }
    public sealed override PK3 BlankPKM => new() { DirectSpeciesIDs = DirectSpeciesIDs };
    public sealed override Type PKMType => typeof(PK3);

    public sealed override ushort MaxMoveID => DirectSpeciesIDs ? Gen3DirectSpecies.MaxDirectMove : Legal.MaxMoveID_3;
    public sealed override ushort MaxSpeciesID => DirectSpeciesIDs ? Gen3DirectSpecies.MaxBaseSpecies : Legal.MaxSpeciesID_3;
''')
replace_once(sav3,
'''    public sealed override bool IsPKMPresent(ReadOnlySpan<byte> data) => EntityDetection.IsPresentGBA(data);
    protected sealed override PK3 GetPKM(Memory<byte> data) => new(data);
    protected sealed override void DecryptPKM(Span<byte> data) => PokeCrypto.Decrypt3(data);
''',
'''    public sealed override bool IsPKMPresent(ReadOnlySpan<byte> data) => EntityDetection.IsPresentGBA(data);
    protected sealed override PK3 GetPKM(Memory<byte> data) => new(data) { DirectSpeciesIDs = DirectSpeciesIDs };
    protected sealed override void DecryptPKM(Span<byte> data) => PokeCrypto.Decrypt3(data);
''')
replace_once(sav3,
'''    protected sealed override void SetDex(PKM pk)
    {
        ushort species = pk.Species;
''',
'''    protected sealed override void SetDex(PKM pk)
    {
        // pokeemerald-expansion hacks such as TMT use their own dex indexing.
        // The vanilla National Dex bitfield is not safe for expanded species.
        if (DirectSpeciesIDs)
            return;

        ushort species = pk.Species;
''')

sav3e = PKHEX / "PKHeX.Core/Saves/SAV3E.cs"
replace_once(sav3e,
'''    protected override SAV3E CloneInternal() => new(GetFinalData()) { Language = Language };
''',
'''    protected override SAV3E CloneInternal() => new(GetFinalData()) { Language = Language, DirectSpeciesIDs = DirectSpeciesIDs };
''')

# ---------------------------------------------------------------------------
# PKVault: TMT profile detection, storage identity, conversion and UI metadata.
# ---------------------------------------------------------------------------
romhacks = PKVAULT / "PKVault.Core/romhacks"
romhacks.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "TooManyTypesCompat.cs", romhacks / "TooManyTypesCompat.cs")
shutil.copyfile(HERE / "TooManyTypesProfile.Generated.cs", romhacks / "TooManyTypesProfile.Generated.cs")

loader = PKVAULT / "PKVault.Core/db/loader/PkmFileLoader.cs"
replace_once(loader,
'''        return $"{pkm.Species:0000}{star} - {speciesName} - {id}.{pkm.Extension}";
''',
'''        var extension = TooManyTypesCompat.GetStorageExtension(pkm);
        return $"{pkm.Species:0000}{star} - {speciesName} - {id}.{extension}";
''')
replace_once(loader,
'''            var ext = Path.GetExtension(filepath.AsSpan());

            FileUtil.TryGetPKM(entity.Data, out var pk, ext, new SimpleTrainerInfo() { Context = context });
            if (pk == null)
            {
                throw new Exception($"TryGetPKM gives null pkm, path={filepath} bytes.length={entity.Data.Length}");
            }
            pkm = pk;
''',
'''            var ext = Path.GetExtension(filepath);

            if (ext.Equals("." + TooManyTypesCompat.StorageExtension, StringComparison.OrdinalIgnoreCase))
            {
                pkm = new PK3((byte[])entity.Data.Clone()) { DirectSpeciesIDs = true };
            }
            else
            {
                FileUtil.TryGetPKM(entity.Data, out var pk, ext.AsSpan(), new SimpleTrainerInfo() { Context = context });
                if (pk == null)
                {
                    throw new Exception($"TryGetPKM gives null pkm, path={filepath} bytes.length={entity.Data.Length}");
                }
                pkm = pk;
            }
''')

saves = PKVAULT / "PKVault.Core/db/loader/save/SavesLoadersService.cs"
replace_once(saves,
'''            saveRaw.Metadata.SetExtraInfo(path);
            if (saveRaw.Generation <= 3)
                SaveLanguage.TryRevise(saveRaw);

            SaveWrapper save = new(saveRaw);
''',
'''            saveRaw.Metadata.SetExtraInfo(path);
            if (saveRaw.Generation <= 3)
                SaveLanguage.TryRevise(saveRaw);

            TooManyTypesCompat.ConfigureSave(saveRaw, path);

            SaveWrapper save = new(saveRaw);
''')

dto = PKVAULT / "PKVault.Core/storage/dto/PkmBaseDTO.cs"
replace_once(dto,
'''    public Gender Gender => Pkm.Gender;
    public List<byte> Types => Pkm.Types;
    public byte? TeraType => Pkm.TeraType;
''',
'''    public Gender Gender => Pkm.Gender;
    public List<byte> Types => Pkm.Types;
    public string? RomHackProfile => TooManyTypesCompat.IsTmt(Pkm) ? TooManyTypesProfileGenerated.ProfileId : null;
    public string[]? RomHackTypes => TooManyTypesCompat.GetTypes(Pkm);
    public byte? TeraType => Pkm.TeraType;
''')

wrapper = PKVAULT / "PKVault.Core/storage/wrapper/SaveWrapper.cs"
replace_once(wrapper,
'''    public bool IsSpeciesAllowed(ushort species)
    {
        // Species 0 is never a normal Pokemon, but an enabled raw-00 PK1
''',
'''    public bool IsSpeciesAllowed(ushort species)
    {
        if (Save is SAV3 { DirectSpeciesIDs: true })
            return TooManyTypesProfileGenerated.Entries.Any(e => e.Species == species);

        // Species 0 is never a normal Pokemon, but an enabled raw-00 PK1
''')

trading = PKVAULT / "PKVault.Core/trading/TradingService.cs"
replace_once(trading,
'''    public const int ProtocolVersion = 2;
''',
'''    public const int ProtocolVersion = 3;
''')
replace_once(trading,
'''                Extension: pkm.Extension,
''',
'''                Extension: TooManyTypesCompat.GetStorageExtension(pkm),
''')

convert = PKVAULT / "PKVault.Core/storage/services/PkmConvertService/PkmConvertService.cs"
replace_once(convert,
'''        Log.Debug($"Convert {sourcePkm.GetMutablePkm().GetType().Name} -> {targetPkmType.Name}");

        var fallbackLang = settingsService.GetSettings().GetSafeLanguageID();
''',
'''        if (targetPkmType == typeof(PK3) && targetSave is SAV3 targetGen3)
        {
            if (targetGen3.DirectSpeciesIDs)
                return ConvertToTooManyTypes(sourcePkm, rndValues);

            if (sourcePkm.GetMutablePkm() is PK3 { DirectSpeciesIDs: true } direct)
                return ConvertFromTooManyTypes(direct, targetGen3, rndValues);
        }

        Log.Debug($"Convert {sourcePkm.GetMutablePkm().GetType().Name} -> {targetPkmType.Name}");

        var fallbackLang = settingsService.GetSettings().GetSafeLanguageID();
''')
replace_once(convert,
'''    private PKM ConvertRecursive(PKM current, Type targetType, LanguageID fallbackLang, PKMRndValues? rndValues)
''',
'''    private ImmutablePKM ConvertToTooManyTypes(ImmutablePKM sourcePkm, PKMRndValues? rndValues)
    {
        TooManyTypesCompat.RequireSupported(sourcePkm.Species, sourcePkm.Form);

        if (sourcePkm.GetMutablePkm() is PK3 { DirectSpeciesIDs: true } alreadyTmt)
            return new(alreadyTmt.Clone());

        var fallbackLang = settingsService.GetSettings().GetSafeLanguageID();
        var proxy = sourcePkm.GetMutablePkm().Clone();

        // PKHeX's normal backward converters reject post-Gen3 species before
        // reaching PK3. Convert a structurally equivalent Gen3-compatible
        // proxy, then restore the real TMT species/form and canonical moves.
        if (proxy.Species > 386 || proxy.Form != 0)
        {
            proxy.Species = (ushort)Species.Pikachu;
            proxy.Form = 0;
        }

        var converted = ConvertRecursive(proxy, typeof(PK3), fallbackLang, rndValues);
        if (converted is not PK3 p3)
            throw new InvalidOperationException("Failed to produce a PK3 for Too Many Types.");

        TooManyTypesCompat.ApplyTmtIdentity(p3, sourcePkm);
        p3.ResetPartyStats();
        p3.RefreshChecksum();
        return new(p3);
    }

    private ImmutablePKM ConvertFromTooManyTypes(PK3 source, SAV3 targetSave, PKMRndValues? rndValues)
    {
        var p3 = TooManyTypesCompat.ConvertDirectToVanilla(source, targetSave);

        // Re-enter the normal legality fixer only after the raw direct species
        // id has been remapped to vanilla Gen3's internal species table.
        pkmConverterUtils.FixCommonLegalityIssues(p3, new(targetSave), rndValues);
        p3.Heal();
        p3.ResetPartyStats();
        p3.RefreshChecksum();
        if (p3.Species == 0)
            throw new InvalidOperationException("Too Many Types -> vanilla Gen3 conversion produced species 0.");
        return new(p3);
    }

    private PKM ConvertRecursive(PKM current, Type targetType, LanguageID fallbackLang, PKMRndValues? rndValues)
''')

print("PKVault V8 TMT patch applied")

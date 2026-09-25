# PKVault V8 alpha4 TMT exact type colors + vanilla-isolation + UI/type test
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

    public sealed override ushort MaxMoveID => (ushort)(DirectSpeciesIDs ? Gen3DirectSpecies.MaxDirectMove : Legal.MaxMoveID_3);
    public sealed override ushort MaxSpeciesID => (ushort)(DirectSpeciesIDs ? Gen3DirectSpecies.MaxBaseSpecies : Legal.MaxSpeciesID_3);
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

dex_dir = PKVAULT / "PKVault.Core/dex/services/gen"
shutil.copyfile(HERE / "DexTmtService.cs", dex_dir / "DexTmtService.cs")

dex_service = PKVAULT / "PKVault.Core/dex/services/DexService.cs"
replace_once(dex_service,
'''            SAV2 sav2 => new Dex123Service(sav2),
            SAV3 sav3 => new Dex123Service(sav3),
''',
'''            SAV2 sav2 => new Dex123Service(sav2),
            SAV3 { DirectSpeciesIDs: true } tmt3 => new DexTmtService(tmt3),
            SAV3 sav3 => new Dex123Service(sav3),
''')

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


# ---------------------------------------------------------------------------
# Frontend/OpenAPI: expose and visibly render TMT type names, while keeping
# normal game types untouched. Also allow ROM-hack Pokemon to borrow an
# official modern sprite when Gen3 has no static sprite entry for the species.
# ---------------------------------------------------------------------------
swagger = PKVAULT / "PKVault.Core/swagger.json"
replace_once(swagger,
'''          "gender": {
            "$ref": "#/components/schemas/Gender"
          },
          "types": {
            "type": "array",
            "items": {
              "type": "integer",
              "format": "byte"
            }
          },
          "teraType": {
''',
'''          "gender": {
            "$ref": "#/components/schemas/Gender"
          },
          "types": {
            "type": "array",
            "items": {
              "type": "integer",
              "format": "byte"
            }
          },
          "romHackProfile": {
            "type": "string",
            "nullable": true
          },
          "romHackTypes": {
            "type": "array",
            "nullable": true,
            "items": {
              "type": "string"
            }
          },
          "teraType": {
''')
replace_once(swagger,
'''          "savE_PATH_OVERRIDES": {
            "type": "object",
            "additionalProperties": {
              "type": "string"
            }
          },
          "language": {
            "type": "string"
          }
''',
'''          "savE_PATH_OVERRIDES": {
            "type": "object",
            "additionalProperties": {
              "type": "string"
            }
          },
          "language": {
            "type": "string"
          },
          "tradeR_NAME": {
            "type": "string"
          }
''')

frontend_romhacks = PKVAULT / "frontend/src/romhacks"
frontend_romhacks.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "tmt-type-item.tsx", frontend_romhacks / "tmt-type-item.tsx")

species_img = PKVAULT / "frontend/src/img/species-img.tsx"
replace_once(species_img,
'''    isEgg?: boolean;
    isShadow?: boolean;
} & Omit<SpriteImgProps, 'spriteInfos' | 'size'>;

export const SpeciesImg: React.FC<SpeciesImgProps> = ({ species, context, form, isFemale, isShiny, isEgg, isShadow, ...imgProps }) => {
''',
'''    isEgg?: boolean;
    isShadow?: boolean;
    allowContextFallback?: boolean;
} & Omit<SpriteImgProps, 'spriteInfos' | 'size'>;

export const SpeciesImg: React.FC<SpeciesImgProps> = ({ species, context, form, isFemale, isShiny, isEgg, isShadow, allowContextFallback, ...imgProps }) => {
''')
replace_once(species_img,
'''    const staticForms = staticData.species[ usedSpecies ]?.forms[ context ];

    if (!staticForms?.[ form ])
''',
'''    const allForms = staticData.species[ usedSpecies ]?.forms;
    const staticForms = allForms?.[ context ]
        ?? (allowContextFallback
            ? Object.values(allForms ?? {}).reverse().find(forms => forms?.[ form ] ?? forms?.[ 0 ])
            : undefined);

    if (!staticForms?.[ form ])
''')

storage_item = PKVAULT / "frontend/src/storage/item/storage-item.tsx"
replace_once(storage_item,
'''  & Pick<SpeciesImgProps, 'species' | 'context' | 'form' | 'isFemale' | 'isShiny' | 'isEgg' | 'isShadow'>;
''',
'''  & Pick<SpeciesImgProps, 'species' | 'context' | 'form' | 'isFemale' | 'isShiny' | 'isEgg' | 'isShadow' | 'allowContextFallback'>;
''')
replace_once(storage_item,
'''  isShadow,

  ...rest
''',
'''  isShadow,
  allowContextFallback,

  ...rest
''')
replace_once(storage_item,
'''      <SpeciesImg species={species} context={context} form={form} isFemale={isFemale} isShiny={isShiny} isEgg={isEgg} isShadow={isShadow} />
''',
'''      <SpeciesImg species={species} context={context} form={form} isFemale={isFemale} isShiny={isShiny} isEgg={isEgg} isShadow={isShadow} allowContextFallback={allowContextFallback} />
''')

storage_main_item = PKVAULT / "frontend/src/storage/item/main/storage-main-item.tsx"
replace_once(storage_main_item,
'''                        'form', 'gender', 'isEgg', 'isAlpha', 'isShiny', 'nSparkle', 'isShadow', 'isExternal', 'heldItem',
''',
'''                        'form', 'gender', 'isEgg', 'isAlpha', 'isShiny', 'nSparkle', 'isShadow', 'isExternal', 'heldItem', 'romHackProfile',
''')
replace_once(storage_main_item,
'''        const { id, species, nickname, level, boxSlot, contextVersion, context, form, gender, isEgg, isAlpha, isShiny, nSparkle, isShadow, isExternal, heldItem } = mainVariant;
''',
'''        const { id, species, nickname, level, boxSlot, contextVersion, context, form, gender, isEgg, isAlpha, isShiny, nSparkle, isShadow, isExternal, heldItem, romHackProfile } = mainVariant;
''')
replace_once(storage_main_item,
'''            isShadow={isShadow}
            name={nickname}
''',
'''            isShadow={isShadow}
            allowContextFallback={!!romHackProfile}
            name={nickname}
''')

storage_save_item = PKVAULT / "frontend/src/storage/item/save/storage-save-item.tsx"
replace_once(storage_save_item,
'''                    'canEvolve',
''',
'''                    'canEvolve', 'romHackProfile',
''')
replace_once(storage_save_item,
'''        const { id, species, nickname, level, boxSlot, form, gender, contextVersion, isAlpha, isShiny, nSparkle, isEgg, isShadow, canEvolve } = savePkm;
''',
'''        const { id, species, nickname, level, boxSlot, form, gender, contextVersion, isAlpha, isShiny, nSparkle, isEgg, isShadow, canEvolve, romHackProfile } = savePkm;
''')
replace_once(storage_save_item,
'''            isShadow={isShadow}
            name={nickname}
''',
'''            isShadow={isShadow}
            allowContextFallback={!!romHackProfile}
            name={nickname}
''')

details_main = PKVAULT / "frontend/src/storage/details/details-main.tsx"
replace_once(details_main,
'''import { TypeItem } from './type-item/type-item';
''',
'''import { TypeItem } from './type-item/type-item';
import { TmtTypeItem } from '../../romhacks/tmt-type-item';
''')
replace_once(details_main,
'''    const staticForms = staticData.species[ pkm.species ]?.forms[ pkm.context ];
    const formObj = staticForms?.[ pkm.form ] ?? staticForms?.[ 0 ];
''',
'''    const allForms = staticData.species[ pkm.species ]?.forms;
    const staticForms = allForms?.[ pkm.context ]
        ?? (pkm.romHackProfile
            ? Object.values(allForms ?? {}).reverse().find(forms => forms?.[ pkm.form ] ?? forms?.[ 0 ])
            : undefined);
    const formObj = staticForms?.[ pkm.form ] ?? staticForms?.[ 0 ];
''')
replace_once(details_main,
'''        types={pkm.types.map(type => <TypeItem key={type} type={type} />)}
''',
'''        types={pkm.romHackTypes?.length
            ? pkm.romHackTypes.map(type => <TmtTypeItem key={type} type={type} />)
            : pkm.types.map(type => <TypeItem key={type} type={type} />)}
''')
replace_once(details_main,
'''            isEgg={pkm.isEgg}
            isShadow={pkm.isShadow}
        />
''',
'''            isEgg={pkm.isEgg}
            isShadow={pkm.isShadow}
            allowContextFallback={!!pkm.romHackProfile}
        />
''')

pokedex_details = PKVAULT / "frontend/src/pokedex/details/pokedex-details.tsx"
replace_once(pokedex_details,
'''import { TypeItem } from '../../storage/details/type-item/type-item';
''',
'''import { TypeItem } from '../../storage/details/type-item/type-item';
import { TmtTypeItem } from '../../romhacks/tmt-type-item';
''')
replace_once(pokedex_details,
'''      types={selectedForm.types.map(type => <TypeItem key={type} type={type} />)}
''',
'''      types={selectedForm.romHackTypes?.length
        ? selectedForm.romHackTypes.map(type => <TmtTypeItem key={type} type={type} />)
        : selectedForm.types.map(type => <TypeItem key={type} type={type} />)}
''')
replace_once(pokedex_details,
'''        form={selectedForm.form}
        isFemale={selectedForm.gender === GenderType.Female}
''',
'''        form={selectedForm.form}
        allowContextFallback={!!selectedForm.romHackTypes?.length}
        isFemale={selectedForm.gender === GenderType.Female}
''')

pokedex_items = PKVAULT / "frontend/src/pokedex/list/hooks/use-pokedex-items.ts"
replace_once(pokedex_items,
'''    isOwned?: boolean;
    isOwnedShiny?: boolean;
};
''',
'''    isOwned?: boolean;
    isOwnedShiny?: boolean;
    romHackTypes?: string[] | null;
};
''')
replace_once(pokedex_items,
'''                    isOwned: oldGroup?.isOwned || form.isOwned,
                    isOwnedShiny: oldGroup?.isOwnedShiny || form.isOwnedShiny,
''',
'''                    isOwned: oldGroup?.isOwned || form.isOwned,
                    isOwnedShiny: oldGroup?.isOwnedShiny || form.isOwnedShiny,
                    romHackTypes: oldGroup?.romHackTypes ?? form.romHackTypes,
''')

dex_form_item = PKVAULT / "frontend/src/pokedex/list/dex-item/dex-form-item.tsx"
replace_once(dex_form_item,
'''  isOwned,
  isOwnedShiny,
}) => {
''',
'''  isOwned,
  isOwnedShiny,
  romHackTypes,
}) => {
''')
replace_once(dex_form_item,
'''      form={form}
      isFemale={genders[ 0 ] == GenderType.Female}
''',
'''      form={form}
      allowContextFallback={!!romHackTypes?.length}
      isFemale={genders[ 0 ] == GenderType.Female}
''')


# ---------------------------------------------------------------------------
# V8 alpha7: TMT is an ownership source for the normal National Dex only.
# TMT-specific typing/presentation stays exclusively in Storage/box details.
# Also reduce Pokédex rendering work while scrolling.
# ---------------------------------------------------------------------------
save_infos_dto = PKVAULT / "PKVault.Core/save-infos/dto/SaveInfosDTO.cs"
replace_once(save_infos_dto,
'''    EntityContext Context,
    byte Generation,
    uint TID,
''',
'''    EntityContext Context,
    byte Generation,
    string? RomHackProfile,
    uint TID,
''')
replace_once(save_infos_dto,
'''            Context: save.Context,
            Generation: save.Generation,
            TID: save.TID,
''',
'''            Context: save.Context,
            Generation: save.Generation,
            RomHackProfile: save.GetSave() is SAV3 { DirectSpeciesIDs: true }
                ? TooManyTypesProfileGenerated.ProfileId
                : null,
            TID: save.TID,
''')

replace_once(swagger,
'''          "generation": {
            "type": "integer",
            "format": "byte"
          },
          "tid": {
''',
'''          "generation": {
            "type": "integer",
            "format": "byte"
          },
          "romHackProfile": {
            "type": "string",
            "nullable": true
          },
          "tid": {
''')

shutil.copyfile(HERE / "use-pokedex-items-v8.ts",
                PKVAULT / "frontend/src/pokedex/list/hooks/use-pokedex-items.ts")
shutil.copyfile(HERE / "use-pokedex-details-select-v8.ts",
                PKVAULT / "frontend/src/pokedex/details/hooks/use-pokedex-details-select.ts")
shutil.copyfile(HERE / "get-save-display-name.ts",
                frontend_romhacks / "get-save-display-name.ts")

shutil.copyfile(HERE / "pokedex-route-v8.tsx",
                PKVAULT / "frontend/src/routes/pokedex.tsx")
shutil.copyfile(HERE / "pokedex-item-v8.tsx",
                PKVAULT / "frontend/src/pokedex/list/pokedex-item.tsx")
shutil.copyfile(HERE / "pokedex-list-v8.tsx",
                PKVAULT / "frontend/src/pokedex/list/pokedex-list.tsx")
shutil.copyfile(HERE / "dex-form-item-v8.tsx",
                PKVAULT / "frontend/src/pokedex/list/dex-item/dex-form-item.tsx")
shutil.copyfile(HERE / "pokedex-details-v8.tsx",
                PKVAULT / "frontend/src/pokedex/details/pokedex-details.tsx")
shutil.copyfile(HERE / "ui-pokedex-main-section-v8.tsx",
                PKVAULT / "frontend/src/ui/pokedex/main/section/ui-pokedex-main-section.tsx")

pokedex_owned = PKVAULT / "frontend/src/pokedex/details/content/pokedex-details-owned.tsx"
replace_once(pokedex_owned,
'''        <SpeciesImg species={species} context={pkm.context} form={pkm.form} isFemale={pkm.gender === Gender.Female}
            isShiny={pkm.isShiny} isEgg={pkm.isEgg} isShadow={pkm.isShadow} />
''',
'''        <SpeciesImg species={species} context={pkm.context} form={pkm.form} isFemale={pkm.gender === Gender.Female}
            isShiny={pkm.isShiny} isEgg={pkm.isEgg} isShadow={pkm.isShadow}
            allowContextFallback={!!pkm.romHackProfile} />
''')

# Save labels: never masquerade a TMT save as plain Emerald in the UI.
saves_page = PKVAULT / "frontend/src/pages/saves.tsx"
replace_once(saves_page,
'''import { getGameInfos } from '../pokedex/details/util/get-game-infos';
''',
'''import { getGameInfos } from '../pokedex/details/util/get-game-infos';
import { getSaveDisplayName } from '../romhacks/get-save-display-name';
''')
replace_once(saves_page,
'''                label={staticData.versions[ save.displayedVersion ]?.name}
''',
'''                label={getSaveDisplayName(staticData.versions[ save.displayedVersion ]?.name, save.romHackProfile)}
''')

game_list = PKVAULT / "frontend/src/storage/panel/game-list/storage-panel-game-list.tsx"
replace_once(game_list,
'''import { getGameInfos } from '../../../pokedex/details/util/get-game-infos';
''',
'''import { getGameInfos } from '../../../pokedex/details/util/get-game-infos';
import { getSaveDisplayName } from '../../../romhacks/get-save-display-name';
''')
replace_once(game_list,
'''            ...saveInfos.map(({ id, displayedVersion, duplicates }): UIGameData => ({
                id: id.toString(),
                imgSrc: getGameInfos(displayedVersion).img,
                label: staticData.versions[ displayedVersion ]?.name ?? '',
                hasDuplicates: duplicates.length > 0,
            })),
''',
'''            ...saveInfos.map(({ id, displayedVersion, duplicates, romHackProfile }): UIGameData => ({
                id: id.toString(),
                imgSrc: getGameInfos(displayedVersion).img,
                label: getSaveDisplayName(staticData.versions[ displayedVersion ]?.name, romHackProfile),
                hasDuplicates: duplicates.length > 0,
            })),
''')

save_item_edit = PKVAULT / "frontend/src/saves/save-item/save-item-edit.tsx"
replace_once(save_item_edit,
'''import { getGameInfos } from '../../pokedex/details/util/get-game-infos';
''',
'''import { getGameInfos } from '../../pokedex/details/util/get-game-infos';
import { getSaveDisplayName } from '../../romhacks/get-save-display-name';
''')
replace_once(save_item_edit,
'''                        label={staticData.versions[ save.displayedVersion ]?.name}
''',
'''                        label={getSaveDisplayName(staticData.versions[ save.displayedVersion ]?.name, save.romHackProfile)}
''')
replace_once(save_item_edit,
'''                            label={staticData.versions[ s.displayedVersion ]?.name}
''',
'''                            label={getSaveDisplayName(staticData.versions[ s.displayedVersion ]?.name, s.romHackProfile)}
''')

details_attached = PKVAULT / "frontend/src/storage/details/details-attached-button.tsx"
replace_once(details_attached,
'''import { Route } from '../../routes/storage';
''',
'''import { Route } from '../../routes/storage';
import { getSaveDisplayName } from '../../romhacks/get-save-display-name';
''')
replace_once(details_attached,
'''        ? <>{staticData.versions[ attachedSave.displayedVersion ]?.name} ({attachedSave.trainerName})</>
''',
'''        ? <>{getSaveDisplayName(staticData.versions[ attachedSave.displayedVersion ]?.name, attachedSave.romHackProfile)} ({attachedSave.trainerName})</>
''')


# ---------------------------------------------------------------------------
# V8 Essentials foundation: Pokémon Uranium + Pokémon Insurgence.
# Alpha9 adds guarded read/write support: profile-local Pokémon retain a
# Ruby source template and only the trainer/storage Marshal streams are rebuilt.
# ---------------------------------------------------------------------------
essentials_pkhex = PKHEX / "PKHeX.Core/PKM/Shared"
shutil.copyfile(HERE / "essentials/PKEssentials.cs", essentials_pkhex / "PKEssentials.cs")

essentials_core = PKVAULT / "PKVault.Core/romhacks/essentials"
essentials_core.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "essentials/RubyMarshal48.cs", essentials_core / "RubyMarshal48.cs")
shutil.copyfile(HERE / "essentials/EssentialsLegacySaveReader.cs", essentials_core / "EssentialsLegacySaveReader.cs")
shutil.copyfile(HERE / "essentials/EssentialsLegacySaveWriter.cs", essentials_core / "EssentialsLegacySaveWriter.cs")

immutable = PKVAULT / "PKVault.Core/storage/wrapper/ImmutablePKM.cs"
replace_once(immutable,
'''    public uint ExpToLevelUp => Experience.GetEXPToLevelUp(Pkm.CurrentLevel, Pkm.PersonalInfo.EXPGrowth);
    public double LevelUpPercent => Experience.GetEXPToLevelUpPercentage(Pkm.CurrentLevel, Pkm.EXP, Pkm.PersonalInfo.EXPGrowth);
''',
'''    public uint ExpToLevelUp => Pkm is PKEssentials ? 0 : Experience.GetEXPToLevelUp(Pkm.CurrentLevel, Pkm.PersonalInfo.EXPGrowth);
    public double LevelUpPercent => Pkm is PKEssentials ? 0 : Experience.GetEXPToLevelUpPercentage(Pkm.CurrentLevel, Pkm.EXP, Pkm.PersonalInfo.EXPGrowth);
''')
replace_once(immutable,
'''    public byte CurrentLevel => Pkm.CurrentLevel;
''',
'''    public byte CurrentLevel => Pkm is PKEssentials essentials ? essentials.StoredLevel : Pkm.CurrentLevel;
''')
replace_once(immutable,
'''    public bool IsSpeciesValid => Species > 0 && Species < GameInfo.Strings.Species.Count;
''',
'''    public bool IsSpeciesValid => Pkm is PKEssentials essentials
        ? essentials.LocalSpeciesId > 0 && !string.IsNullOrWhiteSpace(essentials.ProfileId)
        : Species > 0 && Species < GameInfo.Strings.Species.Count;
''')
replace_once(immutable,
'''    public string GetPKMIdBase(Dictionary<ushort, StaticEvolve> evolves, int boxId = (int)BoxType.Box)
    {
        var clone = Update(clone =>
''',
'''    public string GetPKMIdBase(Dictionary<ushort, StaticEvolve> evolves, int boxId = (int)BoxType.Box)
    {
        if (Pkm is PKEssentials essentials)
        {
            var scoped = BoxLoader.IsScopedBox(boxId) ? $"_{boxId}" : "";
            return $"ESS_{essentials.ProfileId}_{essentials.LocalSpeciesId}_{essentials.PID:X8}_{essentials.ID32:X8}{scoped}";
        }

        var clone = Update(clone =>
''')

# Extend the already-added ROM-hack DTO fields with profile-local Essentials identity.
replace_once(dto,
'''    public string? RomHackProfile => TooManyTypesCompat.IsTmt(Pkm) ? TooManyTypesProfileGenerated.ProfileId : null;
    public string[]? RomHackTypes => TooManyTypesCompat.GetTypes(Pkm);
    public byte? TeraType => Pkm.TeraType;
''',
'''    public string? RomHackProfile => Pkm.GetMutablePkm() is PKEssentials essentials
        ? essentials.ProfileId
        : TooManyTypesCompat.IsTmt(Pkm) ? TooManyTypesProfileGenerated.ProfileId : null;
    public string[]? RomHackTypes => Pkm.GetMutablePkm() is PKEssentials essentials
        ? essentials.TypeNames
        : TooManyTypesCompat.GetTypes(Pkm);
    public string? RomHackSpeciesName => Pkm.GetMutablePkm() is PKEssentials essentials ? essentials.SpeciesName : null;
    public int? RomHackLocalSpeciesId => Pkm.GetMutablePkm() is PKEssentials essentials ? essentials.LocalSpeciesId : null;
    public bool RomHackReadOnly => Pkm.GetMutablePkm() is PKEssentials { ReadOnlySource: true };
    public byte? TeraType => Pkm.TeraType;
''')
replace_once(dto,
'''    public virtual bool CanMoveToSave => IsEnabled && Pkm.Version > 0 && Pkm.Generation > 0 && CanMove;

    public virtual bool CanEdit => IsEnabled && !IsEgg;
''',
'''    public virtual bool CanMoveToSave => IsEnabled
        && (Pkm.GetMutablePkm() is PKEssentials essentials
            ? !essentials.ReadOnlySource && essentials.SourceRubyMarshal.Length > 0
            : Pkm.Version > 0 && Pkm.Generation > 0)
        && CanMove;

    public virtual bool CanEdit => IsEnabled && !IsEgg && Pkm.GetMutablePkm() is not PKEssentials;
''')

# Custom Essentials PKM files are JSON-backed profile-local records, not PKHeX
# official binary PKM structures.
replace_once(loader,
'''        var star = pkm.IsShiny ? " ★" : string.Empty;
        var speciesName = pkm.IsGen1RawZeroGlitch
            ? "'M-RAW00"
            : pkm.IsGen1MissingNo50
                ? "MISSINGNO-RAW50"
                : GameInfo.Strings.Species[pkm.Species].ToUpperInvariant().Replace(":", "");
        var extension = TooManyTypesCompat.GetStorageExtension(pkm);
        return $"{pkm.Species:0000}{star} - {speciesName} - {id}.{extension}";
''',
'''        var star = pkm.IsShiny ? " ★" : string.Empty;
        var speciesName = pkm.GetMutablePkm() is PKEssentials essentials
            ? essentials.SpeciesName.ToUpperInvariant().Replace(":", "")
            : pkm.IsGen1RawZeroGlitch
                ? "'M-RAW00"
                : pkm.IsGen1MissingNo50
                    ? "MISSINGNO-RAW50"
                    : GameInfo.Strings.Species[pkm.Species].ToUpperInvariant().Replace(":", "");
        var extension = pkm.GetMutablePkm() is PKEssentials ? "pkessentials" : TooManyTypesCompat.GetStorageExtension(pkm);
        return $"{pkm.Species:0000}{star} - {speciesName} - {id}.{extension}";
''')
replace_once(loader,
'''            if (ext.Equals("." + TooManyTypesCompat.StorageExtension, StringComparison.OrdinalIgnoreCase))
            {
                pkm = new PK3((byte[])entity.Data.Clone()) { DirectSpeciesIDs = true };
            }
            else
''',
'''            if (ext.Equals(".pkessentials", StringComparison.OrdinalIgnoreCase))
            {
                pkm = PKEssentials.Deserialize(entity.Data);
            }
            else if (ext.Equals("." + TooManyTypesCompat.StorageExtension, StringComparison.OrdinalIgnoreCase))
            {
                pkm = new PK3((byte[])entity.Data.Clone()) { DirectSpeciesIDs = true };
            }
            else
''')
replace_once(loader,
'''    public byte[] GetPKMBytes(ImmutablePKM pkm)
    {
        return pkm.GetDecryptedDataParty();
    }
''',
'''    public byte[] GetPKMBytes(ImmutablePKM pkm)
    {
        if (pkm.GetMutablePkm() is PKEssentials essentials)
            return PKEssentials.Serialize(essentials);
        return pkm.GetDecryptedDataParty();
    }
''')

# OpenAPI fields used by the frontend once profile-local records are present.
replace_once(swagger,
'''          "romHackTypes": {
            "type": "array",
            "nullable": true,
            "items": {
              "type": "string"
            }
          },
          "teraType": {
''',
'''          "romHackTypes": {
            "type": "array",
            "nullable": true,
            "items": {
              "type": "string"
            }
          },
          "romHackSpeciesName": {
            "type": "string",
            "nullable": true
          },
          "romHackLocalSpeciesId": {
            "type": "integer",
            "format": "int32",
            "nullable": true
          },
          "romHackReadOnly": {
            "type": "boolean"
          },
          "teraType": {
''')


print("PKVault V8 TMT + Essentials foundation patch applied")


# ---------------------------------------------------------------------------
# V8 alpha8 Essentials read/write save integration.
# ---------------------------------------------------------------------------
shutil.copyfile(HERE / "essentials/EssentialsLegacySaveFile.cs",
                essentials_core / "EssentialsLegacySaveFile.cs")

saves_essentials = PKVAULT / "PKVault.Core/db/loader/save/SavesLoadersService.cs"
replace_once(saves_essentials,
'''            if (!SaveUtil.TryGetSaveFile((byte[])data.Clone(), out var saveRaw))
                return null;

            saveRaw.Metadata.SetExtraInfo(path);
''',
'''            if (Path.GetExtension(path).Equals(".rxdata", StringComparison.OrdinalIgnoreCase))
            {
                if (!EssentialsLegacySaveReader.TryRead(data, path, out var essentials, out var essentialsError)
                    || essentials == null
                    || essentials.Game is not (EssentialsGameKind.Uranium or EssentialsGameKind.Insurgence))
                {
                    Log.Warning("Unsupported Essentials .rxdata save {Path}: {Error}", path, essentialsError);
                    return null;
                }

                var essentialsSave = new EssentialsLegacySaveFile(essentials);
                essentialsSave.Metadata.SetExtraInfo(path);
                Log.Information("Loaded Essentials save {Profile} ({Count} Pokemon) from {Path}",
                    essentials.ProfileId, essentials.PokemonCount, path);
                return new SaveWrapper(essentialsSave);
            }

            if (!SaveUtil.TryGetSaveFile((byte[])data.Clone(), out var saveRaw))
                return null;

            saveRaw.Metadata.SetExtraInfo(path);
''')

replace_once(immutable,
'''    public string GetOriginMetLocation(string language) => GameInfo.GetStrings(language)
        .GetLocationName(Pkm.WasEgg, Pkm.MetLocation, Pkm.Format, Pkm.Generation, Pkm.Version);
''',
'''    public string GetOriginMetLocation(string language) => Pkm is PKEssentials
        ? ""
        : GameInfo.GetStrings(language).GetLocationName(Pkm.WasEgg, Pkm.MetLocation, Pkm.Format, Pkm.Generation, Pkm.Version);
''')
replace_once(immutable,
'''    public int[] GetStats()
    {
        Pkm.SetStats(Pkm.GetStats(Pkm.PersonalInfo));
        return [
            Pkm.Stat_HPMax,
            Pkm.Stat_ATK,
            Pkm.Stat_DEF,
            Pkm.Stat_SPA,
            Pkm.Stat_SPD,
            Pkm.Stat_SPE,
        ];
    }
''',
'''    public int[] GetStats()
    {
        if (Pkm is PKEssentials)
        {
            return [
                Pkm.Stat_HPMax,
                Pkm.Stat_ATK,
                Pkm.Stat_DEF,
                Pkm.Stat_SPA,
                Pkm.Stat_SPD,
                Pkm.Stat_SPE,
            ];
        }

        Pkm.SetStats(Pkm.GetStats(Pkm.PersonalInfo));
        return [
            Pkm.Stat_HPMax,
            Pkm.Stat_ATK,
            Pkm.Stat_DEF,
            Pkm.Stat_SPA,
            Pkm.Stat_SPD,
            Pkm.Stat_SPE,
        ];
    }
''')

legality = PKVAULT / "PKVault.Core/storage/services/LegalityAnalysisService.cs"
replace_once(legality,
'''    public LegalityAnalysisWrapper GetLegalitySafe(ImmutablePKM pkm, SaveWrapper? save = null, StorageSlotType slotType = StorageSlotType.None)
    {
        if (settingsService.GetSettings().SettingsMutable.SKIP_LEGALITY_CHECKS)
''',
'''    public LegalityAnalysisWrapper GetLegalitySafe(ImmutablePKM pkm, SaveWrapper? save = null, StorageSlotType slotType = StorageSlotType.None)
    {
        if (pkm.GetMutablePkm() is PKEssentials)
            return new(null);

        if (settingsService.GetSettings().SettingsMutable.SKIP_LEGALITY_CHECKS)
''')

variant_dto = PKVAULT / "PKVault.Core/storage/dto/PkmVariantDTO.cs"
replace_once(variant_dto,
'''    public IReadOnlyList<GameVersion> CompatibleWithVersions => VersionChecker.GetCompatibleVersionsForSpecies(Pkm.Species);
''',
'''    public IReadOnlyList<GameVersion> CompatibleWithVersions => Pkm.GetMutablePkm() is PKEssentials
        ? []
        : VersionChecker.GetCompatibleVersionsForSpecies(Pkm.Species);
''')


# Alpha9: preserve profile-local Essentials identity through PKVault move paths.
pkm_convert = PKVAULT / "PKVault.Core/storage/services/PkmConvertService/PkmConvertService.cs"
replace_once(pkm_convert,
'''        Log.Debug($"Convert {sourcePkm.GetMutablePkm().GetType().Name} -> {targetPkmType.Name}");

        var fallbackLang = settingsService.GetSettings().GetSafeLanguageID();
''',
'''        Log.Debug($"Convert {sourcePkm.GetMutablePkm().GetType().Name} -> {targetPkmType.Name}");

        if (sourcePkm.GetMutablePkm() is PKEssentials essentialsSource)
        {
            if (targetPkmType != typeof(PKEssentials))
                throw new InvalidOperationException("Essentials Pokémon cannot be converted to an official PKM format without an explicit profile mapping.");
            if (targetSave is not EssentialsLegacySaveFile essentialsTarget)
                throw new InvalidOperationException("Essentials Pokémon can only be written to an Essentials save.");
            if (!string.Equals(essentialsSource.ProfileId, essentialsTarget.ProfileId, StringComparison.Ordinal))
                throw new InvalidOperationException($"Cross-profile Essentials conversion blocked: {essentialsSource.ProfileId} -> {essentialsTarget.ProfileId}.");
            if (essentialsSource.ReadOnlySource || essentialsSource.SourceRubyMarshal.Length == 0)
                throw new InvalidOperationException("Essentials Pokémon lacks a writable Ruby source template.");
            return new((PKEssentials)essentialsSource.Clone());
        }

        if (targetPkmType == typeof(PKEssentials))
            throw new InvalidOperationException("Official Pokémon cannot be converted into a profile-local Essentials Pokémon without an explicit mapping.");

        var fallbackLang = settingsService.GetSettings().GetSafeLanguageID();
''')

pkm_save_dto = PKVAULT / "PKVault.Core/storage/dto/PkmSaveDTO.cs"
replace_once(pkm_save_dto,
'''    public bool CanMoveToMain => IsEnabled && Pkm.Version > 0 && Pkm.Generation > 0 && CanDelete && !IsShadow && !IsEgg && !IsLocked && Party == -1;
''',
'''    public bool CanMoveToMain => IsEnabled
        && (Pkm.GetMutablePkm() is PKEssentials || (Pkm.Version > 0 && Pkm.Generation > 0))
        && CanDelete && !IsShadow && !IsEgg && !IsLocked && Party == -1;
''')

move_action = PKVAULT / "PKVault.Core/storage/data-action/MovePkmAction.cs"
replace_once(move_action,
'''        if (!targetSaveLoaders.Save.IsSpeciesAllowed(sourcePkmDto.Species))
        {
            throw new ArgumentException($"Save Pkm Species not compatible with save for id={sourcePkmDto.Id}, species={sourcePkmDto.Species}, save.maxSpecies={targetSaveLoaders.Save.MaxSpeciesID}");
        }
''',
'''        if (!targetSaveLoaders.Save.IsPkmAllowed(sourcePkmDto.Pkm))
        {
            throw new ArgumentException($"Save Pkm profile/species not compatible with target save for id={sourcePkmDto.Id}.");
        }
''')
replace_once(move_action,
'''        if (!saveLoaders.Save.IsSpeciesAllowed(pkm.Species))
        {
            throw new ArgumentException($"PkmVariantEntity Species not compatible with save for id={pkmVariant.Id}, species={pkm.Species}, save.maxSpecies={saveLoaders.Save.MaxSpeciesID}");
        }
''',
'''        if (!saveLoaders.Save.IsPkmAllowed(pkm))
        {
            throw new ArgumentException($"PkmVariantEntity profile/species not compatible with target save for id={pkmVariant.Id}.");
        }
''')
replace_once(move_action,
'''        await new DexMainService(sp).EnablePKM(savePkm.Pkm, savePkm.Save);
''',
'''        if (savePkm.Pkm.GetMutablePkm() is not PKEssentials)
            await new DexMainService(sp).EnablePKM(savePkm.Pkm, savePkm.Save);
''')

move_bank_action = PKVAULT / "PKVault.Core/storage/data-action/MovePkmBankAction.cs"
replace_once(move_bank_action,
'''        await new DexMainService(sp).EnablePKM(savePkm.Pkm, savePkm.Save);
''',
'''        if (savePkm.Pkm.GetMutablePkm() is not PKEssentials)
            await new DexMainService(sp).EnablePKM(savePkm.Pkm, savePkm.Save);
''')

print("PKVault V8 alpha9 Essentials guarded read/write move paths applied")

replace_once(wrapper,
'''            string rawKey = $"{(byte)Save.Version}-{Save.Language}-{ID32}-{Save.OT}-{(byte)Save.Gender}";
''',
'''            string rawKey = Save is EssentialsLegacySaveFile essentials
                ? $"essentials-{essentials.ProfileId}-{ID32}-{Save.OT}-{Save.Metadata.FilePath}"
                : $"{(byte)Save.Version}-{Save.Language}-{ID32}-{Save.OT}-{(byte)Save.Gender}";
''')
replace_once(wrapper,
'''    public bool IsSpeciesAllowed(ushort species)
    {
        if (Save is SAV3 { DirectSpeciesIDs: true })
''',
'''    public bool IsPkmAllowed(ImmutablePKM pkm)
    {
        if (Save is EssentialsLegacySaveFile essentials)
            return pkm.GetMutablePkm() is PKEssentials candidate
                && !candidate.ReadOnlySource
                && candidate.SourceRubyMarshal.Length > 0
                && string.Equals(candidate.ProfileId, essentials.ProfileId, StringComparison.Ordinal);

        return IsSpeciesAllowed(pkm.Species);
    }

    public bool IsSpeciesAllowed(ushort species)
    {
        if (Save is EssentialsLegacySaveFile)
            return species > 0 && species <= Save.MaxSpeciesID;

        if (Save is SAV3 { DirectSpeciesIDs: true })
''')

replace_once(save_infos_dto,
'''            RomHackProfile: save.GetSave() is SAV3 { DirectSpeciesIDs: true }
                ? TooManyTypesProfileGenerated.ProfileId
                : null,
''',
'''            RomHackProfile: save.GetSave() switch
            {
                EssentialsLegacySaveFile essentials => essentials.ProfileId,
                SAV3 { DirectSpeciesIDs: true } => TooManyTypesProfileGenerated.ProfileId,
                _ => null,
            },
''')

species_img_ess = PKVAULT / "frontend/src/img/species-img.tsx"
replace_once(species_img_ess,
'''    allowContextFallback?: boolean;
} & Omit<SpriteImgProps, 'spriteInfos' | 'size'>;

export const SpeciesImg: React.FC<SpeciesImgProps> = ({ species, context, form, isFemale, isShiny, isEgg, isShadow, allowContextFallback, ...imgProps }) => {
''',
'''    allowContextFallback?: boolean;
    profileLocalSpecies?: boolean;
} & Omit<SpriteImgProps, 'spriteInfos' | 'size'>;

export const SpeciesImg: React.FC<SpeciesImgProps> = ({ species, context, form, isFemale, isShiny, isEgg, isShadow, allowContextFallback, profileLocalSpecies, ...imgProps }) => {
''')
replace_once(species_img_ess,
'''    const usedSpecies = species === 0
        ? 1
        : species;
''',
'''    if (profileLocalSpecies)
        return null;

    const usedSpecies = species === 0
        ? 1
        : species;
''')

replace_once(details_main,
'''    const staticForms = allForms?.[ pkm.context ]
        ?? (pkm.romHackProfile
            ? Object.values(allForms ?? {}).reverse().find(forms => forms?.[ pkm.form ] ?? forms?.[ 0 ])
            : undefined);
    const formObj = staticForms?.[ pkm.form ] ?? staticForms?.[ 0 ];
    const speciesName = formObj?.name ?? '';
''',
'''    const staticForms = allForms?.[ pkm.context ]
        ?? (pkm.romHackProfile && !pkm.romHackSpeciesName
            ? Object.values(allForms ?? {}).reverse().find(forms => forms?.[ pkm.form ] ?? forms?.[ 0 ])
            : undefined);
    const formObj = staticForms?.[ pkm.form ] ?? staticForms?.[ 0 ];
    const speciesName = pkm.romHackSpeciesName ?? formObj?.name ?? '';
''')
replace_once(details_main,
'''            allowContextFallback={!!pkm.romHackProfile}
        />
''',
'''            allowContextFallback={!!pkm.romHackProfile && !pkm.romHackSpeciesName}
            profileLocalSpecies={!!pkm.romHackSpeciesName}
        />
''')

replace_once(storage_save_item,
'''                    'canEvolve', 'romHackProfile',
''',
'''                    'canEvolve', 'romHackProfile', 'romHackSpeciesName',
''')
replace_once(storage_save_item,
'''        const { id, species, nickname, level, boxSlot, form, gender, contextVersion, isAlpha, isShiny, nSparkle, isEgg, isShadow, canEvolve, romHackProfile } = savePkm;
''',
'''        const { id, species, nickname, level, boxSlot, form, gender, contextVersion, isAlpha, isShiny, nSparkle, isEgg, isShadow, canEvolve, romHackProfile, romHackSpeciesName } = savePkm;
''')
replace_once(storage_save_item,
'''            allowContextFallback={!!romHackProfile}
            name={nickname}
''',
'''            allowContextFallback={!!romHackProfile && !romHackSpeciesName}
            profileLocalSpecies={!!romHackSpeciesName}
            name={nickname}
''')

replace_once(storage_main_item,
'''                        'form', 'gender', 'isEgg', 'isAlpha', 'isShiny', 'nSparkle', 'isShadow', 'isExternal', 'heldItem', 'romHackProfile',
''',
'''                        'form', 'gender', 'isEgg', 'isAlpha', 'isShiny', 'nSparkle', 'isShadow', 'isExternal', 'heldItem', 'romHackProfile', 'romHackSpeciesName',
''')
replace_once(storage_main_item,
'''        const { id, species, nickname, level, boxSlot, contextVersion, context, form, gender, isEgg, isAlpha, isShiny, nSparkle, isShadow, isExternal, heldItem, romHackProfile } = mainVariant;
''',
'''        const { id, species, nickname, level, boxSlot, contextVersion, context, form, gender, isEgg, isAlpha, isShiny, nSparkle, isShadow, isExternal, heldItem, romHackProfile, romHackSpeciesName } = mainVariant;
''')
replace_once(storage_main_item,
'''            allowContextFallback={!!romHackProfile}
            name={nickname}
''',
'''            allowContextFallback={!!romHackProfile && !romHackSpeciesName}
            profileLocalSpecies={!!romHackSpeciesName}
            name={nickname}
''')

path_icon = PKVAULT / "frontend/src/ui/form/globs-input/util/get-path-icon.tsx"
replace_once(path_icon,
'''const saveExts = new Set([ 'sav', 'dsv', 'dat', 'gci', 'srm', 'fla', 'bin' ]);
''',
'''const saveExts = new Set([ 'sav', 'dsv', 'dat', 'gci', 'srm', 'fla', 'bin', 'rxdata' ]);
''')

print("PKVault V8 alpha8 Essentials read/write save integration applied")


# Alpha8: pass the profile-local sprite guard through the shared StorageItem.
storage_item_ess = PKVAULT / "frontend/src/storage/item/storage-item.tsx"
replace_once(storage_item_ess,
'''  & Pick<SpeciesImgProps, 'species' | 'context' | 'form' | 'isFemale' | 'isShiny' | 'isEgg' | 'isShadow' | 'allowContextFallback'>;
''',
'''  & Pick<SpeciesImgProps, 'species' | 'context' | 'form' | 'isFemale' | 'isShiny' | 'isEgg' | 'isShadow' | 'allowContextFallback' | 'profileLocalSpecies'>;
''')
replace_once(storage_item_ess,
'''  isShadow,
  allowContextFallback,

  ...rest
''',
'''  isShadow,
  allowContextFallback,
  profileLocalSpecies,

  ...rest
''')
replace_once(storage_item_ess,
'''      <SpeciesImg species={species} context={context} form={form} isFemale={isFemale} isShiny={isShiny} isEgg={isEgg} isShadow={isShadow} allowContextFallback={allowContextFallback} />
''',
'''      <SpeciesImg species={species} context={context} form={form} isFemale={isFemale} isShiny={isShiny} isEgg={isEgg} isShadow={isShadow}
        allowContextFallback={allowContextFallback} profileLocalSpecies={profileLocalSpecies} />
''')
print("PKVault V8 alpha8 profileLocalSpecies wiring through StorageItem applied")


# ---------------------------------------------------------------------------
# V8 alpha10: make Essentials .rxdata support reachable from the Windows UI.
# ---------------------------------------------------------------------------
settings_service_v8 = PKVAULT / "PKVault.Core/settings/services/SettingsService.cs"
replace_once(settings_service_v8,
'''        var canUploadSaves = !isDesktop;
        var canDeleteSaves = !isDesktop;
''',
'''        // V8: desktop users need the same direct save import path as web
        // so Pokémon Uranium / Insurgence .rxdata files can be tested and used.
        var canUploadSaves = true;
        var canDeleteSaves = !isDesktop;
''')

replace_once(saves_essentials,
'''        string[] globs = [
            settings.SavesUploadsPath,
            ..settings.SettingsMutable.SAVE_GLOBS
        ];
''',
'''        // A directory path by itself is not a reliable file match. Scan the
        // upload directory recursively so uploaded .rxdata saves are reloaded
        // immediately after import.
        var uploadsGlob = MatcherUtil.NormalizePath(Path.Combine(settings.SavesUploadsPath, "**/*"));
        string[] globs = [
            uploadsGlob,
            ..settings.SettingsMutable.SAVE_GLOBS
        ];
''')

save_infos_route_v8 = PKVAULT / "PKVault.Core/save-infos/routes/SaveInfosRoute.cs"
replace_once(save_infos_route_v8,
'''        List<string> savePaths = [];
''',
'''        List<string> savePaths = [];
        List<byte[]> bufferedFiles = [];
''')
replace_once(save_infos_route_v8,
'''            var save = await savesLoadersService.CheckSaveData(fileBytes, filename, overwrite);
            ArgumentException.ThrowIfNullOrWhiteSpace(save.Metadata.FilePath);
''',
'''            bufferedFiles.Add(fileBytes);

            var save = await savesLoadersService.CheckSaveData(fileBytes, filename, overwrite);
            ArgumentException.ThrowIfNullOrWhiteSpace(save.Metadata.FilePath);
''')
replace_once(save_infos_route_v8,
'''        for (var i = 0; i < saveFiles.Length; i++)
        {
            var saveFile = saveFiles[i];
            var savePath = savePaths[i];

            byte[] fileBytes;
            using (var ms = new MemoryStream())
            {
                await saveFile.Stream.CopyToAsync(ms);
                fileBytes = ms.ToArray();
            }

            await savesLoadersService.UploadSaveWithoutCheck(savePath, fileBytes);
        }
''',
'''        for (var i = 0; i < bufferedFiles.Count; i++)
        {
            await savesLoadersService.UploadSaveWithoutCheck(savePaths[i], bufferedFiles[i]);
        }
''')

print("PKVault V8 alpha10 Essentials desktop rxdata import plumbing applied")


# ---------------------------------------------------------------------------
# V8 alpha11: keep the native desktop UI and make folder save locations work.
# ---------------------------------------------------------------------------
# Alpha10 temporarily enabled the server-style upload UI on Windows. That is
# not the desired desktop workflow. Restore upstream desktop behavior.
replace_once(settings_service_v8,
'''        // V8: desktop users need the same direct save import path as web
        // so Pokémon Uranium / Insurgence .rxdata files can be tested and used.
        var canUploadSaves = true;
        var canDeleteSaves = !isDesktop;
''',
'''        var canUploadSaves = !isDesktop;
        var canDeleteSaves = !isDesktop;
''')

# Desktop "Add folder" stores a directory path with a trailing slash. Expand
# those directory entries to recursive file globs before scanning, so a normal
# Uranium/Insurgence save folder discovers Uranium.rxdata/Game.rxdata.
replace_once(saves_essentials,
'''        // A directory path by itself is not a reliable file match. Scan the
        // upload directory recursively so uploaded .rxdata saves are reloaded
        // immediately after import.
        var uploadsGlob = MatcherUtil.NormalizePath(Path.Combine(settings.SavesUploadsPath, "**/*"));
        string[] globs = [
            uploadsGlob,
            ..settings.SettingsMutable.SAVE_GLOBS
        ];
''',
'''        static string ExpandSaveLocation(string raw)
        {
            var trimmed = raw.Trim();
            if (trimmed.Length == 0)
                return trimmed;

            var excluded = trimmed[0] == '!';
            var body = excluded ? trimmed[1..] : trimmed;
            body = MatcherUtil.NormalizePath(body);

            if (body.EndsWith('/'))
                body = body.TrimEnd('/') + "/**/*";

            return excluded ? "!" + body : body;
        }

        var uploadsGlob = MatcherUtil.NormalizePath(Path.Combine(settings.SavesUploadsPath, "**/*"));
        var configuredSaveGlobs = settings.SettingsMutable.SAVE_GLOBS.Select(ExpandSaveLocation);
        string[] globs = [
            uploadsGlob,
            ..configuredSaveGlobs
        ];
''')

print("PKVault V8 alpha11 native desktop rxdata location scanning applied")


# ---------------------------------------------------------------------------
# V8 alpha12: native desktop save additions apply immediately.
# ---------------------------------------------------------------------------
settings_main_right_v8 = PKVAULT / "frontend/src/settings/main/settings-main-right.tsx"
replace_once(settings_main_right_v8,
r'''import { useSettingsGet } from '../../data/sdk/settings/settings.gen';
''',
r'''import { useSettingsEdit, useSettingsGet } from '../../data/sdk/settings/settings.gen';
''')
replace_once(settings_main_right_v8,
r'''    const settingsQuery = useSettingsGet();
    const settings = settingsQuery.data?.data;

    const form = useFormContext<SettingsFormData>();
''',
r'''    const settingsQuery = useSettingsGet();
    const settingsMutation = useSettingsEdit();
    const settings = settingsQuery.data?.data;

    const form = useFormContext<SettingsFormData>();

    const commitAddedSaveLocations = async (value: string) => {
        if (!settings?.settingsMutable)
            return;

        const result = await settingsMutation.mutateAsync({
            data: {
                ...settings.settingsMutable,
                savE_GLOBS: value.split('\n').map(v => v.trim()).filter(Boolean),
            },
        });

        const next = result.data.settings?.settingsMutable;
        if (next)
            form.resetField('savE_GLOBS', {
                defaultValue: next.savE_GLOBS.join('\n'),
            });
    };
''')
replace_once(settings_main_right_v8,
r'''            onChange={(value) => form.setValue('savE_GLOBS', value, { shouldDirty: true })}
            disabled={!settings?.canUpdateSettings}
''',
r'''            onChange={(value) => form.setValue('savE_GLOBS', value, { shouldDirty: true })}
            onAddCommitted={commitAddedSaveLocations}
            disabled={!settings?.canUpdateSettings || settingsMutation.isPending}
''')

globs_list_v8 = PKVAULT / "frontend/src/settings/globs-input/globs-input-list.tsx"
replace_once(globs_list_v8,
r'''        onChange: (value: string) => void;
        limit: number;
''',
r'''        onChange: (value: string) => void;
        onAddCommitted?: (value: string) => void | Promise<void>;
        limit: number;
''')
replace_once(globs_list_v8,
r'''export const GlobsInputList: React.FC<GlobsInputListProps> = ({ name, value, onChange, limit, disabled, extraValue, ...rest }) => {
''',
r'''export const GlobsInputList: React.FC<GlobsInputListProps> = ({ name, value, onChange, onAddCommitted, limit, disabled, extraValue, ...rest }) => {
''')
replace_once(globs_list_v8,
r'''            const newValues = [ ...splittedValue, ...newValue ];
            onChange(newValues.join('\n'));

            if (!desktopMessage.fileExplore) {
''',
r'''            const newValues = [ ...splittedValue, ...newValue ];
            const nextValue = newValues.join('\n');
            onChange(nextValue);
            await onAddCommitted?.(nextValue);

            if (!desktopMessage.fileExplore) {
''')

print("PKVault V8 alpha12 Essentials native location auto-apply applied")


# ---------------------------------------------------------------------------
# V8 alpha14: full Uranium local species registry, packaged game-style icons,
# and safe party -> central-vault extraction.
# ---------------------------------------------------------------------------
shutil.copyfile(HERE / "essentials/UraniumProfile.Generated.cs", essentials_core / "UraniumProfile.Generated.cs")
shutil.copyfile(HERE / "uranium-profile.ts", frontend_romhacks / "uranium-profile.ts")

essentials_reader_v14 = essentials_core / "EssentialsLegacySaveReader.cs"
replace_once(essentials_reader_v14,
'''        if (game == EssentialsGameKind.Uranium && Uranium.TryGetValue(species, out var u))
            return u.Name;
''',
'''        if (game == EssentialsGameKind.Uranium && UraniumProfileGenerated.TryGet(species, out var u))
            return u.Name;
''')
replace_once(essentials_reader_v14,
'''    public static string[] GetTypes(EssentialsGameKind game, int species, int form)
        => game == EssentialsGameKind.Uranium && Uranium.TryGetValue(species, out var u) ? u.Types : [];

    public static int[] GetBaseStats(EssentialsGameKind game, int species, int form)
        => game == EssentialsGameKind.Uranium && Uranium.TryGetValue(species, out var u) ? u.Stats : [1,1,1,1,1,1];
''',
'''    public static string[] GetTypes(EssentialsGameKind game, int species, int form)
        => game == EssentialsGameKind.Uranium && UraniumProfileGenerated.TryGet(species, out var u) ? u.Types : [];

    public static int[] GetBaseStats(EssentialsGameKind game, int species, int form)
        => game == EssentialsGameKind.Uranium && UraniumProfileGenerated.TryGet(species, out var u) ? u.Stats : [1,1,1,1,1,1];
''')

replace_once(species_img_ess,
'''import { getSpritesheetUrl } from './util/get-spritesheet-url';
''',
'''import { getSpritesheetUrl } from './util/get-spritesheet-url';
import { getUraniumIconPath, isUraniumSpeciesId, URANIUM_PROFILE_ID } from '../romhacks/uranium-profile';
''')
replace_once(species_img_ess,
'''    allowContextFallback?: boolean;
    profileLocalSpecies?: boolean;
} & Omit<SpriteImgProps, 'spriteInfos' | 'size'>;

export const SpeciesImg: React.FC<SpeciesImgProps> = ({ species, context, form, isFemale, isShiny, isEgg, isShadow, allowContextFallback, profileLocalSpecies, ...imgProps }) => {
''',
'''    allowContextFallback?: boolean;
    profileLocalSpecies?: boolean;
    romHackProfile?: string | null;
    romHackLocalSpeciesId?: number | null;
    romHackSpeciesName?: string | null;
} & Omit<SpriteImgProps, 'spriteInfos' | 'size'>;

export const SpeciesImg: React.FC<SpeciesImgProps> = ({
    species, context, form, isFemale, isShiny, isEgg, isShadow,
    allowContextFallback, profileLocalSpecies,
    romHackProfile, romHackLocalSpeciesId, romHackSpeciesName,
    ...imgProps
}) => {
''')
replace_once(species_img_ess,
'''    if (profileLocalSpecies)
        return null;
''',
'''    if (profileLocalSpecies) {
        const localSpeciesId = romHackLocalSpeciesId ?? species;
        const isUranium = romHackProfile === URANIUM_PROFILE_ID && isUraniumSpeciesId(localSpeciesId);
        const fallbackIcon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='5' fill='%23444'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-size='20' fill='white'%3E%3F%3C/text%3E%3C/svg%3E";

        return <UISpeciesImg
            {...imgProps}
            data-rom-hack-profile={romHackProfile ?? undefined}
            data-local-species-id={localSpeciesId}
            sheetUrl={isUranium ? getUraniumIconPath(localSpeciesId) : fallbackIcon}
            spriteInfos={{ x: 0, y: 0, width: 32, height: 32 }}
            sourceRealHeight={32}
            species={species || localSpeciesId}
            isShadow={false}
            title={romHackSpeciesName ?? (romHackProfile ?? 'ROM hack') + ' #' + localSpeciesId}
        />;
    }
''')

replace_once(storage_item_ess,
'''  & Pick<SpeciesImgProps, 'species' | 'context' | 'form' | 'isFemale' | 'isShiny' | 'isEgg' | 'isShadow' | 'allowContextFallback' | 'profileLocalSpecies'>;
''',
'''  & Pick<SpeciesImgProps, 'species' | 'context' | 'form' | 'isFemale' | 'isShiny' | 'isEgg' | 'isShadow' | 'allowContextFallback' | 'profileLocalSpecies' | 'romHackProfile' | 'romHackLocalSpeciesId' | 'romHackSpeciesName'>;
''')
replace_once(storage_item_ess,
'''  profileLocalSpecies,

  ...rest
''',
'''  profileLocalSpecies,
  romHackProfile,
  romHackLocalSpeciesId,
  romHackSpeciesName,

  ...rest
''')
replace_once(storage_item_ess,
'''        allowContextFallback={allowContextFallback} profileLocalSpecies={profileLocalSpecies} />
''',
'''        allowContextFallback={allowContextFallback} profileLocalSpecies={profileLocalSpecies}
        romHackProfile={romHackProfile} romHackLocalSpeciesId={romHackLocalSpeciesId}
        romHackSpeciesName={romHackSpeciesName} />
''')

replace_once(storage_save_item,
'''                    'canEvolve', 'romHackProfile', 'romHackSpeciesName',
''',
'''                    'canEvolve', 'romHackProfile', 'romHackSpeciesName', 'romHackLocalSpeciesId',
''')
replace_once(storage_save_item,
'''        const { id, species, nickname, level, boxSlot, form, gender, contextVersion, isAlpha, isShiny, nSparkle, isEgg, isShadow, canEvolve, romHackProfile, romHackSpeciesName } = savePkm;
''',
'''        const { id, species, nickname, level, boxSlot, form, gender, contextVersion, isAlpha, isShiny, nSparkle, isEgg, isShadow, canEvolve, romHackProfile, romHackSpeciesName, romHackLocalSpeciesId } = savePkm;
''')
replace_once(storage_save_item,
'''            profileLocalSpecies={!!romHackSpeciesName}
            name={nickname}
''',
'''            profileLocalSpecies={!!romHackSpeciesName}
            romHackProfile={romHackProfile}
            romHackLocalSpeciesId={romHackLocalSpeciesId}
            romHackSpeciesName={romHackSpeciesName}
            name={romHackSpeciesName ?? nickname}
''')

replace_once(storage_main_item,
'''                        'form', 'gender', 'isEgg', 'isAlpha', 'isShiny', 'nSparkle', 'isShadow', 'isExternal', 'heldItem', 'romHackProfile', 'romHackSpeciesName',
''',
'''                        'form', 'gender', 'isEgg', 'isAlpha', 'isShiny', 'nSparkle', 'isShadow', 'isExternal', 'heldItem', 'romHackProfile', 'romHackSpeciesName', 'romHackLocalSpeciesId',
''')
replace_once(storage_main_item,
'''        const { id, species, nickname, level, boxSlot, contextVersion, context, form, gender, isEgg, isAlpha, isShiny, nSparkle, isShadow, isExternal, heldItem, romHackProfile, romHackSpeciesName } = mainVariant;
''',
'''        const { id, species, nickname, level, boxSlot, contextVersion, context, form, gender, isEgg, isAlpha, isShiny, nSparkle, isShadow, isExternal, heldItem, romHackProfile, romHackSpeciesName, romHackLocalSpeciesId } = mainVariant;
''')
replace_once(storage_main_item,
'''            profileLocalSpecies={!!romHackSpeciesName}
            name={nickname}
''',
'''            profileLocalSpecies={!!romHackSpeciesName}
            romHackProfile={romHackProfile}
            romHackLocalSpeciesId={romHackLocalSpeciesId}
            romHackSpeciesName={romHackSpeciesName}
            name={romHackSpeciesName ?? nickname}
''')

replace_once(details_main,
'''            profileLocalSpecies={!!pkm.romHackSpeciesName}
        />
''',
'''            profileLocalSpecies={!!pkm.romHackSpeciesName}
            romHackProfile={pkm.romHackProfile}
            romHackLocalSpeciesId={pkm.romHackLocalSpeciesId}
            romHackSpeciesName={pkm.romHackSpeciesName}
        />
''')

replace_once(pkm_save_dto,
'''    public bool CanMoveToMain => IsEnabled
        && (Pkm.GetMutablePkm() is PKEssentials || (Pkm.Version > 0 && Pkm.Generation > 0))
        && CanDelete && !IsShadow && !IsEgg && !IsLocked && Party == -1;
''',
'''    public bool CanMoveToMain => IsEnabled
        && (Pkm.GetMutablePkm() is PKEssentials || (Pkm.Version > 0 && Pkm.Generation > 0))
        && CanDelete && !IsShadow && !IsEgg && !IsLocked
        && (Party == -1 || Pkm.GetMutablePkm() is PKEssentials);
''')

replace_once(move_action,
'''        var saveLoaders = savesLoadersService.GetLoaders(sourceSaveId);

        if (savePkm.Pkm.GetMutablePkm() is IShadowCapture savePkmShadow && savePkmShadow.IsShadow)
''',
'''        var saveLoaders = savesLoadersService.GetLoaders(sourceSaveId);
        var keepEssentialsParty = savePkm.Pkm.GetMutablePkm() is PKEssentials && savePkm.Party >= 0;
        var attachToSource = input.attached || keepEssentialsParty;

        if (savePkm.Pkm.GetMutablePkm() is IShadowCapture savePkmShadow && savePkmShadow.IsShadow)
''')
replace_once(move_action,
'''            AttachedSaveId: input.attached ? sourceSaveId : null,
            AttachedSavePkmIdBase: input.attached ? savePkm.IdBase : null,
''',
'''            AttachedSaveId: attachToSource ? sourceSaveId : null,
            AttachedSavePkmIdBase: attachToSource ? savePkm.IdBase : null,
''')
replace_once(move_action,
'''            if (!input.attached)
            {
                pkmVariantEntity.AttachedSaveId = null;
''',
'''            if (!attachToSource)
            {
                pkmVariantEntity.AttachedSaveId = null;
''')
replace_once(move_action,
'''        if (!input.attached)
        {
            // remove pkm from save
            saveLoaders.Pkms.DeleteDto(savePkm.Id);
        }
''',
'''        if (!attachToSource)
        {
            // Remove boxed Pokemon from the save. Essentials party Pokemon stay
            // in-place and become an attached vault copy instead.
            saveLoaders.Pkms.DeleteDto(savePkm.Id);
        }
''')

print("PKVault V8 alpha14 Uranium species/icons and party extraction applied")


# ---------------------------------------------------------------------------
# V8 alpha15: hide the nonstandard party-number badge for Essentials,
# add exact Insurgence species support, and allow safe official/MISSINGNO import.
# ---------------------------------------------------------------------------
shutil.copyfile(HERE / "essentials/InsurgenceProfile.Generated.cs", essentials_core / "InsurgenceProfile.Generated.cs")
shutil.copyfile(HERE / "essentials/EssentialsInterop.cs", essentials_core / "EssentialsInterop.cs")

essentials_reader_v15 = essentials_core / "EssentialsLegacySaveReader.cs"
replace_once(essentials_reader_v15,
'''        if (game == EssentialsGameKind.Insurgence && species > 0 && species < GameInfo.Strings.Species.Count)
            return GameInfo.Strings.Species[species];
''',
'''        if (game == EssentialsGameKind.Insurgence)
        {
            if (InsurgenceProfileGenerated.IsOfficialSpecies(species) && species < GameInfo.Strings.Species.Count)
                return GameInfo.Strings.Species[species];
            if (InsurgenceProfileGenerated.TryGetCustom(species, out var insurgence))
                return insurgence.Name;
        }
''')
replace_once(essentials_reader_v15,
'''    public static string[] GetTypes(EssentialsGameKind game, int species, int form)
        => game == EssentialsGameKind.Uranium && UraniumProfileGenerated.TryGet(species, out var u) ? u.Types : [];

    public static int[] GetBaseStats(EssentialsGameKind game, int species, int form)
        => game == EssentialsGameKind.Uranium && UraniumProfileGenerated.TryGet(species, out var u) ? u.Stats : [1,1,1,1,1,1];
''',
'''    public static string[] GetTypes(EssentialsGameKind game, int species, int form)
    {
        if (game == EssentialsGameKind.Uranium && UraniumProfileGenerated.TryGet(species, out var u))
            return u.Types;
        if (game == EssentialsGameKind.Insurgence)
        {
            if (InsurgenceProfileGenerated.TryGetCustom(species, out var custom))
                return custom.Types;
            if (InsurgenceProfileGenerated.IsOfficialSpecies(species))
            {
                var personal = PersonalTable.AO.GetFormEntry((ushort)species, (byte)Math.Clamp(form, 0, byte.MaxValue));
                var type1 = GameInfo.Strings.Types[personal.Type1];
                var type2 = GameInfo.Strings.Types[personal.Type2];
                return personal.Type1 == personal.Type2 ? [type1] : [type1, type2];
            }
        }
        return [];
    }

    public static int[] GetBaseStats(EssentialsGameKind game, int species, int form)
    {
        if (game == EssentialsGameKind.Uranium && UraniumProfileGenerated.TryGet(species, out var u))
            return u.Stats;
        if (game == EssentialsGameKind.Insurgence)
        {
            if (InsurgenceProfileGenerated.TryGetCustom(species, out var custom))
                return custom.Stats;
            if (InsurgenceProfileGenerated.IsOfficialSpecies(species))
            {
                var personal = PersonalTable.AO.GetFormEntry((ushort)species, (byte)Math.Clamp(form, 0, byte.MaxValue));
                return [personal.HP, personal.ATK, personal.DEF, personal.SPE, personal.SPA, personal.SPD];
            }
        }
        return [1,1,1,1,1,1];
    }
''')

# Official Insurgence species use ordinary PKVault sprites/names rather than
# being treated as profile-local custom IDs.
replace_once(dto,
'''    public string? RomHackSpeciesName => Pkm.GetMutablePkm() is PKEssentials essentials ? essentials.SpeciesName : null;
''',
'''    public string? RomHackSpeciesName => Pkm.GetMutablePkm() is PKEssentials essentials
        ? string.Equals(essentials.ProfileId, InsurgenceProfileGenerated.ProfileId, StringComparison.Ordinal)
            && InsurgenceProfileGenerated.IsOfficialSpecies(essentials.LocalSpeciesId)
                ? null
                : essentials.SpeciesName
        : null;
''')

# The green numeric party badge is not part of the requested Essentials UI.
replace_once(storage_save_item,
'''                party={savePkm.party >= 0 ? savePkm.party : undefined}
''',
'''                party={!romHackProfile && savePkm.party >= 0 ? savePkm.party : undefined}
''')

# Main->save: Essentials targets use explicit profile conversion and do not
# require a synthetic PK3 "same context" variant first.
move_action_v15 = PKVAULT / "PKVault.Core/storage/data-action/MovePkmAction.cs"
replace_once(move_action_v15,
'''        var pkmVariantForContext = pkmVariants.Find(version => version.Context == saveLoaders.Save.Context);

        // if pkmVariant for context doesn't exist
''',
'''        var essentialsTarget = saveLoaders.Save.GetSave() as EssentialsLegacySaveFile;
        var pkmVariantForContext = essentialsTarget != null
            ? pkmVariants.Find(version => version.IsMain) ?? pkmVariants.FirstOrDefault()
            : pkmVariants.Find(version => version.Context == saveLoaders.Save.Context);

        // if pkmVariant for context doesn't exist
''')
replace_once(move_action_v15,
'''        if (pkmVariantForContext == default)
        {
            var mainVariant = pkmVariants.Find(variant => variant.IsMain);
''',
'''        if (pkmVariantForContext == default)
        {
            if (essentialsTarget != null)
                throw new ArgumentException("No source Pokémon variant exists for Essentials import.");

            var mainVariant = pkmVariants.Find(variant => variant.IsMain);
''')
replace_once(move_action_v15,
'''        if (pkmVariant.Context != saveLoaders.Save.Context)
        {
            throw new ArgumentException($"PkmVariantEntity Context not compatible with save for id={pkmVariant.Id}, context={pkmVariant.Context}, save.context={saveLoaders.Save.Context}");
        }

        var pkm = await pkmVariantLoader.GetPKM(pkmVariant);

        if (!saveLoaders.Save.IsPkmAllowed(pkm))
''',
'''        if (pkmVariant.Context != saveLoaders.Save.Context && saveLoaders.Save.GetSave() is not EssentialsLegacySaveFile)
        {
            throw new ArgumentException($"PkmVariantEntity Context not compatible with save for id={pkmVariant.Id}, context={pkmVariant.Context}, save.context={saveLoaders.Save.Context}");
        }

        var pkm = await pkmVariantLoader.GetPKM(pkmVariant);
        if (saveLoaders.Save.GetSave() is EssentialsLegacySaveFile essentialsSave
            && pkm.GetMutablePkm() is not PKEssentials)
        {
            if (input.attached)
                throw new ArgumentException("Cross-format attached moves into Essentials saves are not supported; use a normal move.");
            pkm = EssentialsInterop.ImportTo(essentialsSave, pkm);
        }

        if (!saveLoaders.Save.IsPkmAllowed(pkm))
''')

# Direct save->save into Insurgence uses the same explicit import mapping.
replace_once(move_action_v15,
'''        if (sourcePkmDto.Context != targetSaveLoaders.Save.Context)
        {
            throw new ArgumentException($"Save Pkm not compatible with save for id={sourcePkmDto.Id}, context={sourcePkmDto.Context}, save.context={targetSaveLoaders.Save.Context}");
        }

        if (!targetSaveLoaders.Save.IsPkmAllowed(sourcePkmDto.Pkm))
        {
            throw new ArgumentException($"Save Pkm profile/species not compatible with target save for id={sourcePkmDto.Id}.");
        }

        var targetPkmDto = targetSaveLoaders.Pkms.GetDto(input.targetBoxId, targetBoxSlot);
''',
'''        var targetEssentials = targetSaveLoaders.Save.GetSave() as EssentialsLegacySaveFile;
        if (sourcePkmDto.Context != targetSaveLoaders.Save.Context && targetEssentials == null)
        {
            throw new ArgumentException($"Save Pkm not compatible with save for id={sourcePkmDto.Id}, context={sourcePkmDto.Context}, save.context={targetSaveLoaders.Save.Context}");
        }

        var pkmForTarget = sourcePkmDto.Pkm;
        if (targetEssentials != null && pkmForTarget.GetMutablePkm() is not PKEssentials)
            pkmForTarget = EssentialsInterop.ImportTo(targetEssentials, pkmForTarget);

        if (!targetSaveLoaders.Save.IsPkmAllowed(pkmForTarget))
        {
            throw new ArgumentException($"Save Pkm profile/species not compatible with target save for id={sourcePkmDto.Id}.");
        }

        var targetPkmDto = targetSaveLoaders.Pkms.GetDto(input.targetBoxId, targetBoxSlot);
''')
replace_once(move_action_v15,
'''        if (targetPkmDto != null && !targetPkmDto.CanMove)
        {
            throw new ArgumentException("Save Pkm cannot move");
        }
''',
'''        if (targetPkmDto != null && !targetPkmDto.CanMove)
        {
            throw new ArgumentException("Save Pkm cannot move");
        }
        if (targetPkmDto != null && targetEssentials != null
            && sourcePkmDto.Pkm.GetMutablePkm() is not PKEssentials)
        {
            throw new ArgumentException("Cross-format save-to-save swaps require an empty target slot.");
        }
''')
replace_once(move_action_v15,
'''        sourcePkmDto = sourceSaveLoaders.Pkms.CreateDTO(
            targetSaveLoaders.Save, sourcePkmDto.Pkm, input.targetBoxId, targetBoxSlot
        );
''',
'''        sourcePkmDto = targetSaveLoaders.Pkms.CreateDTO(
            targetSaveLoaders.Save, pkmForTarget, input.targetBoxId, targetBoxSlot
        );
''')

print("PKVault V8 alpha15 Insurgence compatibility + no Essentials party badge applied")


# ---------------------------------------------------------------------------
# V8 alpha16: Uranium is an overlay, not a duplicate National Dex.
# Official base-form species collapse onto normal PKVault presentation/dex;
# Uranium-added species get their own dex and static front battle sprites.
# ---------------------------------------------------------------------------
shutil.copyfile(HERE / "uranium-pokedex.tsx", frontend_romhacks / "uranium-pokedex.tsx")
shutil.copyfile(HERE / "essentials/DexEssentialsService.cs", essentials_core / "DexEssentialsService.cs")

# PKEssentials DTO presentation: official reused Pokémon use normal species/type UI.
replace_once(dto,
'''    public string[]? RomHackTypes => Pkm.GetMutablePkm() is PKEssentials essentials
        ? essentials.TypeNames
        : TooManyTypesCompat.GetTypes(Pkm);
    public string? RomHackSpeciesName => Pkm.GetMutablePkm() is PKEssentials essentials
        ? string.Equals(essentials.ProfileId, InsurgenceProfileGenerated.ProfileId, StringComparison.Ordinal)
            && InsurgenceProfileGenerated.IsOfficialSpecies(essentials.LocalSpeciesId)
                ? null
                : essentials.SpeciesName
        : null;
''',
'''    public string[]? RomHackTypes => Pkm.GetMutablePkm() is PKEssentials essentials
        ? essentials.OfficialNationalDexId > 0 ? null : essentials.TypeNames
        : TooManyTypesCompat.GetTypes(Pkm);
    public string? RomHackSpeciesName => Pkm.GetMutablePkm() is PKEssentials essentials
        ? essentials.OfficialNationalDexId > 0 ? null : essentials.SpeciesName
        : null;
''')

# Uranium local custom sprites now use a real static 80x80 battle-front frame.
replace_once(species_img_ess,
'''import { getUraniumIconPath, isUraniumSpeciesId, URANIUM_PROFILE_ID } from '../romhacks/uranium-profile';
''',
'''import { getUraniumFrontSpritePath, isUraniumSpeciesId, URANIUM_PROFILE_ID } from '../romhacks/uranium-profile';
''')
replace_once(species_img_ess,
'''            sheetUrl={isUranium ? getUraniumIconPath(localSpeciesId) : fallbackIcon}
            spriteInfos={{ x: 0, y: 0, width: 32, height: 32 }}
            sourceRealHeight={32}
''',
'''            sheetUrl={isUranium ? getUraniumFrontSpritePath(localSpeciesId) : fallbackIcon}
            spriteInfos={{ x: 0, y: 0, width: isUranium ? 80 : 32, height: isUranium ? 80 : 32 }}
            sourceRealHeight={isUranium ? 80 : 32}
''')

# Official Pokémon from Essentials saves contribute to the normal National Dex.
dex_service_v16 = PKVAULT / "PKVault.Core/dex/services/DexService.cs"
replace_once(dex_service_v16,
'''            SAV3 { DirectSpeciesIDs: true } tmt3 => new DexTmtService(tmt3),
            SAV3 sav3 => new Dex123Service(sav3),
''',
'''            SAV3 { DirectSpeciesIDs: true } tmt3 => new DexTmtService(tmt3),
            EssentialsLegacySaveFile essentials => new DexEssentialsService(essentials),
            SAV3 sav3 => new Dex123Service(sav3),
''')

# Add the Uranium-added-only section to the ordinary Pokedex page.
pokedex_list_v16 = PKVAULT / "frontend/src/pokedex/list/pokedex-list.tsx"
replace_once(pokedex_list_v16,
'''import { PokedexItem } from "./pokedex-item";
''',
'''import { PokedexItem } from "./pokedex-item";
import { UraniumPokedexSection } from '../../romhacks/uranium-pokedex';
''')
replace_once(pokedex_list_v16,
'''        ])}
    </UIPokedexMain>
''',
'''        ])}

      <UraniumPokedexSection />
    </UIPokedexMain>
''')

# Synthetic Uranium dex selections use the dedicated custom details renderer.
pokedex_wrapper_v16 = PKVAULT / "frontend/src/pokedex/details/pokedex-main-wrapper-details.tsx"
replace_once(pokedex_wrapper_v16,
'''import { PokedexDetails } from './pokedex-details';
''',
'''import { PokedexDetails } from './pokedex-details';
import { UraniumPokedexDetails } from '../../romhacks/uranium-pokedex';
import { URANIUM_DEX_OFFSET, URANIUM_SPECIES_COUNT } from '../../romhacks/uranium-profile';
''')
replace_once(pokedex_wrapper_v16,
'''    const opened = Route.useSearch({ select: search => search.selected !== undefined });

    const navigate = Route.useNavigate();
''',
'''    const selected = Route.useSearch({ select: search => search.selected });
    const opened = selected !== undefined;
    const isUraniumDex = selected !== undefined
        && selected > URANIUM_DEX_OFFSET
        && selected <= URANIUM_DEX_OFFSET + URANIUM_SPECIES_COUNT;

    const navigate = Route.useNavigate();
''')
replace_once(pokedex_wrapper_v16,
'''        details={<PokedexDetails />}
''',
'''        details={isUraniumDex ? <UraniumPokedexDetails /> : <PokedexDetails />}
''')

print("PKVault V8 alpha16 Uranium overlay dex + static front battlers applied")


# ---------------------------------------------------------------------------
# V8 alpha17: normalize Uranium front-sprite artwork to PKVault icon scale.
#
# PKVault's UISpeciesImg reserves the normal 96px species slot. Uranium's
# static 80x80 battle frames were filling that entire slot, making them look
# much larger than the native PKVault artwork. Keep the 96px layout footprint
# so cards/rows do not move, but scale the custom artwork itself to 56px,
# matching the established custom-icon normalization used by PKVault.
# ---------------------------------------------------------------------------
ui_sprite_css_v17 = PKVAULT / "frontend/src/ui/sprite-img/ui-sprite-img.module.css"
replace_once(ui_sprite_css_v17,
'''    transform: scale(var(--scale));
''',
'''    transform: scale(calc(var(--scale) * var(--sprite-content-scale, 1)));
''')

replace_once(species_img_ess,
'''            sourceRealHeight={isUranium ? 80 : 32}
            species={species || localSpeciesId}
''',
'''            sourceRealHeight={isUranium ? 80 : 32}
            style={{
                ...imgProps.style,
                '--sprite-content-scale': isUranium ? (56 / 96) : undefined,
            } as React.CSSProperties}
            species={species || localSpeciesId}
''')

print("PKVault V8 alpha17 Uranium front-sprite sizing normalized to 56px art in the native 96px slot")


# ---------------------------------------------------------------------------
# V8 alpha18: Essentials party drags are real moves, not implicit links.
#
# Alpha14 kept party Pokemon in-place by forcing every Essentials party drag
# into attached mode. SavePkmLoader.DeleteDto() already marks party edits for
# FlushParty(), and SaveToMain() performs that flush after the move. Therefore
# normal party extraction can safely use the same move semantics as box
# extraction: delete the source slot, compact the party, and leave no attached
# save metadata. Explicit attached/link operations still remain attached.
# ---------------------------------------------------------------------------
move_action_v18 = PKVAULT / "PKVault.Core/storage/data-action/MovePkmAction.cs"
replace_once(move_action_v18,
'''        var keepEssentialsParty = savePkm.Pkm.GetMutablePkm() is PKEssentials && savePkm.Party >= 0;
        var attachToSource = input.attached || keepEssentialsParty;
''',
'''        var attachToSource = input.attached;
''')

replace_once(move_action_v18,
'''            // Remove boxed Pokemon from the save. Essentials party Pokemon stay
            // in-place and become an attached vault copy instead.
            saveLoaders.Pkms.DeleteDto(savePkm.Id);
''',
'''            // Normal save-to-vault moves remove the source Pokemon. Party
            // removal is compacted by SaveToMain() via SavePkmLoader.FlushParty().
            saveLoaders.Pkms.DeleteDto(savePkm.Id);
''')

print("PKVault V8 alpha18 Essentials party extraction now performs a real move")


# ---------------------------------------------------------------------------
# V8 alpha19: preflight incompatible Essentials swaps before touching either
# side of the move.
#
# A save -> main drag onto an occupied PKVault slot is a SWAP in upstream
# PKVault. If the source is Uranium/Insurgence, the existing central-vault
# Pokemon must be legal to move back into that Essentials save. Previously we
# moved the source Pokemon first and only discovered the incompatibility while
# trying to send the displaced vault Pokemon back, which made the failure look
# like the Uranium Pokemon had turned into the occupant.
#
# Reject that impossible swap up-front with a precise message. Empty PKVault
# slots continue to perform the real move added in alpha18.
# ---------------------------------------------------------------------------
move_action_v19 = PKVAULT / "PKVault.Core/storage/data-action/MovePkmAction.cs"
replace_once(move_action_v19,
'''        var existingSlots = (await pkmVariantLoader.GetEntitiesByBox(input.targetBoxId, targetBoxSlot)).Values.ToList();
        if (input.attached && existingSlots.Count > 0)
        {
            throw new ArgumentException("Switch not possible with attached move");
        }

        await SaveToMainWithoutCheckTarget(
''',
'''        var existingSlots = (await pkmVariantLoader.GetEntitiesByBox(input.targetBoxId, targetBoxSlot)).Values.ToList();
        if (input.attached && existingSlots.Count > 0)
        {
            throw new ArgumentException("Switch not possible with attached move");
        }

        if (!input.attached && existingSlots.Count > 0
            && saveLoaders.Save.GetSave() is EssentialsLegacySaveFile essentialsSource)
        {
            // Upstream save->main behavior swaps the existing vault occupant
            // back into the exact source save slot. Validate that displaced
            // Pokemon before moving/deleting anything.
            var displacedVariant = existingSlots.Find(v => v.Context == saveLoaders.Save.Context)
                ?? existingSlots.Find(v => v.IsMain)
                ?? existingSlots.First();

            var displacedPkm = await pkmVariantLoader.GetPKM(displacedVariant);
            if (!EssentialsInterop.CanImportTo(essentialsSource, displacedPkm))
            {
                var gameName = essentialsSource.Game switch
                {
                    EssentialsGameKind.Uranium => "Pokémon Uranium",
                    EssentialsGameKind.Insurgence => "Pokémon Insurgence",
                    _ => essentialsSource.ProfileId,
                };
                var displacedName = displacedPkm.GetMutablePkm() is PKEssentials displacedEssentials
                    ? displacedEssentials.SpeciesName
                    : displacedPkm.Nickname;

                throw new ArgumentException(
                    $"Target PKVault slot is occupied by {displacedName}, which cannot be swapped into {gameName}. "
                    + "Drop the Pokémon into an empty PKVault slot instead.");
            }
        }

        await SaveToMainWithoutCheckTarget(
''')

print("PKVault V8 alpha19 Essentials occupied-slot swap preflight applied")


# ---------------------------------------------------------------------------
# V8 alpha20: prevent same-folder concurrent desktop instances.
#
# PKVault uses a fixed db/pkvault-session.db per working directory. Upstream
# desktop startup resets/deletes that file. Launching a second EXE from the
# same folder while the first process is still alive therefore throws
# IOException ("file is being used by another process") and the frontend sees
# HTTP 500. Use a named mutex scoped to the normalized working directory:
# - same PKVault folder => second launch is blocked cleanly
# - separate folders => still allowed (required by our Trader A/B test)
# ---------------------------------------------------------------------------
desktop_program_v20 = PKVAULT / "PKVault.Desktop/Program.cs"

replace_once(desktop_program_v20,
'''using System.Reflection;
using System.Runtime.InteropServices;
using System.Text.Encodings.Web;
''',
'''using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Text.Encodings.Web;
''')

replace_once(desktop_program_v20,
'''    private static IServiceProvider? ServiceProvider = null;
    private static Task SetupTask = Task.CompletedTask;

    [DllImport("kernel32.dll")]
''',
'''    private static IServiceProvider? ServiceProvider = null;
    private static Task SetupTask = Task.CompletedTask;
    private static Mutex? InstanceMutex = null;
    private static bool OwnsInstanceMutex = false;

    [DllImport("kernel32.dll")]
''')

replace_once(desktop_program_v20,
'''    const uint ATTACH_PARENT_PROCESS = 0x0ffffffff;

    [STAThread]
    static void Main(string[] args)
''',
'''    const uint ATTACH_PARENT_PROCESS = 0x0ffffffff;

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    private static extern int MessageBoxW(IntPtr hWnd, string text, string caption, uint type);

    private static bool TryAcquireInstanceMutex()
    {
        var directory = Path.GetFullPath(Directory.GetCurrentDirectory())
            .TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)
            .ToUpperInvariant();
        var hash = Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(directory)));
        var mutexName = $"{(WindowsOS ? @"Local\" : "")}PKVault-{hash}";

        InstanceMutex = new Mutex(initiallyOwned: false, mutexName);
        try
        {
            OwnsInstanceMutex = InstanceMutex.WaitOne(0, false);
        }
        catch (AbandonedMutexException)
        {
            // The previous process died without releasing the mutex. Ownership
            // is transferred to this process, so startup may safely continue.
            OwnsInstanceMutex = true;
        }

        return OwnsInstanceMutex;
    }

    private static void ShowAlreadyRunningMessage()
    {
        const string message =
            "PKVault is already running from this folder.\\n\\n"
            + "Close the existing PKVault window/process before launching this copy again. "
            + "Separate PKVault folders can still run at the same time.";

        if (WindowsOS)
            _ = MessageBoxW(IntPtr.Zero, message, "PKVault already running", 0x00000040);
        else
            Console.Error.WriteLine(message);
    }

    [STAThread]
    static void Main(string[] args)
''')

replace_once(desktop_program_v20,
'''        Core.Program.Initialize();

        if (LinuxOS)
''',
'''        Core.Program.Initialize();

        if (!TryAcquireInstanceMutex())
        {
            ShowAlreadyRunningMessage();
            InstanceMutex?.Dispose();
            InstanceMutex = null;
            return;
        }

        if (LinuxOS)
''')

replace_once(desktop_program_v20,
'''        finally
        {
            LogUtil.Dispose();
        }
''',
'''        finally
        {
            if (OwnsInstanceMutex && InstanceMutex != null)
            {
                try
                {
                    InstanceMutex.ReleaseMutex();
                }
                catch (ApplicationException)
                {
                    // Process teardown safety: nothing else should be attempted.
                }
            }

            InstanceMutex?.Dispose();
            InstanceMutex = null;
            OwnsInstanceMutex = false;
            LogUtil.Dispose();
        }
''')

print("PKVault V8 alpha20 same-folder single-instance crash guard applied")


# ---------------------------------------------------------------------------
# V8 alpha21: profile-aware ROM-hack drag compatibility.
#
# Upstream frontend validates main->save moves with CompatibleWithVersions,
# which is calculated from Pkm.Species. For PKEssentials custom species that
# property is only a PKHeX-facing placeholder and may numerically overlap an
# unrelated official Pokémon. This caused a Uranium Pokémon moved into PKVault
# to become undroppable back into the SAME Uranium save and the refusal toast
# could name a different Pokémon.
#
# ROM-hack profile identity is authoritative:
# - source profile == target profile => compatible; do not interpret the local
#   species ID as an official National Dex ID.
# - source profile != target profile => reject in the frontend before backend.
# - ordinary Pokémon keep the normal CompatibleWithVersions behavior.
# Backend EssentialsInterop / SaveWrapper.IsPkmAllowed remains the final guard.
# ---------------------------------------------------------------------------
validate_root_v21 = PKVAULT / "frontend/src/storage/move/validation/rules/validate-root.ts"
replace_once(validate_root_v21,
'''    sourcePkm: Pick<PkmBaseDTO, 'boxSlot' | 'canMove' | 'nickname' | 'context'>;
    targetBox?: Pick<BoxDTO, 'name' | 'slotCount'>;
    targetPkm?: Pick<PkmBaseDTO, 'boxSlot' | 'canMove' | 'nickname' | 'context'>;
''',
'''    sourcePkm: Pick<PkmBaseDTO, 'boxSlot' | 'canMove' | 'nickname' | 'context' | 'romHackProfile' | 'romHackSpeciesName'>;
    targetBox?: Pick<BoxDTO, 'name' | 'slotCount'>;
    targetPkm?: Pick<PkmBaseDTO, 'boxSlot' | 'canMove' | 'nickname' | 'context' | 'romHackProfile' | 'romHackSpeciesName'>;
''')

validate_save_to_main_v21 = PKVAULT / "frontend/src/storage/move/validation/rules/validate-save-to-main.ts"
replace_once(validate_save_to_main_v21,
'''  sourceSave: Pick<SaveInfosDTO, 'version' | 'context'>;
''',
'''  sourceSave: Pick<SaveInfosDTO, 'version' | 'context' | 'romHackProfile'>;
''')

validate_main_to_save_v21 = PKVAULT / "frontend/src/storage/move/validation/rules/validate-main-to-save.ts"
replace_once(validate_main_to_save_v21,
'''  sourcePkm: Pick<PkmVariantDTO, 'boxId' | 'canMoveToSave' | 'canMoveAttachedToSave' | 'compatibleWithVersions'>;
''',
'''  sourcePkm: Pick<PkmVariantDTO, 'boxId' | 'canMoveToSave' | 'canMoveAttachedToSave' | 'compatibleWithVersions' | 'romHackProfile'>;
''')
replace_once(validate_main_to_save_v21,
'''  if (slotInfos.targetSave && !slotInfos.sourcePkm.compatibleWithVersions.includes(slotInfos.targetSave.version)) {
    return {
      canDrop: false,
      reason: 'main-to-save-incompatible-version',
      slotInfos,
    };
  }
''',
'''  if (slotInfos.targetSave) {
    const sourceProfile = slotInfos.sourcePkm.romHackProfile;
    const targetProfile = slotInfos.targetSave.romHackProfile;

    if (sourceProfile) {
      if (sourceProfile !== targetProfile) {
        return {
          canDrop: false,
          reason: 'main-to-save-incompatible-version',
          slotInfos,
        };
      }
      // Matching ROM-hack profiles own their local species namespace. Do not
      // feed that local ID into official-game version compatibility.
    } else if (!slotInfos.sourcePkm.compatibleWithVersions.includes(slotInfos.targetSave.version)) {
      return {
        canDrop: false,
        reason: 'main-to-save-incompatible-version',
        slotInfos,
      };
    }
  }
''')

help_text_v21 = PKVAULT / "frontend/src/storage/move/validation/utils/get-help-text.ts"
replace_once(help_text_v21,
'''    const sourcePkm = info?.sourcePkm;
    const targetPkm = info?.targetPkm;

    switch (reason) {
''',
'''    const sourcePkm = info?.sourcePkm;
    const targetPkm = info?.targetPkm;
    const sourceName = sourcePkm?.romHackSpeciesName ?? sourcePkm?.nickname;
    const targetName = targetPkm?.romHackSpeciesName ?? targetPkm?.nickname;

    switch (reason) {
''')
for old,new in [
    ("name: sourcePkm?.nickname,", "name: sourceName,"),
    ("name: targetPkm?.nickname,", "name: targetName,"),
]:
    help_content = help_text_v21.read_text()
    if old not in help_content:
        raise SystemExit(f"missing help-text replacement: {old}")
    help_text_v21.write_text(help_content.replace(old, new))


print("PKVault V8 alpha21 ROM-hack drag validation now uses profile identity instead of aliased official species IDs")



# ---------------------------------------------------------------------------
# V8 alpha22: legality-skip synchronization null guard.
#
# LegalityAnalysisService intentionally returns LegalityAnalysisWrapper(null)
# when SKIP_LEGALITY_CHECKS is enabled. PkmSharePropertiesService then
# unconditionally dereferenced legality.la.Info while synchronizing another
# stored variant after a backward-generation move. Example from the field:
# HeartGold Caterpie PK4 -> Red PK1 conversion succeeds, then synchronization
# of the PK1 back to the existing PK4 variant crashes with NullReferenceException.
#
# Ribbon cleanup requires legality encounter data, so skip only that cleanup
# when there is no analysis. All conversion/property copy work still runs.
# ---------------------------------------------------------------------------
share_props_v22 = PKVAULT / "PKVault.Core/storage/services/PkmConvertService/PkmSharePropertiesService.cs"
replace_once(share_props_v22,
'''        var legality = legalityAnalysisService.GetLegalitySafe(new(targetPkm));
        var args = new RibbonVerifierArguments(
            legality.la.Info.Entity,
            legality.la.EncounterMatch,
            legality.la.Info.EvoChainsAllGens
        );
        RibbonApplicator.FixInvalidRibbons(args);

        targetPkm.Heal();
''',
'''        var legality = legalityAnalysisService.GetLegalitySafe(new(targetPkm));
        if (legality.la is not null)
        {
            var args = new RibbonVerifierArguments(
                legality.la.Info.Entity,
                legality.la.EncounterMatch,
                legality.la.Info.EvoChainsAllGens
            );
            RibbonApplicator.FixInvalidRibbons(args);
        }

        targetPkm.Heal();
''')

# Regression coverage for the exact null-analysis contract used by
# SKIP_LEGALITY_CHECKS. This does not need a special Caterpie fixture: the bug
# was an unconditional dereference after SharePropertiesTo's normal copy path.
share_props_tests_v22 = PKVAULT / "PKVault.Core.Tests/storage/services/PkmConvertService/PkmSharePropertiesServiceTests.cs"
replace_once(share_props_tests_v22,
'''    private PkmSharePropertiesService GetService()
    {
''',
'''    private PkmSharePropertiesService GetService(bool skipLegalityChecks = false)
    {
''')
replace_once(share_props_tests_v22,
'''                LANGUAGE: "fr", HIDE_CHEATS: false, SKIP_LEGALITY_CHECKS: false
''',
'''                LANGUAGE: "fr", HIDE_CHEATS: false, SKIP_LEGALITY_CHECKS: skipLegalityChecks
''')
replace_once(share_props_tests_v22,
'''    [Fact]
    public void SharePropertiesTo_CopiesUnique3Ribbons()
''',
'''    [Fact]
    public void SharePropertiesTo_SkipLegalityChecks_DoesNotDereferenceMissingAnalysis()
    {
        var service = GetService(skipLegalityChecks: true);

        var sourcePkm = new PK3
        {
            Species = 25,
            TID16 = 1234,
        };

        var targetPkm = new PK3 { Species = 25 };

        service.SharePropertiesTo(new(sourcePkm), targetPkm, null);

        Assert.Equal((ushort)25, targetPkm.Species);
        Assert.Equal((ushort)1234, targetPkm.TID16);
    }

    [Fact]
    public void SharePropertiesTo_CopiesUnique3Ribbons()
''')

print("PKVault V8 alpha22 legality-skip synchronization null guard applied")


# ---------------------------------------------------------------------------
# V8 alpha23: preserve original-game provenance in converted save copies.
#
# PKVault represents cross-generation compatibility by keeping the original
# main variant (for example HeartGold PK4) and creating a secondary context
# variant (for example Red PK1). The generated PK1 must identify as a Gen1
# target-game Pokémon at the byte-format level because PK1 cannot encode a
# HeartGold origin game. However PKVault still knows the true provenance from
# the grouped main variant. When viewing an attached converted Pokémon inside a
# save, use that main variant for the Origin panel instead of the lossy target
# format. This preserves HeartGold as the displayed origin without corrupting
# the actual Red-compatible PK1 data.
# ---------------------------------------------------------------------------
details_content_v23 = PKVAULT / "frontend/src/storage/details/details-content.tsx"

replace_once(details_content_v23,
'''import { usePkmIndex } from '../../data/hooks/use-pkm-index';
import { usePkmLegality } from '../../data/hooks/use-pkm-legality';
''',
'''import { usePkmIndex } from '../../data/hooks/use-pkm-index';
import { usePkmLegality } from '../../data/hooks/use-pkm-legality';
import { usePkmVariantIndex } from '../../data/hooks/use-pkm-variant-index';
''')

replace_once(details_content_v23,
'''import { switchUtilRequired } from '../../util/switch-util';
import { useCurrentStorage } from '../panel/storage-panel-context';
''',
'''import { switchUtilRequired } from '../../util/switch-util';
import { useSelectCallback } from '../../util/use-select-callback';
import { useCurrentStorage } from '../panel/storage-panel-context';
''')

replace_once(details_content_v23,
'''    const pkmIndexQuery = usePkmIndex(selectedSaveId, data => data.data.byId[ selectedId ?? '' ]);
    const pkm = pkmIndexQuery.data;

    const getPkmVariantAttach = usePkmVariantAttach();
''',
'''    const pkmIndexQuery = usePkmIndex(selectedSaveId, data => data.data.byId[ selectedId ?? '' ]);
    const pkm = pkmIndexQuery.data;

    // A cross-generation save copy (for example PK4 HeartGold -> PK1 Red)
    // cannot physically retain the newer origin-game field in the older PKM
    // format. If that save copy is attached to a grouped PKVault variant,
    // resolve its original/main variant and use that as provenance in Origin.
    const provenanceVariantQuery = usePkmVariantIndex(
        useSelectCallback(data => {
            if (!selectedSaveId || !pkm?.idBase)
                return undefined;

            const attachedVariant = data.data.byAttachedSave[ selectedSaveId ]?.[ pkm.idBase ];
            if (!attachedVariant)
                return undefined;

            const groupedVariants = data.data.byBox[ attachedVariant.boxId ]?.[ attachedVariant.boxSlot ] ?? [];
            return groupedVariants.find(variant => variant.isMain) ?? attachedVariant;
        }, [ selectedSaveId, pkm?.idBase ])
    );
    const provenancePkm = provenanceVariantQuery.data;

    const getPkmVariantAttach = usePkmVariantAttach();
''')

replace_once(details_content_v23,
'''    const natureObj = pkm.nature === undefined ? undefined : staticData.natures[ pkm.nature ];
''',
'''    const natureObj = pkm.nature === undefined ? undefined : staticData.natures[ pkm.nature ];
    const originPkm = provenancePkm ?? pkm;
''')

replace_once(details_content_v23,
'''                game={<Group>
                    <UIGameImg
                        size='1lh'
                        version={pkm.version}
                        name={staticData.versions[ pkm.version ]?.name}
                    />
                    {staticData.versions[ pkm.version ]?.name}
                </Group>}
                ot={pkm.originTrainerName}
                otGender={pkm.originTrainerGender}
                ht={pkm.handlingTrainerName}
                htGender={pkm.handlingTrainerGender}
                tid={pkm.tid}
                sid={pkm.sid}
                originMetLocation={pkm.originMetLocation}
                originMetLevel={pkm.originMetLevel}
                originMetDate={pkm.originMetDate}
                fatefulEncounter={pkm.fatefulEncounter}
''',
'''                game={<Group>
                    <UIGameImg
                        size='1lh'
                        version={originPkm.version}
                        name={staticData.versions[ originPkm.version ]?.name}
                    />
                    {staticData.versions[ originPkm.version ]?.name}
                </Group>}
                ot={originPkm.originTrainerName}
                otGender={originPkm.originTrainerGender}
                ht={originPkm.handlingTrainerName}
                htGender={originPkm.handlingTrainerGender}
                tid={originPkm.tid}
                sid={originPkm.sid}
                originMetLocation={originPkm.originMetLocation}
                originMetLevel={originPkm.originMetLevel}
                originMetDate={originPkm.originMetDate}
                fatefulEncounter={originPkm.fatefulEncounter}
''')

print("PKVault V8 alpha23 converted save copies now display provenance from the original main variant")


# V8 alpha24 inventory bank
exec((Path(__file__).with_name("patch_pkvault_v8_inventory.py")).read_text(encoding="utf-8"), globals())


# V8 alpha25 storage-style inventory
exec((Path(__file__).with_name("patch_pkvault_v8_inventory_storage.py")).read_text(encoding="utf-8"), globals())


# V8 alpha26 item-storage parity
exec((Path(__file__).with_name("patch_pkvault_v8_inventory_storage_parity.py")).read_text(encoding="utf-8"), globals())


# V8 alpha27 true Storage-clone inventory
exec((Path(__file__).with_name("patch_pkvault_v8_inventory_storage_clone.py")).read_text(encoding="utf-8"), globals())


# V8 alpha28 exact Storage drag controls + Gen1 inventory
exec((Path(__file__).with_name("patch_pkvault_v8_inventory_storage_drag.py")).read_text(encoding="utf-8"), globals())


# V8 alpha29 item provenance + generation-folder persistence
exec((Path(__file__).with_name("patch_pkvault_v8_inventory_provenance.py")).read_text(encoding="utf-8"), globals())

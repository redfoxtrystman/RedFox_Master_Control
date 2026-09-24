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
'''import { useSettingsGet } from '../../data/sdk/settings/settings.gen';
''',
'''import { useSettingsEdit, useSettingsGet } from '../../data/sdk/settings/settings.gen';
''')
replace_once(settings_main_right_v8,
'''    const settingsQuery = useSettingsGet();
    const settings = settingsQuery.data?.data;

    const form = useFormContext<SettingsFormData>();
''',
'''    const settingsQuery = useSettingsGet();
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
'''            onChange={(value) => form.setValue('savE_GLOBS', value, { shouldDirty: true })}
            disabled={!settings?.canUpdateSettings}
''',
'''            onChange={(value) => form.setValue('savE_GLOBS', value, { shouldDirty: true })}
            onAddCommitted={commitAddedSaveLocations}
            disabled={!settings?.canUpdateSettings || settingsMutation.isPending}
''')

globs_list_v8 = PKVAULT / "frontend/src/settings/globs-input/globs-input-list.tsx"
replace_once(globs_list_v8,
'''        onChange: (value: string) => void;
        limit: number;
''',
'''        onChange: (value: string) => void;
        onAddCommitted?: (value: string) => void | Promise<void>;
        limit: number;
''')
replace_once(globs_list_v8,
'''export const GlobsInputList: React.FC<GlobsInputListProps> = ({ name, value, onChange, limit, disabled, extraValue, ...rest }) => {
''',
'''export const GlobsInputList: React.FC<GlobsInputListProps> = ({ name, value, onChange, onAddCommitted, limit, disabled, extraValue, ...rest }) => {
''')
replace_once(globs_list_v8,
'''            const newValues = [ ...splittedValue, ...newValue ];
            onChange(newValues.join('\n'));

            if (!desktopMessage.fileExplore) {
''',
'''            const newValues = [ ...splittedValue, ...newValue ];
            const nextValue = newValues.join('\n');
            onChange(nextValue);
            await onAddCommitted?.(nextValue);

            if (!desktopMessage.fileExplore) {
''')

print("PKVault V8 alpha12 Essentials native location auto-apply applied")

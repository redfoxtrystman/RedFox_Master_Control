# PKVault V8 alpha3 TMT vanilla-isolation + UI/type test
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

dex_dto = PKVAULT / "PKVault.Core/dex/dto/DexItemDTO.cs"
replace_once(dex_dto,
'''    bool IsOwnedShiny,
    EntityContext Context = default,
    byte Generation = default
) : IWithId;
''',
'''    bool IsOwnedShiny,
    EntityContext Context = default,
    byte Generation = default,
    string[]? RomHackTypes = null
) : IWithId;
''')

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
          "abilities": {
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
          "romHackTypes": {
            "type": "array",
            "nullable": true,
            "items": {
              "type": "string"
            }
          },
          "abilities": {
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
            ? pkm.romHackTypes.map(type => <Badge key={type} variant='light' size='sm'>{type}</Badge>)
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
'''import { Grid, Group, Text } from '@mantine/core';
''',
'''import { Badge, Grid, Group, Text } from '@mantine/core';
''')
replace_once(pokedex_details,
'''      types={selectedForm.types.map(type => <TypeItem key={type} type={type} />)}
''',
'''      types={selectedForm.romHackTypes?.length
        ? selectedForm.romHackTypes.map(type => <Badge key={type} variant='light' size='sm'>{type}</Badge>)
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

print("PKVault V8 TMT patch applied")

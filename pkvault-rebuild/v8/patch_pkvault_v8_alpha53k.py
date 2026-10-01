from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def replace_once(rel, old, new, marker):
    path = root / rel
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    if old not in text:
        raise RuntimeError(f"alpha53k anchor missing: {rel}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

# ---------------------------------------------------------------------------
# Save Pokémon references
#
# Historically AttachedSavePkmIdBase stored only IdBase. That is ambiguous when
# two save Pokémon intentionally share the same identity (clones / duplicate
# Gen-II IDs). Keep the DB column for compatibility, but store a full exact
# reference: <IdBase>B<Box>S<Slot>. Legacy IdBase-only records still resolve.
# ---------------------------------------------------------------------------
rel = "PKVault.Core/db/loader/save/SavePkmLoader.cs"
replace_once(
    rel,
    '''    public PkmSaveDTO? GetDto(string boxId, int boxSlot);
    public ImmutableDictionary<string, PkmSaveDTO> GetDtosByIdBase(string idBase);
''',
    '''    public PkmSaveDTO? GetDto(string boxId, int boxSlot);
    public PkmSaveDTO? GetDtoByAttachmentRef(string attachmentRef);
    public ImmutableDictionary<string, PkmSaveDTO> GetDtosByIdBase(string idBase);
''',
    "GetDtoByAttachmentRef(string attachmentRef);",
)

replace_once(
    rel,
    '''    public static string GetPKMId(string idBase, int box, int slot)
    {
        return $"{idBase}B{box}S{slot}"; ;
    }
''',
    '''    public static string GetPKMId(string idBase, int box, int slot)
    {
        return $"{idBase}B{box}S{slot}";
    }

    public static string GetPKMIdBaseFromId(string id)
    {
        if (string.IsNullOrWhiteSpace(id))
            return id;

        var sIndex = id.LastIndexOf('S');
        if (sIndex <= 0 || sIndex >= id.Length - 1
            || !int.TryParse(id[(sIndex + 1)..], out _))
            return id;

        var bIndex = id.LastIndexOf('B', sIndex - 1);
        if (bIndex <= 0 || bIndex >= sIndex - 1
            || !int.TryParse(id[(bIndex + 1)..sIndex], out _))
            return id;

        return id[..bIndex];
    }

    public static string GetAttachmentRef(PkmSaveDTO dto)
        => GetPKMId(dto.IdBase, dto.BoxId, dto.BoxSlot);
''',
    "GetPKMIdBaseFromId(string id)",
)

replace_once(
    rel,
    '''    public ImmutableDictionary<string, PkmSaveDTO> GetDtosByIdBase(string idBase)
''',
    '''    public PkmSaveDTO? GetDtoByAttachmentRef(string attachmentRef)
    {
        if (string.IsNullOrWhiteSpace(attachmentRef))
            return null;

        // During the current session an edited/evolved DTO can still be indexed
        // under its pre-edit full Id; prefer that exact object if present.
        var exact = GetDto(attachmentRef);
        if (exact != null)
            return exact;

        var idBase = GetPKMIdBaseFromId(attachmentRef);

        // New exact refs also carry location. If the save was reloaded, rebuild
        // the DTO Id from its current data and verify the same identity is still
        // in that slot.
        if (!string.Equals(idBase, attachmentRef, StringComparison.Ordinal))
        {
            var sIndex = attachmentRef.LastIndexOf('S');
            var bIndex = attachmentRef.LastIndexOf('B', sIndex - 1);
            if (bIndex > 0
                && int.TryParse(attachmentRef[(bIndex + 1)..sIndex], out var box)
                && int.TryParse(attachmentRef[(sIndex + 1)..], out var slot))
            {
                var byLocation = GetDto(box.ToString(), slot);
                if (byLocation != null
                    && string.Equals(byLocation.IdBase, idBase, StringComparison.Ordinal))
                    return byLocation;
            }
        }

        // Backward compatibility for old IdBase-only attachments. Only resolve
        // automatically when it is unambiguous.
        var matches = GetDtosByIdBase(idBase);
        return matches.Count == 1 ? matches.Values.First() : null;
    }

    public ImmutableDictionary<string, PkmSaveDTO> GetDtosByIdBase(string idBase)
''',
    "// Backward compatibility for old IdBase-only attachments.",
)

# ---------------------------------------------------------------------------
# Variant lookup accepts both exact refs and old IdBase-only refs.
# ---------------------------------------------------------------------------
rel = "PKVault.Core/db/loader/PkmVariantLoader.cs"
replace_once(
    rel,
    '''    public async Task<PkmVariantEntity?> GetEntityBySave(uint saveId, string savePkmIdBase)
    {
        var dbSet = await GetDbSet();

        // using var _ = log.Time($"{typeof(PkmVariantEntity)} - GetEntityBySave");

        return await dbSet.Where(p => p.AttachedSaveId == saveId && p.AttachedSavePkmIdBase == savePkmIdBase)
            .Include(p => p.PkmFile)
            .FirstOrDefaultAsync();
    }
''',
    '''    public async Task<PkmVariantEntity?> GetEntityBySave(uint saveId, string savePkmRef)
    {
        var dbSet = await GetDbSet();

        // Exact reference (new format) or legacy exact IdBase match.
        var exact = await dbSet
            .Where(p => p.AttachedSaveId == saveId && p.AttachedSavePkmIdBase == savePkmRef)
            .Include(p => p.PkmFile)
            .FirstOrDefaultAsync();
        if (exact != null)
            return exact;

        var idBase = SavePkmLoader.GetPKMIdBaseFromId(savePkmRef);

        // Caller supplied a full exact ref but DB still has the old base-only
        // attachment. This upgrades transparently when synchronization runs.
        if (!string.Equals(idBase, savePkmRef, StringComparison.Ordinal))
        {
            return await dbSet
                .Where(p => p.AttachedSaveId == saveId && p.AttachedSavePkmIdBase == idBase)
                .Include(p => p.PkmFile)
                .FirstOrDefaultAsync();
        }

        // Caller supplied only IdBase while DB has new exact refs. Return only
        // when there is a single possible attachment; never pick arbitrarily.
        var prefix = idBase + "B";
        var candidates = await dbSet
            .Where(p => p.AttachedSaveId == saveId
                && p.AttachedSavePkmIdBase != null
                && p.AttachedSavePkmIdBase.StartsWith(prefix))
            .Include(p => p.PkmFile)
            .Take(2)
            .ToListAsync();

        return candidates.Count == 1 ? candidates[0] : null;
    }
''',
    "var idBase = SavePkmLoader.GetPKMIdBaseFromId(savePkmRef);",
)

# ---------------------------------------------------------------------------
# Synchronization resolves exact refs first and self-upgrades legacy attachments.
# If an old base-only attachment is ambiguous, use checksum only when that gives
# exactly one match; otherwise fail safely rather than synchronizing the wrong clone.
# ---------------------------------------------------------------------------
rel = "PKVault.Core/storage/data-action/SynchronizePkmAction.cs"
replace_once(
    rel,
    '''    protected override async Task<DataActionPayload> Execute(SynchronizePkmActionInput input, DataUpdateFlags flags)
''',
    '''    private async Task<PkmSaveDTO> ResolveAttachedSavePkm(
        PkmVariantEntity pkmVariantEntity,
        SaveLoadersRecord saveLoaders,
        string savePkmRef
    )
    {
        var resolved = saveLoaders.Pkms.GetDtoByAttachmentRef(savePkmRef);
        if (resolved != null)
            return resolved;

        var idBase = SavePkmLoader.GetPKMIdBaseFromId(savePkmRef);
        var candidates = saveLoaders.Pkms.GetDtosByIdBase(idBase);

        if (candidates.Count > 1)
        {
            var variantPkm = await pkmVariantLoader.GetPKM(pkmVariantEntity);
            var checksumMatches = candidates.Values
                .Where(dto => dto.DynamicChecksum == variantPkm.DynamicChecksum)
                .ToList();

            if (checksumMatches.Count == 1)
                return checksumMatches[0];
        }

        if (candidates.Count == 0)
            throw new KeyNotFoundException(
                $"Attached save Pokémon not found for pkmVariant.id={pkmVariantEntity.Id} savePkmRef={savePkmRef}"
            );

        throw new InvalidOperationException(
            $"Ambiguous legacy save attachment ({candidates.Count} matches) for pkmVariant.id={pkmVariantEntity.Id} "
            + $"savePkmRef={savePkmRef}. Exact box/slot attachment is required."
        );
    }

    private async Task UpgradeAttachmentRef(PkmVariantEntity pkmVariantEntity, PkmSaveDTO savePkm)
    {
        var exactRef = SavePkmLoader.GetAttachmentRef(savePkm);
        if (string.Equals(pkmVariantEntity.AttachedSavePkmIdBase, exactRef, StringComparison.Ordinal))
            return;

        pkmVariantEntity.AttachedSavePkmIdBase = exactRef;
        await pkmVariantLoader.UpdateEntity(pkmVariantEntity);
    }

    protected override async Task<DataActionPayload> Execute(SynchronizePkmActionInput input, DataUpdateFlags flags)
''',
    "private async Task<PkmSaveDTO> ResolveAttachedSavePkm(",
)

replace_once(
    rel,
    '''                    var savePkms = saveLoader.Pkms.GetDtosByIdBase(pkmVariant.AttachedSavePkmIdBase);
                    if (savePkms.Count != 1)
                        continue;

                    var savePkm = savePkms.Values.First();
''',
    '''                    var savePkm = saveLoader.Pkms.GetDtoByAttachmentRef(pkmVariant.AttachedSavePkmIdBase);
                    if (savePkm == null)
                        continue;

                    await UpgradeAttachmentRef(pkmVariant, savePkm);
''',
    "await UpgradeAttachmentRef(pkmVariant, savePkm);",
)

# Two old hard-fail lookup blocks exist, one in each synchronization direction.
path = root / rel
text = path.read_text(encoding="utf-8")
old = '''            var saveLoaders = savesLoadersService.GetLoadersRequired((uint)pkmVariantEntity.AttachedSaveId!);
            var savePkms = saveLoaders.Pkms.GetDtosByIdBase(savePkmIdBase);
            if (savePkms.Count != 1)
            {
                throw new InvalidOperationException($"Multiple savePkms found ({savePkms.Count}) for pkmVariant.id={pkmVariantId} savePkmIdBase={savePkmIdBase}");
            }

            var savePkm = savePkms.First().Value;
'''
new = '''            var saveLoaders = savesLoadersService.GetLoadersRequired((uint)pkmVariantEntity.AttachedSaveId!);
            var savePkm = await ResolveAttachedSavePkm(pkmVariantEntity, saveLoaders, savePkmIdBase);
            await UpgradeAttachmentRef(pkmVariantEntity, savePkm);
'''
count = text.count(old)
if count != 2:
    raise RuntimeError(f"alpha53k expected 2 synchronize lookup blocks, got {count}")
text = text.replace(old, new)
path.write_text(text, encoding="utf-8")

replace_once(
    rel,
    '''            saveLoaders.Pkms.WriteDto(savePkm);
''',
    '''            saveLoaders.Pkms.WriteDto(savePkm);
            await UpgradeAttachmentRef(pkmVariantEntity, savePkm);
''',
    "saveLoaders.Pkms.WriteDto(savePkm);\n            await UpgradeAttachmentRef",
)

# ---------------------------------------------------------------------------
# Warnings should understand exact refs; an unresolved legacy duplicate remains
# a warning rather than being treated as a valid arbitrary match.
# ---------------------------------------------------------------------------
replace_once(
    "PKVault.Core/warnings/services/WarningsService.cs",
    '''            var savePkms = saveLoader.Pkms.GetDtosByIdBase(attachedPkmVariant.AttachedSavePkmIdBase ?? "");

            if (savePkms.Count == 0)
''',
    '''            var savePkm = saveLoader.Pkms.GetDtoByAttachmentRef(attachedPkmVariant.AttachedSavePkmIdBase ?? "");

            if (savePkm == null)
''',
    "GetDtoByAttachmentRef(attachedPkmVariant.AttachedSavePkmIdBase",
)

# ---------------------------------------------------------------------------
# Exact references make duplicate/cloned save Pokémon safe to attach.
# Keep IsDuplicate for display/diagnostics, but don't prohibit attached moves.
# ---------------------------------------------------------------------------
replace_once(
    "PKVault.Core/storage/dto/PkmSaveDTO.cs",
    '''    public bool CanMoveAttachedToMain => CanMoveToMain && !IsDuplicate;
''',
    '''    public bool CanMoveAttachedToMain => CanMoveToMain;
''',
    "public bool CanMoveAttachedToMain => CanMoveToMain;",
)

rel = "PKVault.Core/storage/data-action/MovePkmAction.cs"
path = root / rel
text = path.read_text(encoding="utf-8")

for block in [
'''        if (input.attached)
        {
            var hasDuplicates = pkmVariants.Any(pkm => saveLoaders.Pkms.GetDtosByIdBase(pkm.Id).Count > 0);
            if (hasDuplicates)
            {
                throw new ArgumentException($"Target save already have a pkm with same ID, move attached cannot be done.");
            }
        }

''',
'''        if (input.attached)
        {
            if (savePkm.IsDuplicate)
            {
                throw new ArgumentException($"Target save already have a pkm with same ID, move attached cannot be done.");
            }
        }

''',
]:
    if block not in text:
        raise RuntimeError("alpha53k MovePkmAction duplicate restriction anchor missing")
    text = text.replace(block, "", 1)

repls = {
    "GetEntityBySave(sourcePkmDto.SaveId, sourcePkmDto.IdBase)":
        "GetEntityBySave(sourcePkmDto.SaveId, SavePkmLoader.GetAttachmentRef(sourcePkmDto))",
    "GetEntityBySave(targetPkmDto.SaveId, targetPkmDto.IdBase)":
        "GetEntityBySave(targetPkmDto.SaveId, SavePkmLoader.GetAttachmentRef(targetPkmDto))",
    "switchAttachedVariant.AttachedSavePkmIdBase = switchedSourcePkmDto.IdBase;":
        "switchAttachedVariant.AttachedSavePkmIdBase = SavePkmLoader.GetAttachmentRef(switchedSourcePkmDto);",
    "sourceAttachedVariant.AttachedSavePkmIdBase = sourcePkmDto.IdBase;":
        "sourceAttachedVariant.AttachedSavePkmIdBase = SavePkmLoader.GetAttachmentRef(sourcePkmDto);",
    "pkmVariant.AttachedSavePkmIdBase = pkmSaveDTO.IdBase;":
        "pkmVariant.AttachedSavePkmIdBase = SavePkmLoader.GetAttachmentRef(pkmSaveDTO);",
    "GetEntityBySave(pkmSaveDTO.SaveId, pkmSaveDTO.IdBase)":
        "GetEntityBySave(pkmSaveDTO.SaveId, SavePkmLoader.GetAttachmentRef(pkmSaveDTO))",
    "GetEntityBySave(savePkm.SaveId, savePkm.IdBase)":
        "GetEntityBySave(savePkm.SaveId, SavePkmLoader.GetAttachmentRef(savePkm))",
    "AttachedSavePkmIdBase: attachToSource ? savePkm.IdBase : null,":
        "AttachedSavePkmIdBase: attachToSource ? SavePkmLoader.GetAttachmentRef(savePkm) : null,",
}
for old, new in repls.items():
    if old not in text:
        raise RuntimeError(f"alpha53k MovePkmAction exact-ref anchor missing: {old}")
    text = text.replace(old, new)
path.write_text(text, encoding="utf-8")

# Bank move variant of save->vault.
rel = "PKVault.Core/storage/data-action/MovePkmBankAction.cs"
path = root / rel
text = path.read_text(encoding="utf-8")
dup = '''        if (input.attached)
        {
            if (savePkm.IsDuplicate)
            {
                throw new ArgumentException($"Target save already have a pkm with same ID, move attached cannot be done.");
            }
        }

'''
if dup not in text:
    raise RuntimeError("alpha53k MovePkmBankAction duplicate restriction anchor missing")
text = text.replace(dup, "", 1)
text = text.replace(
    "GetEntityBySave(savePkm.SaveId, savePkm.IdBase)",
    "GetEntityBySave(savePkm.SaveId, SavePkmLoader.GetAttachmentRef(savePkm))"
)
text = text.replace(
    "AttachedSavePkmIdBase: input.attached ? savePkm.IdBase : null,",
    "AttachedSavePkmIdBase: input.attached ? SavePkmLoader.GetAttachmentRef(savePkm) : null,"
)
path.write_text(text, encoding="utf-8")

# Save-side actions must locate the exact attached clone, not any clone sharing IdBase.
for rel in [
    "PKVault.Core/storage/data-action/SaveDeletePkmAction.cs",
    "PKVault.Core/storage/data-action/TakeHeldItemAction.cs",
    "PKVault.Core/storage/data-action/EditPkmSaveAction.cs",
]:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    if "GetEntityBySave(dto.SaveId, dto.IdBase)" in text:
        text = text.replace(
            "GetEntityBySave(dto.SaveId, dto.IdBase)",
            "GetEntityBySave(dto.SaveId, SavePkmLoader.GetAttachmentRef(dto))"
        )
        text = text.replace(
            "new([(attached.Id, dto.IdBase)])",
            "new([(attached.Id, SavePkmLoader.GetAttachmentRef(dto))])"
        )
    if "GetEntityBySave(pkmSave.SaveId, pkmSave.IdBase)" in text:
        text = text.replace(
            "GetEntityBySave(pkmSave.SaveId, pkmSave.IdBase)",
            "GetEntityBySave(pkmSave.SaveId, SavePkmLoader.GetAttachmentRef(pkmSave))"
        )
        text = text.replace(
            "new([(pkmVariant.Id, pkmSave.IdBase)])",
            "new([(pkmVariant.Id, SavePkmLoader.GetAttachmentRef(pkmSave))])"
        )
    path.write_text(text, encoding="utf-8")

# Evolution can change IdBase. Find the attachment using the pre-evolution exact
# ref; synchronization then upgrades it to the evolved exact ref.
rel = "PKVault.Core/storage/data-action/EvolvePkmAction.cs"
path = root / rel
text = path.read_text(encoding="utf-8")
old = '''        var before = dto;
        var oldName = dto.Nickname;
'''
new = '''        var before = dto;
        var beforeAttachmentRef = SavePkmLoader.GetAttachmentRef(before);
        var oldName = dto.Nickname;
'''
if old not in text:
    raise RuntimeError("alpha53k Evolve before anchor missing")
text = text.replace(old, new, 1)
old = '''        var pkmVariant = await pkmVariantLoader.GetEntityBySave(dto.SaveId, dto.IdBase);
        if (pkmVariant != null)
            await synchronizePkmAction.SynchronizeSaveToPkmVariant(new([(pkmVariant.Id, dto.IdBase)]));
'''
new = '''        var pkmVariant = await pkmVariantLoader.GetEntityBySave(dto.SaveId, beforeAttachmentRef);
        if (pkmVariant != null)
            await synchronizePkmAction.SynchronizeSaveToPkmVariant(new([(pkmVariant.Id, beforeAttachmentRef)]));
'''
if old not in text:
    raise RuntimeError("alpha53k Evolve sync anchor missing")
text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")

print("PASS alpha53k exact save attachment refs + duplicate-safe synchronization")

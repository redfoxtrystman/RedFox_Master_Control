from pathlib import Path
import sys

PKVAULT = Path(sys.argv[1]).resolve()

def replace_once(path: Path, old: str, new: str):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"alpha39 anchor missing in {path}: {old[:180]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

# ---------------------------------------------------------------------------
# V8 alpha39
# - compact Pokédollar bank that cannot be flex-shrunk/clipped after tab changes
# - large inventory-bank pages use the same responsive wrapping as Pokémon boxes
# - Uranium/Insurgence @seen/@owned history projects official species into the
#   normal National Dex even after the Pokémon is no longer in party/storage
# ---------------------------------------------------------------------------

money_panel = PKVAULT / "frontend/src/inventory/money-bank-panel.tsx"
replace_once(
    money_panel,
    """    return <Card withBorder radius='md' p='md'>
        <Stack gap='md'>
            <Group justify='space-between' align='flex-start'>
                <Group gap='sm'>
                    <PiggyBankIcon size={30} />
                    <div>
                        <Text fw={700} size='lg'>PKVault Pokédollar Bank</Text>
                        <Text size='sm' c='dimmed'>
                            Shared money storage across loaded saves. Transfers automatically respect each game's money cap.
                        </Text>
                    </div>
                </Group>
                <Badge size='lg' variant='light'>{formatMoney(state.moneyBank)}</Badge>
            </Group>

            <SimpleGrid cols={{ base: 1, md: 3 }} spacing='sm'>
                <Select
                    label='From'
                    data={options}
                    value={sourceValue}
                    onChange={value => value && setSourceValue(value)}
                    leftSection={<WalletCardsIcon size={16} />}
                />
                <Group align='flex-end' wrap='nowrap'>
                    <NumberInput
                        label='Amount'
                        min={1}
                        max={Math.max(1, maxTransfer)}
                        value={amount}
                        onChange={setAmount}
                        allowDecimal={false}
                        thousandSeparator=','
                        flex={1}
                    />
                    <Tooltip label='Use the largest amount that fits the target'>
                        <ActionIcon
                            variant='light'
                            size='lg'
                            disabled={maxTransfer <= 0}
                            onClick={() => setAmount(maxTransfer)}
                        >
                            MAX
                        </ActionIcon>
                    </Tooltip>
                </Group>
                <Select
                    label='To'
                    data={options}
                    value={targetValue}
                    onChange={value => value && setTargetValue(value)}
                    leftSection={<LandmarkIcon size={16} />}
                />
            </SimpleGrid>

            <Stack gap='xs'>
                <Text size='sm' fw={600}>
                    {sourceLabel} → {targetLabel}
                </Text>
                <Text size='xs' c='dimmed'>
                    Transfer room: {formatMoney(maxTransfer)} · Bank exact-storage ceiling: {formatMoney(state.moneyBankMax)}
                </Text>

                <Button
                    color='red'
                    variant='filled'
                    size='md'
                    fullWidth
                    rightSection={<ArrowRightIcon size={18} />}
                    loading={busy}
                    disabled={sourceValue === targetValue || transferAmount <= 0}
                    onClick={() => void transfer(transferAmount)}
                >
                    Transfer {formatMoney(transferAmount)}
                </Button>

                <Group justify='space-between' align='center'>
                    <Text size='xs' c='dimmed'>
                        The red button above is the normal transfer action. Nothing moves until you press it.
                    </Text>
                    <Button
                        size='xs'
                        variant={confirmSweep ? 'filled' : 'subtle'}
                        color={confirmSweep ? 'orange' : 'gray'}
                        disabled={busy || moneySaves.every(save => save.money <= 0)}
                        onClick={() => {
                            if (!confirmSweep) {
                                setConfirmSweep(true);
                                return;
                            }
                            void sweepAll();
                        }}
                    >
                        {confirmSweep ? 'Confirm: deposit ALL loaded saves' : 'Quick action: deposit all loaded saves'}
                    </Button>
                </Group>
            </Stack>

            {moneySaves.length === 0 && <Alert color='yellow'>
                None of the currently loaded saves expose writable Pokédollars.
            </Alert>}
        </Stack>
    </Card>;
""",
    """    return <Card
        withBorder
        radius='md'
        p='xs'
        style={{ flexShrink: 0, overflow: 'visible' }}
    >
        <Stack gap={6}>
            <Group justify='space-between' align='center' wrap='nowrap'>
                <Group gap='xs' wrap='nowrap'>
                    <PiggyBankIcon size={18} />
                    <Text fw={700} size='sm'>PKVault Pokédollar Bank</Text>
                </Group>
                <Badge size='md' variant='light'>{formatMoney(state.moneyBank)}</Badge>
            </Group>

            <SimpleGrid cols={{ base: 1, sm: 2, lg: 4 }} spacing='xs' verticalSpacing='xs'>
                <Select
                    size='xs'
                    label='From'
                    data={options}
                    value={sourceValue}
                    onChange={value => value && setSourceValue(value)}
                    leftSection={<WalletCardsIcon size={14} />}
                />
                <Group align='flex-end' wrap='nowrap' gap={4}>
                    <NumberInput
                        size='xs'
                        label='Amount'
                        min={1}
                        max={Math.max(1, maxTransfer)}
                        value={amount}
                        onChange={setAmount}
                        allowDecimal={false}
                        thousandSeparator=','
                        flex={1}
                    />
                    <Tooltip label='Use the largest amount that fits the target'>
                        <ActionIcon
                            variant='light'
                            size='md'
                            disabled={maxTransfer <= 0}
                            onClick={() => setAmount(maxTransfer)}
                        >
                            MAX
                        </ActionIcon>
                    </Tooltip>
                </Group>
                <Select
                    size='xs'
                    label='To'
                    data={options}
                    value={targetValue}
                    onChange={value => value && setTargetValue(value)}
                    leftSection={<LandmarkIcon size={14} />}
                />
                <Button
                    color='red'
                    variant='filled'
                    size='xs'
                    mt={22}
                    rightSection={<ArrowRightIcon size={15} />}
                    loading={busy}
                    disabled={sourceValue === targetValue || transferAmount <= 0}
                    onClick={() => void transfer(transferAmount)}
                >
                    Transfer {formatMoney(transferAmount)}
                </Button>
            </SimpleGrid>

            <Group justify='space-between' align='center' gap='xs' wrap='wrap'>
                <Text size='xs' c='dimmed'>
                    {sourceLabel} → {targetLabel} · room {formatMoney(maxTransfer)}
                </Text>
                <Button
                    size='xs'
                    variant={confirmSweep ? 'filled' : 'subtle'}
                    color={confirmSweep ? 'orange' : 'gray'}
                    disabled={busy || moneySaves.every(save => save.money <= 0)}
                    onClick={() => {
                        if (!confirmSweep) {
                            setConfirmSweep(true);
                            return;
                        }
                        void sweepAll();
                    }}
                >
                    {confirmSweep ? 'Confirm: deposit ALL loaded saves' : 'Quick: deposit all loaded saves'}
                </Button>
            </Group>

            {moneySaves.length === 0 && <Alert color='yellow' py={4}>
                None of the currently loaded saves expose writable Pokédollars.
            </Alert>}
        </Stack>
    </Card>;
"""
)

inventory_page = PKVAULT / "frontend/src/inventory/inventory-page.tsx"
replace_once(
    inventory_page,
    """        <Stack h='100%' gap='sm'>
""",
    """        <Stack h='100%' gap='xs' style={{ minHeight: 0 }}>
"""
)

inventory_panel = PKVAULT / "frontend/src/inventory/inventory-panel.tsx"
replace_once(
    inventory_panel,
    """    const cols = getBoxColumns(slots.length) ?? 6;
""",
    """    const cols = getBoxColumns(slots.length);
"""
)
replace_once(
    inventory_panel,
    """            style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(' + cols + ', 1fr)',
            }}
""",
    """            style={cols
                ? {
                    display: 'grid',
                    gridTemplateColumns: 'repeat(' + cols + ', 1fr)',
                }
                : undefined}
"""
)

dex_service = PKVAULT / "PKVault.Core/romhacks/essentials/DexEssentialsService.cs"
dex_service.write_text("""using PKHeX.Core;

namespace PKVault.Core;

/// <summary>
/// Projects official Pokémon from Essentials fan-game saves into PKVault's
/// ordinary National Dex. The fan-game @seen/@owned arrays are authoritative
/// history, so an official Pokémon remains Seen/Caught even after it leaves the
/// party/PC. Profile-local Uranium/Insurgence species stay in their own dex UI.
/// </summary>
public sealed class DexEssentialsService(EssentialsLegacySaveFile save) : DexGenService(save)
{
    public override async Task<bool> UpdateDexWithSave(
        Dictionary<ushort, Dictionary<uint, DexItemDTO>> dex,
        StaticSpeciesData staticSpecies,
        HashSet<ushort>? speciesSet)
    {
        var currentPkms = save.GetAllPKM()
            .OfType<PKEssentials>()
            .Where(p => p.OfficialNationalDexId > 0)
            .GroupBy(p => checked((ushort)p.OfficialNationalDexId))
            .ToDictionary(group => group.Key, group => group.ToArray());

        HashSet<ushort> MapHistory(IEnumerable<int> localSpeciesIds)
            => [.. localSpeciesIds
                .Select(localId => EssentialsProfileFallback.GetOfficialNationalDexId(save.Game, localId, 0))
                .Where(nationalId => nationalId > 0 && nationalId <= ushort.MaxValue)
                .Select(nationalId => checked((ushort)nationalId))];

        var seenNational = MapHistory(save.SeenSpecies);
        var caughtNational = MapHistory(save.OwnedSpecies);
        seenNational.UnionWith(caughtNational);

        var officialSpecies = currentPkms.Keys
            .Concat(seenNational)
            .Concat(caughtNational)
            .Distinct()
            .Order();

        foreach (var species in officialSpecies)
        {
            if (speciesSet != null && !speciesSet.Contains(species))
                continue;
            if (!staticSpecies.TryGetValue(species, out var speciesData) || speciesData.Forms.Count == 0)
                continue;

            currentPkms.TryGetValue(species, out var current);
            current ??= [];

            var historySeen = seenNational.Contains(species);
            var historyCaught = caughtNational.Contains(species);
            var contextKey = speciesData.Forms.Keys.Max();
            var context = (EntityContext)contextKey;
            var presentationSave = BlankSaveFile.Get(context);
            var helper = new Dex123Service(presentationSave);
            var staticForms = speciesData.Forms[contextKey];

            var forms = new List<DexItemForm>();
            for (byte form = 0; form < staticForms.Length; form++)
            {
                foreach (var gender in speciesData.Genders)
                {
                    var owned = current.Where(p => p.Form == form && (Gender)p.Gender == gender).ToArray();
                    var isOwned = owned.Length > 0;
                    var isOwnedShiny = owned.Any(p => p.IsShiny);

                    var item = helper.GetDexItemFormComplete(
                        species,
                        isOwned,
                        isOwnedShiny,
                        false,
                        form,
                        gender,
                        staticSpecies
                    );

                    // Essentials stores historical Seen/Owned at species level,
                    // not per form. Apply history to the base form only so the
                    // National Dex species is marked without claiming that every
                    // alternate form was encountered.
                    if (form == 0)
                    {
                        item = item with
                        {
                            IsSeen = item.IsSeen || historySeen || historyCaught,
                            IsCaught = item.IsCaught || historyCaught,
                        };
                    }

                    forms.Add(item);
                }
            }

            if (!dex.TryGetValue(species, out var bySave))
            {
                bySave = [];
                dex.Add(species, bySave);
            }

            var saveId = new SaveWrapper(save).Id;
            bySave[saveId] = new DexItemDTO(
                Id: $"{species}_{saveId}",
                Species: species,
                SaveId: saveId,
                Forms: forms,
                Languages: [LanguageID.English]
            );
        }

        await Task.CompletedTask;
        return true;
    }

    protected override DexItemForm GetDexItemForm(ushort species, bool isOwned, bool isOwnedShiny, byte form, Gender gender)
        => throw new NotSupportedException();

    protected override IEnumerable<LanguageID> GetDexLanguages(ushort species) => [];

    public override Task EnableSpeciesForm(EnableSpeciesFormPayload payload)
        => Task.CompletedTask;
}
""", encoding="utf-8")

print("PKVault V8 alpha39 compact bank + responsive item boxes + fan-game National Dex history applied")

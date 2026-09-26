from pathlib import Path
import sys

PKVAULT = Path(sys.argv[1]).resolve()

def replace_once(path: Path, old: str, new: str):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"alpha38 anchor missing in {path}: {old[:180]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

# ---------------------------------------------------------------------------
# V8 alpha38
# - Insurgence MISSINGNO #722 reuses PKVault's existing Gen-1 MISSINGNO sprite
#   exactly; never render the generated square/glitch placeholder.
# - Pokédollar transfer is the visually dominant action: large red button with
#   amount in the label.
# - "Deposit all loaded saves" is demoted to a secondary quick action and
#   requires a confirmation click to reduce accidental sweeps.
# ---------------------------------------------------------------------------

species_img = PKVAULT / "frontend/src/img/species-img.tsx"

replace_once(
    species_img,
    """    if (species === 0 && context === EntityContext.Gen1) {
""",
    """    const localSpeciesId = romHackLocalSpeciesId ?? species;
    const isInsurgenceMissingNo = profileLocalSpecies
        && romHackProfile === INSURGENCE_PROFILE_ID
        && localSpeciesId === 722;

    if ((species === 0 && context === EntityContext.Gen1) || isInsurgenceMissingNo) {
""",
)

replace_once(
    species_img,
    """            data-species-id={0}
            data-glitch-species="gen1"
""",
    """            data-species-id={isInsurgenceMissingNo ? localSpeciesId : 0}
            data-glitch-species={isInsurgenceMissingNo ? 'insurgence' : 'gen1'}
            data-rom-hack-profile={isInsurgenceMissingNo ? INSURGENCE_PROFILE_ID : undefined}
            data-local-species-id={isInsurgenceMissingNo ? localSpeciesId : undefined}
""",
)

replace_once(
    species_img,
    """            species={1}
            isShadow={false}
            title="MissingNo / 'M Gen 1 glitch Pokemon"
""",
    """            species={isInsurgenceMissingNo ? localSpeciesId : 1}
            isShadow={false}
            title={isInsurgenceMissingNo ? 'Pokémon Insurgence MISSINGNO #722' : "MissingNo / 'M Gen 1 glitch Pokemon"}
""",
)

replace_once(
    species_img,
    """    if (profileLocalSpecies) {
        const localSpeciesId = romHackLocalSpeciesId ?? species;
""",
    """    if (profileLocalSpecies) {
""",
)

money_panel = PKVAULT / "frontend/src/inventory/money-bank-panel.tsx"

replace_once(
    money_panel,
    """    const [ amount, setAmount ] = React.useState<number | string>(1);
    const [ busy, setBusy ] = React.useState(false);
""",
    """    const [ amount, setAmount ] = React.useState<number | string>(1);
    const [ busy, setBusy ] = React.useState(false);
    const [ confirmSweep, setConfirmSweep ] = React.useState(false);
""",
)

replace_once(
    money_panel,
    """        } finally {
            setBusy(false);
        }
    };

    return <Card withBorder radius='md' p='md'>
""",
    """        } finally {
            setBusy(false);
            setConfirmSweep(false);
        }
    };

    const requestedAmount = Math.trunc(Number(amount) || 0);
    const transferAmount = Math.max(0, Math.min(requestedAmount, maxTransfer));
    const sourceLabel = options.find(option => option.value === sourceValue)?.label ?? 'source';
    const targetLabel = options.find(option => option.value === targetValue)?.label ?? 'target';

    return <Card withBorder radius='md' p='md'>
""",
)

replace_once(
    money_panel,
    """            <Group justify='space-between'>
                <Text size='xs' c='dimmed'>
                    Transfer room: {formatMoney(maxTransfer)} · Bank exact-storage ceiling: {formatMoney(state.moneyBankMax)}
                </Text>
                <Group gap='xs'>
                    <Button
                        variant='light'
                        disabled={busy || moneySaves.every(save => save.money <= 0)}
                        onClick={() => void sweepAll()}
                    >
                        Deposit all loaded saves
                    </Button>
                    <Button
                        rightSection={<ArrowRightIcon size={16} />}
                        loading={busy}
                        disabled={sourceValue === targetValue || maxTransfer <= 0}
                        onClick={() => void transfer(Number(amount) || 0)}
                    >
                        Transfer
                    </Button>
                </Group>
            </Group>
""",
    """            <Stack gap='xs'>
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
""",
)

print("PKVault V8 alpha38 MISSINGNO sprite + Pokédollar UI clarity fixes applied")

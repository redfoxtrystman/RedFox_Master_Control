import { Card, Select, SimpleGrid } from '@mantine/core';
import { BoxesIcon, UserRoundIcon } from 'lucide-react';
import type React from 'react';
import { useFormContext, useWatch } from 'react-hook-form';
import { BoxType } from '../../data/sdk/model';
import { useSettingsGet } from '../../data/sdk/settings/settings.gen';
import { useStorageGetBoxes } from '../../data/sdk/storage/storage.gen';
import type { SettingsFormData } from '../../pages/settings';
import { UITextInput } from '../../ui/form/text-input/ui-text-input';
import { UIInputLabel } from '../../ui/form/ui-input-label';

export const SettingsTradingLeft: React.FC = () => {
    const settingsQuery = useSettingsGet();
    const boxesQuery = useStorageGetBoxes({ saveId: undefined });
    const settings = settingsQuery.data?.data;
    const form = useFormContext<SettingsFormData>();

    const [ playerName, tradeBoxId ] = useWatch({
        control: form.control,
        name: [ 'tradeR_NAME', 'tradE_BOX_ID' ],
    });

    const tradeBoxes = [ ...boxesQuery.data?.data ?? [] ]
        .filter(box => box.type === BoxType.Box)
        .sort((a, b) => a.order - b.order || a.name.localeCompare(b.name))
        .map(box => ({
            value: box.id,
            label: box.name,
        }));

    return <Card>
        <SimpleGrid cols={2}>
            <UIInputLabel
                leftSection={<UserRoundIcon />}
                forInput='tradeR_NAME'
                label='Player name'
                description='Shown to other PKVault players while trading.'
            />
            <UITextInput
                name='tradeR_NAME'
                value={playerName ?? ''}
                placeholder='PKVault Player'
                maxLength={32}
                disabled={!settings?.canUpdateSettings}
                onChange={event => form.setValue(
                    'tradeR_NAME',
                    event.currentTarget.value,
                    { shouldDirty: true }
                )}
            />

            <UIInputLabel
                leftSection={<BoxesIcon />}
                forInput='tradE_BOX_ID'
                label='Trade Box'
                description='Optional dedicated destination for every Pokemon received in a trade.'
            />
            <Select
                id='tradE_BOX_ID'
                value={tradeBoxId ?? null}
                data={tradeBoxes}
                placeholder='Automatic / no dedicated Trade Box'
                clearable
                searchable
                disabled={!settings?.canUpdateSettings || boxesQuery.isPending}
                onChange={value => form.setValue(
                    'tradE_BOX_ID',
                    value ?? null,
                    { shouldDirty: true }
                )}
            />
        </SimpleGrid>
    </Card>;
};

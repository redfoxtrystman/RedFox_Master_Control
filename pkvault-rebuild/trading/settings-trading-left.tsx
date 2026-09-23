import { Card, SimpleGrid } from '@mantine/core';
import { UserRoundIcon } from 'lucide-react';
import type React from 'react';
import { useFormContext, useWatch } from 'react-hook-form';
import { useSettingsGet } from '../../data/sdk/settings/settings.gen';
import type { SettingsFormData } from '../../pages/settings';
import { UITextInput } from '../../ui/form/text-input/ui-text-input';
import { UIInputLabel } from '../../ui/form/ui-input-label';

export const SettingsTradingLeft: React.FC = () => {
    const settingsQuery = useSettingsGet();
    const settings = settingsQuery.data?.data;
    const form = useFormContext<SettingsFormData>();

    const [ playerName ] = useWatch({
        control: form.control,
        name: [ 'tradeR_NAME' ],
    });

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
        </SimpleGrid>
    </Card>;
};

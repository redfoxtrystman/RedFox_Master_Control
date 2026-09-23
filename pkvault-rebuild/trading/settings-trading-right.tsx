import { Card, Stack, Text } from '@mantine/core';
import { ArrowLeftRightIcon } from 'lucide-react';
import type React from 'react';

export const SettingsTradingRight: React.FC = () => <Card>
    <Stack gap='xs'>
        <Text fw={700}><ArrowLeftRightIcon size={16} style={{ verticalAlign: 'middle' }} /> Trading identity</Text>
        <Text size='sm'>
            Your Player name is sent to the connected PKVault peer and shown in the Trading storage pane.
        </Text>
        <Text size='sm' c='dimmed'>
            It is independent of the executable name, folder name, save trainer name, and local Windows account.
            Leaving it blank uses “PKVault Player”.
        </Text>
    </Stack>
</Card>;

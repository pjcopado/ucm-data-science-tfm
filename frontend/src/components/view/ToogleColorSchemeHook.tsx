'use client';

import { useMantineColorScheme, useComputedColorScheme, Button } from '@mantine/core';
import { FaMoon, FaSun } from 'react-icons/fa';

export default function ColorSchemeToggle() {
  const { setColorScheme } = useMantineColorScheme();
    const computedColorScheme = useComputedColorScheme('light');
    const toogleColorScheme = () => {
      setColorScheme(computedColorScheme === 'dark' ? 'light' : 'dark');
    }  
  return (
    <Button  mr='xs' size='sm' style={{"marginTop":"0.5rem"}} variant='link' onClick={toogleColorScheme}>
        {computedColorScheme === 'dark' ? <FaSun /> : <FaMoon />}
    </Button>
  );
}

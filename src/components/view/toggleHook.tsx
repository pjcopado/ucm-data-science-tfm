import React, { useState } from 'react';
import { LuPanelLeft } from "react-icons/lu";
import { AppShell } from '@mantine/core';

const ToggleComponent = () => {
    const [isOpen, setIsOpen] = useState(false);
    const toggle = () => {
        setIsOpen(!isOpen);
    };
    return (
        <div style={{'marginTop':'10px'}}>
            <LuPanelLeft size='35' onClick={toggle} />
            {isOpen ?<AppShell.Navbar p="xs"></AppShell.Navbar> : null}            
        </div>
    );
};

export default ToggleComponent;

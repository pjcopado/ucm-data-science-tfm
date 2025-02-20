import { useState } from 'react';

const UseToggleComponent = () => {
    const [isOpen, setIsOpen] = useState(true);

    const toggle = () => {
        setIsOpen(!isOpen);
    };
    return {isOpen, toggle}
};

export default UseToggleComponent;

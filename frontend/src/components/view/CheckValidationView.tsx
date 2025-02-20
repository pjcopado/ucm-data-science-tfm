import { patchValidation } from '@/api/main';
import { useState } from 'react';
import { FaCheck, FaTimes } from 'react-icons/fa';  

const ValidationButtons = ({idChat, idMessage}:{idChat:string, idMessage:string}) => {
    const [isDisable, setDisable ] = useState<boolean>(false)

    const handleValidation = async(isValid:boolean) => {
        setDisable(true)
        await patchValidation(idChat, idMessage,isValid)
    };



    return (
        <div style={{ display: 'flex', gap: '10px', marginTop: '1rem' }}>
            <button 
                onClick={() => handleValidation(true)} 
                disabled={isDisable}
                style={{
                    backgroundColor: 'green',
                    color: 'white',
                    border: 'none',
                    padding: '10px',
                    borderRadius: '5px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}
            >
                <FaCheck /> Sí
            </button>
            <button 
                onClick={() => handleValidation(false)} 
                disabled={isDisable}
                style={{
                    backgroundColor: 'red',
                    color: 'white',
                    border: 'none',
                    padding: '10px',
                    borderRadius: '5px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}
            >
                <FaTimes /> No
            </button>
        </div>
    );
};


export default ValidationButtons;

import React from 'react';
import { Card, Box, Flex, Text } from '@mantine/core';
import { FirstDataResponse } from "../../interface/query";
import {  useAppDispatch } from '@/hooks/reduxHooks';
import { setActiveMessage } from '@/features';

const NavbarAsideView = ({ data, openNewChat }: { data: FirstDataResponse[], openNewChat: (id: string) => Promise<void> }) => {
     
    const dispatch = useAppDispatch()

    interface HandleClickEvent extends React.MouseEvent<HTMLDivElement> {
        preventDefault: () => void;
    }

    const handleClick = (e: HandleClickEvent, id: string) => {
        dispatch(setActiveMessage('message1'));
        openNewChat(id);
        e.preventDefault();
    };
    return (
        <Box style={{ "width": "20rem" }} className="chat">
            {data.map((item) => {
                return (
                
                <div key={item.id} className="space-y-2">
                    <Flex align="center" justify="flex-start" style={{ "marginBottom": "0.2rem" }}>
                        <Card
                            shadow="sm"
                            padding="xs"
                            radius="md"
                            style={{ "backgroundColor": "rgba(50, 50, 50, 0.85", "maxWidth": '100%' }}                        >
                            <Text onClick={(e) => handleClick(e, item.id)} truncate="end" style={{cursor:"pointer", listStyleType:"none", "overflowWrap": "break-word", "fontFamily": "sans-serif" }} size="md" c="#ececec">{item.first_message.question}</Text>
                        </Card>
                    </Flex>
                </div>
                )})}

        
        </Box>
    );
};

export default NavbarAsideView;
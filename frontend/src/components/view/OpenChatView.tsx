import '../../app/globals.css'; 
import React from 'react';
import { Card, Avatar,  Box,  Flex, Text } from '@mantine/core';
import { IconUser } from '@tabler/icons-react';
import {  Query } from "../../interface/query";
import ResponseQuery from './ResponseQuery';
import EllipsisLoader from '@/hooks/usePoint';

const OpenChatView = ({ data, newQuery, question, setQuestion, idChat }:{ data: Query[],newQuery:(e: React.FormEvent<HTMLInputElement>) => void, question: string, setQuestion: React.Dispatch<React.SetStateAction<string>>, idChat:string}) => {
    const formatDate = (timestamp: string | number | Date) => {
        const date = new Date(timestamp);
        return date.toLocaleString();
    };

   
    return (
        <div style={{ position: 'relative', height: '100vh' }}>        
            <div style={{ "marginTop": "2rem", "marginLeft": "5rem", "width": "70rem", overflowY: 'auto','height': 'calc(100vh - 70px)', 'paddingBottom': '10rem'}} className="no-scrollbar">                
                {data.map((item) => (     
                    <div key={item.created_at} className="space-y-2">
                        <Flex align="center" justify="flex-end" gap="md" style={{ "margin": "3rem" }}>
                            <Avatar color="blue" radius="xl">
                                <IconUser size={20} />
                            </Avatar>
                            <Card
                                shadow="sm"
                                padding="md"
                                radius="md"
                                withBorder
                                style={{ "backgroundColor": "rgba(50, 50, 50, 0.85", "maxWidth": '50%' }}
                            >
                                <Text style={{ "overflowWrap": "break-word", "fontFamily": "sans-serif" }} size="lg" c="#ececec">{item.question}</Text>
                                <Text size="md" c="rgba(176, 176, 176, 1)" ta="right" mt="xs">
                                    {formatDate(item.created_at)}
                                </Text>
                            </Card>
                        </Flex>
                        {item.status === 'pending' ? <EllipsisLoader/> : <ResponseQuery created_at={item.created_at} status={item.status} response={item.response} query_explanation={item.query_explanation} idChat={idChat} idMessage={item.id}/>}
                    </div>
                ))}
            </div>
            <Box>
                <input onKeyDown={e => {if (e.key === 'Enter') newQuery(e)}} value={question} onChange={(e) => setQuestion(e.target.value)} className='inputfixed' type="text" placeholder="Preguntame algo nuevo en este chat..."></input>
            </Box>

            
        </div>

    );
};

export default OpenChatView;
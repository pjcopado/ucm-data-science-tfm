'use client'
import React from 'react';
import { Card, Avatar, Flex, Text } from '@mantine/core';
import { IconDeviceLaptop } from '@tabler/icons-react';
import ValidationButtons from './CheckValidationView';


const ResponseQuery = ({ created_at, status, response, query_explanation, idChat, idMessage }: { created_at: string, status: string, response: string, query_explanation: string, idChat: string, idMessage: string }) => {
    const formatDate = (timestamp: string | number | Date) => {
        const date = new Date(timestamp);
        return date.toLocaleString();
    };
    let responseMessage
    switch (status) {
        case 'error':
            responseMessage = 'Unknown error. We are resolving the error. Please refresh the website, if the error persists try again later';
            break;
        case 'query_invalid':
            responseMessage = 'The text is irrelevant to generate a response. Please verify your question';
            break;
        case 'query_failed':
            responseMessage = 'An error occurred while trying to make your request. Please try again later - Model Error';
            break;
        case 'query_execution_failed':
            responseMessage = 'Our software crashed while executing your question. Please try again later';
            break;
        case 'insight_failed':
            responseMessage = 'An error occurred while attempting to generate the response. Disparity error between query and response';
            break;
        default:
            responseMessage = response;
            break;
    }

    return (
        <Flex align="center" direction="column" justify='start'>
            <Flex>
                <Avatar style={{ "marginLeft": "5rem" }} color="green" radius="xl">
                    <IconDeviceLaptop size={20} />
                </Avatar>
                <Card
                    shadow="sm"
                    padding="md"
                    radius="md"
                    withBorder
                    style={{ "backgroundColor": "rgba(50, 50, 50, 0.85)", "maxWidth": '80%', "marginLeft": "0.2rem" }}
                >
                    <Text style={{ "overflowWrap": "break-word", "fontFamily": "sans-serif" }} size="lg" c="#ececec">{responseMessage !== '' ? responseMessage : response}</Text>
                    <Text size="md" c="rgba(176, 176, 176, 1)" ta="left" mt="xs">
                        {formatDate(created_at)}
                    </Text>
                </Card>
            </Flex>
            <Flex direction='row'>
                <Card
                    shadow="sm"
                    padding="lg"
                    radius="md"
                    withBorder
                    style={{ backgroundColor: "rgba(50, 50, 50, 0.85)", maxWidth: '80%', margin: '1rem' }}
                >
                    <Text style={{ overflowWrap: "break-word", fontFamily: "sans-serif" }} size="lg" c="#ececec">
                        {query_explanation}
                    </Text>
                    <ValidationButtons idChat={idChat} idMessage={idMessage} />
                </Card>
            </Flex>
        </Flex>

    )

};

export default ResponseQuery
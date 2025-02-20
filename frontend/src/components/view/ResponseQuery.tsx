'use client'
import React from 'react';
import '@mantine/charts/styles.css';
import { DonutChart } from '@mantine/charts'
import { Card, Avatar, Flex, Text } from '@mantine/core';
import { IconDeviceLaptop } from '@tabler/icons-react';
import ValidationButtons from './CheckValidationView';


const ResponseQuery = ({ created_at, status, response, query_explanation, idChat, idMessage, confidence_score }: { created_at: string, status: string, response: string, query_explanation: string, idChat: string, idMessage: string, confidence_score: number }) => {
    const formatDate = (timestamp: string | number | Date) => {
        const date = new Date(timestamp);
        return date.toLocaleString();
    };
    let responseMessage
    let correctResponse
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
            correctResponse = response;
            break;
    }

    return (
        <Flex align="center" direction="column" justify='stretch' style={{ "width": "70%" }}>
            <Flex align="center">
                <Flex align="center">
                    <Avatar style={{ "marginLeft": "5rem", 'marginRight': '10px' }} color="green" radius="xl">
                        <IconDeviceLaptop size={20} />
                    </Avatar>
                    <Card
                        shadow="sm"
                        padding="md"
                        radius="md"
                        withBorder
                        style={{ "backgroundColor": "rgba(50, 50, 50, 0.85)", "maxWidth": '80%', "marginLeft": "0.2rem" }}
                    >
                        <Text style={{ "overflowWrap": "break-word", "fontFamily": "sans-serif" }} size="lg" c="#ececec">{correctResponse !== '' ? correctResponse : responseMessage}</Text>
                        <Text size="md" c="rgba(176, 176, 176, 1)" ta="left" mt="xs">
                            {formatDate(created_at)}
                        </Text>
                    </Card>
                </Flex>
                <div style={{"marginLeft":"5px"}}>
                    <DonutChart  size={100}
                        data={[
                            { name: 'scorage', value: ((confidence_score * 100)), color: 'blue' },
                            { name: 'Other', value: (100 - (confidence_score * 100)), color: 'gray.6' },
                        ]}
                        chartLabel={confidence_score}
                    />
                </div>

            </Flex> 
            {correctResponse !== '' ? <Flex direction='row'>
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
            </Flex> : null}
        </Flex>

    )

};

export default ResponseQuery
import React from 'react';
import { Box, Flex, Button, Input } from '@mantine/core';
import useChatHook from "../../hooks/useChatHook";
import { Typewriter, Cursor } from "react-simple-typewriter"


const NewMessageView = () => {
    const { query, refreshQuery, openChatQuery } = useChatHook()
    return (
        <Flex direction='column' align='center' justify='center'>
        <Box mt="20vh">
          <span style={{ color: "white", fontWeight: 'bold', fontSize: '4vh' }}>¿What is your <span>
            <Typewriter
              words={['Query?', 'Doubt?', 'Question?']}
              loop={0}
              typeSpeed={120}
              deleteSpeed={80}
            /></span></span>
          <span style={{ color: 'white', fontWeight: 'bold', fontSize: '4vh' }}>
            <Cursor cursorStyle='|'/>
          </span></Box>
        <Flex direction='column' align='center' justify='center'>
          <Input style={{ width: "250%" }} size="xl" type="text" value={query} onChange={refreshQuery} />
          <Box mt='xl'>
            <Button onClick={openChatQuery} size="xl">Send</Button>
          </Box>
        </Flex>
      </Flex>    
      );
};

export default NewMessageView;
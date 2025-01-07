import { Box, Text, Flex, Space, Button, Input } from "@mantine/core"
import useInputHook from "@/hooks/useInputHook";
import { Typewriter, Cursor } from "react-simple-typewriter"

const Home = () => {

  const { query, refreshQuery, sendQuery } = useInputHook()

  return (
    <Flex direction='column' align='center' justify='center'>
          <Box mt="20vh">   
          <span style={{color:"white", fontWeight:'bold', fontSize:'4vh'}}>¿Cual es tu <span>
          <Typewriter          
            words={['Consulta?', 'Duda?','Pregunta?']}
            loop={0}                      
            typeSpeed={120}
            deleteSpeed={80}
          /></span></span>
          <span style={{color: 'white', fontWeight:'bold', fontSize:'4vh'}}>
            <Cursor cursorStyle='|'/>
          </span></Box>
      <Flex direction='column' align='center' justify='center'>         
        <Input sx={() => ({ width: "120%" })} size="xs" type="text" value={query} onChange={refreshQuery} />
        <Box mt='xl'>
          <Button onClick={sendQuery} size="xs">Consultar</Button>
        </Box>

      </Flex>
    </Flex>

  )
}

export default Home;
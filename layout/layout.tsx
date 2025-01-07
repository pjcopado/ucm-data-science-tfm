import { AppShell, Avatar, Box, Button, Center, Flex, Group, Header, Menu, Navbar, Text } from '@mantine/core'
import Image from 'next/image'
import Link from 'next/link'
import { ChevronDown, Container, Home2, Logout } from "tabler-icons-react"

const Layout = ({ children }: { children: React.ReactNode }) => {
    return (
    
        <AppShell 
            sx={() => ({ display: "flex", backgroundColor:"black" })} 
            padding="md"       
            header={
                <Header height={80} p='xs'>                
                
                    <Box sx={() => ({ display: "flex" })}>
                        <Box sx={() => ({ flex: "1" })}>
                            <Link href={'/'}>
                                <Flex justify={'flex-start'} align="center">
                                    <Image src="/thinking.png" alt='logo' width="80" height="60" />
                                    <p>My Brain GPT</p>
                                </Flex>
                            </Link>
                        </Box>
                        <Flex align='center' justify='center'>
                            <Button ml='lg' className="button">Login</Button>
                        </Flex>
                    </Box>
                </Header>
            }
        >

        <Flex justify='center' align='center' >        
            <main>
                {children}
            </main>
            </Flex>
        </AppShell>
       
    )

}


export default Layout
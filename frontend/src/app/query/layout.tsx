"use client"
import "../globals.css";
import '@mantine/core/styles.css';
import React from "react";
import { AppShell, Flex, Transition, Box } from '@mantine/core';
import { LuPanelLeftOpen, LuPanelRightOpen } from "react-icons/lu";
import { BsPencilSquare } from "react-icons/bs";
import dynamic from 'next/dynamic';
import UseToggleComponent from '../../hooks/useToogleHook';
import { NavbarAsideContainer } from '@/components/container/NavbarAsideContainer';
import Link from "next/link";
import { HiOutlineHome } from "react-icons/hi2";

const ColorToogleDynamic = dynamic(() => import('../../components/view/ToogleColorSchemeHook'), {
  ssr: false,
});

export default function SecondaryLayout({ children }: { children: React.ReactNode }) {
  const { isOpen, toggle } = UseToggleComponent();
  return (
    <AppShell
      header={{ height: 50 }}
      navbar={{
        width: 300,
        breakpoint: 'sm',
        collapsed: { mobile: !isOpen },
      }}>
      <AppShell.Header>
        <Flex justify="space-between" align='center'>
          <Flex justify='space-between'>
            {isOpen ? <Box><LuPanelLeftOpen style={{ "marginTop": "0.5rem" }} size='35' onClick={toggle} />
              <Link href={{ pathname: '/' }} style={{ "textDecoration": "none", 'marginLeft':'5px' }}><HiOutlineHome color="white" size='35'  /></Link>
            </Box> : <Box><LuPanelRightOpen style={{ "marginTop": "0.5rem" }} size='35' onClick={toggle} />
              <Link href={{ pathname: '/' }} style={{ "textDecoration": "none" ,'marginLeft':'5px' }}><HiOutlineHome color="white" size='35' /></Link>
            </Box>}
            <Flex justify='space-between'>
            <Link href={{ pathname: '/query/new' }} style={{ "textDecoration": "none" }}><BsPencilSquare style={{ "marginTop": "0.7rem" ,'marginLeft':'10px', color:"white" }} size='30'/></Link>
            </Flex>
          </Flex>
          <Flex justify='space-between'>
            <ColorToogleDynamic/>
          </Flex>

        </Flex>
      </AppShell.Header>
      <Transition mounted={isOpen} transition="fade" duration={400} timingFunction="ease">
        {(styles) => <div style={styles}><AppShell.Navbar style={{ "width": "21rem" }} ml='xs' mt="sm"><NavbarAsideContainer /></AppShell.Navbar></div>}
      </Transition>
      <AppShell.Main>
        {children}
      </AppShell.Main>
    </AppShell>

  );

}
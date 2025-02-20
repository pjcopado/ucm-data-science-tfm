"use client"
import React from 'react';
import { NavbarMainContainer } from "../../../components/container/NavbarMainContainer";
import { FC } from 'react';

interface Params {
  chatid: string;
}

const Page: FC<{ params: Promise<Params> }> = () => {
  return (
    <>
    <NavbarMainContainer/>    
    </>
  )  
};


export default Page;
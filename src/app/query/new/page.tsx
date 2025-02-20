"use client"
import React from 'react';
import { FC } from 'react';
import NewMessageView from '@/components/view/newMessage';

interface Params {
  chatid: string;
}

const Page: FC<{ params: Promise<Params> }> = ( ) => {
  return (
    <>
    <NewMessageView/>    
    </>
  )  
};


export default Page;
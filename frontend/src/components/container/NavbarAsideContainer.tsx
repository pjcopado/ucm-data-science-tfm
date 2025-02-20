"use client"
import { useEffect } from 'react';
import { getAllQueries } from "../../features";
import { useAppDispatch } from "../../hooks/reduxHooks";
import { useAppSelector } from "../../hooks/reduxHooks"
import NavbarAsideView from "../view/NavbarAsideView";
import useChatHook from '@/hooks/useChatHook';


export const NavbarAsideContainer:React.FC = () => {
    const dispatch = useAppDispatch()
    const useSelector = useAppSelector
    const queryState = useSelector((state) => state.query)
    const { openChatById } = useChatHook(); 


    const AllQueries = async () => {
        try {
          await dispatch(getAllQueries()); 
        } catch (error) {
          console.error('Error during query fetch:', error);
        }
      };  
      
      useEffect(() => {
          AllQueries()
      }, []);
      // eslint-disable-next-line react-hooks/exhaustive-deps

      useEffect(() => {
        AllQueries()
    }, [queryState.queryIdChat.id]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
    const uniqueData = queryState.queryList.items
    return (
        <>
        {queryState.queryList.items ? <NavbarAsideView data={uniqueData} openNewChat={openChatById}/> : <>cargando</> }
        </>
    )
}



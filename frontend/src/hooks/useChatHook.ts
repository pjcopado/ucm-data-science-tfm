"use client"
import React, {  useEffect, useState } from "react"
import { postNewQuery, getQueriesById, resetReducer, setActiveMessage } from "../features/index";
import { useAppDispatch } from "./reduxHooks";
import { useAppSelector } from "./reduxHooks"
import { useRouter } from "next/navigation";

const useChatHook = () => {
  const router = useRouter();
  const [query, setQuery] = useState<string>('')  
  const dispatch = useAppDispatch()
  const useSelector = useAppSelector
  const queryState = useSelector((state) => state.query)

  useEffect(() => {
    const id = queryState.queryIdChat.id
    if (id) {
      router.push(`/query/${id}`);
    }
    dispatch(resetReducer())
  }, [queryState.queryIdChat.id])

  const refreshQuery = (e: React.FormEvent<HTMLInputElement>) => {    
    setQuery(e.currentTarget.value)    
   
  }

  const openChatQuery = async () => {
    try {
      await dispatch(postNewQuery(query));       
      dispatch(setActiveMessage('message2'))
    }catch (error) {
      console.error('Error during query fetch:', error);
    }
  }


  const openChatById = async (id:string) => {
    try {
      await dispatch(getQueriesById(id)); 
      router.push(`/query/${id}`);
    } catch (error) {
      console.error('Error during query fetch:', error);
    }
  };

  

  return {query, refreshQuery, openChatQuery, openChatById}
}

export default useChatHook
"use client"
import {  useEffect, useState } from "react";
import { useAppDispatch, useAppSelector } from "../../hooks/reduxHooks"
import OpenChatView from "../view/OpenChatView";
import {  Query } from "@/interface/query";
import { usePathname, useRouter } from 'next/navigation'
import { getQueriesById, postQueriesById } from "@/features";
import { RootState } from "@/types/reduxTypes";


export const NavbarMainContainer: React.FC = () => {

  const dispatch = useAppDispatch()
  const useSelector = useAppSelector
  const queryState = useSelector((state) => state.query)
  const [data, setData] = useState<Array<Query>>([])
  const [query, setQuery] = useState<string>('')
  const activeMessage = useSelector((state: RootState) => state.query.activeMessage)
  const pathname = usePathname();
  const segments = pathname.split("/");
  const lastParam = segments.pop();
  const router = useRouter()


  const newMessage = async () => {
    if (lastParam) {
      dispatch(postQueriesById({ id: lastParam, question: query }))
    }
    
    const newQuestion: Query = {
      id: Date.now().toString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      question: query,
      response: '',
      is_valid: false,
      query_explanation: '',
      status: 'pending',
      llm_response_id: "",
      query: "",
      query_response: "",
      confidence_score: 0
    }
    setQuery('')
    setData([...data, newQuestion]);

    const queryItems = queryState.query.items;
    useEffect(() =>{
      const updatedQuestion = {      
        ...newQuestion,
        response: queryItems[queryItems.length - 1]?.response,
        is_valid: queryItems[queryItems.length - 1]?.is_valid,
        query_explanation: queryItems[queryItems.length - 1]?.query_explanation,
        status: queryItems[queryItems.length - 1]?.status,
        updated_at: queryItems[queryItems.length - 1]?.updated_at,
      };
  
      setData((prev) => {
        return prev.map((qa) =>
          qa.id === newQuestion.id ? updatedQuestion : qa
        );
      });

    },[queryItems[queryItems.length - 1]?.response])
  }


  useEffect(() => {
    if (lastParam) {
      dispatch(getQueriesById(lastParam));
      router.push(`/query/${lastParam}`)
    }
  }, []);

  useEffect(() => {
    if (activeMessage === 'message1') {
      setData(queryState.query.items);
    }
    if (activeMessage === 'message2') {
      setData([queryState.queryIdChat.first_message]);
    }
  }, [activeMessage]);
  // eslint-disable-next-line react-hooks/exhaustive-deps

  return (
    <>
      <OpenChatView data={data} newQuery={newMessage} question={query} setQuestion={setQuery} idChat={lastParam!}/>

    </>
  )
}

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
  const pathname = usePathname();
  const segments = pathname.split("/");
  const lastParam = segments.pop();
  const router = useRouter()
  const activeMessage = useSelector((state: RootState) => state.query.activeMessage)
  

  
  const newMessage = async () => {

    setData([])
    if (activeMessage === 'message1') {
      setData(queryState.query.items);
    }
    if (activeMessage === 'message2') {
      setData([queryState.queryIdChat.first_message]);
    }
  
    dispatch(postQueriesById({ id: lastParam!, question: query }))
    
    
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

    const lastItem = queryItems[queryItems.length - 1];

    if (lastItem.response) {
      const updatedQuestion = {
        ...newQuestion,
        response: lastItem.response,
        is_valid: lastItem.is_valid,
        query_explanation: lastItem.query_explanation,
        status: lastItem.status,
        updated_at: lastItem.updated_at,
      }

    setData((prev) => {
      prev.map((qa) =>
        console.log(qa.id, newQuestion.id)
      );
      return prev.map((qa) =>
        qa.id === newQuestion.id ? updatedQuestion : qa
      );
    })};

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

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
  const [change, setChange] = useState(false)
  const activeMessage = useSelector((state: RootState) => state.query.activeMessage)
  

  
  const newMessage = async () => {
    setData([])  
    dispatch(postQueriesById({ id: lastParam!, question: query }))
    setChange(true)
    setQuery('')
  }

  
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Si tienes una operación asíncrona aquí (como obtener datos)
        const items = queryState.query.items;
        setData(items);
      } catch (error) {
        console.error("Error:", error);
      } finally {
        setChange(false);
      }
    };
  
    fetchData();
  
  }, [change]);
  
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

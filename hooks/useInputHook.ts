import React, { useState } from "react"
import { postQuery } from "@/api/main"

const useInputHook = () => {
  const [query, setQuery] = useState<string>('')

  const refreshQuery = (e: React.FormEvent<HTMLInputElement>) => {
    setQuery(e.currentTarget.value)    
  }

  const sendQuery = async(e: React.MouseEvent<HTMLInputElement>) => {
    e.preventDefault()
    await postQuery({"query":query})
  }
  return {query, refreshQuery, sendQuery}
 
}

export default useInputHook
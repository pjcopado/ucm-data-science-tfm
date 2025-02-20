import axios from 'axios'
const mainBase = "http://localhost:5000"


export const getQueriesAll = async () => {
    const res = await axios.get(`${mainBase}/v1/chats`)
    return res.data
}


export const postNewChat = async (question: string) => {
    const res = await axios.post(`${mainBase}/v1/chats`, {question:question})          
    return res.data
}

export const GetQueryById = async (id: string) => {
    const res = await axios.get(`${mainBase}/v1/chats/${id}/messages`)   
    return res.data
}


export const postQueryById= async(id:string, question:string ) => {
    const res = await axios.post(`${mainBase}/v1/chats/${id}/messages`, {question:question})  
    return res.data
}

export const patchValidation= async(chatId:string, messageId: string, is_valid:boolean, ) => {
    const res = await axios.patch(`${mainBase}/v1/chats/${chatId}/messages/${messageId}`,{is_valid:is_valid})  
    return res.data
}

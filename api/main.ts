import axios from 'axios'
axios.defaults.withCredentials = true
const mainBase = "http://localhost:8000"
axios.defaults.withCredentials = true


export const postQuery = async (query: object) => {
    const res = await axios.post("http://localhost:8000/query", query)
    console.log(res.data)
}


import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { QueryState, queryList,queryById, Query } from '../../interface/query';
import { getQueriesAll, postNewChat, GetQueryById, postQueryById } from '@/api/main';


const initialState: QueryState = {
    loading: false,
    query: {} as queryById,    
    queryList: {} as queryList,
    queryNewMessage: {} as Query,
    queryIdChat: {
        id: '',
        created_at: '',
        updated_at: '',
        first_message: {
            id: '',
            created_at: '',
            updated_at: '',
            question: '',
            response: '',
            is_valid: false,
            query_explanation: '',
            status: '',
            llm_response_id: '',
            query: '',
            query_response: '',
            confidence_score: 0
        },
    },
    error: undefined,
    activeMessage: null
    
}

const initialQueryIdChat = {
    id: '',
    created_at: '',
    updated_at: '',
    first_message: {
        id: '',
        created_at: '',
        updated_at: '',
        question: '',
        response: '',
        is_valid: false,
        query_explanation: '',
        status: '',
        llm_response_id: '',
        query: '',
        query_response: '',
        confidence_score: 0
},
  };


// GET ALL QUERIES
export const getAllQueries = createAsyncThunk('GET_QUERIES_LIST', async () => {
    const response = await getQueriesAll()
    return response
})


// GET QUERIES BY ID
export const getQueriesById = createAsyncThunk('GET_QUERIES_BY_ID', async (id: string) => {
    const response = await GetQueryById(id)
    return response
})

// POST QUERIES BY ID
export const postQueriesById = createAsyncThunk('POST_QUERY_BY_ID', async ({ id, question }: { id: string, question: string }) => {
    const response = await postQueryById(id, question)
    return response
})

// POST NEW QUERY
export const postNewQuery = createAsyncThunk('OPEN_CHAT', async (question: string) => {

    const response = await postNewChat(question)
    return response
})

// STREAMING JSON TEXT
// export const streamingJsonText = createAsyncThunk('JSON_STREAMING', async() => {

// })

const querySlice = createSlice({
    name: 'query',
    initialState,
    reducers: {
        setActiveMessage: (state, action: PayloadAction<'message1' | 'message2'>) => {
            state.activeMessage = action.payload;
          },
        resetReducer:(state) =>{
            state.queryIdChat = initialQueryIdChat
        },
        resetReducerMessage:(state) =>{
            state.queryNewMessage = {} as Query
        },
     },
    extraReducers: (builder) => {

        // ------- GET ALL QUERIES --------

        builder.addCase(getAllQueries.pending, (state) => {
            state.loading = true
        })
        builder.addCase(getAllQueries.fulfilled, (state, action) => {
            state.loading = false
            state.queryList = action.payload
            state.error = ''
        })
        builder.addCase(getAllQueries.rejected, (state, action) => {
            state.loading = false
            state.query = {} as queryById
            state.error = action.error.message
        })

        // ------- GET QUERIES BY ID -------

        builder.addCase(getQueriesById.pending, (state) => {
            state.loading = true
        })
        builder.addCase(getQueriesById.fulfilled, (state, action) => {
            state.loading = false
            state.query = action.payload
            state.error = ''
            state.activeMessage = 'message1'
        })
        builder.addCase(getQueriesById.rejected, (state, action) => {
            state.loading = false
            state.query = {} as queryById
            state.error = action.error.message
        })

        // --------  POST QUERIES BY ID --------

        builder.addCase(postQueriesById.pending, (state) => {
            state.loading = true
            
        })
        builder.addCase(postQueriesById.fulfilled, (state, action) => {
            state.loading = false
            state.queryNewMessage = action.payload
            state.error = ''
            state.activeMessage = 'message1'
        })
        builder.addCase(postQueriesById.rejected, (state, action) => {
            state.loading = false
            state.query = {} as queryById
            state.error = action.error.message
        })

        // --------  POST NEW QUERY --------

        builder.addCase(postNewQuery.pending, (state) => {
            state.loading = true
        })
        builder.addCase(postNewQuery.fulfilled, (state, action) => {
            state.loading = false
            state.queryIdChat = action.payload
            state.error = ''
            state.activeMessage = 'message2'
        })
        builder.addCase(postNewQuery.rejected, (state, action) => {
            state.loading = false
            state.query = {} as queryById
            state.error = action.error.message
        })

    },
})
export const { setActiveMessage, resetReducer,resetReducerMessage } = querySlice.actions;
export const queryReducer = querySlice.reducer
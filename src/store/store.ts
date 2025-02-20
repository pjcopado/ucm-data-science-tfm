import { configureStore } from '@reduxjs/toolkit'
import { useDispatch } from 'react-redux'
import {queryReducer} from '../features'

// Function to create and configure the Redux store
export const makeStore = () => configureStore({
  reducer: {
    query: queryReducer,
  },
});





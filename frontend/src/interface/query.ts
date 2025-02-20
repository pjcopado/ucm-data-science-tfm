export interface Query {
  id: string;
  created_at: string;
  updated_at: string;
  question: string;
  llm_response_id:string;
  query:string;
  query_explanation: string;
  query_response: string;
  confidence_score: number;
  response: string;
  is_valid: boolean;
  status: string;

}

export interface Question{
  id: string;
  created_at: string;
  updated_at: string;
  question: string;
}

export interface Response{
  id:string
  updated_at:string,
  llm_response_id:string;
  query:string;
  query_explanation: string;
  query_response: string;
  confidence_score: number;
  response: string;
  is_valid: boolean;
  status: string;

}

export interface responseBack {
  question: string;
  response: string;
}

export interface QueryState {
  loading: boolean;
  query: queryById;
  queryList: queryList
  queryIdChat: FirstDataResponse;
  error: string | undefined;
  activeMessage: 'message1' | 'message2' | null; 
}



export interface QueryByIdResponse{
  query: Query;
  thunkName: string;
}

export interface QueryPostResponse{
  query: FirstDataResponse;
  thunkName: string;
}

export interface FirstDataResponse{
  id: string;
  created_at: string;
  updated_at: string;
  first_message: Query;

}

export interface DB_MOCK {
  id: string;
  created_at: string;
  updated_at: string;
  message: Query[]

}

export interface queryList{
  items:FirstDataResponse[],
  page:number,
  pages:number,
  size: number,
  total: number
}


export interface queryById{
  items:Query[],
  page:number,
  pages:number,
  size: number,
  total: number
}
export interface PostQueryByIdParams {
  id: string;
  question: string;
}
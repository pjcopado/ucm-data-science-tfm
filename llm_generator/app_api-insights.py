from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modules.insights_generator import InsightGenerator

app = FastAPI()

# Initialize the InsightGenerator singleton
insight_gen = InsightGenerator()


class QueryRequest(BaseModel):
    user_question: str
    sql_result: str


class QueryResponse(BaseModel):
    response: str


@app.post("/generate_response", response_model=QueryResponse)
def generate_response(request: QueryRequest):
    try:
        response = insight_gen.generate_response(
            request.user_question, request.sql_result
        )
        return QueryResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)

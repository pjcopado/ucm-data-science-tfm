from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from modules.sql_generator import SQLQueryGenerator
import os
import dotenv

dotenv.load_dotenv(".env.docker")
app = FastAPI()

# Model name
model_name = "llama-3-sqlcoder-8b-Q8_0"

# Database configuration
db_config = {
    "host": os.getenv("EXTERNAL_POSTGRES_HOST"),
    "port": os.getenv("EXTERNAL_POSTGRES_PORT"),
    "database": os.getenv("EXTERNAL_POSTGRES_DB"),
    "user": os.getenv("EXTERNAL_POSTGRES_USERNAME"),
    "password": os.getenv("EXTERNAL_POSTGRES_PASSWORD"),
}

# Initialize the SQLQueryGenerator class
sql_generator = SQLQueryGenerator(
    model_name=model_name, db_config=db_config, max_attempts=3
)


class QueryRequest(BaseModel):
    user_question: str
    user_instruction: Optional[str] = None
    db_schema: Optional[str] = None


class QueryResponse(BaseModel):
    query: str


@app.post("/sql_generator", response_model=QueryResponse)
def generate_response(request: QueryRequest):
    try:
        response = sql_generator.generate_sql_query(
            request.user_question, request.user_instruction, request.db_schema
        )
        return QueryResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)

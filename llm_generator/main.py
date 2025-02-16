import uuid
from contextlib import asynccontextmanager
from typing import Optional
import os
import dotenv

from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from modules.sql_generator import SQLQueryGenerator
from modules.insights_generator import InsightGenerator

dotenv.load_dotenv(".env.docker")

# Model name
MODEL_NAME = "llama-3-sqlcoder-8b-Q8_0"
# https://www.google.com/url?sa=j&url=https%3A%2F%2Fhuggingface.co%2Fbartowski%2Fllama-3-sqlcoder-8b-GGUF%2Fresolve%2Fmain%2Fllama-3-sqlcoder-8b-Q8_0.gguf&uct=1739397252&usg=Pwk2TVtVFQ6ZsJqwEOzhUy9yEfA.&opi=76390225&source=meet

# Database configuration
db_config = {
    "host": os.getenv("EXTERNAL_POSTGRES_HOST"),
    "port": os.getenv("EXTERNAL_POSTGRES_PORT"),
    "database": os.getenv("EXTERNAL_POSTGRES_DB"),
    "user": os.getenv("EXTERNAL_POSTGRES_USERNAME"),
    "password": os.getenv("EXTERNAL_POSTGRES_PASSWORD"),
}


# # Mock function for SQL generator
# def mock_generate_sql_query(user_question, user_instruction=None, db_schema=None):
#     return {
#         "id": uuid.uuid4(),
#         "query": f"SELECT * FROM mock_table WHERE question = '{user_question}'",
#         "confidence_score": 0.99,
#         "status": "success",
#     }


# # Mock function for Insight generator
# def mock_generate_response(user_question, query_result):
#     return {
#         "insight_response": f"Mock insight for query result: {query_result}",
#         "query_explanation": f"Mock explanation for query: {user_question}",
#         "status": "success",
#     }


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Mocking model initialization to speed up startup"""
#     print("✅ Mock initialization started...")

#     # Ensure app.state.llms is initialized
#     if not hasattr(app.state, "llms"):
#         app.state.llms = {}

#     app.state.llms["sql_generator"] = type(
#         "MockSQLGenerator", (), {"generate_sql_query": mock_generate_sql_query}
#     )()
#     app.state.llms["insight_generator"] = type(
#         "MockInsightGenerator", (), {"generate_response": mock_generate_response}
#     )()

#     yield

#     print("🛑 Cleaning up...")
#     app.state.llms.clear()


def lifespan(app: FastAPI):
    app.state.llms = dict()
    sql_generator = SQLQueryGenerator(
        model_name=MODEL_NAME,
        db_config=db_config,
        max_attempts=3,
    )
    app.state.llms["sql_generator"] = sql_generator
    insight_generator = InsightGenerator()
    app.state.llms["insight_generator"] = insight_generator
    yield
    app.state.llms.clear()


# def model_loader(*args, **kwargs):
#     print("Model loaded")


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print(3)
#     app.state.llms = dict()
#     app.state.llms["sql_generator"] = model_loader
#     app.state.llms["insight_generator"] = model_loader
#     print(app)
#     print(app.state.llms)
#     yield
#     app.state.llms.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


#### SQL Generator


class SqlGeneratorRequest(BaseModel):
    user_question: str
    user_instruction: Optional[str] = None
    db_schema: Optional[str] = None


class SqlGeneratorResponse(BaseModel):
    id: Optional[uuid.UUID] = None
    query: Optional[str] = None
    confidence_score: Optional[float] = None
    status: str


@app.post("/sql_generator", response_model=SqlGeneratorResponse, tags=["SQL Generator"])
def generate_sql(request: Request, obj_in: SqlGeneratorRequest):
    sql_generator = request.app.state.llms["sql_generator"]
    try:
        response = sql_generator.generate_sql_query(
            obj_in.user_question,
            obj_in.user_instruction,
            obj_in.db_schema,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch(
    "/sql_generator/{id}", response_model=SqlGeneratorResponse, tags=["SQL Generator"]
)
def update_sql(
    request: Request,
    id: uuid.UUID,
    is_correct: bool = Body(..., embed=True),
):
    # TODO pass function to update
    pass


#### Insight Generator


class InsightGeneratorRequest(BaseModel):
    user_question: str
    query_result: str


class InsightGeneratorResponse(BaseModel):
    insight_response: Optional[str] = None
    query_explanation: Optional[str] = None
    status: str


@app.post(
    "/insight_generator",
    response_model=InsightGeneratorResponse,
    tags=["Insight Generator"],
)
def generate_insight(request: Request, obj_in: InsightGeneratorRequest):
    insight_generator = request.app.state.llms["insight_generator"]
    try:
        response = insight_generator.generate_response(
            obj_in.user_question,
            obj_in.query_result,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)

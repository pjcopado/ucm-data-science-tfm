from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.services.insight import InsightGenerator


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    app.state.insight_model = InsightGenerator()
    yield

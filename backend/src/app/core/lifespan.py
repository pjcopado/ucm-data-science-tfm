from contextlib import asynccontextmanager

from fastapi import FastAPI

llms = dict()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

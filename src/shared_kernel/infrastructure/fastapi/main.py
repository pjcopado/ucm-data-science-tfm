from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn



app = FastAPI()
    
origins = [
    
    "http://localhost:8080",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class prueba(BaseModel):
    query: str
   

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/query/")
async def query(query:prueba):    
    json_compatible_item_data = jsonable_encoder(query)
    return JSONResponse(content=json_compatible_item_data)
    





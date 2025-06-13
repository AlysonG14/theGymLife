from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.configs import settings
from api.v1.api import api_router
import uvicorn

app = FastAPI(title='GymForce - Academia de Musculação')
origins = ["http://localhost", "http://localhost:8000", "http://localhost:5500"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
allow_methods=["*"], allow_headers=["*"],)


app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get('/')
async def message():
    return {"Welcome": "to GymForce"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level='info', reload=True)
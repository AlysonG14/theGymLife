from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.configs import settings
from api.v1.router import api_router

app = FastAPI(title='GymForce - Academia de Musculação')
origins = ["htto://localhost", "http://localhost:8080", "http://localhost:5500"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
allow_methods=["*"], allow_headers=["*"],)


app.include_router(api_router, prefix=settings.API_V1_STR)

app = FastAPI()

@app.get('/')
async def message(self):
    return {"Welcome": "to GymForce"}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8080, log_level='info', reload=True)
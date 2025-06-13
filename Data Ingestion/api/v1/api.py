from fastapi import APIRouter

from api.v1.endpoints import academia

api_router = APIRouter()
api_router.include_router(academia.router, prefix='/academia', tags=['academia'])
from fastapi import APIRouter

from api.v1.endpoints import academia

APIRouter = APIRouter()
APIRouter.include_router(academia.router, prefix='/academia', tags=['academia'])
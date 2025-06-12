from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.academia_model import AcademiaModel
from schemas.academia_schema import AcademiaSchema
from core.deps import get_session

router = APIRouter()

# Rota para listar os aparelhos da academia

@router.get("/academia/")
async def listar_aparelho(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query =  select(AcademiaModel)
        result = await session.execute(query)
        academia: List[AcademiaModel] = result.scalars().all()

# Rota para listar todos os aparelhos da academia com ID 

@router.get("/academia/{academia_id}", response_model=AcademiaModel,
            status_code=status.HTTP_200_OK)
async def listar_aparelho_id(academia_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AcademiaModel).filter(AcademiaModel.id == academia_id)
        result = await session.execute(query)
        academia = result.scalar_one_or_none()

# Rota para criar um novo aparelho da academia

@router.post("/academia/criar/", status_code=status.HTTP_201_CREATED, response_model=AcademiaSchema)

async def criar_aparelho(academia: AcademiaSchema, db: AsyncSession = Depends(get_session)):
    novo_aparelho = AcademiaModel(aparelho=academia.aparelho, variacao=academia.variacao,
                                  carga=academia.carga, serie=academia.serie,
                                  repeticao=academia.repeticao)
    db.add(novo_aparelho)
    await db.commit()

    return novo_aparelho

# Rota para atualizar aparelho



# Rota para deletar o aparelho

@router.delete('/{academia_id}', status_code=status.HTTP_204_NO_CONTENT)

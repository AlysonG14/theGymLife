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

@router.put("academia/atualizar/{academia_id}",
            response_model=AcademiaModel,
            status_code=status.HTTP_202_ACCEPTED)
async def atualizar_aparelho(academia_id: int, academia: AcademiaSchema,
                             db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AcademiaSchema).filter(AcademiaModel.id == academia_id)
        result = await session.execute(query)
        academia_up = result.scalar_one_or_none()

        if academia_up:
            academia_up.aparelho = academia.aparelho
            academia_up.variacao = academia.variacao
            academia_up.carga = academia.carga
            academia_up.serie = academia.serie
            academia_up.repeticao = academia.repeticao

            await session.commit()

            return academia_up
        else:
            raise HTTPException(detail='Aparelho de Academia não Encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# Rota para deletar o aparelho

@router.delete('/academia/delete/{academia_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_aparelho(academia_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(AcademiaModel).filter(AcademiaModel.id == academia_id)
        result = await session.execute(query)
        academia_del = result.scalar_one_or_none()
        if academia_del:
            await session.delete(academia_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Aparelho de Academina não Encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


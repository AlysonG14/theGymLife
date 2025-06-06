from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.academia_model import AcademiaModel
from schemas.academia_schema import AcademiaSchema
from core.deps import get_session

router = APIRouter
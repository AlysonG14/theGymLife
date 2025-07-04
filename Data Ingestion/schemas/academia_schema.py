from typing import Optional
from pydantic import BaseModel as SCBaseModel

class AcademiaSchema(SCBaseModel):
    id: Optional[int] = None
    aparelho: str
    variacao: str
    carga: bool
    serie: int
    repeticao: int

class Config:
    orm_mode = True